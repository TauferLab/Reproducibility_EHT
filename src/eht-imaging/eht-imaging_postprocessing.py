#!/usr/bin/python

# This file implements a variety of EHT Image postprocessing steps which
# are given as command line argumets. The output filename should also be
# passed as a command line argument.
#
# See the EHT-Imaging/scripts/run-postprocessing.sh file for examples
# of running this script.
#
import matplotlib
matplotlib.use('Agg')
import os
import argparse
import ehtim as eh
import ehtplot.color

# Load and parse command-line arguments
parser = argparse.ArgumentParser(description="Script to convert EHT_Difmap fits files to pdf images")
parser.add_argument('-i', '--infile'    , default=""   , help="input FITS file")
parser.add_argument('-o', '--outfile'   , default=""   , help="output PDF file")
parser.add_argument('-s', '--scale'     , default=False, help="display scale in output"          , action='store_true')
parser.add_argument('-b', '--beam'      , default=False, help="display beam size in output"      , action='store_true')
parser.add_argument('-l', '--blur'      , default=False, help="apply Gaussian blur to image"     , action='store_true')
parser.add_argument('-u', '--afmhot10us', default=False, help="use the afmhot_10us colormap"     , action='store_true')
parser.add_argument('-t', '--notitle'   , default=False, help="display with no title or padding" , action='store_true')
parser.add_argument('-a', '--all'       , default=False, help="perform all post-processing steps", action='store_true')
args = parser.parse_args()

# Check for input file
if(args.infile == ""):
    print("An input file is required to be given using '--infile <filename>'")
    quit()

# Set name of output file to [input]_processded.pdf if no outfile name specified
if(args.outfile == ""):
    args.outfile = args.infile[:-5]+'_processed.pdf'

print("Exporting PDF to: ", args.outfile)

# Set params for display based on user args
scale = 'scale' if (args.scale or args.all) else 'none'
cmap = 'afmhot_10us' if (args.afmhot10us or args.all) else 'afmhot'
title = False if (args.notitle or args.all) else True

# Load fits file into image object and set params for beam
im_obj = eh.image.load_fits(args.infile)
params = [8.29e-11, 8.29e-11, 0] # This is for EHT-Imaging (17.1 uas) in Paper IV

# Blur the image object using Gaussian blur if specified
if(args.blur or args.all): im_obj.blur_gauss(params)

# Display image object
if(args.beam or args.all):
    im_obj.display(cbar_unit=['Tb'], has_title=title, cfun=cmap, cbar_orientation='horizontal', label_type=scale, beamparams=params, export_pdf=args.outfile)
else:
    im_obj.display(cbar_unit=['Tb'], has_title=title, cfun=cmap, cbar_orientation='horizontal', label_type=scale, export_pdf=args.outfile)
