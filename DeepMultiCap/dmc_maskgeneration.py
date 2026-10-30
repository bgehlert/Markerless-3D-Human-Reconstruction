import os
import cv2

try:
    from rembg import remove
except ImportError:
    print("Installing missing dependencies ('rembg'). Please wait...")
    os.system('pip install rembg opencv-python')
    from rembg import remove

def generate_binary_masks():
    camera_ids = ['0', '1', '2', '3']
    
    print("Initializing mask generation pipeline...")
    
    for cam in camera_ids:
        img_dir = f'images/{cam}'
        mask_dir = f'masks/{cam}'
        
        # Create output mask directory if it doesn't exist
        os.makedirs(mask_dir, exist_ok=True)
        
        if not os.path.exists(img_dir):
            print(f"Skipping Camera {cam}: Source directory '{img_dir}' not found.")
            continue
            
        print(f"Processing background removal for Camera {cam}...")
        
        # Fetch and sort all matching PNG frames
        all_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith('.png')])
        
        if not all_files:
            print(f"  -> No PNG frames found inside '{img_dir}'")
            continue
            
        for filename in all_files:
            img_path = os.path.join(img_dir, filename)
            mask_path = os.path.join(mask_dir, filename)
            
            # Read image frame
            input_img = cv2.imread(img_path)
            if input_img is None:
                continue
                
            # Strip background and get alpha channel mask
            output_rgba = remove(input_img)
            alpha_channel = output_rgba[:, :, 3]
            
            # Convert alpha channel into strict solid binary black & white (0 or 255)
            _, binary_mask = cv2.threshold(alpha_channel, 10, 255, cv2.THRESH_BINARY)
            
            # Save the final mask
            cv2.imwrite(mask_path, binary_mask)
            
        print(f"  -> Completed formatting masks for Camera {cam}!")

    print("\nAll background matting masks successfully created and sorted!")

if __name__ == '__main__':
    generate_binary_masks()
