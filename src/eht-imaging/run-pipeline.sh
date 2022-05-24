#!/usr/bin/env bash
#
# Copyright (C) 2019 The Event Horizon Telescope Collaboration
#
# Traverse the data directory and run eht-imaging_pipeline on each day's
# lo and hi band .uvfits files.
#
# To save .pdf of final image, uncomment --savepdf arg.
# To save .pdf of image summary statistics, uncomment --imsum (This doesn't work currently)
#

echo "=============== Beginning EHT-Imaging Pipeline Execution ========================="
cd scripts
for d in 095 096 100 101; do
    python eht-imaging_pipeline.py \
        -i  ../data/uvfits/SR1_M87_2017_${d}_lo_hops_netcal_StokesI.uvfits \
        -i2 ../data/uvfits/SR1_M87_2017_${d}_hi_hops_netcal_StokesI.uvfits \
        -o  ../output/SR1_M87_2017_${d}.fits \
       --savepdf \
       --imgsum
done
echo "=============== Completed EHT-Imaging Pipeline Execution ========================="
echo "                                                                                  "
echo "================ Beginning EHT-Imaging Post-processing ==========================="
bash run-postprocessing.sh
echo "================ Completed EHT-Imaging Post-processing ==========================="
cd ~