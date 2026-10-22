# import the required libraries for the conversion code to execute
import yaml
import numpy as np
from scipy.spatial.transform import Rotation as R

# Custom Dumper forces small sequences/lists into single inline brackets [x, y, z] to replicate MAMMA formatting
class InlineSequenceDumper(yaml.SafeDumper):
    def represent_sequence(self, tag, sequence, flow_style=None):
        # force lists of floats/ints/strings to stay inline horizontally
        if all(isinstance(x, (int, float, str)) for x in sequence):
            flow_style = True
        return super().represent_sequence(tag, sequence, flow_style)

# defines the main function to convert EasyMocap calibration data to MAMMA format
def convert_easymocap_to_mamma(intri_path, extri_path, output_path):
    
    # load and read intrinsic parameters from EasyMocap intri.yml file
    with open(intri_path, 'r') as f:
        lines = f.readlines()
        # removes custom OpenCV formatting and YAML headers, keeping only the relevant data
        clean_lines = [line.replace('!!opencv-matrix', '') for line in lines if not line.strip().startswith('%YAML')]
        # parse all cleaned lines into a Python dictionary
        intri_data = yaml.safe_load("".join(clean_lines))

    # extrinsic file is read and processed similarly to the intrinsic file using the same cleaning and parsing steps
    with open(extri_path, 'r') as f:
        lines = f.readlines()
        clean_lines = [line.replace('!!opencv-matrix', '') for line in lines if not line.strip().startswith('%YAML')]
        extri_data = yaml.safe_load("".join(clean_lines))
     
    # initializes a dictionary to hold the flattened camera data for MAMMA 
    flat_camera_data = {}
    cam_names = intri_data.get('names', [])
    
    # retrieves camera names and converts each to an iterable integer 
    for idx, cam in enumerate(cam_names):
        # converts the camera label to an integer object
        cam_label = int(idx)
        
        # extract the relevant data for each camera from the intrinsic and extrinsic dictionaries 
        k_data = intri_data.get(f"K_{cam}", {}).get('data', [])             
        dist_data = intri_data.get(f"dist_{cam}", {}).get('data', [])       
        r_data = extri_data.get(f"R_{cam}", {}).get('data', [])           
        t_data = extri_data.get(f"T_{cam}", {}).get('data', [])             

        # flattened intrinsics in the order [fx, fy, cx, cy] for MAMMA's expected format 
        intrinsics_flat = [float(k_data[0]), float(k_data[4]), float(k_data[2]), float(k_data[5])]
        
        # truncate to first 4 coefficients for MAMMA's radtan model, 5th coefficient is 1 and not used in MAMMA's distortion model
        distortion_coeffs = [float(x) for x in dist_data[:4]]       
        
        # obtains original World-to-Camera (W2C) Rotation Matrix
        rotation_w2c = R.from_rotvec(r_data)
        R_w2c = rotation_w2c.as_matrix()
        T_w2c = np.array(t_data).reshape(3, 1)
        
        # computes Camera-to-World (C2W) Transposition Matrix
        R_c2w = R_w2c.T
        
        # Translation Vector Back-Projection (-R^T * T)
        T_c2w = -np.dot(R_c2w, T_w2c).flatten()
        translation_flat = [float(x) for x in T_c2w]
        
        # converts C2W Matrix into MAMMA's target quaternion format (Hamilton convention)
        rotation_c2w = R.from_matrix(R_c2w)
        hamilton_quaternion = rotation_c2w.as_quat(scalar_first=True).tolist()
        
        # builds expected MAMMA structure block
        flat_camera_data[cam_label] = {
            'camera_model': 'pinhole',                  # pinhole camera model used for iPhone video collection                  
            'distortion_model': 'radtan',               # radtan distortion model used for iPhone video collection        
            'intrinsics': intrinsics_flat,              # uses [fx, fy, cx, cy] extracted above   
            'distortion_coeffs': distortion_coeffs,     # distortion coefficients 
            'resolution':[1080, 1920],                  # resolution of iPhone SE 3rd generation vertical video capture on rear camera
            'translation': translation_flat,            # translation vector for camera extrinsics          
            'rotation_quaternion': hamilton_quaternion  # quaternion vector for camera rotation in Hamilton convention (w, x, y, z)                 
        }
        
    # fills the MAMMA calibration dictionary with the flattened camera data for all cameras        
    mamma_calib = {
        "cameras": flat_camera_data
    }
    
    # writes output file using above defined Custom Dumper    
    with open(output_path, 'w') as f:
        yaml.dump(mamma_calib, f, Dumper=InlineSequenceDumper, default_flow_style=False, sort_keys=False)
   # prints confirmation message indicating successful conversion and location of the generated output file
    print(f"Converted calibration data successfully saved to {output_path}")

# specifies the paths for the input and output files for the conversion process
intrinsic_file = r"C:\week6calibration\intri\output\intri.yml"   
extrinsic_file = r"C:\week6calibration\extri\extri.yml"          
output_file = r"C:\week6calibration\mamma_outputv3.yaml"           

# calls the conversion function using the above file paths are inputs and outputs the converted data to the specified output file
convert_easymocap_to_mamma(intrinsic_file, extrinsic_file, output_file)








