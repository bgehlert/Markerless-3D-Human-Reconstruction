# DeepMultiCap Installation and Demo
The following README.md file outlines the installation steps, and required configurations and downloads regarding the initial implementation of DeepMultiCap.

| Environment Element    | Version/Model |
| -------- | ------- |
| GPU  | NVIDIA RTX 2000 Ada Generation |
| Python  |  |
| PyTorch  |  |
| CUDA  |  |
| cuDNN  |  |
| DeepMultiCap GitHub Repository | git describe --tags |
| GitHub Commit ID | git log -n 1 --oneline |

## Installation Steps


DeepMultiCap requires a **NVIDIA GPU** and **CUDA drivers** for installation and implementation. This is available using the LIMB Lab computer which operates using a **NVIDIA RTX 2000 Ada Generation**. Connect using Windows Remote Desktop Connection as required. Detailed instructions in connecting remotely can be found on the LIMB Lab Wiki.


### 1. Host Environment and WSL Setup
Begin by downloading WSL (Windows Subsystem for Linux). The cloned code will not operate natively inside an Anaconda Prompt on Windows.


WSL can be downloaded through Anaconda Prompt by executing:
```bash
wsl --install
```
* **Restart:** After installation, restart the computer as prompted. A new Unix user account and password can be configured. Alternatively, the LIMB lab credentials are as follows:
  * **Unix user account:** `labadmindy`
  * **Password:** `L1MBlab421!`

When installed successfully, the screen will display a green command line. All subsequent steps must be executed entirely inside the WSL Linux environment.
<img width="1475" height="275" alt="image" src="https://github.com/user-attachments/assets/0119e72d-eb67-4b18-b0b0-111a2ef66e25" />

### 2. Miniconda Environment Preparation
This setup is necessary if it is the first time Miniconda is being used on the WSL Linux environment. Download and execute the Miniconda Linux installation package script:
```bash
mkdir -p ~/miniconda3
wget https://anaconda.com -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
Link the conda executables into the native command terminal profile:
```bash
~/miniconda3/bin/conda init bash
source ~/.bashrc
```
*(The command prompt line should now display `(base)`)*.

Accept the Anaconda terms of service with the following commands:
```bash
conda tos accept --override-channels --channel https://anaconda.com
conda tos accept --override-channels --channel https://anaconda.com
```
### 3. Base System Dependencies and Repository Setup
Build a clean, native Python 3.8 environment and activate it:
```bash
conda create -n deepmulticap python=3.8 -y
conda activate deepmulticap
```
*(The command prompt line should now switch to displaying `(deepmulticap)`)*.

Move inside the appropriate file directory to begin repository cloning:
```bash
cd /home/labadmindy
git clone https://github.com/DSaurus/deepmulticap.git
cd deepmulticap
```
### 4. Core Framework Dependencies
The below libraries must be downloaded separately from the cloned code.
```bash
pip install torchvision trimesh numpy matplotlib Pillow scikit-image tqdm opencv-python
```
Specify and install the required versions of `taichi` and `taichi three`:
```bash
pip install taichi==0.7.15 taichi_three taichi_glsl==0.0.10
```
Install `tensorboard` and `configargparse`:
```bash
pip install tensorboard
pip install configargparse
```
Visit (https://www.patrickmin.com/binvox/) to download the Linux 64 bit executable:
<img width="1290" height="892" alt="image" src="https://github.com/user-attachments/assets/56463e72-d0a9-4e88-8eeb-06f1230bf8cf" />
Copy the downloaded file into the Linux environment:
```bash
cp /mnt/c/Users/labadmin/Downloads/binvox ~/deepmulticap/
chmod +x ~/deepmulticap/binvox
sudo mv ~/deepmulticap/binvox /usr/local/bin/
```
*(You will be prompted to enter a password. See credentials above if using the previously initialized `labadmindy` account)*.

### 5. Optional: ProcessError Environment Fixes
The following steps were used to resolve `CalledProcessError` and may not be required for every installation.

Update the core package index and install necessary graphics, OpenGL, and window system libraries:
```bash
sudo apt-get update && sudo apt-get install -y libgl1 libglu1-mesa libx11-6
```

Create a symbolic link between missing file link and existing library file:
```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libGL.so.1 /usr/lib/libGL.so
```

Resolve Boolean error due to libraries and/or files that have changed with updated versions:
```bash
 sed -i 's/np.bool/bool/g' ~/deepmulticap/lib/sdf.py
sed -i 's/np.bool/bool/g' ~/deepmulticap/lib/data/DMCDataset.py
sed -i 's/marching_cubes_lewiner/marching_cubes/g' ~/deepmulticap/lib/mesh_util.py
sed -i 's/marching_cubes_lewiner/marching_cubes/g' ~/deepmulticap/lib/mesh_util.py
```
