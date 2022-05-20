# SMILI Container

The SMILI pipeline is one of three pipelines (along with EHT-Imaging and DIFMAP) used to produce the M87* Black Hole images released by the Event Horizon Telescope Collaboration (EHTC). This project aims to provide findings about the reproducibility process of reconstructing an image of a black hole using the SMILI Python library for imaging.

NOTE: SMILI uses an older version of astropy, but the newest version of astropy is needed for some post-processing steps. Consider looking into this if running into errors in these parts.

## Summary of Contents
`~/Src_EHT` contains the reproducibility files. The other files in the home (`/root`) directory are all dependencies, and `~/smili` is the SMILI imaging program installation.  
* `~/Src_EHT/data` contains the .uvfits files, which are passed as input into the pipeline
* `~/Src_EHT/smili` contains the scripts necessary to generate the .fits files (grayscale images) and perform post-processing using the `ehtim` Python module.
  * `example_driver.py` -- (from a comment within the file) "The script is an example driver of the SMILI M87 Stokes I Imaging Pipeline
(smili_imaging_pipeline.py) for EHT observations in April 2017 attached in the
same directory. For more detail instructions for smili_imaging_pipeline.py
please read the help document associated in the imaging script
"python smili_imaging_pipeline.py --help"
  * `smili_postprocessing.py` -- Python script that creates a PDF image from a .fits file and puts it in `/post`
  * `run.sh` -- runs the driver code for SMILI to generate .fits files
  * `run_postprocessing.sh` -- runs the post-processing script on all observation days
  * `run_complete.sh` -- runs `run.sh` and `run_postprocessing.sh`, the whole SMILI pipeline

## Pulling and Running the Container
```
docker pull globalcomputinglab/reproducibility-eht:smili
```
```
docker run -it -p 9000:8888 globalcomputinglab/reproducibility-eht:smili
```

## Executing the Pipeline
From `~/Src_EHT/smili`, you can execute the pipeline and post-processing with the following command

```
./run_complete.sh
```

## Post-Processing
The black hole images shown in Paper IV uses the afmhot_10us colormap as well as a restoring beam for blurring. ```run_postprocessing.sh``` should run ```smili_postprocessing.py``` for the four days of observation and output a PDF of the image. There are some flags and edits you can make to the code to change the output.

*The post-processing is built into the main run script (`run_complete.sh`), but to edit the output images, use the separate post-processing run script (`run_postprocessing.sh`).*

## Copying Output Images to Local Machine
Obtain the container id of the latest entry with
```
docker ps -a
```
and copy the output folder to the current local directory with
```
docker cp [container id]:/root/Src_EHT/smili/post .
```