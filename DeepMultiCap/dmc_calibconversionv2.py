import os
import yaml
import numpy as np

def clean_opencv_yaml(filepath):
    """Removes OpenCV custom tags and fixes malformed headers so PyYAML can parse it."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        if line.startswith("%YAML:1.0"):
            line = "%YAML 1.0\n"
        if "!!opencv-matrix" in line:
            line = line.replace("!!opencv-matrix", "")
        cleaned_lines.append(line)
        
    return yaml.safe_load("".join(cleaned_lines))

def convert_easymocap_to_deepmulticap():
    intri_path = 'intri.yml'
    extri_path = 'extri.yml'
    
    # Target the strict directory layout expected by DeepMultiCap's dataloader
    output_dir = 'parameter'  
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(intri_path) or not os.path.exists(extri_path):
        print("Error: Make sure intri.yml and extri.yml are in this folder.")
        return

    # Parse raw text configs safely
    intri_data = clean_opencv_yaml(intri_path)
    extri_data = clean_opencv_yaml(extri_path)

    camera_ids = ['0', '1', '2', '3']
    
    for cam in camera_ids:
        # 1. Extract and format Intrinsic K Matrix (3x3 float32 array)
        k_flat = intri_data[f'K_{cam}']['data']
        k_matrix = np.array(k_flat, dtype=np.float32).reshape(3, 3)

        # 2. Extract Extrinsic Rotation R Matrix (3x3)
        rot_flat = extri_data[f'Rot_{cam}']['data']
        r_matrix = np.array(rot_flat, dtype=np.float32).reshape(3, 3)

        # 3. Extract Extrinsic Translation T Matrix (3x1)
        t_flat = extri_data[f'T_{cam}']['data']
        t_matrix = np.array(t_flat, dtype=np.float32).reshape(3, 1)

        # 4. Construct the unified 4x4 Extrinsic Matrix [R | T] expected by the repo
        extrinsic_4x4 = np.eye(4, dtype=np.float32)
        extrinsic_4x4[:3, :3] = r_matrix
        extrinsic_4x4[:3, 3] = t_matrix.flatten()

        # 5. Save directly as separate numpy arrays for each camera and matrix type
        np.save(os.path.join(output_dir, f'{cam}_intrinsic.npy'), k_matrix)
        np.save(os.path.join(output_dir, f'{cam}_extrinsic.npy'), extrinsic_4x4)

    print(f"Successfully converted calibration configuration!")
    print(f"Generated 8 separate matrix files inside: {os.path.abspath(output_dir)}/")

if __name__ == '__main__':
    convert_easymocap_to_deepmulticap()
