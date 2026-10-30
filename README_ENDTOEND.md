# End-to-End Completion of Selected Pipelines
The following markdown file describes  the process required to take a common capture and produce outputs from both explored methods: MAMMA and DeepMultiCap.


## Camera Calibration
Video capture protocol for calibration is detailed in Capture Protocol_v2, with information regarding camera setup, intrinsic and extrinsic video requirements, and required commands to install and run the EasyMoCap Calibration Module. 

Calibration should be completed and verified before proceeding with trial data capture. Ensure the reprojection errors are smaller than 0.5 px, otherwise repeat the calibration video capture. If using the EasyMocap Calibration Module, as suggested in Capture Protocol_v2, two output files will be produced upon completion: `intri.yml` and `extri.yml`.

* **Intrinsic Video Capture**: Each camera records separately. Videos will not be synchronized with one another. Take the checkerboard and move it slowly to all corners of the camera frame. Then, tilt (left/right/front/back) and rotate (clockwise/counterclockwise) the board, while keeping it completely in frame. It is suggested to capture the intrinsic videos from the location of the anticipated subject. Label videos as `0.mp4`, `1.mp4`, `2.mp4`, `3.mp4` based on the device the respective video was recorded on. Note that intrinsic and extrinsic videos from the same device must share matching filenames.
Intrinsic videos for calibration can be reused, even if the cameras are moved.

* **Extrinsic Video Capture**:  The checkerboard is stationary and in a position where it can be seen by all cameras. Each camera records a short clip of the checkerboard, ideally at the same time. Since the scene is static, with no moving board, this is not a hard requirement and calibration may be successful without synchronized extrinsic calibration videos. Label videos as `0.mp4`, `1.mp4`, `2.mp4`, `3.mp4` based on the device the respective video was recorded on.
The cameras must remain fixed after the extrinsic calibration for the calculated extrinsic parameters to remain valid – moving the cameras will require recalibrating the system entirely.

## Video Capture
Video capture protocol for trials is detailed in Trial Protocol_v1, with information regarding selected motions, naming conventions, and variable control.

* **Trial Capture**: Recorded motion trials can be recorded once and run end-to-end through each of the methods. The following sections will describe how to prepare the videos post-capture for the methods. An audio cue (i.e., a clap) must be completed at the beginning and end of each
trial so the multi-view clips can later be synchronized. 

## Video Synchronization
Each of the explored methods requires synchronized videos before entering the preprocessing stages. Synchronized videos indicates temporal alignment, meaning Frame 1 in each of the videos represents the same moment in time during the trial.
DaVinci Resolve is a free video editing software that successfully aligns the multi-view cameras with the audio cue mentioned above. Note that videos should be renamed and converted to .mp4 files before importing into DaVinci Resolve.
Name each of the clips according to the camera they were recorded on. .MOV files can be converted to .mp4 files by simply renaming without any file compatibility issues.

1. Create a new project and add the recorded trials clips under File > Import > Media . Import each of the uncut trial videos. Holding Shift, select each of the individual clips and right-click to "Create New Timeline Using Selected Clips".
<img width="307" height="159" alt="image" src="https://github.com/user-attachments/assets/06ec168d-a6dd-475f-90c0-5b239c4f18a6" />

2. Arrange the video (blue) and audio (green) tracks by dragging and dropping each clip onto its own horizontal row. There should not be more than one clip per row.
<img width="638" height="198" alt="image" src="https://github.com/user-attachments/assets/9c7f6064-69f9-44c5-93dd-f864cdda6b09" />

3. Once the videos are correctly arranged, Ctrl + A will allow all of the video and audio tracks to be selected within the timeline. Right-click and select "Automatically Align Clips". Allow the clips to be synchronized using Waveform.
<img width="253" height="109" alt="image" src="https://github.com/user-attachments/assets/b22165f5-cca7-46a7-bc5e-b2b878540382" />

4. Once the beginning and end claps of each clip are arranged, the videos can be cut with only the motion trial preserved. The claps are not needed in the final multi-view videos. Navigate frame-by-frame using the left/right arrow keys and determine where the desired video frames are within the clip.
Ctrl + Shift + [ will trim off whatever is to the left of the red cursor. Ctrl + Shift + ] will trim off whatever it to the right of the red cursor.

5. When ready to export, navigate to the rocket icon on the bottom right of the screen. Make sure to render individual files in MP4 format with an H.264 codec and 1080 x 1920 HD resolution. Replicate the configurations in the provided images.
<img width="278" height="449" alt="image" src="https://github.com/user-attachments/assets/c787d6ea-5e74-417a-b36f-0ecef113bc6d" />
<img width="278" height="449" alt="image" src="https://github.com/user-attachments/assets/d47bff3b-40a5-4610-ac6d-617646748982" />


6. When ready, select "Add to Render Queue" and finally "Render All" on the right to export the synchronized clips. The video source names (`0.mp4`, `1.mp4`, `2.mp4`, `3.mp4`) will be preserved and the files will be exported to the specified location.

# MAMMA Pipeline
Complete steps for running the MAMMA Pipeline are provided below. 

<img width="1152" height="691" alt="image" src="https://github.com/user-attachments/assets/90372a43-b952-49af-81f5-348eeabe4f8c" />

### Folder Organization
When using your collected videos (i.e., non-demo videos), ensure the below folder organization is used. Synchronized videos should all be placed together in the videos subfolder as .mp4 files.  

<img width="164" height="122" alt="image" src="https://github.com/user-attachments/assets/952bf502-7ab1-4162-b66f-15a7bf9b7876" />

### Command Execution
The following deliverable describes the exact processing script and commands required to obtain a successful human body model representation. Note that MAMMA accepts the `.mp4` video files directly and does not require further preprocessing steps aside from the video synchronization and calibration conversion script.

#### Calibration Conversion
It is recommended to complete calibration using the EasyMocap Calibration Module. Detailed instructions regarding the recording processes of the intrinsic and extrinsic videos and the specific commands can be found in the [Capture Protocol](https://docs.google.com/document/u/0/d/1phfJObMjjyiV8yENfap7JooZPrde2X_-KivPoNmvfNo/edit). The intri.yml and extri.yml files are only valid for a single camera setup. If the cameras are moved, this requires the entire EasyMocap Calibration module script to be rerun. After the `intri.yml` and `extri.yml` files are obtained from the EasyMocap script, they must be converted into a single, acceptable .yaml file for MAMMA input. A [calibconversion.py](http://calibconversion.py) script has been prepared for this process. This script receives the `intri.yml` and `extri.yml` file path locations and will create a converted calibration file, `mamma_output.yaml`, or as otherwise named.

Upon launching Windows Subsystem for Linux (WSL), execute the following commands to convert the calibration file:

Move inside the downloaded project folder :  
```bash
cd ~/mamma/configs/examples/calib/
```
*Note that this file directory should be where the `calibconversion.py` script is stored.*

Call the calibration conversion script:
```bash
python calibconversion.py
```
Return to the main project folder to prepare for mesh reconstruction steps:
```bash
cd ~/mamma
```

#### Reconstruction Command
The GUI was not able to be used with our own recorded videos and failed at the first stage of the pipeline, ma_cap. Human mesh representations can still be obtained by running the following set of commands directly in the WSL terminal. The legend indicates how to modify this command to your unique capture.  
   
```bash
MPLBACKEND=Agg python \-m inference run \

  \--cfg      configs/examples/presets/full.yaml \

  \--footage  /home/labadmindy/mamma/data/week6trial \

  \--seq\_name neutral \

  \--calib    /home/labadmindy/mamma/configs/examples/calib/mamma\_outputv3.yaml \

  \--out-tag  run03 \-v
```
Do not modify the above order of commands.

#### Legend 
Modify the above script as follows to reflect the desired trial.

| Command | Do not modify this line in any way. `MPLBACKEND=Agg python \-m interference run \` |
| :---- | :---- |
| Configuration | Modify this line to process 30 frames (`quick.yaml`) or the entire clip (`full.yaml`). The remaining file directory does not change. Choose between running the following configurations: Quick (30 frames): `configs/examples/presets/quick.yaml` or Full (complete clip): `configs/examples/presets/full.yaml`. If a custom configuration is desired, this `.yaml` must be prepared by replicating the file format. |
| Footage | Modify this line to indicate the absolute footage path. A variety of sequence or trial subfolders may be present within this absolute footage path. The folder structure should not be changed, although “week6trial” may be replaced with an alternate folder name. `/home/labadmindy/mamma/data/week6trial/` |
| Sequence Name | Modify this line to indicate the desired sequence (i.e., trial or motion). This sequence should be a subfolder within the above absolute footage path. `neutral \` |
| Calibration File | Indicate the file path of the *converted* YAML calibration file. Only the file name (`mamma\_outputv3.yaml`) may change from this line and the file nesting should be exactly as displayed. `/home/labadmindy/mamma/configs/examples/calib/mamma\_outputv3.yaml \` |
| Output Name | Enter the name under which the relevant outputs will be stored by replacing . The `-v` must remain to view intermediate processing steps and detailed progress. `run03 \-v` |

### Pipeline Processing 
As the above script runs, it will progress through the five stages of the pipeline: ma\_cap, ma\_masks, ma\_2d, ma\_3d, ma\_vis. 

At each stage, the terminal will display: 
```bash
INFO inference.status: status: ma_cap[neutral] -> Running pid=17404
```
or in the general format:  
```bash
INFO inference.status: status: ma_pipelinestage[sequencename] -> Running pid=XXX
```
   
and upon completion:  
```bash
INFO inference.status: status: ma_masks[neutral] -> Done
```
or in the general format:  
```bash
INFO inference.status: status: ma_pipelinestage[sequencename] -> Done
```
<img width="1835" height="362" alt="image" src="https://github.com/user-attachments/assets/9a31364e-4bb9-4886-9544-592c5b778d5a" />

If a stage of the pipeline fails, it will display:  
```bash
INFO inference.status: status: ma_masks[neutral] -> Failed  
ERROR inference.runner: ma_masks[neutral] exit=134 -- check output/logs/jobs/labadmindy/run02/ma_masks/neutral.err
```
or in the general format:
```bash
INFO inference.status: status: ma_pipelinestage[sequencename] -> Failed  
ERROR inference.runner: ma_pipelinestage[sequencename] exit=XXX -- check output/logs/jobs/labadmindy/runname/ma_pipelinestage/sequencename.err
```

These printed lines indicate at which stage the processing failed and where the error file can be located. Follow the file path directory to open the `sequencename.err` file and determine the cause for failure. Note that if a pipeline stage fails, the subsequent stages will *all* cancel. See below.

 <img width="1827" height="237" alt="image" src="https://github.com/user-attachments/assets/b8820211-4da4-4db4-ae5c-44b018c1fa80" />

### Primary Outputs 
After pipeline completion, a `preview.mp4` and `scene.rrd` file will be outputted in the output subfolder at the following file path directory: `/home/labadmindy/mamma/output/ma_vis/runname/`

The `.mp4` video file consists of a superimposed mesh overlay onto the original video for each camera view. This is viewable in a standard desktop media player.  
<img width="1537" height="907" alt="image" src="https://github.com/user-attachments/assets/6093e9cd-bcd4-4b51-86df-14b62c9f2057" />

The `.rrd` file consists of a point cloud generated for each camera view as well as a complete 4D body reconstruction of the filmed subject. This output has been confirmed to be plausibly metric.   

 <img width="1507" height="790" alt="image" src="https://github.com/user-attachments/assets/7b45f5c0-55f1-4336-986f-db81dc60bcbf" />


# DeepMultiCap Pipeline
Complete steps for running the DeepMultiCap pipeline are provided below. Note that calibration and synchronization steps covered above should be completed before advancing through the following stages.

<img width="992" height="695" alt="image" src="https://github.com/user-attachments/assets/246d7899-53aa-4510-9c3b-c24b9c4ed7c6" />

### Folder Organization
When running the DeepMultiCap pipeline, it is recommended to work between two main folders, one where preprocessing steps are completed, and another where inputs are prepared to be fed into the pipeline. The following folder structure is recommended. Note that the `multihuman/` folder and its subfolders should be created from dowloaded the demo data; the rest must be created manually. 

<img width="210" height="228" alt="image" src="https://github.com/user-attachments/assets/5bfae97e-90a0-4dcf-af34-143cc3f34625" />

### Command Execution
The following deliverable describes the exact processing scripts and commands required to obtain a successful human body model representation. Note that DeepMultiCap cannot directly accept `.mp4` video files and further preprocessing steps are required after video synchronization.

#### Calibration Conversion
It is recommended to complete calibration using the EasyMocap Calibration Module. Detailed instructions regarding the recording processes of the intrinsic and extrinsic videos and the specific commands can be found in the Capture Protocol. The intri.yml and extri.yml files are only valid for a single camera setup. If the cameras are moved, this requires the entire EasyMocap Calibration module script to be rerun. After the `intri.yml` and `extri.yml` files are obtained from the EasyMocap script, they must be converted into an individual intrinsic and extrinsic camera parameter file per camera. When recording with four cameras, this equates to eight separate `.npy` files. A [dmc_calibconversionv2.py](dmc_calibconversionv2.py) has been prepared for this process. This script receives the `intri.yml` and `extri.yml` file path locations and will create the converted calibration files in the appropriate subfolder.

Upon launching Windows Subsystem for Linux (WSL), execute the following commands to obtain a successful representation.

Move inside the downloaded project folder:  
```bash
cd ~/deepmulticap/dataset/week7trial/neutral/
```
*Note that this file directory should be where the `dmc_calibconversionv2.py` script is stored.*

Activate the created DeepMultiCap environment:
```bash
conda activate deepmulticap
```

Call the calibration conversion script:
```bash
python3 dmc_calibconversionv2.py
```

#### Frame Extraction
Extract the frames from the synchronized videos:
```bash
ffmpeg -i videos/0.mp4 -q:v 2 images/0/%d.jpg
ffmpeg -i videos/1.mp4 -q:v 2 images/1/%d.jpg
ffmpeg -i videos/2.mp4 -q:v 2 images/2/%d.jpg
ffmpeg -i videos/3.mp4 -q:v 2 images/3/%d.jpg
```
#### Mask Generation
Create mask subfolders and generate the masks using the `dmc_maskgeneration.py` script:
Return to the main project folder:
```bash
mkdir -p masks/0 masks/1 masks/2 masks/3
python3 dmc_maskgeneration.py
```
#### EasyMocap Preparation
The SMPL-X model fitting is the most intensive step of the DeepMultiCap pipeline as it requires using the EasyMocap pipeline and outputs. EasyMocap must be installed prior to use. Create the environment by [downloading the environment.yml file] available in this repository.

Document where it is stored on the desktop. Change directory to the file location by replacing `path/to/your/EasyMocap-folder` with the specific `environment.yml` file location.
```bash
cd ~/path/to/your/EasyMocap-folder
```
Replicate the environment that has been already been created.
```bash
conda env create -f environment.yml
```
Activate the environment:
```bash
conda activate easymocap
```
*(The command prompt line should now switch to displaying `(easymocap)`)*.

Organize the EasyMocap files as follows:

<img width="157" height="142" alt="image" src="https://github.com/user-attachments/assets/a4c63493-d027-4d9d-b602-0b1c38d82a9b" />

The `videos/` folder should contain the four synchronized `.mp4` videos, and the `images/` folder should contain the subfolders of extracted frames. These files have already been obtained by following earlier steps. Organize the files by copy/pasting or using terminal commands. Note that when these files are copy/pasted, a `ZONE.Identifier` file will accompany each file. These will need to be deleted from everywhere they appear.

Download each of the model weights and place them at `EasyMocap/data/models/yolov4.weights` and `EasyMocap/data/models/pose_hrnet_w48_384x288.pth`. 
It may be possible to directly extract the model weights to these locations after downloading.

```bash
mkdir -p data/models
wget -c https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights -O data/models/yolov4.weights
curl -L -o data/models/pose_hrnet_w48_384x288.pth https://huggingface.co/Prophetetc/cocopose/resolve/main/pose_hrnet_w48_384x288.pth
```
Extract the 2D keypoints from each of the video frames. 
```bash
python3 apps/preprocess/extract_keypoints.py week8trial --mode yolo-hrnet
```
An `annots/` folder will be generated with `0/`, `1/`, `2/`, `3/` subfolders populated with `.json` files for each frame.

*Note that week8trial explicitly refers to the folder where the images, videos, and calibration files have been copied. This may be different depending on how you have organized your respective files.*

Complete the EasyMocap pipeline by running the `mv1p.py` demo script on your recorded data:
```bash
python3 apps/demo/mv1p.py week8trial --out week8trial/output --vis_det --vis_repro --undis --vis_smpl
```

The `.json` files contained within the `smpl/` output folder will be used for the DeepMultiCap pipeline.

#### Obtaining the SMPL-X Model
Upon completion of the EasyMocap pipeline, the outputted `.json` files must be converted to `.npz` files. 

Return back to the DeepMultiCap project folder and virtual environment:
```bash
cd ~/deepmulticap
conda activate deepmulticap
```
A custom script, [dmc_repackv2.py](dmc_repackv2.py) is used to convert the `.json` files to `.npz` files. To access this script, navigate to the project folder where it is stored, for example `deepmulticap/dataset/week7trial/neutral/`, and call the script:

```bash
cd ~/deepmulticap/dataset/week7trial/neutral/
python3 dmc_repackv2.py
```
The `.npz` files will be saved to deepmulticap/dataset/week7trial/neutral/smplx_v2/`.

Finally, [convert_with_easymocapv4.py](convert_with_easymocapv4.py) is used to obtain a `smplx.obj` model:
```bash
python3 convert_with_easymocapv4.py
```
A `XXXXXX.obj` file will be saved directly to `deepmulticap/dataset/week7trial/neutral/`

#### Preparing a Configuration File

### Pipeline Processing
Before running the DeepMultiCap pipeline, confirm there is the following prepared:

* (1) `jpg` extracted video frame;
* (1) `.jpg` generated mesh file;
* (8) `.npy` calibration files;
* (1) `.obj` generated SMPL-X file and;
* (1) `.yaml` prepared configuration file

Enter the main project folder and activate the virtual environment:
```bash
cd ~/deepmulticap
conda activate deepmulticap
```
Call the `eval_3d.py` script to execute the reconstruction using the following command: 

```bash
python apps/eval_3d.py --config configs/week7trial.yaml --dataroot dataset/multihuman
```

*Note that `week7trial.yaml` and `/multihuman` will be replaced with your specific configuration file name and nested folder, respectively.* 

### Primary Outputs
Upon pipeline completion, an `inference_eval_subfoldername_0.obj` and `inference_eval_foldername_0.png` file will be outputted in the results subfolder at the following file path directory: `home/labadmindy/deepmulticap/results/projectfoldername/. 
DeepMultiCap will provide these two outputs per inputted frame.

The `.obj` 3D file consists of a textured mesh viewable in a 3D viewer, such as MeshLab or Blender. 

<img width="1918" height="1111" alt="image" src="https://github.com/user-attachments/assets/e969dd72-bc19-4bbe-92c9-e285eab1376c" />


The `.png` image file consists of both the multi-view camera captures, and 3D mesh and normal maps. A normal map is a texture mapping technique, with the color indicating which direction the surface geometry is facing.

<img width="1857" height="245" alt="image" src="https://github.com/user-attachments/assets/1a6d8562-3ffe-4a47-acef-5854b28fc065" />


