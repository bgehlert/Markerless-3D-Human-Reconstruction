import os
import sys
import pickle
import numpy as np
import trimesh

# ==========================================
# FILE PATHS CONFIGURATION (SMPL-X ACTIVE)
# ==========================================
MODEL_PATH = '/home/labadmindy/EasyMocap/data/models/smplx/SMPLX_NEUTRAL.pkl'
FRAME = sys.argv[1] if len(sys.argv) > 1 else '000000'
NPZ_PATH = f'smplx_v2/{FRAME}.npz'
OUTPUT_OBJ = f'{FRAME}_v4.obj'

print(f"Reading parameters from: {NPZ_PATH}")
data = np.load(NPZ_PATH)

poses = np.squeeze(data['poses']).astype(np.float64).reshape(-1)
shapes = np.squeeze(data['shapes']).astype(np.float64).reshape(-1)
trans = np.squeeze(data['translations']).astype(np.float64).reshape(-1)

# CANONICAL FRAME: drop EasyMocap's global rotation (Rh) and translation (Th)
# so the mesh stays y-up and centered, like the original zero-pose smplx.obj.
poses[:3] = 0.0
trans[:] = 0.0
print(f"poses: {poses.shape}, shapes: {shapes.shape}, trans: {trans.shape}")

print(f"Loading raw template matrices from: {MODEL_PATH}")
with open(MODEL_PATH, 'rb') as f:
    smpl_model = pickle.load(f, encoding='latin1')


def to_np(x):
    """Convert chumpy / scipy sparse / array-likes to dense numpy arrays."""
    if hasattr(x, 'toarray'):
        return np.asarray(x.toarray())
    return np.asarray(x)


faces = to_np(smpl_model['f']).astype(np.int64)
v_template = to_np(smpl_model['v_template'])
shapedirs = to_np(smpl_model['shapedirs'])
posedirs = to_np(smpl_model['posedirs'])
J_regressor = to_np(smpl_model['J_regressor'])
kintree_table = to_np(smpl_model['kintree_table'])
weights = to_np(smpl_model['weights'])

num_verts = v_template.shape[0]
num_joints = J_regressor.shape[0]  # 55 for SMPL-X

# ------------------------------------------------------------------
# Build full axis-angle pose: 55 joints * 3 = 165 values
# Joint order: pelvis(0), body(1-21), jaw(22), leye(23), reye(24),
#              left hand(25-39), right hand(40-54)
# ------------------------------------------------------------------
if poses.shape[0] == num_joints * 3:
    full_pose = poses
elif poses.shape[0] == 87:
    # EasyMocap layout: global(3) + body(63) + hands PCA(6+6) + head(9)
    print("Detected 87-dim EasyMocap pose (PCA hands). Expanding to 165.")
    body = poses[:66]
    hand_coeffs_l = poses[66:72]
    hand_coeffs_r = poses[72:78]
    head = poses[78:87]  # jaw, leye, reye

    comps_l = to_np(smpl_model['hands_componentsl'])[:6]
    comps_r = to_np(smpl_model['hands_componentsr'])[:6]
    mean_l = to_np(smpl_model.get('hands_meanl', np.zeros(45)))
    mean_r = to_np(smpl_model.get('hands_meanr', np.zeros(45)))
    # Assumes flat hand mean (EasyMocap default). Use zeros for the mean:
    hand_l = hand_coeffs_l @ comps_l
    hand_r = hand_coeffs_r @ comps_r
    full_pose = np.concatenate([body, head, hand_l, hand_r])
else:
    # Fallback: pad/truncate to 165
    print(f"WARNING: unexpected pose size {poses.shape[0]}, padding/truncating to 165.")
    full_pose = np.zeros(num_joints * 3)
    n = min(poses.shape[0], full_pose.shape[0])
    full_pose[:n] = poses[:n]

pose_vec = full_pose.reshape(num_joints, 3)

# 1. Shape blendshapes
num_shapes = min(shapes.shape[0], shapedirs.shape[2])
v_shaped = v_template + np.dot(shapedirs[:, :, :num_shapes], shapes[:num_shapes])

# 2. Joint locations
joints = J_regressor.dot(v_shaped)


def rodrigues(r):
    """Axis-angle (3,) -> rotation matrix (3, 3)."""
    theta = np.linalg.norm(r)
    if theta < 1e-8:
        return np.eye(3)
    k = r / theta
    K = np.array([[0, -k[2], k[1]],
                  [k[2], 0, -k[0]],
                  [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * np.dot(K, K)


# 3. Pose rotation matrices and pose blendshapes
pose_mats = np.stack([rodrigues(pose_vec[i]) for i in range(num_joints)])

pose_feature = (pose_mats[1:] - np.eye(3)).reshape(-1)  # (54*9 = 486,)
num_pose_features = posedirs.shape[2]

if pose_feature.shape[0] > num_pose_features:
    pose_feature = pose_feature[:num_pose_features]
elif pose_feature.shape[0] < num_pose_features:
    pose_feature = np.pad(pose_feature, (0, num_pose_features - pose_feature.shape[0]))

v_posed = v_shaped + posedirs.dot(pose_feature)

# 4. Forward kinematics
parent = {i: int(kintree_table[0, i]) for i in range(1, num_joints)}
G = np.zeros((num_joints, 4, 4))

G[0, :3, :3] = pose_mats[0]
G[0, :3, 3] = joints[0]
G[0, 3, 3] = 1.0

for i in range(1, num_joints):
    p = parent[i]
    G_local = np.eye(4)
    G_local[:3, :3] = pose_mats[i]
    G_local[:3, 3] = joints[i] - joints[p]
    G[i] = np.dot(G[p], G_local)

# Remove rest-pose joint offset so G transforms rest-pose vertices directly
for i in range(num_joints):
    G[i, :3, 3] -= np.dot(G[i, :3, :3], joints[i])

# 5. Linear blend skinning (vectorized)
T = np.tensordot(weights, G, axes=((1,), (0,)))        # (V, 4, 4)
v_homo = np.concatenate([v_posed, np.ones((num_verts, 1))], axis=1)  # (V, 4)
vertices = np.einsum('vij,vj->vi', T, v_homo)[:, :3]

# EasyMocap rotates about the model origin, not the pelvis.
# Convert: R(v - j0) + j0  ->  R v  by adding (R j0 - j0).
vertices += pose_mats[0] @ joints[0] - joints[0]

# Global translation
vertices += trans

# 6. Export
print(f"Mesh compiled successfully. Exporting to {OUTPUT_OBJ}...")

if faces.min() == 1:
    faces = faces - 1

mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
mesh.export(OUTPUT_OBJ)

print(f"\nSuccess! Posed SMPL-X model compiled with {vertices.shape[0]} vertices and {faces.shape[0]} faces.")

check = trimesh.load(OUTPUT_OBJ, process=False)
print(f"Check: {len(check.vertices)} vertices (expected 10475), {len(check.faces)} faces (expected 20908)")