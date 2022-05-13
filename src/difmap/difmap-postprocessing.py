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
parser.add_argument('-o', '--outfile', default=""   , help="output PDF file")
parser.add_argument('-r', '--regrid' , default=False, help="regrid image object"              , action='store_true')
parser.add_argument('-c', '--center' , default=False, help="center image object"              , action='store_true')
parser.add_argument('-s', '--scale'  , default=False, help="display scale in output"          , action='store_true')
parser.add_argument('-b', '--beam'   , default=False, help="display beam size in output"      , action='store_true')
parser.add_argument('-a', '--all'    , default=False, help="perform all post-processing steps", action='store_true')
parser.add_argument('-n', '--notitle', default=False, help="remove title and colorbar"        , action='store_true') 
args = parser.parse_args()

if(args.outfile == ""):
    args.outfile = 'difmap-pdfs/'+args.infile[:-4]+'pdf'

print("Exporting PDF image to", args.outfile)

if(args.scale or args.all): scale = 'scale'
else: scale = 'none'

# Load fits file into image object
im_obj = eh.image.load_fits(args.infile)
if(args.center or args.all): im_obj = im_obj.shift([8, 0]) # Not an exact value, but a close estimate
if(args.regrid or args.all): im_obj = im_obj.regrid_image(128*eh.RADPERUAS, 192) # The parameters here seem to change the resolution. The second was originally 64, and I somewhat arbitrarily increased it to 192 in testing.
params = [9.696e-11, 9.696e-11, 0] # This is for DIFMAP (20 uas) -- do NOT blur, as it is already applied. This is used only for display()’s beamparams

# Create color map of afmhot_10us, vals copied from ehtplot/color/ctabs/afmhot_10us.ctab file
colors = np.loadtxt("afmhot_10us.cmap", delimiter=" ", unpack=False)
newcmp = matplotlib.colors.ListedColormap(colors)

if(args.notitle):
    if(args.beam or args.all): im_obj.display(has_title=False, has_cbar=False, cfun=newcmp, label_type=scale, beamparams=params, export_pdf=args.outfile)
    else: im_obj.display(has_title=False, has_cbar=False, cfun=newcmp, label_type=scale, export_pdf=args.outfile)  
elif(args.beam or args.all): im_obj.display(has_title=False, cbar_unit=['Tb'], cfun=newcmp, cbar_orientation='horizontal', label_type=scale, beamparams=params, export_pdf=args.outfile)
else: im_obj.display(cbar_unit=['Tb'], cfun=newcmp, label_type=scale, export_pdf=args.outfile)
print("\n====================\n")

