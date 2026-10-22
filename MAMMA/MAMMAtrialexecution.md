# MAMMA Trial Execution
## Folder Organization
When using your collected videos (i.e., non-demo videos), ensure the below folder organization is used. Synchronized videos should all be placed together in the videos subfolder as .mp4 files.  

<img width="327" height="243" alt="image" src="https://github.com/user-attachments/assets/952bf502-7ab1-4162-b66f-15a7bf9b7876" />

*Figure 1: Required file organization for MAMMA implementation*

## Command Execution
The following deliverable describes the exact processing script and commands required to obtain a successful human body model representation. 

1. It is recommended calibration is completed using the EasyMocap Calibration module. Detailed instructions regarding the recording processes of the intrinsic and extrinsic videos and the specific commands can be found in the [Capture Protocol](https://docs.google.com/document/u/0/d/1phfJObMjjyiV8yENfap7JooZPrde2X_-KivPoNmvfNo/edit) and the [Calibration Installation and Implementation](https://docs.google.com/document/u/0/d/1WL8AmytKCTCHUoV0wRJeFKKUasOBdrss0I2sqI7HtfM/edit), respectively. Intrinsic videos may be reused, however extrinsic calibration videos must be repeated each time the cameras move. The intri.yml and extri.yml files are only valid for a single camera setup. If the cameras are moved, this requires the entire EasyMocap Calibration module script to be rerun. After the intri.yml and extri.yml files are obtained from the EasyMocap script, they must be converted into a single, acceptable .yaml file for MAMMA input. A [calibconversion.py](http://calibconversion.py) script has been prepared for this process. This script receives the intri.yml and extri.yml file path locations and will create a converted calibration file, mamma\_output.yaml, or as otherwise specified.

2. Upon launching Windows Subsystem for Linux (WSL), execute the following commands to obtain a successful representation.

Move inside the downloaded project folder :  
```bash
cd mamma
```

Activate the created MAMMA environment:
```bash
conda activate mamma
```

3. The GUI was not able to be used with our own recorded videos and failed at the first stage of the pipeline, ma_cap. Human representations can still be obtained by running the following set of commands directly in the WSL terminal. The legend indicates how to modify this command to your unique capture.  
   
```bash
MPLBACKEND=Agg python \-m inference run \

  \--cfg      configs/examples/presets/full.yaml \

  \--footage  /home/labadmindy/mamma/data/week6trial \

  \--seq\_name neutral \

  \--calib    /home/labadmindy/mamma/configs/examples/calib/mamma\_outputv3.yaml \

  \--out-tag  run03 \-v
```
Do not modify the above order of commands.

## Legend 
Modify the above script as follows to reflect the desired trial.

| Command | Do not modify this line in any way. MPLBACKEND=Agg python \-m interference run \\ |
| :---- | :---- |
| Configuration | Modify this line to process 30 frames (`quick.yaml`) or the entire clip (`full.yaml`). The remaining file directory does not change. Choose between running the following configurations: Quick (30 frames): `configs/examples/presets/quick.yaml` or Full (complete clip): `configs/examples/presets/full.yaml`. If a custom configuration is desired, this `.yaml` must be prepared by replicating the file format. |
| Footage | Modify this line to indicate the absolute footage path. A variety of sequence or trial subfolders may be present within this absolute footage path. The folder structure should not be changed, although “week6trial” may be replaced with an alternate folder name. `/home/labadmindy/mamma/data/week6trial/` |
| Sequence Name | Modify this line to indicate the desired sequence (i.e., trial or motion). This sequence should be a subfolder within the above absolute footage path. `neutral \` |
| Calibration File | Indicate the file path of the *converted* YAML calibration file. Only the file name (`mamma\_outputv3.yaml`) may change from this line and the file nesting should be exactly as displayed. `/home/labadmindy/mamma/configs/examples/calib/mamma\_outputv3.yaml \` |
| Output Name | Enter the name under which the relevant outputs will be stored by replacing . The `-v` must remain to view intermediate processing steps and detailed progress. `run03 \-v` |

*Table 1: Legend explaining the components of the execution command to obtain the desired MAMMA output*

## Pipeline Processing 
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

*Figure 2: Successful command execution and pipeline stage ma\_cap completion for neutral sequence*

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

*Figure 3: Failed pipeline stage ma_masks and cancelling of all subsequent stages*

## Primary Outputs 
After pipeline completion, a `preview.mp4` and `scene.rrd` file will be outputted in the output subfolder at the following file path directory: `/home/labadmindy/mamma/output/ma_vis/runname/`

The .mp4 video file consists of a superimposed mesh overlay onto the original video for each camera view. This is viewable in a standard desktop media player.  
<img width="1537" height="907" alt="image" src="https://github.com/user-attachments/assets/6093e9cd-bcd4-4b51-86df-14b62c9f2057" />

*Figure 4: `.mp4` video overlay file from MAMMA pipeline completion*

The .rrd file consists of a point cloud generated for each camera view as well as a complete 4D body reconstruction of the filmed subject.   

 <img width="1507" height="790" alt="image" src="https://github.com/user-attachments/assets/7b45f5c0-55f1-4336-986f-db81dc60bcbf" />

*Figure 5: `.rrd file` viewed in [rerun.io](http://rerun.io) from MAMMA pipeline completion*
