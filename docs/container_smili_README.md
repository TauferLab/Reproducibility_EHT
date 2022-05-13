# SMILI Container

The SMILI pipeline is one of three pipelines (along with DIFMAP & EHT-Imaging) used to produce the first image of a black hole in M87. This project aims to provide findings about the reproducibility process of reconstructing an image of a black hole using SMILI's software.

NOTE: SMILI uses an older version of astropy, but the newest version of astropy is needed for some post-processing steps. Consider looking into this if running into errors in these parts.

## Executing the Pipeline
From `~/Src_EHT/smili`, you can execute the pipeline with the following command

```
./run.sh
```

## Post-Processing
The black hole images shown in Paper IV uses the afmhot_10us colormap as well as a restoring beam for blurring. ```run_postprocessing.sh``` should run ```smili_postprocessing.py``` for the four days of observation and output a pdf of the image. There are some notable commands and edits you can make to the code depending on each output.

### Applying afmhot_10us
```
colors = np.loadtxt("afmhot_10us.cmap", delimiter=" ", unpack=False)
newcmp = matplotlib.colors.ListedColormap(colors)
```

### Restoring Beam (blur)
```
if(args.blur or args.all): im_obj = im_obj.blur_gauss(params)
```

### Extra Notes
* Remove ```cbar_orientation='horizontal'``` for units
* Remove ```beamparams=params``` to remove circle

## Copying Output Images to Local Machine
Obtain the container id with
```
docker ps -a
```
and copy the output folder to the current local directory with
```
docker cp [container id]:/root/Src_EHT/smili/post .
```