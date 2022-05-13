# DIFMAP Container

The `reproducibility-eht:difmap` Docker container image contains everything needed to generate the images and data summaries of M87's black hole using the DIFMAP pipeline to generate the .fits files.  
This includes:
  * raw data provided by The Event Horizon Telescope Collaboration (EHT) in the form of .uvfits files
  * an installation of DIFMAP, the imaging algorithm used in this pipeline
  * files from EHT's repository necessary to run DIFMAP (slightly modified `EHT_Difmap` script, mask file, and shell scripts to automate the process)
  * Python scripts written by me that use EHT's ehtim module to perform the post-processing steps on the .fits files output by EHT\_Difmap
	 and generate final images and image summary PDFs

## Summary of Contents

`~/uvf_difmap_2.5k` -- this is the entire DIFMAP installation  
`~/DIFMAP/data/uvfits` -- contains the .uvfits files provided by EHT, and since their results only use the lo-band data, I have separated out the unused files into `uvfits_hi`  
`~/DIFMAP/difmap` -- contains all of the files and scripts used to run the pipeline, detailed below:
  * `EHT_Difmap` -- DIFMAP script written by EHT to process the .uvfits files for this project, modified to place the files into `/difmap-output`
  * `difmap.sh and run.sh` -- shell scripts provided by EHT to run the `EHT_Difmap` DIFMAP script on each .uvfits file in `/data/uvfits` and outputs .fits files to `/difmap-output`
  * `difmap-postprocessing.py` -- Python script that creates a PDF image from a .fits file and puts it in `/difmap-pdfs`
  * `difmap-imgsum.py` -- Python script that generates a PDF summary of the data from a .fits file and puts it in `/difmap-imgsums`
  * `d-pp.sh` -- shell script that runs `difmap-postprocessing.py` and `difmap-imgsum.py` on all the .fits files in `/difmap-output`
  * `difmap-complete.sh` -- shell script that runs the entire DIFMAP pipeline

## Executing the Pipeline
From `~/DIFMAP/difmap`, you can execute the pipeline with the following command
```
./difmap-complete.sh
```

## Copying Output Images to Local Machine
Obtain the container id with
```
docker ps -a
```
and copy the output folder to the current local directory with
```
docker cp [container id]:/home/eht/DIFMAP/difmap/difmap-output .
```