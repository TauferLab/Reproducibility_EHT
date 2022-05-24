#!/usr/bin/env bash
cp difmap-output/*.fits .

for f in *.fits; do 
  python difmap-postprocessing.py -i $f --all
done

for d in 095 096 100 101; do
	python difmap-imgsum.py \
		-i SR1_M87_2017_${d}_lo_hops_netcal_StokesI.CircMask_r30_x-0.002_y0.022.RT-10.CF0.5.ALMA0.1.UVW2_-1.noresiduals.fits \
		-o ../data/uvfits/SR1_M87_2017_${d}_lo_hops_netcal_StokesI.uvfits
done

rm *.fits
