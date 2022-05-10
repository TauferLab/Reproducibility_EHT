#!/usr/bin/python

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, MaxNLocator)

# Stores paths to repository root, data, and generated plots
PATH = os.getcwd() 
ROOT = PATH[0:-8]
DATA = f'{ROOT}/data/csv'
CONVERTED=f'{DATA}/converted'
PLOTS = f'{ROOT}/images'
ORIGINAL = f'{PLOTS}/Original_Days'
REPRODUCED = f'{PLOTS}/Reproduced_Days'

# Days that data was reported in April 2017
days = ['095', '096', '100', '101']

# Each telescope from the data 
telescopes = ['AA', 'LM', 'AP', 'AZ', 'SM', 'JC', 'PV']

# Stores Telescope Baselines in a dictionary to keep track of colors associated with each pair
telescopesColorsDict = {'AA_LM': '#0A5286', 
                        'AA_AP': '#000000', 
                        'AA_AZ': '#2FC527', 
                        'AA_SM': '#BE7FFF', 
                        'AA_JC': '#BE7FFF', 
                        'AA_PV': '#2A82FF', 
                        'LM_SM': '#BD00BF', 
                        'LM_PV': '#855327', 
                        'AP_LM': '#0A5286', 
                        'AP_AZ': '#2FC527', 
                        'AP_SM': '#BE7FFF', 
                        'AP_JC': '#BE7FFF', 
                        'AP_PV': '#2A82FF', 
                        'AZ_LM': '#2500FF', 
                        'AZ_SM': '#BE8706', 
                        'AZ_JC': '#BE8706', 
                        'AZ_PV': '#A3A606', 
                        'JC_LM': '#BD00BF',
                        'JC_SM': '#656565', 
                        'JC_PV': '#C6A478', 
                        'PV_SM': '#C6A478'
                       }

'''
--------------------------------------------------
Functions to Convert Original, Processed EHT Data
--------------------------------------------------
'''

def convertData(oldFile, day, base, prefix):
    
    # Save high and low images to these files
    if base == 'High':
        if prefix == 'G':
            converted = f'{CONVERTED}/Day_{day}_2017_HIGH_Giga.csv'
        if prefix == 'M':
            converted = f'{CONVERTED}/Day_{day}_2017_HIGH_Mega.csv'
    else: 
        if prefix == 'G':
            converted = f'{CONVERTED}/Day_{day}_2017_LOW_Giga.csv'
        if prefix == 'M':
            converted = f'{CONVERTED}/Day_{day}_2017_LOW_Mega.csv'
        
    
    # Reads these 4 columns from the csv files & stores into DataFrames
    oldData = pd.read_csv(oldFile, skiprows=[0], usecols=['T1', 'T2', 'U(lambda)', 'V(lambda)'])

    # Stores size of columns
    U_size = oldData[oldData.columns[0]].count()

    # Updates each value in the U and V columns to converted number (indicated by prefix)
    for i in range(U_size) : 
        oldVal = oldData.iloc[[i],[2, 3]]
        if (prefix == 'G'):
            newVal = oldVal / 1000000000
        if (prefix == 'M'):
            newVal = oldVal / 1000000
        oldData.iloc[[i],[2, 3]] = newVal
    
    # \u03BB - lambda in unicode
    # New column names 
    newCols=['T1', 'T2', 'U (G\u03BB)', 'V (G\u03BB)']

    # Export updated data to a new csv file
    oldData.to_csv(converted, index=False, header=newCols)
    
    return converted

def conversionProcess(day, base, prefix):
    
    # Path to original project data for high and low frequencies for each day
    if base=="High":
        BASE = f'{DATA}/SR1_M87_2017_{day}_hi_hops_netcal_StokesI.csv'
    else:
        BASE = f'{DATA}/SR1_M87_2017_{day}_lo_hops_netcal_StokesI.csv'
    
    # Converts data & saves to new csv files
    print("Converting Day {} - {}...".format(day, base))
    new = convertData(BASE, day, base, prefix)
    
    return pd.read_csv(new)

'''
--------------------------------------------------
Functions to plot original or converted data into...
1. High and Low frequencies for each day (8 plots total)
2. Combined high and low frequencies for each day (4 plots total)
3. Replica of Paper IV's Figure 1 (3 plots total)

These options are here for anyone who wants to view the data on plots at refined or coarse levels.
--------------------------------------------------
'''

'''
--------------------------------------------------
1. High and Low Frequencies for each day (8 plots total)**

To view all 8 plots, please run the following in a new cell:

for i in days:
    freq(i, "High")
    freq(i, "Low")

--------------------------------------------------
'''

def plot_settings(ax, fig, date, base): 
    
    # This is for creating figure titles
    if (base == "None"): 
        ax.set_title(f"{date} Frequencies of Different Baselines")
    else:
        ax.set_title(f"{date} {base} Frequencies of Different Baselines")
    ax.set_xlabel("u (G\u03BB)")
    ax.set_ylabel("v (G\u03BB)")
    
    # Set figure size
    fig.set_figheight(7)
    fig.set_figwidth(7)
    
    # Plots the baseline lengths corresponding to fringe spacings
    circle1 = plt.Circle((0, 0), radius=8.1, color="grey", fill=False, linestyle='--', linewidth='3.0', label='25 \u03BCas')
    circle2 = plt.Circle((0, 0), radius=4, color="grey", fill=False, linestyle='--', linewidth='3.0', label='50 \u03BCas')
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='grey')

    # Adds axes (inverses the x axis)
    ax.set_xlim([10, -10])
    ax.set_ylim([-10, 10])

    # Adds ticks and grid lines
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # Adds and labels baseline lengths in the plot
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.text(4.8, 7,'25 \u03BCas', rotation=30)
    ax.text(3.5, 3, '50 \u03BCas', rotation=30)

    return

def plot(df, fig, ax):
    
    index = 0

    # Iterates through each Telescope-Telescope (Baseline) pair
    for i in telescopes: 
        for j in telescopes: 
            if (i != j): 
                
                # Finds the baseline pair and stores it into new DataFrame
                baseline = df[df['T1'].str.contains(i) & df['T2'].str.contains(j)]
                  
                # Plots the baseline pair if it exists
                if baseline.shape[0] != 0:
                    base = f"{i}_{j}"
                    uh = baseline["U (G\u03BB)"]
                    vh = baseline["V (G\u03BB)"]
                    inverse_uh = -1 * baseline["U (G\u03BB)"]
                    inverse_vh = -1 * baseline["V (G\u03BB)"]
                    
                    ax.scatter(uh, vh, s=30, label=base, marker='o', c=telescopesColorsDict[base])
                    ax.scatter(inverse_uh, inverse_vh, s=30, label=base, marker='o', c=telescopesColorsDict[base])
                    
                index = index + 1
    return 

def freq(day, base, showPlot=False):
    
    if not (os.path.isdir(ORIGINAL)):
        os.mkdir(ORIGINAL)
    
    # Path to original project data for high and low frequencies for each day
    if base=="High":
        BASE = f'{DATA}/SR1_M87_2017_{day}_hi_hops_netcal_StokesI.csv'
        SAVE = f'{ORIGINAL}/Original_Day_{day}_2017_HIGH.eps'
    else:
        BASE = f'{DATA}/SR1_M87_2017_{day}_lo_hops_netcal_StokesI.csv'
        SAVE = f'{ORIGINAL}/Original_Day_{day}_2017_LOW.eps'
    
    # Converts data & saves to new csv files
    print("Converting Day {} - {}...".format(day, base))
    new = convertData(BASE, day, base)

    # Read the converted data from new csv file
    df = pd.read_csv(new)

    print(f'Plotting...')
    
    # Plot the data
    fig, ax = plt.subplots()
    plot(df, fig, ax)

    # Decides proper plot settings for each day and frequency
    if i=='095':
        plot_settings(ax, fig, "April 5th, 2017", base)
    elif i=='096':
        plot_settings(ax, fig, "April 6th, 2017", base)
    elif i=='100':
        plot_settings(ax, fig, "April 10th, 2017", base)
    else: 
        plot_settings(ax, fig, "April 11th, 2017", base)
        
    # Saves plot as .jpg in images/ directory
    print("Saving figure...")
    plt.savefig(SAVE, bbox_inches='tight')
    
    # Toggle for showing plot in Notebook
    if (showPlot == False):
        plt.close()

    print(f'Complete! Generated image available at {SAVE}')
    return fig

'''
--------------------------------------------------
2. Combined high and low frequencies for each day (4 plots total)

To view all 4 plots, please run the following code in a new cell:

for i in days:
    highFreq = f'{DATA}/Converted/Day_{i}_2017_HIGH.csv'
    lowFreq = f'{DATA}/Converted/Day_{i}_2017_LOW.csv'
    
    reproducePlotForDay(i, highFreq, lowFreq)

 
NOTE: Please make sure data has been converted before running code!
--------------------------------------------------
'''

def reproducePlotForDay(day, highFreq, lowFreq, showPlot=False):
      
    # Reads the high and low frequency csv files for the day & stores them into DataFrames
    high = pd.read_csv(highFreq)
    low = pd.read_csv(lowFreq)
    
    # Plots the data
    fig2, ax2 = plt.subplots()
    plot(high, fig2, ax2)
    plot(low, fig2, ax2)
    
    if day=='095':
        plot_settings(ax2, fig2, "April 5th, 2017", base="None")
    elif day=='096':
        plot_settings(ax2, fig2, "April 6th, 2017", base="None")
    elif day=='100':
        plot_settings(ax2, fig2, "April 10th, 2017", base="None")
    else: 
        plot_settings(ax2, fig2, "April 11th, 2017", base="None")
        
    # Saves the reproduced plots as .jpgs in images/ directory (.png or .eps instead of .jpg)
    if not(os.path.isdir(REPRODUCED)):
        os.mkdir(REPRODUCED)
    SAVE = f'{REPRODUCED}/Reproduced_Day_{day}_Frequencies.eps'
    print("Saving figure...")
    plt.savefig(SAVE, bbox_inches='tight')
    
    # Toggle for showing plot in Notebook
    if (showPlot == False):
        plt.close()

    print(f'Complete! Generated image available at {SAVE}')
    return fig2

'''
--------------------------------------------------
3. Replica of Paper IV's Figure 1 (3 plots total)
--------------------------------------------------
'''
def reproducedAllDaysSettings(ax2, fig2):

    # Set figure size
    fig2.set_figheight(10)
    fig2.set_figwidth(20)

    # Sets up axes, tick marks, lines, and alignemnts for each plot
    for a in ax2:
        a.set_xlim(xmin=10, xmax=-10)
        a.set_ylim(ymin=-10, ymax=10)

        a.tick_params(top=True, right=True, bottom=True, left=True, width=1.5, direction='in', which='both', labelsize='16')

        a.xaxis.set_minor_locator(MultipleLocator(1))
        a.xaxis.set_major_locator(MaxNLocator(nbins=4, prune='lower'))

        a.yaxis.set_minor_locator(MultipleLocator(1))
        a.yaxis.set_major_locator(MaxNLocator(nbins=4, prune='lower'))
        a.set_aspect('equal')

        # Plots the baseline lengths corresponding to fringe spacings
        circle1 = plt.Circle((0, 0), radius=8.1, color="grey", fill=False, linestyle='--', linewidth='2.5', label='25 \u03BCas')
        circle2 = plt.Circle((0, 0), radius=4, color="grey", fill=False, linestyle='--', linewidth='2.5', label='50 \u03BCas')
        a.axhline(0, linestyle='-', linewidth='1.5', color='grey')
        a.axvline(0, linestyle='-', linewidth='1.5', color='grey')

        # Adds and labels baseline lengths in the plot
        a.add_patch(circle1)
        a.add_patch(circle2)

    plt.subplots_adjust(wspace=0)

    return

def subplot(df, ax):
    
    index = 0

    # Iterates through each Telescope-Telescope (Baseline) pair
    for i in telescopes: 
        for j in telescopes: 
            if (i != j): 

                # Finds the baseline pair and stores it into new DataFrame
                baseline = df[df['T1'].str.contains(i) & df['T2'].str.contains(j)]

                # Plots the baseline pair if it exists
                if baseline.shape[0] != 0:
                    base = f"{i}_{j}"
                    uh = baseline["U (G\u03BB)"]
                    vh = baseline["V (G\u03BB)"]
                    inverse_uh = -1 * baseline["U (G\u03BB)"]
                    inverse_vh = -1 * baseline["V (G\u03BB)"]

                    ax.scatter(uh, vh, s=30, label=base, marker='o', c=telescopesColorsDict[base], zorder=4)
                    ax.scatter(inverse_uh, inverse_vh, s=30, label=base, marker='o', c=telescopesColorsDict[base], zorder=4)

                index = index + 1                
    return 

def allFrequenciesPlotSettings(ax, fig): 
    
    # Set figure size
    fig.set_figheight(15)
    fig.set_figwidth(15)
       
    # Set figure size
    fig.set_figheight(7)
    fig.set_figwidth(7)
    
    # Plots the baseline lengths corresponding to fringe spacings
    circle1 = plt.Circle((0, 0), radius=8.1, color="grey", fill=False, linestyle='--', linewidth='2.5', label='25 \u03BCas')
    circle2 = plt.Circle((0, 0), radius=4, color="grey", fill=False, linestyle='--', linewidth='2.5', label='50 \u03BCas')
    ax.axhline(0, linestyle='-', linewidth='1.5', color='grey', zorder=1)
    ax.axvline(0, linestyle='-', linewidth='1.5', color='grey', zorder=1)
    ax.axhline(5, linestyle='-', linewidth='0.75', color='#E9E9E9', zorder=1)
    ax.axhline(-5, linestyle='-', linewidth='0.75', color='#E9E9E9', zorder=1)
    ax.axvline(5, linestyle='-', linewidth='0.75', color='#E9E9E9', zorder=1)
    ax.axvline(-5, linestyle='-', linewidth='0.75', color='#E9E9E9', zorder=1)

    # Sets up axes, tick marks, lines, and alignemnts for each plot
    ax.set_xlim([10, -10])
    ax.set_ylim([-10, 10])
    
    ax.tick_params(top=True, right=True, bottom=True, left=True, width=1.5, direction='in', which='both', labelsize='16')

    # Adds ticks and grid lines
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4, prune='both'))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    
    # Adds and labels baseline lengths in the plot
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.text(5.2, 6.75, '25 \u03BCas', rotation=30, fontsize=14.0, fontstyle='oblique')
    ax.text(3.5, 3, '50 \u03BCas', rotation=30, fontsize=14.0, fontstyle='oblique')

    return

def allFrequenciesPlotLabels(ax, fig):
    
    # Adds axis labels in the appropriate locations
    ax.set_xlabel("u (G\u03BB)", fontsize='18')
    ax.set_ylabel("v (G\u03BB)", fontsize='18')
    
    # Telescope baseline labels
    ax.text(1.35, -3.4, 'ALMA-LMT', color=telescopesColorsDict['AA_LM'], fontsize=11.0, weight='bold')
    ax.text(1.5, 0.4, 'ALMA-APEX', color=telescopesColorsDict['AA_AP'], fontsize=11.0, weight='bold')
    ax.text(4.0, -5.75, 'ALMA-SMT', color=telescopesColorsDict['AA_AZ'], fontsize=11.0, weight='bold')
    ax.text(-5.75, 4.5, 'ALMA-SMA', color=telescopesColorsDict['AA_SM'], fontsize=11.0, weight='bold')
    ax.text(9.5, -4.5, 'ALMA-JCMT', color=telescopesColorsDict['AA_JC'], fontsize=11.0, weight='bold')
    ax.text(-1.0, -6.3, 'ALMA-PV', color=telescopesColorsDict['AA_PV'], fontsize=11.0, weight='bold')
    ax.text(-4.0, 1.0, 'LMT-SMA', color=telescopesColorsDict['LM_SM'], fontsize=11.0, weight='bold')
    ax.text(-3.5, -3.0, 'LMT-PV', color=telescopesColorsDict['LM_PV'], fontsize=11.0, weight='bold')
    ax.text(1.9, 3.0, 'APEX-LMT', color=telescopesColorsDict['AP_LM'], fontsize=11.0, weight='bold')
    ax.text(-1.8, 5.35, 'APEX-SMT', color=telescopesColorsDict['AP_AZ'], fontsize=11.0, weight='bold')
    ax.text(-6.5, 3.5, 'APEX-SMA', color=telescopesColorsDict['AP_SM'], fontsize=11.0, weight='bold')
    ax.text(9.5, -5.1, 'APEX-JCMT', color=telescopesColorsDict['AP_JC'], fontsize=11.0, weight='bold')
    ax.text(4.0, 5.9, 'APEX-PV', color=telescopesColorsDict['AP_PV'], fontsize=11.0, weight='bold')
    ax.text(-0.25, 1.5, 'LMT-SMT', color=telescopesColorsDict['AZ_LM'], fontsize=11.0, weight='bold') 
    ax.text(-0.75, -1.75, 'SMT-SMA', color=telescopesColorsDict['AZ_SM'], fontsize=11.0, weight='bold')
    ax.text(3.5, 1.4, 'JCMT-SMT', color=telescopesColorsDict['AZ_JC'], fontsize=11.0, weight='bold')
    ax.text(7.0, -0.75, 'SMT-PV', color=telescopesColorsDict['AZ_PV'], fontsize=11.0, weight='bold')
    ax.text(5.5, -1.5, 'JCMT-LMT', color=telescopesColorsDict['JC_LM'], fontsize=11.0, weight='bold')
    ax.text(1.5, -0.65, 'JCMT-SMA', color=telescopesColorsDict['JC_SM'], fontsize=11.0, weight='bold')
    ax.text(-6.5, -2.5, 'JCMT-PV', color=telescopesColorsDict['JC_PV'], fontsize=11.0, weight='bold')
    ax.text(8.8, 2.1, 'PV-SMA', color=telescopesColorsDict['PV_SM'], fontsize=11.0, weight='bold')

    return

def closeUpPlotSettings(ax, fig):
    
    # Set figure size
    fig.set_figheight(8)
    fig.set_figwidth(8)
    
    # Plots the baseline lengths corresponding to fringe spacings
    circle = plt.Circle((0, 0), radius=1, color="grey", fill=False, linestyle='--', linewidth='2.5', label='0.2"')
    ax.axhline(0, linestyle='-', linewidth='1.5', color='grey', zorder=1)
    ax.axhline(0.5, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axhline(-0.5, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axhline(1, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axhline(-1, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axhline(1.5, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axhline(-1.5, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    
    ax.axvline(0, linestyle='-', linewidth='1.5', color='grey', zorder=1)
    ax.axvline(1, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axvline(-1, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axvline(2, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)
    ax.axvline(-2, linestyle='-', linewidth='0.75', color='#E7E7E7', zorder=1)

    # Sets up axes, tick marks, lines, and alignemnts for each plot
    ax.set_xlim([2.1, -2.1])
    ax.set_ylim([-2, 2])
    
    ax.tick_params(top=True, right=True, bottom=True, left=True, width=1.5, direction='in', which='both', labelsize='16')

    # Adds ticks and grid lines
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    
    # Adds and labels baseline lengths in the plot
    ax.add_patch(circle)
    ax.text(0.81, 0.75, '0.2"', rotation=40, fontsize=18.0, fontstyle='oblique')
    ax.text(-0.4, 1.45, 'ALMA-APEX', color=telescopesColorsDict['AA_AP'], fontsize=14.0, weight='bold')
    ax.text(-0.1, 0.15, 'JCMT-SMA', color=telescopesColorsDict['JC_SM'], fontsize=14.0, weight='bold')

    return

def closeUpPlot(df, ax):
    
    index = 0

    # Iterates through each Telescope-Telescope (Baseline) pair
    for i in telescopes: 
        for j in telescopes: 
            if (i != j): 
                
                # ALMA-APEX telescope baseline
                if (i == 'AA' and j == 'AP'):
                    # Finds the baseline pair and stores it into new DataFrame
                    aa_ap = df[df['T1'].str.contains('AA') & df['T2'].str.contains('AP')]
                    
                    # Plots the baseline pair if it exists
                    uh_aa_ap = aa_ap["U (G\u03BB)"]
                    vh_aa_ap = aa_ap["V (G\u03BB)"]
                    inverse_uh_aa_ap = -1 * aa_ap["U (G\u03BB)"]
                    inverse_vh_aa_ap = -1 * aa_ap["V (G\u03BB)"]
                    
                    ax.scatter(uh_aa_ap, vh_aa_ap, s=30, label='AA_AP', marker='o', c=telescopesColorsDict['AA_AP'], zorder=4)
                    ax.scatter(inverse_uh_aa_ap, inverse_vh_aa_ap, s=30, label='AA_AP', marker='o', c=telescopesColorsDict['AA_AP'], zorder=4)
                
                # JCMT-SMA telescope baseline
                if (i == 'JC' and j == 'SM'):
                    jc_sm = df[df['T1'].str.contains('JC') & df['T2'].str.contains('SM')]

                    uh_jc_sm = jc_sm["U (G\u03BB)"]
                    vh_jc_sm = jc_sm["V (G\u03BB)"]
                    inverse_uh_jc_sm = -1 * jc_sm["U (G\u03BB)"]
                    inverse_vh_jc_sm = -1 * jc_sm["V (G\u03BB)"]

                    ax.scatter(uh_jc_sm, vh_jc_sm, s=30, label='JC_SM', marker='o', c=telescopesColorsDict['JC_SM'], zorder=4)
                    ax.scatter(inverse_uh_jc_sm, inverse_vh_jc_sm, s=30, label='JC_SM', marker='o', c=telescopesColorsDict['JC_SM'], zorder=4)

    return 

'''
--------------------------------------------------
Create Paper IV: Figure 1

To view this figure, please run the code in the cells below.

Results will be in the `images/` directory.
--------------------------------------------------
'''

# Create figure of 4 plots in 1 graph
fig2, ax2 = plt.subplots(1,4, sharey=True, squeeze=True)

# Sets up plot settings 
reproducedAllDaysSettings(ax2, fig2)

counter = 0
for i in days:
    # Paths to converted high and low frequency files (Converted to default Giga)
    highFreq = f'{CONVERTED}/Day_{i}_2017_HIGH_Giga.csv'
    lowFreq = f'{CONVERTED}/Day_{i}_2017_LOW_Giga.csv'
    
    # Converts the original data and saves to new .csv files if files do not exist
    if not(os.path.exists(highFreq)):
        high = conversionProcess(i, "High", 'G')
    if not (os.path.exists(lowFreq)):
        low = conversionProcess(i, "Low", 'G')
    
    high = pd.read_csv(highFreq)
    low = pd.read_csv(lowFreq)

    print("Plotting Day {}...\n".format(i))
    
    # Plots the converted data 
    subplot(high, ax2[counter])
    subplot(low, ax2[counter])
    
    if i=='095':
        dayLabel = 'April 5'
    elif i=='096':
        dayLabel = 'April 6'
    elif i=='100':
        dayLabel = 'April 10'
    else: 
        dayLabel = 'April 11'
    
    ax2[counter].text(-3.75, 8.0, dayLabel, fontsize=20.0)
    
    counter = counter + 1

# Adds axis labels in the appropriate locations
ax2[2].set_xlabel("u (G\u03BB)", fontsize='18', loc='left')
ax2[0].set_ylabel("v (G\u03BB)", fontsize='18')

# Saves the reproduced plots as .jpgs in images/ directory (.png or .eps instead of .jpg)
print("Saving figure...")

SAVE = f'{PLOTS}/Reproduced_All_Days.eps'
plt.savefig(SAVE, bbox_inches='tight')
plt.close()
print(f'Complete! Generated image available at {SAVE}')
print("\n")
'''
--------------------------------------------------
'''

# Create figure for plots
fig, ax = plt.subplots()

# Sets up plot settings 
allFrequenciesPlotSettings(ax, fig)

for i in days:
    # Paths to converted high and low frequency files (Converted to default Giga)
    highFreq = f'{CONVERTED}/Day_{i}_2017_HIGH_Giga.csv'
    lowFreq = f'{CONVERTED}/Day_{i}_2017_LOW_Giga.csv'
    
    # Converts the original data and saves to new .csv files if files do not exist
    if not(os.path.exists(highFreq)):
        high = conversionProcess(i, "High", 'G')
    if not (os.path.exists(lowFreq)):
        low = conversionProcess(i, "Low", 'G')
        print("")
    
    
    high = pd.read_csv(highFreq)
    low = pd.read_csv(lowFreq)
    
    # Plots the converted data 
    subplot(high, ax)
    subplot(low, ax)

allFrequenciesPlotLabels(ax, fig)

# Saves the reproduced plots as .jpgs in images/ directory (.png or .eps instead of .jpg)
print("\nSaving figure...")
SAVE = f'{PLOTS}/All_Frequencies.eps'
plt.savefig(SAVE, bbox_inches='tight')
plt.close()
print(f'Complete! Generated image available at {SAVE}')
print("\n")
'''
--------------------------------------------------
'''

# Create figure for plots
fig, ax = plt.subplots()

# Sets up plot settings 
closeUpPlotSettings(ax, fig)

for i in days:
    # Paths to converted high and low frequency files
    highFreq = f'{CONVERTED}/Day_{i}_2017_HIGH_Mega.csv'
    lowFreq = f'{CONVERTED}/Day_{i}_2017_LOW_Mega.csv'
    
    # Converts the original data and saves to new .csv files if files do not exist
    if not(os.path.exists(highFreq)):
        high = conversionProcess(i, "High", 'M')
    if not (os.path.exists(lowFreq)):
        low = conversionProcess(i, "Low", 'M')
        print("")
    
    
    high = pd.read_csv(highFreq)
    low = pd.read_csv(lowFreq)
    
    # Plots the converted data 
    closeUpPlot(high, ax)
    closeUpPlot(low, ax)

# Adds axis labels in the appropriate locations
ax.set_xlabel("u (M\u03BB)", fontsize='20')
ax.set_ylabel("v (M\u03BB)", fontsize='20')

# Saves the reproduced plots as .jpgs in images/ directory (.png or .eps instead of .jpg)
print("\nSaving figure...")
SAVE = f'{PLOTS}/Close_Up_Frequencies.eps'
plt.savefig(SAVE, bbox_inches='tight')
plt.close()
print(f'Complete! Generated image available at {SAVE}')
print("\n")
'''
--------------------------------------------------
'''