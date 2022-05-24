# DIFMAP Container

The DIFMAP pipeline is one of three pipelines (along with EHT-Imaging and SMILI) used to produce the M87* Black Hole images released by the Event Horizon Telescope Collaboration (EHTC). The container aims to provide findings about the reproducibility process of reconstructing an image of a black hole using the DIFMAP imaging program.

The `reproducibility-eht:difmap` Docker container image contains everything needed to generate the images and data summaries of M87's black hole using the DIFMAP pipeline to generate the .fits files (grayscale images).  
This includes:
  * raw data provided by The Event Horizon Telescope Collaboration (EHT) in the form of .uvfits files
  * an installation of DIFMAP, the imaging program used in this pipeline
  * files from EHT's repository necessary to run DIFMAP (slightly modified `EHT_Difmap` script, mask file, and shell scripts to automate the process)
  * Python scripts that use EHT's `ehtim` module to perform the post-processing steps on the .fits files output by EHT\_Difmap and generate final images and image summary PDFs

## Summary of Contents

* `~/uvf_difmap_2.5k` -- this is the entire DIFMAP installation  
* `~/DIFMAP/data/uvfits` -- contains the .uvfits files provided by EHT, and since their results only use the lo-band data, the unused files have been separated out into `uvfits_hi`  
* `~/DIFMAP/difmap` -- contains all of the files and scripts used to run the pipeline, detailed below:
  * `EHT_Difmap` -- DIFMAP script written by EHT to process the .uvfits files for this project, modified to place the files into `/difmap-output`
  * `difmap.sh and run.sh` -- shell scripts provided by EHT to run the `EHT_Difmap` DIFMAP script on each .uvfits file in `/data/uvfits` and outputs .fits files to `/difmap-output`
  * `difmap-postprocessing.py` -- Python script that creates a PDF image from a .fits file and puts it in `/difmap-pdfs`
  * `difmap-imgsum.py` -- Python script that generates a PDF summary of the data from given .fits and .uvfits files and puts it in `/difmap-imgsums`
  * `run-postprocessing.sh` -- shell script that runs `difmap-postprocessing.py` and `difmap-imgsum.py` on all the .fits files in `/difmap-output`
  * `difmap-complete.sh` -- shell script that runs `run.sh` and `run-postprocessing.sh`, the whole DIFMAP pipeline

## Pulling and Running the Container
The Docker image is available on our DockerHub [here](https://hub.docker.com/r/globalcomputinglab/reproducibility-eht/tags). Pull the `difmap` container using the command

```
docker pull globalcomputinglab/reproducibility-eht:difmap
```
When the image is done building, run 
```
docker run -it -p 9000:8888 globalcomputinglab/reproducibility-eht:difmap
```
This runs the container and forwards everything from port 8888 in the container to the local machine's port 9000 (or any other port number above), allowing you to interact with the container locally.

## Executing the Pipeline
From `~/DIFMAP/difmap`, you can execute the pipeline with the following command
```
./difmap-complete.sh
```
## Post-Processing
The black hole images shown in Paper IV uses the afmhot_10us colormap as well as a restoring beam for blurring.  
```run-postprocessing.sh``` will run post-processing for the four days of observation and output a PDF of the image. There are some flags and edits you can make to the code to change the output.

*The post-processing is built into the main run script (`difmap-complete.sh`), but to edit the output images, use the separate post-processing run script (`run-postprocessing.sh`).*

## Copying Output Images to Local Machine
Obtain the container id of the latest entry with
```
docker ps -a
```
and copy the output folder to the current local directory with
```
docker cp [container id]:/home/eht/DIFMAP/difmap/difmap-pdfs .
```