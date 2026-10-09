# MAMMA Installation and Demo
The following README.md file outlines the installation steps, commands and configuration, input and output descriptions, and performance metric and notes regarding the initial implementation of MAMMA (Markerless Accurate Multi-person Motion Acquisition).

| Environment Element    | Version/Model |
| -------- | ------- |
| GPU  | NVIDIA RTX 2000 Ada Generation |
| Python  | 3.11.16 |
| PyTorch  | 2.6.0+cu124 |
| CUDA  | 12.4 |
| cuDNN  | 90100 |
| MAMMA GitHub Repository | v1.0.1 |
| Commit ID | 588492f |

## Installation Steps


MAMMA installation requires a **NVIDIA GPU** and **CUDA drivers** for installation and implementation. This is available using the LIMB Lab computer which operates using a **NVIDIA RTX 2000 Ada Generation**. Connect using Windows Remote Desktop Connection as needed. Detailed instructions in connecting remotely are found on the LIMB Lab Wiki.


### 1. Host Environment and WSL Setup
Begin by downloading WSL (Windows Subsystem for Linux). The cloned code will not operate natively inside an Anaconda Prompt on Windows.


WSL can be downloaded through Anaconda Prompt by executing:
```bash
wsl --install
```
* **Restart:** After installation, restart the computer as prompted.
* **Credentials:** A new terminal window titled "labadmindy@LWELTE-LB01" will appear. The default Unix user credentials have already been configured:
  * **Unix user account:** `labadmindy`
  * **Password:** `L1MBlab421!`


When installed successfully, the screen will display a green command line. All subsequent steps must be executed entirely inside the WSL Linux environment.
<img width="1475" height="275" alt="image" src="https://github.com/user-attachments/assets/0119e72d-eb67-4b18-b0b0-111a2ef66e25" />

### 2. Base System Dependencies and Repository Setup
Update the core package index and install required external video encoders:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y nodejs npm ffmpeg
```
Clone the MAMMA code repository from GitHub and move inside the downloaded project folder:
```bash
git clone https://github.com/cuevhv/mamma.git
cd mamma
```
Force temporary package compilation paths onto the main storage block rather than the small default WSL root space. This is to avoid a "No space left on device" error.
```bash
mkdir -p ~/mamma/tmp && export TMPDIR=~/mamma/tmp
```
### 3. Miniconda Environment Preparation
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
Build a clean, native Python environment and activate it:
```bash
conda create -n mamma python=3.11 -y
conda activate mamma
```
*(The command prompt line should now switch to displaying `(mamma)`)*.

### 4. Core Framework Dependencies
The below libraries must be downloaded separately from the cloned code.
Install the repository requirements directly from the folder configuration index:
```bash
pip install --no-cache-dir -r requirements/requirements.txt
pip install --no-cache-dir flask flask-cors pyyaml opencv-python python-dotenv decord
```
Install **Meta Detectron2 2D posturing** and **PyTorch SDF 3D collision geometry** directly from source:
```bash
pip install --no-build-isolation -r requirements/requirements_no_build_isolation.txt
```
Install the specific **CUDA 12.2 Toolkit** package:
```bash
conda install -c nvidia/label/cuda-12.4.1 cuda-toolkit -y
```
Export environmental variables for the active session:
```bash
export CUDA_HOME="$CONDA_PREFIX"
export PATH="CUDAHOME/bin:PATH"
```
### 5. Runtime Script Environment Fixes
Creates a filter for Conda manager to handle cleaned execution commands correctly:
```bash
rm -f ~/.local/bin/conda
cat << 'EOF' > ~/.local/bin/conda
#!/bin/bash
if [ "$1" = "run" ]; then
 shift
 args=()
 for arg in "$@"; do
 [ "arg"!="--"]&&args+=("arg")
 done
 exec /home/labadmindy/miniconda3/bin/conda run "${args[@]}"
else
 exec /home/labadmindy/miniconda3/bin/conda "$@"
fi
EOF
chmod +x ~/.local/bin/conda
```


Create workspace paths so that background processing routines can find internal modules across terminal reboots and prevent `file not found` errors:
```bash
echo 'export PYTHONPATH=PYTHONPATH:(pwd)/gui/backend' >> ~/.bashrc
source ~/.bashrc
```


### 6. Weights Unpacking Patch
The below step is necessary to trust the `weights` file containing the memory the deep learning model gained during training and refusing to open the file as it would a virus.


Open the 2D execution script to patch a weights validation security block:
```bash
nano /home/labadmindy/mamma/landmarks/run_ma_2d.py
```
Locate this specific line:
```python
model.load_state_dict(torch.load(args.weights)['state_dict'])
```
Modify it to incorporate the `weights_only=False` bypass parameter. The line should now appear as so:
```python
model.load_state_dict(torch.load(args.weights, weights_only=False)['state_dict'])
```
*Press `Ctrl + O` then `Enter` to save, and `Ctrl + X` to exit the nano editor.*


### 7. Diagnostics and Verification
Run local diagnostics to verify dependencies, weights, and environments return clean passes:
```bash
python -m inference doctor
```
Once the inference doctor returns "**`PASS - environment looks healthy.`**", it is safe to run the below command to open the interactive user interface and submit a task.
<img width="1499" height="603" alt="image" src="https://github.com/user-attachments/assets/5f962744-ed2b-4b09-9c42-524d68bb4cf5" />

```bash
bash gui/scripts/dev.sh
```
<img width="1639" height="981" alt="image" src="https://github.com/user-attachments/assets/dc7c4729-2c2b-46fd-833f-fe146a92695b" />

Once inside the web browser interface, download the following, located under Pipeline assets:
* **YOLO12x detector**
* **SAM 2.1 (large)**
* **SMPL-X locked head**
* **Downsampled SMPL-X vertices**
* **MammaNet landmark .ckpt model file**
<img width="1253" height="685" alt="image" src="https://github.com/user-attachments/assets/47f50bf4-f690-4a1c-910b-f83033e94f83" />


### Optional: WSL Memory Allocation Expansion
If encountering an Out Of Memory (OOM) error when running the demo files, the following fix can be employed to expand default WSL memory limits:
```powershell
powershell.exe -Command "Set-Content -Path \$env:USERPROFILE\.wslconfig -Value '[wsl2]', 'memory=24GB', 'swap=16GB' -Force"
```
Execute the below command to close the WSL terminal and apply the effective changes. Reopen WSL.
```bash
wsl.exe --shutdown
```

## Downloading Model Weight Files
Both SMPL-X and MAMMA downloads must be completed before a trial will run successfully.

### a. From SMPL-X Website


1. Register for a free account at the SMPL-X website (https://smpl-x.is.tue.mpg.de/register.php)
2. Navigate to the "Download" tab.
3. Download the following module: SMPL-X with removed head bun (NPZ+PKL, 830 MB) - Use this for SOMA/MoSh/AMASS codebase
   <img width="1411" height="416" alt="image" src="https://github.com/user-attachments/assets/6ee829f4-9451-4834-a092-875890f346b2" />

5. Unzip the download. Move the downloaded female/male/neutral folders to the following file directory: Linux/Ubuntu/home/labadmindy/mamma/data/models/smplx

The models/ and smplx/ folders will need to be created.
______
### b. From MAMMA database


1. Register for a free account at the MAMMA website (https://mamma.is.tue.mpg.de/register.php).
2. Inside the active WSL terminal run the following command to download the indoors iPhone video trials (16 sequences). Other demo datasets are available for download - the command below can be modified to adjust which dataset is being downloaded.
```bash
bash data/download_mamma_iphone.sh--meta--pred--videos--indoors
```
  <img width="1545" height="438" alt="image" src="https://github.com/user-attachments/assets/a3467cfe-951e-4218-9e18-5f7a6987cfe4" />

3. Enter the previously registered email and password from Step 1 to allow the download to proceed.

## Alternative Installation Process
An environment.yml file has been prepared where the exact software environment can be replicated, avoiding the extensive library installations. Ensure that WSL is used as the main terminal and Miniconda/Anaconda has been installed within WSL. Detailed steps are provided earlier in this README.md file.
Create the environment (includes PyTorch+cu124 and all 216 dependencies):
Download the environment.yml file available here and document where it is stored on your desktop.
Change directory to the file location by replacing `path/to/your/project-folder` with your specific file location.
```bash
cd path/to/your/project-folder
```
Replicate the environment that has been already been created.
```bash
conda env create -f environment.yml
```
Activate the environment:
```bash
conda activate mamma
```
Download MAMMA and SMPL-X model weight files using the process outlined in the section above. The web browser interface is now ready to be used.
```bash
bash gui/scripts/dev.sh
```
Once inside the web browser interface, download the following, located under Pipeline assets:
* **YOLO12x detector**
* **SAM 2.1 (large)**
* **SMPL-X locked head**
* **Downsampled SMPL-X vertices**
* **MammaNet landmark .ckpt model file**

## When Reopening
Follow the below steps when reopening MAMMA after all previous installations have been completed. Note that all the indicated prompts are to be commanded in WSL.

Move inside the downloaded project folder.
```bash
cd mamma
```
Activate the created MAMMA environment.
```bash
conda activate mamma
```
Open the user-friendly GUI interface. A demo task is ready to be submitted.
```bash
bash gui/scripts/dev.sh
```

The Google Chrome browser with the MAMMA interface will open after commanding the above. The terminal must remain open for MAMMA to be interactive.
