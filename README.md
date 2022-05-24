# Reproducibility_EHT

Relevant links:
* [Link to original EHTC repository](https://github.com/eventhorizontelescope/2019-D01-02)
* [Link to our Docker containers](https://hub.docker.com/r/globalcomputinglab/reproducibility-eht/tags)

This contains
* Documentation for running the pipelines within their Docker containers
* Scripts for generating our images for the paper 
* Scripts for generating statistical output
* Auxiliary final outputs (images coming from the pipelines, statistical outputs) 

## Summary of Contents
  
* `/docs` -- relevant README materials for executing our code and Docker containers
  
* `/data-validation` -- reproduce our work on the validation of EHT's data
  * script to unpack the data
  * script to reproduce **Figure 2b** in our paper (**Figure 1** in EHT's Paper IV)
   
* `/eht-images` -- reproduce our work on producing our figure from the images we generated from the pipelines
  * image folder for each pipeline
  * Jupyter notebook, used to reproduce **Figure 6b** in our paper
  
* `/src` -- scripts we created to fill in gaps between running the imaging program and reproducing EHT's results, especially for quantitative study
  * `/difmap` 
    * post-processing script
    * script to generate "image summaries"
  * `/eht-imaging` 
    * post-processing script
    * (image summaries are a built-in feature of EHT-Imaging)
  * `/smili`  
    * post-processing script
    * script to generate "image summaries" (does not work within the container)
