import matplotlib
matplotlib.use('Agg')
import os
import argparse
import ehtim as eh
import numpy as np

#-------------------------------------------------------------------------------
# Load command-line arguments
#-------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Script to convert EHT fits files to pdf images")
parser.add_argument('-i', '--infile' , default=""   , help="input FITS file")
parser.add_argument('-o', '--obsfile', default=""   , help="input UVFITS file")
parser.add_argument('-r', '--regrid' , default=False, help="regrid image object"              , action='store_true')
parser.add_argument('-c', '--center' , default=False, help="center image object"              , action='store_true')
parser.add_argument('-s', '--scale'  , default=False, help="display scale in output"          , action='store_true')
parser.add_argument('-b', '--beam'   , default=False, help="display beam size in output"      , action='store_true')
parser.add_argument('-a', '--all'    , default=False, help="perform all post-processing steps", action='store_true')
parser.add_argument('-n', '--notitle', default=False, help="remove title and colorbar"        , action='store_true') 
args = parser.parse_args()

if(args.scale or args.all): scale = 'scale'
else: scale = 'none'

# Load fits file into image object
im_obj = eh.image.load_fits(args.infile)
if(args.center or args.all): im_obj = im_obj.shift([8, 0]) # Not an exact value, but a close estimate
if(args.regrid or args.all): im_obj = im_obj.regrid_image(128*eh.RADPERUAS, 192) #im_obj.regrid_image(160*eh.RADPERUAS, 1920) # 128->192, 64->128->192
params = [9.696e-11, 9.696e-11, 0] # This is for DIFMAP (20 uas) -- do NOT blur, as it is already applied. This is used only for display()’s beamparams

# Create color map of afmhot_10us, vals copied from ehtplot/color/ctabs/afmhot_10us.ctab file
colors = np.loadtxt("afmhot_10us.cmap", delimiter=" ", unpack=False)
newcmp = matplotlib.colors.ListedColormap(colors)

#-------------------------------------------------------------------------------
# Fiducial imaging parameters obtained from the eht-imaging parameter survey
#-------------------------------------------------------------------------------
zbl        = 0.60               # Total compact flux density (Jy)
sys_noise  = 0.02               # fractional systematic noise
                                # added to complex visibilities

# initial data weights - these are updated throughout the imaging pipeline
data_term = {'amp'    : 0.2,    # visibility amplitudes
             'cphase' : 1.0,    # closure phases
             'logcamp': 1.0}    # log closure amplitudes

#-------------------------------------------------------------------------------
# Fixed imaging parameters
#-------------------------------------------------------------------------------
obsfile   = args.obsfile        # Pre-processed observation file
imfile    = args.infile         # Image file as .fits
ttype     = 'nfft'              # Type of Fourier transform ('direct', 'nfft', or 'fast')
                                # for unaccounted sensitivity loss
                                # than for unaccounted sensitivity improvement
uv_zblcut = 0.1e9               # uv-distance that separates the inter-site "zero"-baselines
                                # from intra-site baselines

#-------------------------------------------------------------------------------
# Load the obs data file and the image file
#-------------------------------------------------------------------------------

# --------------- This block is done in EHT-Imaging ----------------------------
# load the uvfits file
obs = eh.obsdata.load_uvfits(obsfile)

# scan-average the data
# identify the scans (times of continous observation) in the data
obs.add_scans()

#  coherently average the scans, which can be averaged due to ad-hoc phasing
obs = obs.avg_coherent(0.,scan_avg=True)

# Estimate the total flux density from the ALMA(AA) -- APEX(AP) zero baseline
zbl_tot = np.median(obs.unpack_bl('AA','AP','amp')['amp'])
if zbl > zbl_tot:
        print('Warning: Specified total compact flux density ' +
                          'exceeds total flux density measured on AA-AP!')

# Flag out sites in the obs.tarr table with no measurements
allsites = set(obs.unpack(['t1'])['t1'])|set(obs.unpack(['t2'])['t2'])
obs.tarr = obs.tarr[[o in allsites for o in obs.tarr['site']]]
obs = eh.obsdata.Obsdata(obs.ra, obs.dec, obs.rf, obs.bw, obs.data, obs.tarr,
                         source=obs.source, mjd=obs.mjd,
                         ampcal=obs.ampcal, phasecal=obs.phasecal)

# This ends where any modifications are made to the obs object for im summary 
# ------------------------------------------------------------------------------

# Add a large gaussian component to account for the missing flux
# so the final image can be compared with the original data

#im_obj = eh.image.load_fits(args.infile)

im_obj = im_obj.add_zblterm(obs, uv_zblcut, debias=True)
obs_sc_addcmp = eh.selfcal(obs, im_obj, method='both', ttype=ttype)

# Save an image summary sheet
matplotlib.pyplot.close('all')
outimgsum = 'difmap-imgsums/'+args.infile[:-4]+'pdf'
print("\nSaving image summary to", outimgsum)
print()
eh.imgsum(im_obj, obs_sc_addcmp, obs, outimgsum, cp_uv_min=uv_zblcut)
print("\n====================\n")

