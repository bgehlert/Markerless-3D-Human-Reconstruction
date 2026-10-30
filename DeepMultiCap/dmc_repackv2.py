import os
import json
import numpy as np
 
src_dir = './smpl/smpl'   # EasyMocap fit output (JSON per frame)
out_dir = './smplx_v2'
os.makedirs(out_dir, exist_ok=True)
 
if not os.path.exists(src_dir):
    raise SystemExit("Error: Could not find your EasyMocap smpl results folder.")
 
 
def to_smplx_pose(poses, rh):
    """Build a 165-dim SMPL-X axis-angle pose from an EasyMocap fit."""
    poses = np.asarray(poses, dtype=np.float64).reshape(-1)
    rh = np.asarray(rh, dtype=np.float64).reshape(-1)
    out = np.zeros(165)
    if poses.size == 72:
        # SMPL: global(3) + 23 joints. Body joints 0-21 are shared with SMPL-X.
        out[:66] = poses[:66]
        out[:3] = rh                      # global rotation lives in Rh
    elif poses.size == 165:
        out[:] = poses
        out[:3] = rh
    else:
        raise ValueError(f"Unexpected pose size {poses.size}")
    return out
 
 
json_files = sorted(f for f in os.listdir(src_dir) if f.endswith('.json'))
for filename in json_files:
    with open(os.path.join(src_dir, filename), 'r') as f:
        data = json.load(f)
 
    if len(data) == 0:
        print(f"WARNING: {filename} has no tracked person, skipping")
        continue
 
    person = data[0]
    for key in ('poses', 'shapes', 'Rh', 'Th'):
        if key not in person:
            raise KeyError(f"{filename}: missing key '{key}'. Found: {list(person.keys())}")
 
    pose165 = to_smplx_pose(person['poses'], person['Rh'])
    frame_data = {
        'poses': pose165.astype(np.float32).reshape(1, -1),
        'shapes': np.array(person['shapes'], dtype=np.float32).reshape(1, -1),
        'translations': np.array(person['Th'], dtype=np.float32).reshape(1, -1),
    }
 
    np.savez(os.path.join(out_dir, filename.replace('.json', '.npz')), **frame_data)
    print(f"{filename}: shoulders(16,17) = {np.round(pose165[48:54], 3)}")
 
print("Repacked EasyMocap fits into DeepMultiCap .npz frames.")