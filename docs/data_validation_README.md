# Data Validation

## Data Integrity Validation Instructions

**_In order to fully validate that there has been no modifications of the [EHT Calibrated M87 Data](https://datacommons.cyverse.org/browse/iplant/home/shared/commons_repo/curated/EHTC_FirstM87Results_Apr2019), please follow the instructions in this section. Once completed, please move on to the "Docker Build Instructions" section below this section._**

1. Please download the tar file that contains the data from [here](https://datacommons.cyverse.org/browse/iplant/home/shared/commons_repo/curated/EHTC_FirstM87Results_Apr2019/EHTC_FirstM87Results_Apr2019_csv.tgz) to your local machine. The file is called `EHTC_FirstM87Results_Apr2019_csv.tgz`. 

2. Once downloaded, please check the `md5sum` of the data on your local machine by running the following command: 
   * For Linux users: `md5sum EHTC_FirstM87Results_Apr2019_csv.tgz`
   * For Mac users:  `md5 EHTC_FirstM87Results_Apr2019_csv.tgz`
   * For Windows users: `certutil -hashfile EHTC_FirstM87Results_Apr2019_csv.tgz MD5`

3. The `md5sum` of the data should be matching to this: `fe11e10a4f9562cb6a2846206d86860c`. 
   * If the checksums are matching, this means that the data in the repository has not been corrupted or modified. **_Everything should be ready to use!_**
   * If the checksums differ, you will end up using the data from the time this container was built, which is stored in the `EHTC_FirstM87Results_Apr2019_csv.tgz` tarball in the `data_validation` directory. You do not have to do anything with this tarball.

------------------------------------------------------------------

## Data-Validation Container Build Instructions

1. The Docker image is available on our DockerHub [here](https://hub.docker.com/r/globalcomputinglab/reproducibility-eht/tags). Pull the `data-validation` container using the command `docker pull globalcomputinglab/reproducibility-eht:data-validation`.

2. Once the image has finished building, run the following command: `docker run -it -p 9000:8888 data-validation`. This runs the container and forwards everything from `port 8888` in the container to the local machine's `port 9000` (or any other port number above), allowing you to interact with the container locally.

3. Voila! The Docker container should be ready to go! Please move on to the "Data Validation Jupyter Notebook Instructions" section below.

------------------------------------------------------------------

## Data Validation Jupyter Notebook Instructions
1. Once inside the container, please run `bash scripts/unpack_data.sh ` from the root directory (`/home/eht`) in the container. It will untar all of the data required for the script to run and create the necessary directories.

2. Run the command `cd scripts`. 

3. To easily view all files and run the notebook in the Jupyter Lab GUI, please run `jLab`. It is an alias for the command `jupyter lab --ip 0.0.0.0 --no-browser`. This will allow you to use a Jupyter Lab GUI to easily navigate around the repository.
   * If visualization capabilities are limited and you cannot view the Jupyter Lab GUI, please run the following command: `python ReproducePlots.py`. This will produce the same outputs as the Jupyter Notebook.

4. In your local machine’s browser, type `localhost:9000`. It should ask for a token. Please copy and paste the token given in the Jupyter log that you see in the Docker container's shell. Here is an example:
    * Copy and paste the string of numbers/letters (Ex. `e3ad1f3c9421a249e20f33d3100f6bc86cebb17dcd0b1c56`) into the token prompt.

```
...
[I 2022-02-07 11:45:14.924 ServerApp] Jupyter Server 1.4.1 is running at:
[I 2022-02-07 11:45:14.924 ServerApp] http://localhost:8888/lab?token=e3ad1f3c9421a249e20f33d3100f6bc86cebb17dcd0b1c56
[I 2022-02-07 11:45:14.924 ServerApp]  or http://127.0.0.1:8888/lab?token=e3ad1f3c9421a249e20f33d3100f6bc86cebb17dcd0b1c56
...

```


5. Please open the `ReproducePlots.ipynb` Jupyter Notebook in the Jupyter Lab GUI to run the data validation. 

6. Once opened, run all of the cells.
   - If certain plots are desired, there are instructions to indicate what sections correspond to those plots. 
   - They will create plots of the data at refined or coarse levels. Please see the "Options for Reproducing Different Plots" section below to view your options.


#### Options for Reproducing Different Plots:
1. High and Low Frequencies for Each Day _**(8 Plots Total)**_
2. Combined High and Low Frequencies for Each Day _**(4 Plots Total)**_
3. Replica of Paper IV's Figure 1 _**(3 Plots Total)**_
   - _**Recommend running this section because this validates what is in the original paper!**_


#### Notes:
* In order to view the images produced, which are formatted as `.eps`, you will need to download the images to your local machine in order to view them. Just right click on the files in the left navigation bar and click on "Download".

------------------------------------------------------------------

## Expected Outputs

Here is what the outputs of the notebook (or `ReproducePlots.py` script):

![All telescope baselines for all days](https://github.com/TauferLab/Src_EHT/blob/main/data_validation/expected_outputs/All_Frequencies.jpg)

![Short telescope baselines](https://github.com/TauferLab/Src_EHT/blob/main/data_validation/expected_outputs/Close_Up_Frequencies.jpg)

![Telescope baselines for all days - Both high and low](https://github.com/TauferLab/Src_EHT/blob/main/data_validation/expected_outputs/Reproduced_All_Days.jpg)

