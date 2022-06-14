# EHT-Imaging Container

The EHT-Imaging pipeline is one of three pipelines (along with SMILI and DIFMAP) used to produce the M87* Black Hole images released by the Event Horizon Telescope Collaboration (EHTC). The container aims to provide findings about the reproducibility process of reconstructing an image of a black hole using the EHT-Imaging Python modules.

The [`eht-imaging`](https://github.com/achael/eht-imaging) repository contains the original pipline script developed by the EHTC.

## Summary of Contents
* `~/notebook` -- Jupyter Notebook showing detailed pipeline execution and post-processing steps that we have taken
* `~/data/uvfits` -- contains the .uvfits files, which are passed as input into the pipeline
* `~/scripts` -- Python scripts of original pipeline and our image post-processing
  * `eht-imaging_pipeline.py` -- Python script that creates .fits files, generates a default `ehtim` image PDF, and generates an image summary PDF (suffixed with "_imgsum")
  * `eht-imaging_postprocessing.py` -- Python script that creates a PDF image from a .fits file and puts it in `~/output` (suffixed with "_processed")
  * `run-pipeline.sh` -- runs `eht-imaging_pipeline.py` to generate .fits files and runs the post-processing script with default settings
  * `run-postprocessing.sh` -- runs the post-processing script on all observation days

## Pulling and Running the Container
The Docker image is available on our DockerHub [here](https://hub.docker.com/r/globalcomputinglab/reproducibility-eht/tags). Pull the `eht-imaging` container using the command

```
docker pull globalcomputinglab/reproducibility-eht:eht-imaging
```
When the image is done building, run 
```
docker run -it -p 9000:8888 globalcomputinglab/reproducibility-eht:eht-imaging
```
This runs the container and forwards everything from port 8888 in the container to the local machine's port 9000 (or any other port number above), allowing you to interact with the container locally.

## Executing the Pipeline

There is no need to worry about unpacking the data or where it is located before executing the pipeline because the `run-pipeline.sh` script will automatically ensure it is in the correct location.

Before running the pipeline, you can edit the `run-pipeline.sh` script to specify if you want the pipeline to save the images as `.pdf` files. Instructions are in the comments of the file on how to do this. By default, all outputs (`.fits` image, `.pdf` image, `.pdf` of image summary statistics) from the pipeline are saved. The output files will be saved in a new directory `/eht/output`. This directory will be created automatically by the `run-pipeline.sh` script.

You can run the pipeline with the following command: (This assumes that you are currently in the `eht` directory, the `run-pipeline.sh` script must be executed from this directory in order to find the data properly)
```
bash scripts/run-pipeline.sh
```

## Post-Processing
The black hole images shown in Paper IV uses the afmhot_10us colormap as well as a restoring beam for blurring. ```run-postprocessing.sh``` should run ```eht-imaging_postprocessing.py``` for the four days of observation and output a PDF of the image. There are some flags and edits you can make to the code to change the output.

Additionally, you can uncomment the "timeline" code in `run-postprocessing.sh` to view the different stages of applied changes (original output from the pipeline -> correct colormap -> apply beam blur)

*The post-processing is built into the main run script (`run-pipeline.sh`), but to edit the output images, use the separate post-processing run script (`run-postprocessing.sh`).*

---

#### Optional: Run the Jupyter Notebook
You can run the Jupyter notebook version of the post-processing script if you want to view the images as they are generated. To start the Jupyter Lab IDE, run the following commands:
```
cd ~/notebook
jupyter-lab --ip 0.0.0.0 --no-browser
```

In your local browser, go to `localhost:<port_number>`, port_number being the port you are forwarding to (such as `localhost:9000`). You will have to copy and paste the token that is generated in the URL (`token=...`). For example,

```
[C 2022-06-14 02:52:02.620 ServerApp]

    To access the server, open this file in a browser:
        file:///home/eht/.local/share/jupyter/runtime/jpserver-170-open.html
    Or copy and paste one of these URLs:
        http://0b710d47db10:8888/lab?token=81c1f1c36e1194315e1f2c96ec34282f8562b622c664eb85
     or http://127.0.0.1:8888/lab?token=81c1f1c36e1194315e1f2c96ec34282f8562b622c664eb85

```

All notebook generated files are stored in the the ~/notebook dir. This is done to ease viewing and accessing images/files within the Jupyter session.


## Copying Output Images to Local Machine
Obtain the container id of the latest entry with
```
docker ps -a
```
and copy the output folder to the current local directory with
```
docker cp [container id]:/home/eht/output .
```
