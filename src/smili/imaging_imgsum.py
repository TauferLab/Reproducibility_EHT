#-------------------------------------------------------------------------------
# Modules
#-------------------------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')

import os
import argparse
import ehtim as eh
import numpy as np

#-------------------------------------------------------------------------------
# Load command-line arguments
#-------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Fiducial eht-imaging script for M87")
parser.add_argument('-i', '--in_fits',    default="obs.uvfits",help="input UVFITS file")
parser.add_argument('-i2', '--in_uvfits',  default="",          help="optional 2nd input file (different band) for imaging")
parser.add_argument('-o', '--outfile',   default='out.fits',  help='output FITS image')
parser.add_argument('--imgsum',          default=False,       help='generate image summary pdf',action='store_true')
args = parser.parse_args()

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
obsfile   = args.in_uvfits       # Pre-processed observation file
imfile    = args.in_fits        # Image file as .fits
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

# coherently average the scans, which can be averaged due to ad-hoc phasing
obs = obs.avg_coherent(0.,scan_avg=True)

# Estimate the total flux density from the ALMA(AA) -- APEX(AP) zero baseline
zbl_tot   = np.median(obs.unpack_bl('AA','AP','amp')['amp'])
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

# load in the image object from in_fits infile here
im_obj = eh.image.load_fits(imfile)


# Add a large gaussian component to account for the missing flux
# so the final image can be compared with the original data
im_addcmp = im_obj.add_zblterm(obs, uv_zblcut, debias=True)
obs_sc_addcmp = eh.selfcal(obs, im_addcmp, method='both', ttype=ttype)

# Save an image summary sheet
matplotlib.pyplot.close('all')
outimgsum = os.path.splitext(args.outfile)[0] + '_imgsum.pdf'
eh.imgsum(im_addcmp, obs_sc_addcmp, obs, outimgsum ,cp_uv_min=uv_zblcut)
