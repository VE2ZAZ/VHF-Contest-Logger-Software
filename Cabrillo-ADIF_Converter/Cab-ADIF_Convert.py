#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Designed for Python 3
#
# Cabrillo-to-ADIF log file conversion
# Version 1.0, January 2023
# By Bert, VE2ZAZ / VA2IW

# Basic conversion of Cabrillo file to ADIF file. This script is fine-tuned for a typical VHF contest.
# Note: This script considers FT8 as the only digital mode used during the contest.
#
# Website: http://ve2zaz.net
# Github: https://github.com/VE2ZAZ/VHF_Contest_Logger_Software
# Note: Please be forgiving about the coding style and its quality. The author's expertise is hardware, not software...
#
#  This software, along with all accompanying files and scripts, is free software: you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or any later version. see https://www.gnu.org/licenses/ . When modifying the
#  software, a mention of the original author, namely Bert-VE2ZAZ, would be a gracious consideration.
    
# Release History
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Version 1.0 (January 2023):
# - Initial release.    
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import tkinter
from tkinter import filedialog as fd
import os

cab_band_list = ["1800","3500","5300","7000","10100","14000","18068","21000","24890","28000","50","70","144","222"  ,"432" ,"902" ,"1.2G","2.3G","3.4G","5.7G","10G","24G"   ,"47G","75G","122G" ]
adi_band_list = ["160m","80m" ,"60m" ,"40m" ,"30m"  ,"20m"  ,"17m"  ,"15m"  ,"12m"  ,"10m"  ,"6m","4m","2m" ,"1.25m","70cm","33cm","23cm","13cm","9cm" ,"6cm" ,"3cm","1.25cm","6mm","4mm","2.5mm"]
cab_mode_list = ["CW","PH" ,"FM","RY"  ,"DG" ]
adi_mode_list = ["CW","SSB","FM","RTTY","FT8"]

root = tkinter.Tk()
root.withdraw()

# Select Cabrillo input file using a popup window and open it
cab_filename = fd.askopenfilename(title="Select Cabrillo File...", filetypes=(("Cabrillo files","*.cab"),("Text files","*.txt"),("All files","*.*")))
f_cab = open(cab_filename, "t+r")
# Open and ADIF output file with the same name prefix as the Cabrillo file. 
adi_filename = os.path.splitext(cab_filename)[0] + ".adi"
f_adi = open(adi_filename,"t+w")

# Read first line
f_cab_line = f_cab.readline()
#Conversion loop, one QSO entry at a time
while (f_cab_line != "END-OF-LOG:\n"):
    if (f_cab_line[0:4] == "QSO:"):     #Search for a QSO entry line

        # Parse cabrillo QSO entry
        " ".join(f_cab_line.split())        # Remove extra spaces
        f_cab_line = f_cab_line.replace("\n", "")
        f_cab_line_list = f_cab_line.split(' ')      # Create list by splitting string by space separator
        print(f_cab_line_list)        

        # Do some string format conversion (adif different from cabrillo)
        # Mode replacement using the mode lists
        for i in range(len(cab_band_list)):
            if (cab_band_list[i] == f_cab_line_list[1]): f_cab_line_list[1] = adi_band_list[i]
        # Band replacement using the band lists
        for i in range(len(cab_mode_list)):
            if (cab_mode_list[i] == f_cab_line_list[2]): f_cab_line_list[2] = adi_mode_list[i]
        # Date formatting, no dashes used in ADIF.
        f_cab_line_list[3] = f_cab_line_list[3].replace("-", "")
        
        # Write ADIF line to adi file
        f_adi_line =    "<call:" + str(len(f_cab_line_list[7])) + ">" + f_cab_line_list[7] \
                      + "<band:" + str(len(f_cab_line_list[1])) + ">" + f_cab_line_list[1] \
                      + "<mode:" + str(len(f_cab_line_list[2])) + ">" + f_cab_line_list[2] \
                      + "<qso_date:" + str(len(f_cab_line_list[3])) + ">" + f_cab_line_list[3] \
                      + "<time_on:" + str(len(f_cab_line_list[4])) + ">" + f_cab_line_list[4] \
                      + "<eor>\n"
        print(f_adi_line)
        f_adi.write(f_adi_line)
        f_adi.flush()
    f_cab_line = f_cab.readline()   # Read next line
f_adi.close
f_cab.close

# Display result popup window
tkinter.messagebox.showinfo(title="Conversion Completed" , message="Conversion Completed.\nFile Saved:\n" + os.path.basename(adi_filename))
print("Conversion Completed.")        

# End program
quit() 
