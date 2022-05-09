# Reproducibility_EHT

This contains
* Dcoumentation for running the pipelines
* Link to Docker containers 
* Scripts for generating our images for the paper 
* Scripts for generating statistical output
* Auxiliary final outputs (images coming from the pipelines, statistical outputs) 

  
/docs << HOW TO USE THE MATERIALS IN THIS REPO AND RUN THE CONTAINERS THAT WE LINK
 <relevant readme materials>
  
/data-validation << REPRODUCE OUR WORK ON THE VALIDATION OF THE EHT DATA
 unpack
 reproduce-figX-inourpaper
   
/eht-images << REPRODUCE OUR WORK ON THE EHT IMAGES, AND OPTIONALLY REPRODUCE A NEW FIGURE FROM ANOTHER PIPELINE EXECUTION
 /images
  reproduce-figY-inourpaper
  
/src << SCRIPTS THAT WE CREATED TO MAKE THINGS WORK OR FILL IN GAPS, ESPECIALLY FOR QUANTITATIVE STUDY
 /difmap
   post-processing
 /eht-imaging
 /smili
   post-processing
  
Please ensure
* Documentation for containers matches behaviour
* This README contains all the instructions to use the repository, license, references the paper, links original repos 
