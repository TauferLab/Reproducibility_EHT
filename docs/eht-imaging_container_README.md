# EHT-Imaging Container

The EHT-Imaging pipeline is one of three pipelines (along with SMILI and DIFMAP) used to produce the M87* Black Hole images released by the Event Horizon Telescope Collaboration (EHTC). This project aims to provide findings about the reproducibility process of reconstructing an image of a black hole using the EHT-Imaging workflow.

This [`EHT-Imaging`](https://github.com/achael/eht-imaging) repository contains the original pipline script developed by the EHTC as well as scripts that we have developed in our efforts to fully reproduce the EHTC released black hole images. We also provide detailed instructions for installing all necessary dependencies and for running the pipeline on your local machine, as well as a Jupyter Notebook detailing the pipeline's execution and image creation process.

## Summary of Contents
* Jupyter Notebook showing detailed pipeline execution and post-processing steps that we have taken
* Python scripts of original pipeline and our image post-processing

## Executing the Pipeline

There is no need to worry about unpacking the data or where it is located before executing the pipeline because the `run-pipeline.sh` script will automatically ensure it is in the correct location.

Before running the pipeline, you can edit the `run-pipeline.sh` script to specify if you want the pipeline to save the images as `.pdf` files. Instructions are in the comments of the file on how to do this. By default, all outputs (`.fits` image, `.pdf` image, `.pdf` of image summary statistics) from the pipeline are saved. The output files will be saved in a new directory `EHT/EHT-Imaging/output`. This directory will be created automatically by the `run-pipeline.sh` script.

You can run the pipeline with the following command: (This assumes that you are currently in the `EHT/EHT-Imaging` directory, the `run-pipeline.sh` script must be executed from this directory in order to find the data properly)
```
bash scripts/run-pipeline.sh
```

## Copying Output Images to Local Machine
Obtain the container id with
```
docker ps -a
```
and copy the output folder to the current local directory with
```
docker cp [container id]:/home/eht/output .
```