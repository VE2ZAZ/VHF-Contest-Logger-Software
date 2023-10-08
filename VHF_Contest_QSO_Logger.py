#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Designed for Python 3
#
# VCL - VHF & Microwave Contest Logger Software
# By Bert, VE2ZAZ / VA2IW
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
# Version 1.5 (October 2023):
# - Added support for several North-American microwave contests and the VHF/UHF Sprints.
# - Added support for 6-character grid squares by selecting the proper contest description in the Setup window.
# - The Statistics window now shows the total distance of all QSOs. Used in microwave contest score calculation.
# - The Statistics window now shows the total distance multiplied by the Band factors of all QSOs.
#   Used for the 222 MHz and Up Contest score calculation.
# - Added the display of the latest QSO distance in kilometers at the bottom of the QSO Entry window.
# - The QSO List banner now shows the Contest description along with the Logbook file name.
# - Changed validation of grid square syntax. Now restricted to <A-R><A-R><0-9><0-9><A-X><A-X>. Follows allowed ranges.
# - Now accepts call signs of up to 10 characters to allow special call sign stations.
# - Renamed the software to "VCL - VHF & Microwave Contest Logger Software"
# - Updated Splash screen information
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Version 1.4 (October 2023):
# - Added the logging of WSJT-X QSOs via local UDP ports 2237 and 2239. Two WSJT-X sessions can run concurrently,
#   one per UDP port. Can be enabled in the Setup window. Settings are saved in config file
# - Added the default station values when there is no config.sav file available in the directory. Would crash at launch otherwise.
# - Duplicated QSOs "Dupes": Corrected the score calculation algorithm to reject duplicate QSOs. A new stat of Dupes is displayed
# - Duplicated QSOs "Dupes": The QSO list now shows any subsequent dupe QSOs in red. The first QSO (valid) is shown in orange.
# - Updated Splash screen information
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Version 1.3 (January 2023):
# - Corrected the score calculation algorithm to accurately take into account the January VHF contest.
# - Updated Splash screen information
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Version 1.2 (January 2023):
# - Added "import sys", which was not needed on the author's computer in order to work. It should have been there...
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Version 1.1 (September 2021):
# - In the QSO Capture window, corrected the date value to update based on UTC time, not on local time.
# - In the Grid Map window, added Distance Circle and Azimuth Line display options, along with associated checkboxes.
# - In the setup menu: 
#   - Now converts operator's call sign and grid square to uppercase.
#   - Now supports the operator's gridsquare in 6-character format, allowing for better location accuracy on the gridsquare map.
#   - Now checks the operator's gridsquare for proper format (2-chars/2-digits/2-chars).
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Version 1.0 (July 2021):
# - Initial release.    
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    
# L_I_B_R_A_R_Y  I_M_P_O_R_T_S

from tkinter import *       # Allows the creation of windows and widgets
from tkinter import ttk     # Required for Combobox widget
import datetime
from tkinter.messagebox import askyesno, showerror, showinfo, showwarning
from tkinter import filedialog
import os
import os.path
from shutil import copy
from tkinter.scrolledtext import ScrolledText       # A textbox that cans scroll
import re       # Allows to split using several delimiters for splitting strings
#import math
import sys
sys.path.append("./great_circle_calculator")
import great_circle_calculator as gcc
import socket
from math import sin, cos, sqrt, atan2, radians

# C_O_N_S_T_A_N_T_S

SW_VERSION = " 1.5  08/10/2023"
DATE_POS = 0
TIME_POS = 1
BAND_POS = 2
MODE_POS = 3
CALLSIGN_POS = 4
GRIDSQUARE_POS = 5
X1_MAP_HEIGHT = 2880
X1_MAP_WIDTH = 5760
UDP_IP = ''
UDP_PORT1 = 2237
UDP_PORT2 = 2239

CONTEST_BANDS = ['50','70','144','222','432','902','1.2G','2.3G','3.4G','5.7G','10G','24G','47G','75G','122G','134G','241G','LIGHT']

CONTESTS = ['Please Select Contest',                       # 0
            'ARRL January VHF Contest',                    # 1
            'ARRL June/September VHF Contest',             # 2
            'NA VHF/UHF Sprint',                           # 3
            'NA Microwave Sprint (6-char. Grid Sq.)',      # 4
            'ARRL 222 MHz+ Contest (6-char. Grid Sq.)',    # 5
            'ARRL 10 GHz+ Contest (6-char. Grid Sq.)']     # 6

QSO_POINTS_TBL = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],               # 0
                 [1, 1, 1, 2, 2, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],                # 1
                 [1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],                # 2
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],                # 3
                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],                # 4
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],                # 5
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 0]]  # 6

# Band Factor only applies to 10 GHz and Up contest
BAND_FACTOR =    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           # 0
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],           # 1
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],           # 2
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],           # 3
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],           # 4
                  [0, 0, 0, 2, 1, 4, 2, 6, 10, 10, 6, 20, 20, 20, 20, 20, 20, 0],   # 5
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 5, 0]]           # 6

# Distance factor: Contests with "True" will take the distance into account for score calculation
CONTEST_DIST =  [False,   # 0
                 False,   # 1
                 False,   # 2
                 False,   # 3
                 True,    # 4                
                 True,    # 5         
                 True]    # 6

# G_L_O_B_A_L  V_A_R_I_A_B_L_E_S

Contest_File_Name = ""
Stop_DateTime_Updates = False
Edit_QSO_Action = False
Edit_QSO_Index = 0
Number_QSOs = 0
Number_Grids = 0
Number_Bands = 0
QSO_Points = 0
Multiplier = 0
Total_Dist = 0
Tot_Band_Factor_Dist = 0
Score = 0
Own_Callsign = ""
Own_Gridsquare = ""
Contest_Number = 0
Stats_Window_Geometry_X = 100
Stats_Window_Geometry_Y = 100
Stats_Window_Open = False
Default_BG_Color = ""
QSO_List = []
QSO_Line = []
Map_Scale_Factor = 1
Map_Height = 2880
Lat_Grid_Pitch = 0
Long_Grid_Pitch = 0
wsjt_1_logging_enabled = False
wsjt_2_logging_enabled = False
Number_Dupes = 0
Latest_QSO_Dist = 0

# M_A_I_N__C_O_D_E

# This function checks for a duplicate QSO in the QSO list vs. what is currently entered in the QSO entry window fields
def dupe_check():
    global QSO_Line
    global Edit_QSO_Action
    if (Edit_QSO_Action) and ((QSO_Line[BAND_POS] == Band_Combo_Val.get())   # Verifies if all fields are the same as the recalled QSO in Edit mode
            and (QSO_Line[CALLSIGN_POS] == CallSign_Entry_Val.get()) and (CallSign_Entry_Val.get() != "")
            and (QSO_Line[GRIDSQUARE_POS] == GridSquare_Entry_Val.get()) and (Band_Combo_Val.get() != "")
            and (CallSign_Entry_Val.get() != "")):
                QSO_Entry_Window.configure(bg = Default_BG_Color)    
                QSO_Listbox.configure(selectbackground="dodger blue")
                QSO_Listbox.selection_clear(0, END)
    else:   # Now search for dupe QSO in QSO listbox.
        for i in range(0,QSO_Listbox.size()):
            QSO_String = QSO_Listbox.get(i)
            if (not(CONTEST_DIST[Contest_Number])
            and (CallSign_Entry_Val.get()+" " in QSO_String)
            and (CallSign_Entry_Val.get() != "")
            and (GridSquare_Entry_Val.get()[0:4] in QSO_String)
            and (GridSquare_Entry_Val.get() != "")
            and ("  " + Band_Combo_Val.get() + "  " in QSO_String)):
                QSO_Listbox.selection_clear(0, END)         # Dupe is found; set orange color to QSO Entry window widgets
                QSO_Entry_Window.configure(bg = "sienna1")    
                QSO_Lower_button_frame.configure(bg = "sienna1")    
                QSO_Upper_button_frame.configure(bg = "sienna1")    
                QSO_Buttons_Frame.configure(bg = "sienna1")    
                Date_Entry_Label.configure(bg = "sienna1")    
                Time_Entry_Label.configure(bg = "sienna1")    
                Band_Combo_Label.configure(bg = "sienna1")    
                CallSign_Entry_Label.configure(bg = "sienna1")    
                GridSquare_Entry_Label.configure(bg = "sienna1")    
                Mode_Combo_Label.configure(bg = "sienna1")    
                QSO_Listbox.configure(selectbackground="sienna1")
                QSO_Listbox.selection_set(i)
                QSO_Listbox.index(i)
                QSO_Listbox.see(i)
                break
            elif ((CONTEST_DIST[Contest_Number])
            and (CallSign_Entry_Val.get()+" " in QSO_String)
            and (CallSign_Entry_Val.get() != "")
            and (GridSquare_Entry_Val.get()[0:6] in QSO_String)
            and (GridSquare_Entry_Val.get() != "")
            and ("  " + Band_Combo_Val.get() + "  " in QSO_String)):
                QSO_Listbox.selection_clear(0, END)         # Dupe is found; set orange color to QSO Entry window widgets
                QSO_Entry_Window.configure(bg = "sienna1")    
                QSO_Lower_button_frame.configure(bg = "sienna1")    
                QSO_Upper_button_frame.configure(bg = "sienna1")    
                QSO_Buttons_Frame.configure(bg = "sienna1")    
                Date_Entry_Label.configure(bg = "sienna1")    
                Time_Entry_Label.configure(bg = "sienna1")    
                Band_Combo_Label.configure(bg = "sienna1")    
                CallSign_Entry_Label.configure(bg = "sienna1")    
                GridSquare_Entry_Label.configure(bg = "sienna1")    
                Mode_Combo_Label.configure(bg = "sienna1")    
                QSO_Listbox.configure(selectbackground="sienna1")
                QSO_Listbox.selection_set(i)
                QSO_Listbox.index(i)
                QSO_Listbox.see(i)
                break
            else:      # No duplicate, set the various widget colors back to normal
                QSO_Entry_Window.configure(bg = Default_BG_Color)    
                QSO_Listbox.configure(selectbackground="dodger blue")
                QSO_Lower_button_frame.configure(bg = Default_BG_Color)    
                QSO_Upper_button_frame.configure(bg = Default_BG_Color)    
                QSO_Buttons_Frame.configure(bg = Default_BG_Color)
                Date_Entry_Label.configure(bg = Default_BG_Color)    
                Time_Entry_Label.configure(bg = Default_BG_Color)    
                Band_Combo_Label.configure(bg = Default_BG_Color)    
                CallSign_Entry_Label.configure(bg = Default_BG_Color)    
                GridSquare_Entry_Label.configure(bg = Default_BG_Color)    
                Mode_Combo_Label.configure(bg = Default_BG_Color)
                QSO_Listbox.selection_clear(0, END)
    QSO_Entry_Window.update()

# This function is required because the ComboBox sends an event as parameter, unlike other widgets
def combobox_dupe_check(event):
    dupe_check()

# This function scans for duplicate QSOs and colors them in red font in the QSO listbox.
def qso_listbox_dupe_check():
    global Number_Dupes
    global Contest_Number
    Number_Dupes = 0
    for i in range (0,QSO_Listbox.size()): QSO_Listbox.itemconfig(i, {'foreground':'black'}) # First, color all entries in black.
    for i in range (0,QSO_Listbox.size()): # Then, color the duplicated QSOs in red
        for j in range (i+1,QSO_Listbox.size()):  # Allows to not check a pair of QSOs twice
            QSO_1 =  QSO_Listbox.get(i).split(" ")
            while "" in QSO_1: QSO_1.remove("") # Removes empty strings from list
            QSO_2 =  QSO_Listbox.get(j).split(" ")
            while "" in QSO_2: QSO_2.remove("") # Removes empty strings from list
            if (not(CONTEST_DIST[Contest_Number])
            and (QSO_1[BAND_POS] == QSO_2[BAND_POS])
            and (QSO_1[CALLSIGN_POS] == QSO_2[CALLSIGN_POS])
            and (QSO_1[GRIDSQUARE_POS][0:4] == QSO_2[GRIDSQUARE_POS][0:4])):
                QSO_Listbox.itemconfig(i, {'foreground':'red'})
                QSO_Listbox.itemconfig(j, {'foreground':'DarkOrange'})
                QSO_Listbox.see(i)
            elif ((CONTEST_DIST[Contest_Number])
            and (QSO_1[BAND_POS] == QSO_2[BAND_POS])
            and (QSO_1[CALLSIGN_POS] == QSO_2[CALLSIGN_POS])
            and (QSO_1[GRIDSQUARE_POS][0:6] == QSO_2[GRIDSQUARE_POS][0:6])):
                QSO_Listbox.itemconfig(i, {'foreground':'red'})
                QSO_Listbox.itemconfig(j, {'foreground':'DarkOrange'})
                QSO_Listbox.see(i)
    for i in range (0,QSO_Listbox.size()):
        if  (QSO_Listbox.itemcget(i, 'foreground') == 'red'):
            Number_Dupes = Number_Dupes + 1

def Update_QSO_List_Banner():
    global Contest_Number
    global Contest_File_Name
    QSO_List_Window.title("VCL - " + CONTESTS[Contest_Number] + "  :  " + os.path.basename(Contest_File_Name).split(".VHFlog")[0])

# Derives the latitude and longitude of a grid square
def GridSquare_2_LatLong(gs):
    #Decode Latitude: 2nd character (a letter)
    gs_lat = (ord(gs[1]) - 65) * 10
    #Decode Latitude: 4th character (a digit)
    gs_lat += int(gs[3])
    #Decode Latitude: 6th character (a letter)
    gs_lat += ((ord(gs[5]) - 65)/24) + (1/48) - 90 
    #Decode Longitude: 1st character (a letter)
    gs_lon = (ord(gs[0]) - 65) * 20
    #Decode Longitude: 3rd character (a digit)
    gs_lon += int(gs[2]) * 2
    #Decode Longitude: 5th character (a letter)
    gs_lon += ((ord(gs[4]) - 65)/12) + (1/24) - 180
    return [round(gs_lat,4), round(gs_lon,4)]

# Calculates the distance between two grid squares, based on the haversine formula, which assumes the earth is a sphere.
def Dist_Between_2_GridSquares(gs1,gs2):
    R = 6373.0       # Approximate radius of earth in km
    lat1 = radians(GridSquare_2_LatLong(gs1)[0])
    lon1 = radians(GridSquare_2_LatLong(gs1)[1])
    lat2 = radians(GridSquare_2_LatLong(gs2)[0])
    lon2 = radians(GridSquare_2_LatLong(gs2)[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = round(R * c)
    return distance

# This function calculates the score based on the ARRL VHF Contest rules
def calculate_score(Contest):
    global Number_QSOs
    global Number_Grids
    global Number_Bands
    global Number_Dupes
    global QSO_Points
    global Multiplier
    global Total_Dist
    global Tot_Band_Factor_Dist
    global Contest_Number
    global Score
    global QSO_List
    
    Grid_List = []
    Band_List = []
    update_qso_list()
    # QSO points and band factor calculations. Some contests consider QSO points as multipliers!
    QSO_Points = 0
    for i in range(0,len(QSO_List)):
        Grid_List.append(QSO_List[i][GRIDSQUARE_POS])
        Band_List.append(QSO_List[i][BAND_POS])
        if not (QSO_Listbox.itemcget(i, 'foreground') == 'red'): # Rejects dupes in the QSO points calculation
            QSO_Points += QSO_POINTS_TBL[Contest_Number][CONTEST_BANDS.index(QSO_List[i][BAND_POS])]
    # Calculate Multipliers. Rule: The number of different grid squares contacted from each band.
    # Each grid square counts as a multiplier on each band.
    Unique_Band_List= []
    Multiplier = 0
    Temp_List = []
    Unique_Band_List = list(set(Band_List))  # creates a list of unique bands (no duplicates)
    for i in range(0,len(Unique_Band_List)):
        Temp_List = []
        for j in range(0,len(QSO_List)):
            if Band_List[j] == Unique_Band_List[i]: Temp_List.append(Grid_List[j][0:4]) # Only consider first 4 grid square characters
        Multiplier += len(list(set(Temp_List))) # The sum of all unique grids contacted per band        
    Number_QSOs = QSO_Listbox.size()
    Number_Grids = len(set(Grid_List))   # Counts unique grids
    Number_Bands = len(set(Band_List))   # Counts unique bands
    # Calculate total distance with Band Factor. Band factor is for 10 GHz and Up Contest.
    Total_Dist = 0
    Tot_Band_Factor_Dist = 0
    for i in range(0,len(QSO_List)):
        if (len(QSO_List[i][GRIDSQUARE_POS]) == 4):   # 4-character grid square
            stuffed_gridsquare = QSO_List[i][GRIDSQUARE_POS] + 'LL'  # Assumes the center of the grid
            QSO_Dist = Dist_Between_2_GridSquares(Own_Gridsquare,stuffed_gridsquare)
            Total_Dist += QSO_Dist
        else:   # Full 6-character grid square
            if (Own_Gridsquare == QSO_List[i][GRIDSQUARE_POS]):
                Total_Dist += 1
                Tot_Band_Factor_Dist += 1 * BAND_FACTOR[Contest_Number][CONTEST_BANDS.index(QSO_List[i][BAND_POS])]
            else:
                QSO_Dist = Dist_Between_2_GridSquares(Own_Gridsquare,QSO_List[i][GRIDSQUARE_POS])
                Total_Dist += QSO_Dist
                Tot_Band_Factor_Dist += QSO_Dist * BAND_FACTOR[Contest_Number][CONTEST_BANDS.index(QSO_List[i][BAND_POS])]                
    # Calculate final score, depending on contest
    if not(CONTEST_DIST[Contest_Number]):   # Check of it is a 4 character grid square contest
        Score = QSO_Points * Multiplier
    elif (Contest_Number == 4):
        Score = Total_Dist
    elif (Contest_Number == 5):
        Score = Tot_Band_Factor_Dist
    elif (Contest_Number == 6):
        Score = Tot_Band_Factor_Dist + QSO_Points

#Converts the Callsign to uppercase and check for duplicates on-the-fly
def validate_callsign(event):
    CallSign_Entry_Val.set(CallSign_Entry_Val.get().upper())
    if len(CallSign_Entry_Val.get()) > 10: CallSign_Entry_Val.set(CallSign_Entry_Val.get()[:-1])
    CallSign_Entry_Val.set(re.sub('[^A-Z0-9/]', '', CallSign_Entry_Val.get()))  # Filters out characters other than digits, letters and '/'
    dupe_check()

#Converts the grid square to uppercase and check for duplicates on-the-fly. Also returns whether the 2-letter/2digits(/2-letter) grid square format is met
def validate_gridsquare(event):
    global Contest_Number
    GridSquare_Entry_Val.set(GridSquare_Entry_Val.get().upper())
    if ((len(GridSquare_Entry_Val.get()) > 4) and not(CONTEST_DIST[Contest_Number])): GridSquare_Entry_Val.set(GridSquare_Entry_Val.get()[:-1])
    elif (len(GridSquare_Entry_Val.get()) > 6): GridSquare_Entry_Val.set(GridSquare_Entry_Val.get()[:-1])
    GridSquare_Breakdown_List = list(GridSquare_Entry_Val.get())
    if (len(GridSquare_Breakdown_List) == 1):
        GridSquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0]))
    elif (len(GridSquare_Breakdown_List) == 2):
        GridSquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]))
    elif (len(GridSquare_Breakdown_List) == 3):
        GridSquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2]))
    elif (len(GridSquare_Breakdown_List) == 4):
        GridSquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2] + GridSquare_Breakdown_List[3]))
    if (CONTEST_DIST[Contest_Number]):
        if (len(GridSquare_Breakdown_List) == 5):
            GridSquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2] + GridSquare_Breakdown_List[3]) + re.sub('[^A-X]', '', GridSquare_Breakdown_List[4]))
        elif (len(GridSquare_Breakdown_List) == 6):
            GridSquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2] + GridSquare_Breakdown_List[3]) + re.sub('[^A-X]', '', GridSquare_Breakdown_List[4] + GridSquare_Breakdown_List[5]))
            dupe_check()
            return True
    else:
        dupe_check()
        return True
    dupe_check()
    return False

# Filters out characters other than 0-9 and "-" in the time entry.
def validate_date(event):
    if len(Date_Entry_Val.get()) > 10: Date_Entry_Val.set(Date_Entry_Val.get()[:-1])
    Date_Entry_Val.set(re.sub('[^-0-9]', '', Date_Entry_Val.get()))  # Filters out characters other than digits and '-'

# Filters out characters other than 0-9 in the date entry.
def validate_time(event):
    if len(Time_Entry_Val.get()) > 4: Time_Entry_Val.set(re.sub('[^0-9]', '', Time_Entry_Val.get()[:-1])) # Filters out characters other than digits

# Save listbox data (QSOs) to the log file
def log_file_save():
    global Contest_File_Name
    try:   # Catches a shutil.SameFileError bug that occurs only in Windows
        if os.path.exists(Contest_File_Name): copy(Contest_File_Name,Contest_File_Name + ".bak") # copies original log to a backup file before any modification.
    except:
        pass     # Catches a file copy error.
    file = open(Contest_File_Name,'w') # Open text file for writing
    for i in range(0,QSO_Listbox.size()):    
        QSO_Line = QSO_Listbox.get(i).split(" ")
        while "" in QSO_Line: QSO_Line.remove("") # Removes empty strings from list
        file.write(QSO_Line[DATE_POS] + ","
                 + QSO_Line[TIME_POS] + ","
                 + QSO_Line[BAND_POS] + ","
                 + QSO_Line[MODE_POS] + ","
                 + QSO_Line[CALLSIGN_POS] + ","
                 + QSO_Line[GRIDSQUARE_POS] + "\n")
    file.close()
    if (os.path.exists(Contest_File_Name.split(".VHFlog")[0])):
        os.remove(Contest_File_Name.split(".VHFlog")[0]) # Required to delete extraneous file created on open (...,'w'): It is a Python bug.
    update_qso_list()
    update_grid_boxes_no_event()

# Loads a selected log book file and populates the QSO listbox with the QSOs from the log book file.
def log_file_load():
    global Contest_File_Name
    global QSO_Listbox
    QSO_Listbox.delete (0 , QSO_Listbox.size()-1)  # First clear all old QSOs in the QSO listbox
    try:
        file = open(Contest_File_Name,'r') # Open text file for reading
        OneLine = file.readline()
        while OneLine:
            QSO_Line_List = OneLine.split(",")
            QSO_Listbox.insert(END,QSO_Line_List[DATE_POS].ljust(12, ' ') + QSO_Line_List[TIME_POS].ljust(6, ' ') + QSO_Line_List[BAND_POS].ljust(6, ' ')
                               + QSO_Line_List[MODE_POS].ljust(4, ' ') + QSO_Line_List[CALLSIGN_POS].ljust(10, ' ') + QSO_Line_List[GRIDSQUARE_POS][:-1].ljust(6, ' '))
            OneLine = file.readline()
        for i in range(0,QSO_Listbox.size()): # Color the QSO backgrounds in the listbox with alternate colors
            if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2") 
            else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3")
        file.close()
        No_Log_Loaded_Label.pack_forget() # This makes the label disappear
        Update_QSO_List_Banner()
    except IOError:
        No_Log_Loaded_Label.pack(expand=True, fill=None) # This makes the label appear
        QSO_List_Window.title("VCL - No Log Loaded")
    update_qso_list()
    qso_listbox_dupe_check()

# Saves the QSO captured in the QSO entry window to the logbook file.
def save_qso_button_clicked():
    global Edit_QSO_Action
    global Stop_DateTime_Updates
    global Edit_QSO_Index
    # Add QSO to QSO listbox
    style= ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",fieldbackground= "orange", background= "white")
    if ((CallSign_Entry_Val.get()=="") or (GridSquare_Entry_Val.get()=="")):
        if (CallSign_Entry_Val.get()==""): Callsign_Entry.configure(bg="orange")
        if (GridSquare_Entry_Val.get()==""): GridSquare_Entry.configure(bg="orange")
        dupe_check()    # Done to clear any dupe check colors
        return
    elif (not validate_gridsquare(None)):
        GridSquare_Entry.configure(bg="orange")
        return
    else:
        Callsign_Entry.configure(bg="white")
        GridSquare_Entry.configure(bg="white")
    if Edit_QSO_Action:
        QSO_Index = Edit_QSO_Index
        QSO_Listbox.delete(Edit_QSO_Index)        
    else: QSO_Index = 0
    QSO_Listbox.insert(QSO_Index,Date_Entry_Val.get().ljust(12, ' ')
                       + Time_Entry_Val.get().ljust(6, ' ')
                       + Band_Combo_Val.get().ljust(6, ' ')
                       + Mode_Combo_Val.get().ljust(4, ' ')
                       + CallSign_Entry_Val.get().ljust(10, ' ')
                       + GridSquare_Entry_Val.get().ljust(6, ' '))
    if (len(GridSquare_Entry_Val.get()) == 4):   # 4-character grid square
        stuffed_gridsquare = GridSquare_Entry_Val.get() + 'LL'  # Assumes the center of the grid
        Latest_QSO_Dist = Dist_Between_2_GridSquares(Own_Gridsquare,stuffed_gridsquare)
        Dist_Text_Label.config(text = 'Latest QSO Distance (Km): ~' + str(Latest_QSO_Dist))
    else:
        Latest_QSO_Dist = Dist_Between_2_GridSquares(Own_Gridsquare,GridSquare_Entry_Val.get())
        Dist_Text_Label.config(text = 'Latest QSO Distance (Km): ' + str(Latest_QSO_Dist))
    for i in range(0,QSO_Listbox.size()):
        if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2")  # even lines
        else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3")   # Odd lines
    log_file_save()
    QSO_Listbox.selection_clear(0, END) # Deselects any remaining items
    CallSign_Entry_Val.set("")
    GridSquare_Entry_Val.set("")
    Date_Entry.configure(bg=Default_BG_Color, fg="gray44")
    Time_Entry.configure(bg=Default_BG_Color, fg="gray44")
    Save_QSO_Button.configure(text = "Save QSO", fg = "dark green")        
    QSO_Entry_Window.configure(bg = Default_BG_Color)    
    QSO_Listbox.configure(selectbackground="dodger blue")
    QSO_Lower_button_frame.configure(bg = Default_BG_Color)    
    QSO_Upper_button_frame.configure(bg = Default_BG_Color)    
    QSO_Buttons_Frame.configure(bg = Default_BG_Color)
    Date_Entry_Label.configure(bg = Default_BG_Color)    
    Time_Entry_Label.configure(bg = Default_BG_Color)    
    Band_Combo_Label.configure(bg = Default_BG_Color)    
    CallSign_Entry_Label.configure(bg = Default_BG_Color)    
    GridSquare_Entry_Label.configure(bg = Default_BG_Color)    
    Mode_Combo_Label.configure(bg = Default_BG_Color)    
    QSO_Entry_Window.grab_release()
    Callsign_Entry.focus_set()
    qso_listbox_dupe_check()
    Stop_DateTime_Updates = False
    Edit_QSO_Action = False
    
# Checks if a new QSO has appeared on UDP port assigned to WSJT-X, and enters it as a new QSO in the QSO listbox.
def check_and_save_qso_from_wsjt_thread():
    global Edit_QSO_Action
    global Stop_DateTime_Updates
    global Edit_QSO_Index
    global wsjt_1_logging_enabled
    global wsjt_2_logging_enabled
    global sock1
    global sock2
    global Contest_Number

    def extract_to_QSO_Listbox():
        temp_split = log_string.split('<call:') # Index 1: string length and the rest of the string
        temp_split = temp_split[1].split('>')   # Index 0: string length, Index 1: desired string and the rest
        wsjt_callsign = temp_split[1][0:int(temp_split[0])]  # Extrats just desired string
        
        temp_split = log_string.split('<gridsquare:') # Index 1: string length and the rest of the string
        temp_split = temp_split[1].split('>')   # Index 0: string length, Index 1: desired string and the rest
        wsjt_gridsquare = temp_split[1][0:int(temp_split[0])]  # Extrats just desired string
        if ((CONTEST_DIST[Contest_Number]) and (len(wsjt_gridsquare) == 4)): # A 6-character grid contest            
            showerror(title='WSJT-X Config Error', message='Error: WSJT-X only sending 4-character Grid Squares. Change WSJT-X Special Operating Activity settings.')
            return
        elif (not(CONTEST_DIST[Contest_Number]) and (len(wsjt_gridsquare) == 6)): # A 4-character grid contest
            showwarning(title='WSJT-X Config Warning', message='Warning: WSJT-X is sending 6-character Grid Squares. Last two characters are dropped.')
            
        wsjt_mode = 'DG'

        temp_split = log_string.split('<qso_date:') # Index 1: string length and the rest of the string
        temp_split = temp_split[1].split('>')   # Index 0: string length, Index 1: desired string and the rest
        wsjt_date = temp_split[1][0:8]  # Extrats just desired string
        wsjt_date = wsjt_date[0:4] + '-' + wsjt_date[4:6] + '-' + wsjt_date[6:8]

        temp_split = log_string.split('<time_on:') # Index 1: string length and the rest of the string
        temp_split = temp_split[1].split('>')   # Index 0: string length, Index 1: desired string and the rest
        wsjt_time = temp_split[1][0:4]  # Extrats just desired string

        temp_split = log_string.split('<freq:') # Index 1: string length and the rest of the string
        temp_split = temp_split[1].split('>')   # Index 0: string length, Index 1: desired string and the rest
        wsjt_band = temp_split[1][0:int(temp_split[0])]  # Extrats just desired string

        if (int(wsjt_band.split('.')[0])) in range(50,53): wsjt_band = "50"
        elif (int(wsjt_band.split('.')[0])) in range(69,71): wsjt_band = "70"
        elif (int(wsjt_band.split('.')[0])) in range(144,149): wsjt_band = "144"
        elif (int(wsjt_band.split('.')[0])) in range(220,226): wsjt_band = "222"
        elif (int(wsjt_band.split('.')[0])) in range(420,451): wsjt_band = "432"
        elif (int(wsjt_band.split('.')[0])) in range(900,929): wsjt_band = "902"
        elif (int(wsjt_band.split('.')[0])) in range(1240,1301): wsjt_band = "1.2G"
        elif (int(wsjt_band.split('.')[0])) in range(2300,2451): wsjt_band = "2.3G"
        elif (int(wsjt_band.split('.')[0])) in range(3300,3451): wsjt_band = "3.4G"
        elif (int(wsjt_band.split('.')[0])) in range(5650,5926): wsjt_band = "5.7G"
        elif (int(wsjt_band.split('.')[0])) in range(10000,10501): wsjt_band = "10G"
        elif (int(wsjt_band.split('.')[0])) in range(24000,24251): wsjt_band = "24G"
        elif (int(wsjt_band.split('.')[0])) in range(47000,47201): wsjt_band = "47G"
        elif (int(wsjt_band.split('.')[0])) in range(76000,81001): wsjt_band = "75G"
        elif (int(wsjt_band.split('.')[0])) in range(122250,123001): wsjt_band = "122G"
        elif (int(wsjt_band.split('.')[0])) in range(134000,141001): wsjt_band = "134G"
        elif (int(wsjt_band.split('.')[0])) in range(241000,250001): wsjt_band = "241G"
        else: wsjt_band = "???"            

        QSO_Index = 0
        QSO_Listbox.insert(QSO_Index,wsjt_date.ljust(12, ' ')
                            + wsjt_time.ljust(6, ' ')
                            + wsjt_band.ljust(6, ' ')
                            + wsjt_mode.ljust(4, ' ')
                            + wsjt_callsign.ljust(10, ' ')
                            + wsjt_gridsquare.ljust(6, ' '))
        for i in range(0,QSO_Listbox.size()):
            if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2")  # even lines
            else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3")   # Odd lines
        log_file_save()
        QSO_Listbox.selection_clear(0, END) # Deselects any remaining items
        CallSign_Entry_Val.set("")
        GridSquare_Entry_Val.set("")
        Date_Entry.configure(bg=Default_BG_Color, fg="gray44")
        Time_Entry.configure(bg=Default_BG_Color, fg="gray44")
        Save_QSO_Button.configure(text = "Save QSO", fg = "dark green")        
        QSO_Entry_Window.configure(bg = Default_BG_Color)    
        QSO_Listbox.configure(selectbackground="dodger blue")
        QSO_Lower_button_frame.configure(bg = Default_BG_Color)    
        QSO_Upper_button_frame.configure(bg = Default_BG_Color)    
        QSO_Buttons_Frame.configure(bg = Default_BG_Color)
        Date_Entry_Label.configure(bg = Default_BG_Color)    
        Time_Entry_Label.configure(bg = Default_BG_Color)    
        Band_Combo_Label.configure(bg = Default_BG_Color)    
        CallSign_Entry_Label.configure(bg = Default_BG_Color)    
        GridSquare_Entry_Label.configure(bg = Default_BG_Color)    
        Mode_Combo_Label.configure(bg = Default_BG_Color)    
        QSO_Entry_Window.grab_release()
        Callsign_Entry.focus_set()
        qso_listbox_dupe_check()
        Stop_DateTime_Updates = False
        Edit_QSO_Action = False

    if (wsjt_1_logging_enabled):
        try:
            data, addr = sock1.recvfrom(1024) # buffer size is 1024 bytes
            if data[11] == 12:
                log_string  = data[36:].decode('ascii')
                extract_to_QSO_Listbox()
        except: pass
    if (wsjt_2_logging_enabled):
        try:
            data, addr = sock2.recvfrom(1024) # buffer size is 1024 bytes
            if data[11] == 12:
                log_string  = data[36:].decode('ascii')
                extract_to_QSO_Listbox()
        except: pass
    QSO_Entry_Window.after(100, check_and_save_qso_from_wsjt_thread)


# This function erase the data that is already in the entry boxes of the Capture window.
def clear_qso_text_button_clicked():
    global Stop_DateTime_Updates
    global Edit_QSO_Action
    CallSign_Entry_Val.set("")
    GridSquare_Entry_Val.set("")
    Save_QSO_Button.configure(text = "Save QSO", fg = "dark green")        
    Date_Entry.configure(bg=Default_BG_Color, fg="gray44")
    Time_Entry.configure(bg=Default_BG_Color, fg="gray44")
    QSO_Entry_Window.configure(bg = Default_BG_Color)    
    QSO_Listbox.configure(selectbackground="dodger blue")
    Callsign_Entry.configure(bg="white")
    GridSquare_Entry.configure(bg="white")
    Callsign_Entry.focus_set()
    QSO_Entry_Window.grab_release()
    Stop_DateTime_Updates = False
    Edit_QSO_Action = False
    qso_listbox_dupe_check()
    dupe_check()

# Associates a hint (help) text to a hover action on a widget and displays it in the Hint window.
def create_hint(widget,hint_text):
    
    def display_hint(event):
        Hint_Text_Box.config(state='normal')
        Hint_Text_Box.delete("1.0", "end")
        Hint_Text_Box.insert(END, hint_text)
        Hint_Text_Box.config(state='disabled')
        
    widget.bind("<Enter>", display_hint)

# This function is required because an Entry sends an event as parameter, unlike other widgets
def save_qso_returnkey_pressed(event):
    save_qso_button_clicked()
    
def clear_qso_returnkey_pressed(event):
    clear_qso_text_button_clicked()

# Creates the stats window and displays the statistics and score into it 
def stats_button_clicked():
    # Convert QSO lines to a list
    global Number_QSOs
    global Number_Grids
    global Number_Bands
    global QSO_Points
    global Multiplier
    global Number_Dupes
    global Total_Dist
    global Tot_Band_Factor_Dist
    global Score
    global Stats_Window_Geometry_X
    global Stats_Window_Geometry_Y
    global Stats_Window_Open
    global Contest_Number
    global Latest_QSO_Dist

    if not Stats_Window_Open:  # Otherwise more than one instance of that wndow will be created
        def window_position_save(event):
            global Stats_Window_Geometry_X
            global Stats_Window_Geometry_Y
            Stats_Window_Geometry_X = Stats_Window.geometry().split("+")[1]
            Stats_Window_Geometry_Y = Stats_Window.geometry().split("+")[2]
            Stats_Window.protocol('WM_DELETE_WINDOW', stats_window_exit)

        if (Contest_Number == 0):
            showerror("Error!","The Score Calculation requires that you first configure the contest settings. Please fill out the Settings window first.")
            return
        # Create window
        Stats_Window = Toplevel(QSO_List_Window)
        Stats_Window.title("VCL - Statistics")    
        Stats_Window.geometry('{}x{}+{}+{}'.format(320,280,Stats_Window_Geometry_X,Stats_Window_Geometry_Y))
        Stats_Window.configure(bg = Default_BG_Color)
        Stats_Window.resizable(0, 0) # Makes Log entry window size fixed
        Stats_Window.iconphoto(True, PhotoImage(file = "./images/VCL_Icon_350x350.png"))  # Only accepts .PNG files
        Stats_Window.bind("<Configure>", window_position_save)
        create_hint(Stats_Window,("""This window displays the log statistics in real time as per the ARRL rules. The score takes into account that the """
                                  """January contest rules awards a higher score to UHF and microwave QSOs. The microwave contests use the distance """
                                  """between the two stations in all QSOs for the score calculation."""))

        Contest_Name_Title_Label = Label(Stats_Window, text="Contest:", bg = Default_BG_Color )
        Contest_Name_Title_Label.place(x=30,y=15)
        Contest_Name_Label = Label(Stats_Window, text=CONTESTS[Contest_Number], bg = Default_BG_Color )
        Contest_Name_Label.place(x=30,y=32)

        Contest_Results_Text2_Label = Label(Stats_Window, text="Num. QSOs:", bg = Default_BG_Color )
        Contest_Results_Text2_Label.place(x=30,y=60)
        Contest_Results_Text3_Label = Label(Stats_Window, text="Num. Dupes:", bg = Default_BG_Color )
        Contest_Results_Text3_Label.place(x=30,y=80)
        Contest_Results_Text4_Label = Label(Stats_Window, text="Num. Grids:", bg = Default_BG_Color)
        Contest_Results_Text4_Label.place(x=30,y=100)
        Contest_Results_Text5_Label = Label(Stats_Window, text="Num. Bands:", bg = Default_BG_Color)
        Contest_Results_Text5_Label.place(x=30,y=120)
        Contest_Results_Text6_Label = Label(Stats_Window, text="QSO Points:", bg = Default_BG_Color)
        Contest_Results_Text6_Label.place(x=30,y=140)
        Contest_Results_Text7_Label = Label(Stats_Window, text="Multipliers:", bg = Default_BG_Color)
        Contest_Results_Text7_Label.place(x=30,y=160)
        Contest_Results_Text8_Label = Label(Stats_Window, text="Total Dist. (Km):", bg = Default_BG_Color)
        Contest_Results_Text8_Label.place(x=30,y=180)
        Contest_Results_Text9_Label = Label(Stats_Window, text="Total Band Factor Dist:", bg = Default_BG_Color)
        Contest_Results_Text9_Label.place(x=30,y=200)
        Contest_Results_Text10_Label = Label(Stats_Window, text="Total Score:", bg = Default_BG_Color, font='Helvetica 11 bold')
        Contest_Results_Text10_Label.place(x=30,y=225)

        Contest_Results_Number2_Label = Label(Stats_Window, text=Number_QSOs, bg = Default_BG_Color)
        Contest_Results_Number2_Label.place(x=200,y=60)
        Contest_Results_Number3_Label = Label(Stats_Window, text=Number_Dupes, bg = Default_BG_Color)
        Contest_Results_Number3_Label.place(x=200,y=80)
        Contest_Results_Number4_Label = Label(Stats_Window, text=Number_Grids, bg = Default_BG_Color)
        Contest_Results_Number4_Label.place(x=200,y=100)
        Contest_Results_Number5_Label = Label(Stats_Window, text=Number_Bands, bg = Default_BG_Color)
        Contest_Results_Number5_Label.place(x=200,y=120)
        Contest_Results_Number6_Label = Label(Stats_Window, text=QSO_Points, bg = Default_BG_Color)
        Contest_Results_Number6_Label.place(x=200,y=140)
        Contest_Results_Number7_Label = Label(Stats_Window, text=Multiplier, bg = Default_BG_Color)
        Contest_Results_Number7_Label.place(x=200,y=160)
        Contest_Results_Number8_Label = Label(Stats_Window, text=Total_Dist, bg = Default_BG_Color)
        Contest_Results_Number8_Label.place(x=200,y=180)
        Contest_Results_Number9_Label = Label(Stats_Window, text=Tot_Band_Factor_Dist, bg = Default_BG_Color)
        Contest_Results_Number9_Label.place(x=200,y=200)
        Contest_Results_Number10_Label = Label(Stats_Window, text=Score, bg = Default_BG_Color, font='Helvetica 11 bold')
        Contest_Results_Number10_Label.place(x=200,y=225)

        # This function is defined inside the stats_button_clicked function because it refers to its widgets
        def update_stats():
            calculate_score(Contest_Number)
            Contest_Name_Label.config(text = CONTESTS[Contest_Number])
            Contest_Results_Number2_Label.config(text = Number_QSOs)
            Contest_Results_Number3_Label.config(text = Number_Dupes)
            Contest_Results_Number4_Label.config(text = Number_Grids)
            Contest_Results_Number5_Label.config(text = Number_Bands)
            Contest_Results_Number6_Label.config(text = QSO_Points)
            Contest_Results_Number7_Label.config(text = Multiplier)
            Contest_Results_Number8_Label.config(text = Total_Dist)
            Contest_Results_Number9_Label.config(text = Tot_Band_Factor_Dist)
            Contest_Results_Number10_Label.config(text = Score)
            Stats_Window.after(500, update_stats)

        # This function is defined inside the stats_button_clicked function because it refers to its widgets      
        def stats_window_exit():
            global Stats_Window_Open
            Stats_Window_Open = False
            Stats_Window.destroy()

        update_stats()
        Stats_Window_Open = True

# Opens an existing contest log book file and loads the file content into the QSO listbox.
def open_contest_button_clicked():
    global Contest_File_Name
    Temp = filedialog.askopenfilename(title="Open Log File",
                    filetypes=(("log files", "*.VHFlog"),("all files", "*.*"))) # opens file dialog and returns file name
    if (len(Temp) == 0): return
    Contest_File_Name = Temp
    log_file_load()
    Update_QSO_List_Banner()
    update_qso_list()
    update_grid_boxes_no_event()
    qso_listbox_dupe_check()
    grid_has_4_chars = False
    for i in range(0,QSO_Listbox.size()):    
        if ((len(QSO_List[i][GRIDSQUARE_POS]) < 6) and (CONTEST_DIST[Contest_Number])): grid_has_4_chars = True
    if (grid_has_4_chars):
        showwarning(title='Contest Config Warning', message='Warning: The QSO list contains 4-character grid squares, but the selected contest calls for 6-character grid squares. Score calculation will be wrong!')
    showinfo('Select Contest Type', 'Make sure to select the Current Contest Type in the Setup window.')
    Hints_Window.lift()
    
# Clears the existing QSOs from the QSO listbox and opens a new contest logbook file
def new_contest_button_clicked():
    global Contest_File_Name
    Contest_File_Name = filedialog.asksaveasfile(title="New Log File",
                    filetypes=(("log files", "*.VHFlog"),("all files", "*.*"))).name # opens file dialog and returns file name
    Contest_File_Name_List = Contest_File_Name.split(".")
    if (Contest_File_Name_List[len(Contest_File_Name_List)-1] != "VHFlog"):
        Contest_File_Name = Contest_File_Name + ".VHFlog"
    QSO_Listbox.delete(0, last=QSO_Listbox.size()-1)
    log_file_save()
    Update_QSO_List_Banner()
    update_qso_list()
    showinfo('Select Contest Type', 'Make sure to select the Current Contest Type in the Setup window.')

# Brings up the splash window to act as an about page
def about_button_clicked():
    def hide_splash_window(event):    
        Splash_Window.grab_release()
        Splash_Window.withdraw()
    # Display the splashed window centered over the QSO list window    
    x = int(QSO_List_Window.geometry().split("+")[1]) + int(re.split("[x+]",QSO_List_Window.geometry())[0])/2 - 150
    y = int(QSO_List_Window.geometry().split("+")[2]) + int(re.split("[x+]",QSO_List_Window.geometry())[1])/2 - 100
    Splash_Window.geometry("%dx%d+%d+%d" % (300,200,x,y))  # Place splash screen at center of screen
    Splash_Window.grab_set()
    Splash_Window.deiconify()   
    Splash_Window_Canvas.bind("<ButtonPress-1>", hide_splash_window)  # Aclick on the splash window clears it.

# Brings up the highlighted QSO data into the QSO entry window for editing (to make corrections)
def edit_qso_button_clicked():
    global Stop_DateTime_Updates
    global Edit_QSO_Action
    global Edit_QSO_Index
    global QSO_Line
    Stop_DateTime_Updates = True
    Edit_QSO_Action = True
    Date_Entry.configure(bg="white", fg="black")
    Time_Entry.configure(bg="white", fg="black")
    Callsign_Entry.configure(bg="white")
    GridSquare_Entry.configure(bg="white")
    Save_QSO_Button.configure(text = "Update QSO", fg = "dark green")        
    QSO_Entry_Window.grab_set()
    Edit_QSO_Index = QSO_Listbox.curselection()
    QSO_Line = QSO_Listbox.get(QSO_Listbox.curselection()).split(" ")
    while "" in QSO_Line: QSO_Line.remove("") # Removes empty strings from list
    Date_Entry_Val.set(QSO_Line[DATE_POS])
    Time_Entry_Val.set(QSO_Line[TIME_POS])
    Band_Combo_Val.set(QSO_Line[BAND_POS])
    Mode_Combo_Val.set(QSO_Line[MODE_POS])
    CallSign_Entry_Val.set(QSO_Line[CALLSIGN_POS])
    GridSquare_Entry_Val.set(QSO_Line[GRIDSQUARE_POS])
    for i in range(0,QSO_Listbox.size()):
        if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2") 
        else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3")
    update_qso_list()
    qso_listbox_dupe_check()

# Erase all QSOs from the QSO entry listbox and from the logbook file.
def erase_log_button_clicked():
    answer = askyesno("Delete All QSOs", "Are you sure you want to delete ALL QSOs from the QSO list?")
    if not(answer): return
    QSO_Listbox.delete(0, last=QSO_Listbox.size()-1)
    log_file_save()

# Erase highlighted QSO from the QSO list.
def erase_qso_button_clicked():
    answer = askyesno("Erase QSOs Confirmation", "Are you sure you want to erase the selected QSO?")
    if not(answer): return
    selected_line = QSO_Listbox.curselection()
    QSO_Listbox.delete(selected_line)
    for i in range(0,QSO_Listbox.size()):
        if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2") 
        else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3")
    log_file_save()
    qso_listbox_dupe_check()

# Function executed when the delete key is pressed.
def erase_qso_event(event):
    erase_qso_button_clicked()

# Sort the QSOs in the QSO listbox and saves to the logbook file
def sort_qsos(field):  
    global QSO_List
    # Create list of QSOs
    update_qso_list()
    QSO_List.sort(key=lambda x: x[field])
    for i in range(0,QSO_Listbox.size()):    
        QSO_Listbox.delete(i)
        QSO_Listbox.insert(i,QSO_List[i][DATE_POS].ljust(12, ' ') + QSO_List[i][TIME_POS].ljust(6, ' ') + QSO_List[i][BAND_POS].ljust(6, ' ')
                        + QSO_List[i][MODE_POS].ljust(4, ' ') + QSO_List[i][CALLSIGN_POS].ljust(10, ' ') + QSO_List[i][GRIDSQUARE_POS].ljust(6, ' '))
        if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2") 
        else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3") 
    log_file_save()
    qso_listbox_dupe_check()
    
# Different sort function required for date/time sort of QSOs
def sort_qsos_by_date():  
    global QSO_List
    # Create list of QSOs
    update_qso_list()
    QSO_List.sort(key=lambda x:(x[DATE_POS], x[TIME_POS]), reverse=True )   
    for i in range(0,QSO_Listbox.size()):    
        QSO_Listbox.delete(i)
        QSO_Listbox.insert(i,QSO_List[i][DATE_POS].ljust(12, ' ') + QSO_List[i][TIME_POS].ljust(6, ' ') + QSO_List[i][BAND_POS].ljust(6, ' ')
                        + QSO_List[i][MODE_POS].ljust(4, ' ') + QSO_List[i][CALLSIGN_POS].ljust(10, ' ') + QSO_List[i][GRIDSQUARE_POS].ljust(6, ' '))
        if (i%2==0): QSO_Listbox.itemconfigure(i, bg = "lightcyan2") 
        else: QSO_Listbox.itemconfigure(i, bg = "lightcyan3")
    log_file_save()
    qso_listbox_dupe_check()

def update_qso_list():
    global QSO_List
    # Create list of QSOs
    QSO_List = []
    for i in range(0,QSO_Listbox.size()):    
        QSO_Line = QSO_Listbox.get(i).split(" ")
        while "" in QSO_Line: QSO_Line.remove("") # Removes empty strings from list
        QSO_List.append(QSO_Line)

def date_time_has_focus(event):
    global Stop_DateTime_Updates
    Stop_DateTime_Updates = True
    Date_Entry.configure(fg="black", bg="white")
    Time_Entry.configure(fg="black", bg="white")
        
# Define a function for the update thread
def update_datetime_and_misc():
    global Stop_DateTime_Updates
    # Update date and time in the QSO entry fields
    if not Stop_DateTime_Updates:
        Date_Entry_Val.set(datetime.datetime.utcnow().strftime('%Y-%m-%d'))
        Time_Entry_Val.set(datetime.datetime.utcnow().strftime('%H%M'))
    # Update QSO edit and delete buttons state (disabled if no QSO is selected in list, enabled otherwise)
    if (len(QSO_Listbox.curselection()) == 0):  # Checks if a line is selected
        Erase_QSO_Button['state'] = DISABLED
        Edit_QSO_Button['state'] = DISABLED
    else:
        Erase_QSO_Button['state'] = NORMAL
        Edit_QSO_Button['state'] = NORMAL
    QSO_Entry_Window.after(100, update_datetime_and_misc)

def grid_map_button_clicked():
    Grid_Map_Window.deiconify()
    if (int(Grid_Map_Window.geometry().split("x")[0]) == 1):  # catches when the grid map window has not been open yet. Size is 1x1
        Grid_Map_Window.geometry('{}x{}'.format(500,500))   # Sets a larger window size
    update_grid_boxes_no_event()

def hints_button_clicked():
    Hints_Window.deiconify()   # Show the splash window.
    x = round(int(QSO_List_Window.geometry().split("+")[1]) + int(re.split("[x+]",QSO_List_Window.geometry())[0])/2 - int(re.split("[x+]",Hints_Window.geometry())[0])/2)
    y = round(int(QSO_List_Window.geometry().split("+")[2]) + int(re.split("[x+]",QSO_List_Window.geometry())[1])/2 - int(re.split("[x+]",Hints_Window.geometry())[1])/2)
    Hints_Window.geometry("%dx%d+%d+%d" % (400,100,x,y))  # Place splash screen at center of screen

def cabrillo_file_button_clicked():
    global Contest_Number
    global Own_Callsign
    global Own_Gridsquare
    calculate_score(Contest_Number)
    if (Own_Callsign == "") or (Own_Gridsquare == ""):
        showerror("Error!","Cabrillo file Generation requires that you first configure the contest settings. Please fill out the Settings window first.")
        return
    cabrillo_file = Contest_File_Name.split(".")[0] + ".cablog"
    cabrillo_file = open(cabrillo_file,'w') # Open config file for rewriting
    cabrillo_file.write("START-OF-LOG: 3.0\n")
    cabrillo_file.write("LOCATION: \n")
    cabrillo_file.write("CALLSIGN: " + Own_Callsign + "\n")
    cabrillo_file.write("CATEGORY-ASSISTED: \n")
    cabrillo_file.write("CATEGORY-BAND: \n")
    cabrillo_file.write("CATEGORY-MODE: \n")
    cabrillo_file.write("CATEGORY-OPERATOR: \n")
    cabrillo_file.write("CATEGORY-POWER: \n")
    cabrillo_file.write("CATEGORY-STATION: \n")
    cabrillo_file.write("CATEGORY-TRANSMITTER: \n")
    cabrillo_file.write("NAME: \n")
    cabrillo_file.write("ADDRESS: \n")
    cabrillo_file.write("ADDRESS-CITY: \n")
    cabrillo_file.write("ADDRESS-STATE-PROVINCE: \n")
    cabrillo_file.write("ADDRESS-POSTALCODE: \n")
    cabrillo_file.write("ADDRESS-COUNTRY: \n")
    cabrillo_file.write("EMAIL: \n")
    for i in range(0,QSO_Listbox.size()):    
        QSO_Line = QSO_Listbox.get(i).split(" ")
        while "" in QSO_Line: QSO_Line.remove("") # Removes empty strings from list
        cabrillo_file.write("QSO: " + QSO_Line[BAND_POS] + " " + QSO_Line[MODE_POS]  + " " + QSO_Line[DATE_POS] + " "
                            + QSO_Line[TIME_POS] + " " + Own_Callsign.upper() + " " + Own_Gridsquare.upper() + " "
                            + QSO_Line[CALLSIGN_POS] + " "  + QSO_Line[GRIDSQUARE_POS] + "\n")
    cabrillo_file.write("END-OF-LOG:\n")
    cabrillo_file.close()
    showinfo("Cabrillo File Generation Complete","The Cabrillo file was saved as: \n" + cabrillo_file.name)


# Creates and opens the Settings window, and treats the settings capture
def settings_button_clicked():
    global Own_Callsign
    global Own_Gridsquare
    global Contest_Number
    global wsjt_1_logging_enabled
    global wsjt_2_logging_enabled
    global sock1
    global sock2
    global QSO_List

    
    #Converts the operator's grid square to uppercase. Also checks whether the 2-letter/2digits/2-letter grid square format is met
    def validate_setup_gridsquare(event):
        Own_Gridsquare_Entry_Val.set(Own_Gridsquare_Entry_Val.get().upper())
        if len(Own_Gridsquare_Entry_Val.get()) > 6: Own_Gridsquare_Entry_Val.set(Own_Gridsquare_Entry_Val.get()[:-1])
        GridSquare_Breakdown_List = list(Own_Gridsquare_Entry_Val.get())
        if (len(GridSquare_Breakdown_List) == 1):
            Own_Gridsquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0]))
        elif (len(GridSquare_Breakdown_List) == 2):
            Own_Gridsquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]))
        elif (len(GridSquare_Breakdown_List) == 3):
            Own_Gridsquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2]))
        elif (len(GridSquare_Breakdown_List) == 4):
            Own_Gridsquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2] + GridSquare_Breakdown_List[3]))
        elif (len(GridSquare_Breakdown_List) == 5):
            Own_Gridsquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2] + GridSquare_Breakdown_List[3]) + re.sub('[^A-X]', '', GridSquare_Breakdown_List[4]))
        elif (len(GridSquare_Breakdown_List) == 6):
            Own_Gridsquare_Entry_Val.set(re.sub('[^A-R]', '', GridSquare_Breakdown_List[0] + GridSquare_Breakdown_List[1]) + re.sub('[^0-9]', '', GridSquare_Breakdown_List[2] + GridSquare_Breakdown_List[3]) + re.sub('[^A-X]', '', GridSquare_Breakdown_List[4] + GridSquare_Breakdown_List[5]))

    def update_qso_font_size(self):
        QSO_Listbox.configure(font=("Consolas", Font_Size_Scale_Val.get(), "")) # Font_Size_Scale_Val.get()
        # The following workaround is required to refresh the listbox after the font size change.
        QSO_List_Window.geometry('{}x{}'.format(QSO_List_Window.winfo_width()+1, QSO_List_Window.winfo_height()))
        QSO_List_Window.update()
        QSO_List_Window.geometry('{}x{}'.format(QSO_List_Window.winfo_width()-1, QSO_List_Window.winfo_height()))
        QSO_List_Window.update()

    def validate_settings_info(event):
        global Own_Callsign 
        global Own_Gridsquare
        Own_Callsign = Own_Callsign_Entry_Val.get().upper()
        
    def validate_contest_combobox(event):
        global Contest_Number
        global QSO_List
        grid_has_4_chars = False
        Contest_Number = Contest_Select_Combo.current()
        for i in range(0,QSO_Listbox.size()):    
            if ((len(QSO_List[i][GRIDSQUARE_POS]) < 6) and (CONTEST_DIST[Contest_Number])): grid_has_4_chars = True
        if (grid_has_4_chars):
            showwarning(title='Contest Config Warning', message='Warning: The QSO list contains 4-character grid squares, but the selected contest calls for 6-character grid squares. Score calculation will be wrong!')
            Settings_Window.lift()
        qso_listbox_dupe_check()
        
    def settings_window_exit():
        global Own_Gridsquare
        global Contest_Number
        Own_Callsign = Own_Callsign_Entry_Val.get().upper()
        Own_Gridsquare = Own_Gridsquare_Entry_Val.get()
        if (Enable_WSJT_1_Logging_Checkbox_Val.get() == "checked"): wsjt_1_logging_enabled = True
        else: wsjt_1_logging_enabled = False
        if (Enable_WSJT_2_Logging_Checkbox_Val.get() == "checked"): wsjt_2_logging_enabled = True
        else: wsjt_2_logging_enabled = False       
        Settings_Window.withdraw()
        Settings_Window.grab_release()
        update_grid_boxes_no_event()
        Grid_Map_Window.update()
        qso_listbox_dupe_check()
        Update_QSO_List_Banner()

        
    def Validate_WSJT_1_Checkbox():
        global wsjt_1_logging_enabled
        if (Enable_WSJT_1_Logging_Checkbox_Val.get() == "checked"):
            wsjt_1_logging_enabled = True
            try:
                while sock1.recv(1024): pass  # Empty socket buffer
            except: pass
        else: wsjt_1_logging_enabled = False

    def Validate_WSJT_2_Checkbox():
        global wsjt_2_logging_enabled
        if (Enable_WSJT_2_Logging_Checkbox_Val.get() == "checked"):
            wsjt_2_logging_enabled = True
            try:
                while sock2.recv(1024): pass  # Empty socket buffer
            except: pass            
        else: wsjt_2_logging_enabled = False

    # Open dialog
    Settings_Window = Toplevel(QSO_List_Window)
    Settings_Window.title("VCL - Setup")     
    Settings_Window.geometry('{}x{}+{}+{}'.format(350,300,str(int(QSO_List_Window.geometry().split("+")[1])+100),str(int(QSO_List_Window.geometry().split("+")[2])+100)))
    Settings_Window.configure(bg = Default_BG_Color)
    Settings_Window.resizable(0, 0) # Makes Log entry window size fixed
    Settings_Window.iconphoto(True, PhotoImage(file = "./images/VCL_Icon_350x350.png"))  # Only accepts .PNG files
    Settings_Window.grab_set()
    Settings_Window.protocol('WM_DELETE_WINDOW',settings_window_exit) 

    Contest_Select_Label = Label(Settings_Window,text="Current Contest Type", bg = Default_BG_Color)
    Contest_Select_Label.place(x=10,y=10)
    Contest_Select_Label.pack()
    Contest_Select_Combo = ttk.Combobox(Settings_Window, justify='center', width = 40)
    Contest_Select_Combo['values'] = CONTESTS
    Contest_Select_Combo.bind('<<ComboboxSelected>>', validate_contest_combobox)
    Contest_Select_Combo['state'] = 'readonly'
    Contest_Select_Combo.pack()
    Contest_Select_Combo.current(Contest_Number)
    create_hint(Contest_Select_Combo,'A contest selection is required for score calculation and proper Grid Square handling. If 6-character GridSquares are required, then the "MicroWave Contest" entry must be selected')

    Callsign_Enter_Label = Label(Settings_Window,text="Your Call Sign", bg = Default_BG_Color)
    Callsign_Enter_Label.pack(pady = (8,0))

    Own_Callsign_Entry_Val = StringVar(Settings_Window)     
    if Own_Callsign != "": Own_Callsign_Entry_Val.set(Own_Callsign)
    Own_Callsign_Entry = Entry(Settings_Window, textvariable=Own_Callsign_Entry_Val)  
    Own_Callsign_Entry.bind("<KeyRelease>", validate_settings_info)
    Own_Callsign_Entry.configure(width=10)
    Own_Callsign_Entry.pack()
    create_hint(Own_Callsign_Entry,"Your callsign and gridsquare are required for Cabrillo file generation.")

    Gridsquare_Enter_Label = Label(Settings_Window,text="Your Grid Square", bg = Default_BG_Color)
    Gridsquare_Enter_Label.pack(pady = (8,0))

    Own_Gridsquare_Entry_Val = StringVar(Settings_Window)      
    if Own_Gridsquare != "": Own_Gridsquare_Entry_Val.set(Own_Gridsquare)
    Own_Gridsquare_Entry = Entry(Settings_Window, textvariable=Own_Gridsquare_Entry_Val)  
    Own_Gridsquare_Entry.bind("<KeyRelease>", validate_setup_gridsquare)
    Own_Gridsquare_Entry.configure(width=10)
    Own_Gridsquare_Entry.pack()
    create_hint(Own_Gridsquare_Entry,"Your callsign and gridsquare are required for Cabrillo file generation and location mapping. Entering a six-character gridsquare will give better location accuracy on the grid map.")

    Font_Size_Label = Label(Settings_Window,text="QSO List Font Size", bg = Default_BG_Color)
    Font_Size_Label.pack(pady = (8,0))
    Font_Size_Scale_Val = IntVar(Settings_Window)
    Font_Size_Scale = Scale(Settings_Window, from_=6, to=20, orient=HORIZONTAL, var = Font_Size_Scale_Val, command = update_qso_font_size, bg = Default_BG_Color, showvalue = 0)
    Font_Size_Scale.pack()
    Font_Size_Scale.set(QSO_Listbox.cget("font").split(" ")[1])
    create_hint(Font_Size_Scale,"This cursor adjusts the font size of the QSOs in the QSO list box.")

    Enable_WSJT_1_Logging_Checkbox_Val = StringVar(Settings_Window)
    Enable_WSJT_1_Logging_Checkbox = Checkbutton(Settings_Window, text='WSJT-X #1 Logging\n(UDP Port 2237)',variable=Enable_WSJT_1_Logging_Checkbox_Val, onvalue = "checked", offvalue = "unchecked", command=Validate_WSJT_1_Checkbox)
    if (wsjt_1_logging_enabled):
        Enable_WSJT_1_Logging_Checkbox_Val.set("checked")
#        if (sock1.fileno() == -1): sock1.bind((UDP_IP, UDP_PORT1))  # Closed socket, open it.
    else:
        Enable_WSJT_1_Logging_Checkbox_Val.set("unchecked")
    Enable_WSJT_1_Logging_Checkbox.pack(pady = (8,0))
    create_hint(Enable_WSJT_1_Logging_Checkbox,"This check box enables the logging of QSOs made the first instance of WSJT-X.")

    Enable_WSJT_2_Logging_Checkbox_Val = StringVar(Settings_Window)
    Enable_WSJT_2_Logging_Checkbox = Checkbutton(Settings_Window, text='WSJT-X #2 Logging\n(UDP Port 2239)',variable=Enable_WSJT_2_Logging_Checkbox_Val, onvalue = "checked", offvalue = "unchecked", command=Validate_WSJT_2_Checkbox)
    if (wsjt_2_logging_enabled):
        Enable_WSJT_2_Logging_Checkbox_Val.set("checked")
    else:
        Enable_WSJT_2_Logging_Checkbox_Val.set("unchecked")
    Enable_WSJT_2_Logging_Checkbox.pack(pady = (2,0))
    create_hint(Enable_WSJT_2_Logging_Checkbox,"This check box enables the logging of QSOs made the second instance of WSJT-X.")
    Settings_Window.update()

# Called when either the QSO Entry window or the QSO List window is closed. Signals the program exit.
def process_app_exit():
    global Contest_Number
    # Save all settings to the config file
    file = open("./config.sav",'w') # Open config file for reading
    file.write(Contest_File_Name + "\n")
    file.write(QSO_Entry_Window.geometry().split("+")[1] + "\n")
    file.write(QSO_Entry_Window.geometry().split("+")[2] + "\n")
    file.write(str(QSO_List_Window.geometry()) + "\n")
    file.write(str(Stats_Window_Geometry_X) + "\n")
    file.write(str(Stats_Window_Geometry_Y) + "\n")
    file.write(QSO_Listbox.cget("font").split(" ")[1]  + "\n")
    file.write(str(Contest_Number) + "\n")
    file.write(Own_Callsign + "\n")
    file.write(Own_Gridsquare + "\n")
    file.write(Grid_Map_Window.geometry() + "\n")
    file.write(str(Map_Canvas.xview()[0]) + "\n")
    file.write(str(Map_Canvas.yview()[0]) + "\n")
    file.write(Band1_Combo.get() + "\n")
    file.write(Band2_Combo.get() + "\n")
    file.write(Band3_Combo.get() + "\n")
    file.write(Band4_Combo.get() + "\n")
    file.write(str(Map_Scale_Factor) + "\n")
    file.write(str(wsjt_1_logging_enabled) + "\n")
    file.write(str(wsjt_2_logging_enabled) + "\n")
    file.close()
    # Close the remaining window
    try:    
        QSO_List_Window.destroy()
    except TclError:
        pass       
    try:
        QSO_Entry_Window.destroy()
    except TclError:
        pass
    
#Sends an existing QSO to the QSO entry window. This is used when working the same station on different bands.
def recall_qso_in_entry(event):
    if (QSO_Listbox.curselection()):  # Checks that one line is selected, otherwise gets triggered by deselection
        Callsign_Entry.configure(bg="white")
        GridSquare_Entry.configure(bg="white")
        Save_QSO_Button.configure(text = "Save as New QSO", fg = "dark green")        
        QSO_Line = QSO_Listbox.get(QSO_Listbox.curselection()).split(" ")
        while "" in QSO_Line: QSO_Line.remove("") # Removes empty strings from list
        Date_Entry_Val.set(QSO_Line[DATE_POS])
        Time_Entry_Val.set(QSO_Line[TIME_POS])
        Band_Combo_Val.set(QSO_Line[BAND_POS])
        Mode_Combo_Val.set(QSO_Line[MODE_POS])
        CallSign_Entry_Val.set(QSO_Line[CALLSIGN_POS])
        GridSquare_Entry_Val.set(QSO_Line[GRIDSQUARE_POS])

#Main window creation
QSO_List_Window = Tk()
QSO_List_Window.withdraw()
Default_BG_Color = QSO_List_Window.cget('bg')
QSO_List_Window.geometry('{}x{}'.format(485,486))
QSO_List_Window.configure(bg = Default_BG_Color)
QSO_List_Window.update()
QSO_List_Window.iconphoto(True, PhotoImage(file = "./images/VCL_Icon_350x350.png"))  # Only accepts .PNG files
QSO_List_Window.option_add('*Dialog.msg.font', 'Verdana 10') # Changes the default font for all standard dialogs

#Create the splash screen
Splash_Window = Toplevel(QSO_List_Window)
Splash_Window.withdraw()
Splash_Window.overrideredirect(True)  #Remove border of the splash Window
Splash_Window.grab_set()
Splash_Window_Frame = Frame(Splash_Window, bd=5, relief=RAISED)
Splash_Window_Frame.pack(side = BOTTOM, fill = BOTH, expand=True)
Splash_Window_Canvas = Canvas(Splash_Window_Frame, bd = 0, width=300, height=200)
BG_Image = PhotoImage(file = "./images/VCL_Icon_300x200_Darker.png")
Splash_Window_Canvas.Map_Image = Splash_Window_Canvas.create_image(0,0, anchor=NW, image=BG_Image)
Splash_Window_Canvas.pack(side=TOP,expand=True,fill=BOTH)
Splash_Window_Canvas.create_text(150,30,text = "VHF & Microwave",font="Verdana 15", fill="white")
Splash_Window_Canvas.create_text(150,50,text = "Contest Logger",font="Verdana 15", fill="white")
Splash_Window_Canvas.create_text(150,75,text = "Version " + SW_VERSION, font="Verdana 12", fill="white")
Splash_Window_Canvas.create_text(150,110,text = "By Bert - VE2ZAZ / VA2IW",font="Verdana 10", fill="white")
Splash_Window_Canvas.create_text(150,130,text = "Website: https://ve2zaz.net",font="Verdana 10", fill="white")
Splash_Window_Canvas.create_text(150,150,text = "Github: https://github.com/VE2ZAZ",font="Verdana 10", fill="white")
Splash_Window.update()
create_hint(Splash_Window,"To clear this popup window, just click on it.")

# Now populate main screen with the widgets

# First row of buttons contained inside this frame
button_frame1 = Frame(QSO_List_Window, relief=RAISED, borderwidth=1)
button_frame1.pack(fill=BOTH, expand=False)

Sort_By_Date_Button = Button(button_frame1, text = "↑Date/Time",command = sort_qsos_by_date, fg = "blue", font = "Verdana 8",bd = 2)
Sort_By_Date_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Sort_By_Date_Button,"Sorts the QSOs by the reversed time/date columns (newest on top).")

Sort_By_Band_Button = Button(button_frame1, text = "↓Band",command = lambda: sort_qsos(2), fg = "blue", font = "Verdana 8", bd = 2)
Sort_By_Band_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Sort_By_Band_Button,"Sorts the QSOs by alphabetical order of the radio band column.")

Sort_By_Mode_Button = Button(button_frame1, text = "↓Mode", command = lambda: sort_qsos(3), fg = "blue", font = "Verdana 8", bd = 2)
Sort_By_Mode_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Sort_By_Mode_Button,"Sorts the QSOs by alphabetical order of the mode (PH, CW, DIG,...) column.") 

Sort_By_Call_Button = Button(button_frame1, text = "↓Call Sign", command = lambda: sort_qsos(4), fg = "blue", font = "Verdana 8", bd = 2)
Sort_By_Call_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Sort_By_Call_Button,"Sorts the QSOs by alphabetical order of the call sign column.")

Sort_By_Grid_Button = Button(button_frame1, text = "↓Grid", command = lambda: sort_qsos(5), fg = "blue", font = "Verdana 8", bd = 2)
Sort_By_Grid_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Sort_By_Grid_Button,"Sorts the QSOs by alphabetical order of the grid square column.")

QSO_Listbox = Listbox(QSO_List_Window, width=46, height=15, selectmode="single")  
QSO_Listbox.pack(fill=BOTH, expand=True)
QSO_Listbox.configure(font=("Consolas",10 , ""))
QSO_Listbox_Yscrollbar = Scrollbar(QSO_Listbox,orient=VERTICAL)
QSO_Listbox_Yscrollbar.pack(side = RIGHT, fill = BOTH)
QSO_Listbox_Xscrollbar = Scrollbar(QSO_Listbox,orient=HORIZONTAL)
QSO_Listbox_Xscrollbar.pack(side = BOTTOM, fill = BOTH)
QSO_Listbox.configure(yscrollcommand = QSO_Listbox_Yscrollbar.set, xscrollcommand = QSO_Listbox_Xscrollbar.set)
QSO_Listbox_Yscrollbar.configure(command = QSO_Listbox.yview)
QSO_Listbox_Xscrollbar.configure(command = QSO_Listbox.xview)
QSO_Listbox.configure(selectbackground="dodger blue")
QSO_Listbox.configure(bg=Default_BG_Color)
QSO_Listbox.bind('<<ListboxSelect>>', recall_qso_in_entry)  #<ButtonPress-1>
create_hint(QSO_Listbox,"""The QSO List shows the QSOs that are saved in the logbook file. \n\nAny QSO displayed in red font flags a call_sign-band-grid duplicate of a previous QSO displayed in orange. \n\nAlso, clicking on a QSO """
                        """in the list will recall the information in the QSO capture window to save time in logging repeating stations on different bands.""")

# Add a label used when there are no log files loaded at startup, but do not pack it yet.
No_Log_Loaded_Label = Label(QSO_Listbox, text="Please open an existing log file\nor create a new log.", bg = Default_BG_Color,font="Verdana 12")

# Second row of buttons contained inside this frame
button_frame2 = Frame(QSO_List_Window, relief=RAISED, borderwidth=1)
button_frame2.pack(fill=BOTH, expand=False)

Stats_Button = Button(button_frame2, text = "Statistics", command = stats_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
Stats_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Stats_Button,"Brings up the logbook statistics window.")

Grid_Map_Button = Button(button_frame2, text = "Grid Map", command = grid_map_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
Grid_Map_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Grid_Map_Button,"Brings up the worked grid square map.")

Open_Contest_Button = Button(button_frame2, text = "Open Log", command = open_contest_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
Open_Contest_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Open_Contest_Button,"Opens an existing contest logbook file (.VHFlog extension)")

New_Contest_Button = Button(button_frame2, text = "New Log", command = new_contest_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
New_Contest_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(New_Contest_Button,"Clears the logbook list and allows to create a new logbook file. This does not erase any previously-opened logbook file contents")

Hints_Button = Button(button_frame2, text = "Help", command = hints_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
Hints_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Hints_Button,"Brings up the Help window to display additional information on each function or button.")

About_Button = Button(button_frame2, text = "About", command = about_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
About_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(About_Button,"Brings up the splash screen with program and author information. You can click on the splash screen to get rid of it.")

# Third row of buttons contained inside this frame
button_frame3 = Frame(QSO_List_Window, relief=RAISED, borderwidth=1)
button_frame3.pack(fill=BOTH, expand=False)

Settings_Button = Button(button_frame3, text = "Setup",command = settings_button_clicked, fg = "red", font = "Verdana 8",bd = 2)
Settings_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Settings_Button,"Brings up the setup window to configure various program settings.")

Edit_QSO_Button = Button(button_frame3, text = "Edit QSO", command = edit_qso_button_clicked, fg = "red", font = "Verdana 8", bd = 2)
Edit_QSO_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Edit_QSO_Button,"Sends the selected QSO to the QSO Capture window for entry correction.")

Erase_QSO_Button = Button(button_frame3, text = "Delete QSO", command = erase_qso_button_clicked, fg = "red", font = "Verdana 8", bd = 2)
Erase_QSO_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Erase_QSO_Button,"Deletes the selected QSO from the QSO list.")

Erase_Log_Button = Button(button_frame3, text = "Delete All QSOs", command = erase_log_button_clicked, fg = "red", font = "Verdana 8", bd = 2)
Erase_Log_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Erase_Log_Button,"Deletes ALL QSOs from the QSO list.")

Cabrillo_Button = Button(button_frame3, text = "Cabrillo File", command = cabrillo_file_button_clicked, fg = "red", font = "Verdana 8", bd = 2)
Cabrillo_Button.pack(side=LEFT,fill="x", expand=True)
create_hint(Cabrillo_Button,"Produces a Cabrillo-formatted file (.vhfcab) required to submit your contest results to the ARRL.")

# Create the QSO Entry window and populate it with widgets

QSO_Entry_Window = Toplevel(QSO_List_Window)
QSO_Entry_Window.title("VCL - QSO Capture")     
QSO_Entry_Window.geometry('{}x{}'.format(260,150))
QSO_Entry_Window.resizable(0, 0) # Makes Log entry window size fixed
QSO_Entry_Window.iconphoto(True, PhotoImage(file = "./images/VCL_Icon_350x350.png"))  # Only accepts .PNG files
first_element_offset = 12

# First row of widgets 
QSO_Upper_button_frame = Frame(QSO_Entry_Window, relief=RAISED, borderwidth=0, height=100, width=100, bg = Default_BG_Color)
QSO_Upper_button_frame.pack()

Date_Entry_Label = Label(QSO_Upper_button_frame,text="Date", bg = Default_BG_Color)
Date_Entry_Label.grid(row=0, column=0, padx=2)  
Date_Entry_Val = StringVar(QSO_Entry_Window)      
Date_Entry_Val.set(datetime.date.today())        
Date_Entry = Entry(QSO_Upper_button_frame, textvariable=Date_Entry_Val, bg=Default_BG_Color)  
Date_Entry.bind("<FocusIn>",date_time_has_focus)
Date_Entry.bind("<KeyRelease>", validate_date)
Date_Entry.configure(width=10)
Date_Entry.grid(row=1, column=0, padx=2)  
Date_Entry.configure(bg=Default_BG_Color, fg="gray44")
create_hint(Date_Entry,"QSO date entry: Automatically filled in with the current UTC date. When clicked on, allows to manually capture a different date.")

Time_Entry_Label = Label(QSO_Upper_button_frame,text="Time-UTC", bg = Default_BG_Color)
Time_Entry_Label.grid(row=0, column=1, padx=2,)  
Time_Entry_Val = StringVar(QSO_Entry_Window)     
Time_Entry_Val.set(datetime.datetime.utcnow().strftime('%H:%M'))          
Time_Entry = Entry(QSO_Upper_button_frame, textvariable=Time_Entry_Val, bg=Default_BG_Color)  
Time_Entry.bind("<FocusIn>",date_time_has_focus)
Time_Entry.bind("<KeyRelease>", validate_time)
Time_Entry.configure(width=10)
Time_Entry.grid(row=1, column=1, padx=2)    
Time_Entry.configure(bg=Default_BG_Color, fg="gray44")
create_hint(Time_Entry,"QSO time entry. Automatically filled in with the current UTC time. When clicked on, allows to manually capture a different time.")

Band_Combo_Label = Label(QSO_Upper_button_frame,text="Band", bg = Default_BG_Color)
Band_Combo_Label.grid(row=0, column=2, padx=2)  
Band_Combo_Val = StringVar(QSO_Entry_Window)     
Band_Combo = ttk.Combobox(QSO_Upper_button_frame, width = 6, textvariable=Band_Combo_Val)
Band_Combo.bind("<<ComboboxSelected>>", combobox_dupe_check)
Band_Combo['values'] = (CONTEST_BANDS)
Band_Combo['state'] = 'readonly'
Band_Combo.set("50")
Band_Combo.grid(row=1, column=2, padx=2)    
create_hint(Band_Combo,"Amateur frequency band used for the QSO. Actively checked for call_sign-Band-grid duplication against the QSO list.")

# Second row of widgets 
QSO_Lower_button_frame = Frame(QSO_Entry_Window, relief=RAISED, borderwidth=0, height=100, width=100, bg = Default_BG_Color)
QSO_Lower_button_frame.pack()

CallSign_Entry_Label = Label(QSO_Lower_button_frame,text="Call Sign", bg = Default_BG_Color)
CallSign_Entry_Label.grid(row=2, column=0, padx=2)  
CallSign_Entry_Val = StringVar(QSO_Lower_button_frame)     
CallSign_Entry_Val.set("")      
Callsign_Entry = Entry(QSO_Lower_button_frame, textvariable=CallSign_Entry_Val) 
Callsign_Entry.bind("<KeyRelease>", validate_callsign)
Callsign_Entry.bind("<Return>", save_qso_returnkey_pressed)
Callsign_Entry.configure(width=10)
Callsign_Entry.grid(row=3, column=0, padx=2)    
create_hint(Callsign_Entry,"Other station's callsign. Actively checked for callsign-Band-grid duplication against the QSO list.")

GridSquare_Entry_Label = Label(QSO_Lower_button_frame,text="Grid Square", bg = Default_BG_Color)
GridSquare_Entry_Label.grid(row=2, column=1)  
GridSquare_Entry_Val = StringVar(QSO_Lower_button_frame)   
GridSquare_Entry_Val.set("")        
GridSquare_Entry = Entry(QSO_Lower_button_frame, textvariable=GridSquare_Entry_Val) 
GridSquare_Entry.bind("<KeyRelease>", validate_gridsquare)
GridSquare_Entry.bind("<Return>", save_qso_returnkey_pressed)
GridSquare_Entry.configure(width=10)
GridSquare_Entry.grid(row=3, column=1, padx=2)    
create_hint(GridSquare_Entry,"Other station's Maidenhead grid square. Actively checked for callsign-Band-grid duplication against the QSO list.")

Mode_Combo_Label = Label(QSO_Lower_button_frame,text="Mode", bg = Default_BG_Color)
Mode_Combo_Label.grid(row=2, column=2, padx=2)  
Mode_Combo_Val = StringVar(QSO_Lower_button_frame)      
Mode_Combo = ttk.Combobox(QSO_Lower_button_frame, width = 6, textvariable=Mode_Combo_Val)
Mode_Combo['values'] = ('CW','PH','FM','RY','DG')
Mode_Combo['state'] = 'readonly'
Mode_Combo.set("PH")
Mode_Combo.grid(row=3, column=2, padx=2)    
create_hint(Mode_Combo,"Modulation mode used for the QSO. Provided in the Cabrillo file submitted to the ARRL.")

# Create a frame to contain the Save and Cancel buttons
QSO_Buttons_Frame = Frame(QSO_Entry_Window, relief=RAISED, borderwidth=0, height=100, width=100, bg = Default_BG_Color)
QSO_Buttons_Frame.pack()
Save_QSO_Button = Button(QSO_Buttons_Frame, text = "Save QSO", command = save_qso_button_clicked, fg = "dark green", font = "Verdana 8", bd = 2)
Save_QSO_Button.bind('<Return>', save_qso_returnkey_pressed)
Save_QSO_Button.grid(row=0, column=0, padx=2 , pady=5)    
create_hint(Save_QSO_Button,"Saves the QSO as captured in the entry fields. When editing a QSO, updates the QSO list with the entry fields information.")

Clear_QSO_Text_Button = Button(QSO_Buttons_Frame, text = "Cancel", command = clear_qso_text_button_clicked, fg = "red", font = "Verdana 8", bd = 2, height = 1)
Clear_QSO_Text_Button.bind('<Return>', clear_qso_returnkey_pressed)
Clear_QSO_Text_Button.grid(row=0, column=1, padx=2 , pady=5)    
create_hint(Clear_QSO_Text_Button,"Clears the information currently captured in the entry fields. Does not save or update the QSO.")

Dist_Text_Label = Label(QSO_Entry_Window, text="Latest QSO Distance (Km): 0", bg = Default_BG_Color )
Dist_Text_Label.pack()    

# Create the World Grid map window and populate it with some widgets

Grid_Map_Window = Toplevel(QSO_List_Window)
Grid_Map_Window.withdraw()
Grid_Map_Window.title("VCL - Worked Grid Squares Map")     
Grid_Map_Window.geometry('{}x{}'.format(500,500))
Grid_Map_Window.iconphoto(True, PhotoImage(file = "./images/VCL_Icon_350x350.png"))  # Only accepts .PNG files

# Create the canvas that will contain the world map and color rectangles
Map_Canvas = Canvas(Grid_Map_Window, bd = 0, width=8640, height=4320, scrollregion=(0,0,8640,4320))
Sby = Scrollbar(Map_Canvas,orient=VERTICAL)
Sby.pack(side = RIGHT, fill = Y)
Sbx = Scrollbar(Map_Canvas,orient=HORIZONTAL)
Sbx.pack(side = BOTTOM, fill = X)
Map_Canvas.config(yscrollcommand = Sby.set, xscrollcommand = Sbx.set)
Sbx.config(command=Map_Canvas.xview)
Sby.config(command=Map_Canvas.yview)
Map_Canvas.pack(side=TOP,expand=True,fill=BOTH)
create_hint(Map_Canvas,"""Shows the worked amateur radio bands for each Maidenhead grid square on a world map. Map centering can be changed by dragging map """
                        """(left-click and drag) or by using scroll bars.""")

Wait_For_Loading_Label = Label(Map_Canvas, text="Map is loading. Please wait...", bg = Default_BG_Color,font="Verdana 14")
Wait_For_Loading_Label.pack(expand=True, fill=None) 

# Draws a dot at the operator's location on the Worked Gridsquare map
def create_qth_dot(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill = "red",outline = "blue", tags='Distance_Azimuth')

# Updates the worked grid color boxes on the map
def update_grid_boxes(event):
    global QSO_List
    global Lat_Grid_Pitch
    global Long_Grid_Pitch
    global Map_Height
    global Map_Scale_Factor
    global Default_BG_Color
    global Distances_Checkbutton_Val
    global Own_Gridsquare_X
    global Own_Gridsquare_Y
    
    Map_Canvas.delete('Color_Boxes')
    # Band 1 color rectangles
    if (len(QSO_List) > 0):
        Grid_Character_List = []
        for i in range(0, len(QSO_List)):
            if QSO_List[i][BAND_POS] == Band1_Combo_Val.get():
                Grid_Character_List.append(list(QSO_List[i][GRIDSQUARE_POS][0:4]))
        for i in range(0, len(Grid_Character_List)):
            Coord_X = 10 * (ord(Grid_Character_List[i][0]) - 65) * Long_Grid_Pitch
            Coord_X = Coord_X + ((ord(Grid_Character_List[i][2]) - 48) * Long_Grid_Pitch)
            Coord_Y = Map_Height - (10 * (ord(Grid_Character_List[i][1]) - 65) * Lat_Grid_Pitch)
            Coord_Y = Coord_Y - ((ord(Grid_Character_List[i][3]) - 48) * Lat_Grid_Pitch)
            Map_Canvas.create_polygon([Coord_X+1,Coord_Y-1,Coord_X+Long_Grid_Pitch-1,Coord_Y-1,Coord_X+Long_Grid_Pitch-1,Coord_Y-Lat_Grid_Pitch+1,Coord_X+1,Coord_Y-Lat_Grid_Pitch+1],
                                      outline='orchid3', fill = '', width=3, tags='Color_Boxes')
            
        Grid_Character_List = []
        for i in range(0, len(QSO_List)):
            if QSO_List[i][BAND_POS] == Band2_Combo_Val.get():
                Grid_Character_List.append(list(QSO_List[i][GRIDSQUARE_POS][0:4]))
        for i in range(0, len(Grid_Character_List)):
            Coord_X = 10 * (ord(Grid_Character_List[i][0]) - 65) * Long_Grid_Pitch
            Coord_X = Coord_X + ((ord(Grid_Character_List[i][2]) - 48) * Long_Grid_Pitch)
            Coord_Y = Map_Height - (10 * (ord(Grid_Character_List[i][1]) - 65) * Lat_Grid_Pitch)
            Coord_Y = Coord_Y - ((ord(Grid_Character_List[i][3]) - 48) * Lat_Grid_Pitch)
            Map_Canvas.create_polygon([Coord_X+4,Coord_Y-4,Coord_X+Long_Grid_Pitch-4,Coord_Y-4,Coord_X+Long_Grid_Pitch-4,Coord_Y-Lat_Grid_Pitch+4,Coord_X+4,Coord_Y-Lat_Grid_Pitch+4],
                                      outline='springgreen3', fill = '', width=3, tags='Color_Boxes') #
            
        if (Map_Scale_Factor != 1): # 4th band is too much for scale=1
            Band3_frame.config(bg='orange',relief=RAISED)
            Band3_Combo.pack(side=LEFT,expand=False,fill=BOTH, padx=2, pady=2)
            Grid_Character_List = []
            for i in range(0, len(QSO_List)):
                if QSO_List[i][BAND_POS] == Band3_Combo_Val.get():
                    Grid_Character_List.append(list(QSO_List[i][GRIDSQUARE_POS][0:4]))
            for i in range(0, len(Grid_Character_List)):
                Coord_X = 10 * (ord(Grid_Character_List[i][0]) - 65) * Long_Grid_Pitch
                Coord_X = Coord_X + ((ord(Grid_Character_List[i][2]) - 48) * Long_Grid_Pitch)
                Coord_Y = Map_Height - (10 * (ord(Grid_Character_List[i][1]) - 65) * Lat_Grid_Pitch)
                Coord_Y = Coord_Y - ((ord(Grid_Character_List[i][3]) - 48) * Lat_Grid_Pitch)
                Map_Canvas.create_polygon([Coord_X+7,Coord_Y-7,Coord_X+Long_Grid_Pitch-7,Coord_Y-7,Coord_X+Long_Grid_Pitch-7,Coord_Y-Lat_Grid_Pitch+7,Coord_X+7,Coord_Y-Lat_Grid_Pitch+7],
                                          outline='orange', fill = '', width=3, tags='Color_Boxes') #
        else:
            Band3_Combo.pack_forget()
            Band3_frame.config(bg=Default_BG_Color,relief=FLAT)        

        if (Map_Scale_Factor == 2): # 4th band is too much for scale=1
            Band4_frame.config(bg='cyan',relief=RAISED)
            Band4_Combo.pack(side=LEFT,expand=False,fill=BOTH, padx=2, pady=2)
            Grid_Character_List = []
            for i in range(0, len(QSO_List)):
                if QSO_List[i][BAND_POS] == Band4_Combo_Val.get():
                    Grid_Character_List.append(list(QSO_List[i][GRIDSQUARE_POS][0:4]))
            for i in range(0, len(Grid_Character_List)):
                Coord_X = 10 * (ord(Grid_Character_List[i][0]) - 65) * Long_Grid_Pitch
                Coord_X = Coord_X + ((ord(Grid_Character_List[i][2]) - 48) * Long_Grid_Pitch)
                Coord_Y = Map_Height - (10 * (ord(Grid_Character_List[i][1]) - 65) * Lat_Grid_Pitch)
                Coord_Y = Coord_Y - ((ord(Grid_Character_List[i][3]) - 48) * Lat_Grid_Pitch)
                Map_Canvas.create_polygon([Coord_X+10,Coord_Y-10,Coord_X+Long_Grid_Pitch-10,Coord_Y-10,Coord_X+Long_Grid_Pitch-10,Coord_Y-Lat_Grid_Pitch+10,
                                           Coord_X+10,Coord_Y-Lat_Grid_Pitch+10],
                                          outline='cyan', fill = '', width=3, tags='Color_Boxes',stipple="gray50") #
        else:
            Band4_Combo.pack_forget()
            Band4_frame.config(bg=Default_BG_Color,relief=FLAT)
    if (Azimuth_Checkbutton_Val.get() == 1) or (Distances_Checkbutton_Val.get() == 1):
        create_qth_dot(Own_Gridsquare_X,Own_Gridsquare_Y,5,Map_Canvas)
    Grid_Map_Window.update()

# Is used to call the grid box updates when no event is passed.
def update_grid_boxes_no_event():
    update_grid_boxes("")


def draw_dist_and_az_lines():
    global Map_Height
    global Lat_Grid_Pitch
    global Long_Grid_Pitch
    global Own_Gridsquare_X
    global Own_Gridsquare_Y
    # Add the distance circles and azimuth lines
    Map_Canvas.delete('Distance_Azimuth')
    Own_Gridsquare_X = 10 * (ord(Own_Gridsquare[0]) - 65) * Long_Grid_Pitch
    Own_Gridsquare_X = Own_Gridsquare_X + ((ord(Own_Gridsquare[2]) - 48) * Long_Grid_Pitch)     
    if len(Own_Gridsquare) == 6: Own_Gridsquare_X = Own_Gridsquare_X + round((ord(Own_Gridsquare[4]) - 65) * Long_Grid_Pitch/24)
    else: Own_Gridsquare_X = Own_Gridsquare_X + 0.5 * Long_Grid_Pitch
    Own_Gridsquare_Y = Map_Height - (10 * (ord(Own_Gridsquare[1]) - 65) * Lat_Grid_Pitch)
    Own_Gridsquare_Y = Own_Gridsquare_Y - ((ord(Own_Gridsquare[3]) - 48) * Lat_Grid_Pitch) # - 0.5 * Lat_Grid_Pitch
    if len(Own_Gridsquare) == 6: Own_Gridsquare_Y = Own_Gridsquare_Y - round((ord(Own_Gridsquare[5]) - 65) * Lat_Grid_Pitch/24)
    else: Own_Gridsquare_Y = Own_Gridsquare_Y - 0.5 * Lat_Grid_Pitch
    lat_km_per_pixel = 180 * 111 / Map_Height  # 111 kilometers per degree of latitude
    if (Azimuth_Checkbutton_Val.get() == 1) or (Distances_Checkbutton_Val.get() == 1):
        Circle_Point_Pix_List = []  
        for j in range(0,11):  # The number of points by 500 km increments
            for i in range(0,120):  # 3 degree increments, so 120 points per circle
                (Circle_Point_Deg_Lon, Circle_Point_Deg_Lat) = gcc.point_given_start_and_bearing((-180 + 2*Own_Gridsquare_X/Long_Grid_Pitch, 90 - Own_Gridsquare_Y/Lat_Grid_Pitch), i*3 , j * 500 * 1000, unit='meters') # This unpacks the (long,lat) tuple                
                Circle_Point_Pix_List.append([round(Map_Height*2/2 + Circle_Point_Deg_Lon * Map_Height*2/360), round(Map_Height/2 - Circle_Point_Deg_Lat * Map_Height/180)])   # Draws a distance circle every 500 km
                if i in range(1,360) and (Distances_Checkbutton_Val.get() == 1):
                    Map_Canvas.create_line(Circle_Point_Pix_List[120*j+i-1][0], Circle_Point_Pix_List[120*j+i-1][1], Circle_Point_Pix_List[120*j+i][0], Circle_Point_Pix_List[120*j+i][1], fill="dark orange", width=1, dash=(5,5), tags='Distance_Azimuth')
                if (i in range(0,360,5)) and (j in range(1,11) and (Azimuth_Checkbutton_Val.get() == 1)):  # Draws an azimuth line every 15 degrees
                    Map_Canvas.create_line(Circle_Point_Pix_List[120*j+i-120][0], Circle_Point_Pix_List[120*j+i-120][1], Circle_Point_Pix_List[120*j+i][0], Circle_Point_Pix_List[120*j+i][1], fill="red", width=1, dash=(5,5), tags='Distance_Azimuth')
        # Now draw labels over the lines
        if (Distances_Checkbutton_Val.get() == 1):
            for j in (2,4,6,8,10):  
                for i in range(3,120,15):   
                    canvas_text = Map_Canvas.create_text(Circle_Point_Pix_List[120*j+i][0], Circle_Point_Pix_List[120*j+i][1], text=j*500, font = "Verdana 7", anchor="center", fill="dark orange", tags='Distance_Azimuth')
                    bgnd_box=Map_Canvas.create_rectangle(Map_Canvas.bbox(canvas_text),fill="white", outline="white", tags='Distance_Azimuth')
                    Map_Canvas.tag_lower(bgnd_box,canvas_text)
        if (Azimuth_Checkbutton_Val.get() == 1):
            for j in (2,4,6,8,10):  
                for i in range(0,120,10):   
                    canvas_text = Map_Canvas.create_text(Circle_Point_Pix_List[120*j+i][0] - (Circle_Point_Pix_List[120*j+i][0]-Circle_Point_Pix_List[120*(j-1)+i][0])/2, Circle_Point_Pix_List[120*j+i][1] - (Circle_Point_Pix_List[120*j+i][1]-Circle_Point_Pix_List[120*(j-1)+i][1])/2, text=i*3, font = "Verdana 7", anchor="center", fill="red", tags='Distance_Azimuth')
                    bgnd_box=Map_Canvas.create_rectangle(Map_Canvas.bbox(canvas_text),fill="white", outline="white", tags='Distance_Azimuth')
                    Map_Canvas.tag_lower(bgnd_box,canvas_text)
    if (Azimuth_Checkbutton_Val.get() == 1) or (Distances_Checkbutton_Val.get() == 1):
        create_qth_dot(Own_Gridsquare_X,Own_Gridsquare_Y,5,Map_Canvas)
    Grid_Map_Window.update()

# Now add the band color selection comboboxes to the World Grid map window

Bands_Tuple = ('None','50','70','144','222','432','902','1.2G','2.3G','3.4G','5.7G','10G','24G','47G','75G','122G','134G','241G','LIGHT')
Band1_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
Band1_frame.config(bg='orchid3') #magenta
Band1_frame.pack(side=LEFT, expand=False)
Band1_Combo_Val = StringVar(Band1_frame)     
Band1_Combo = ttk.Combobox(Band1_frame, width = 6, textvariable=Band1_Combo_Val)
Band1_Combo.bind("<<ComboboxSelected>>", update_grid_boxes)
Band1_Combo['values'] = Bands_Tuple
Band1_Combo['state'] = 'readonly'
Band1_Combo.set("BAND1")
Band1_Combo.pack(side=LEFT,expand=False,fill=BOTH, padx=2, pady=2)  #,expand=True,fill=BOTH
create_hint(Band1_Combo,"Allows to select which radio band to display with color #1.")

Band2_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
Band2_frame.config(bg='springgreen3')
Band2_frame.pack(side=LEFT, expand=False)
Band2_Combo_Val = StringVar(Band2_frame)     
Band2_Combo = ttk.Combobox(Band2_frame, width = 6, textvariable=Band2_Combo_Val)
Band2_Combo.bind("<<ComboboxSelected>>", update_grid_boxes)
Band2_Combo['values'] = Bands_Tuple
Band2_Combo['state'] = 'readonly'
Band2_Combo.set("BAND2")
Band2_Combo.pack(side=LEFT,expand=False,fill=BOTH, padx=2, pady=2)  #,expand=True,fill=BOTH
create_hint(Band2_Combo,"Allows to select which radio band to display with color #2.")

Band3_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
Band3_frame.config(bg='orange')
Band3_frame.pack(side=LEFT, expand=False)
Band3_Combo_Val = StringVar(Band3_frame)     
Band3_Combo = ttk.Combobox(Band3_frame, width = 6, textvariable=Band3_Combo_Val)
Band3_Combo.bind("<<ComboboxSelected>>", update_grid_boxes)
Band3_Combo['values'] = Bands_Tuple
Band3_Combo['state'] = 'readonly'
Band3_Combo.set("BAND3")
Band3_Combo.pack(side=LEFT,expand=False,fill=BOTH, padx=2, pady=2)  #,expand=True,fill=BOTH
create_hint(Band3_Combo,"Allows to select which radio band to display with color #3.")

Band4_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
Band4_frame.config(bg='cyan')
Band4_frame.pack(side=LEFT, expand=False)
Band4_Combo_Val = StringVar(Band4_frame)     
Band4_Combo = ttk.Combobox(Band4_frame, width = 6, textvariable=Band4_Combo_Val)
Band4_Combo.bind("<<ComboboxSelected>>", update_grid_boxes)
Band4_Combo['values'] = Bands_Tuple
Band4_Combo['state'] = 'readonly'
Band4_Combo.set("BAND4")
Band4_Combo.pack(side=LEFT,expand=False,fill=BOTH, padx=2, pady=2)  #,expand=True,fill=BOTH
create_hint(Band4_Combo,"Allows to select which radio band to display with color #4.")

# Creating the frame and the zoom combobox in the World Grid map window
World_Scale_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
World_Scale_frame.pack(side=LEFT, expand=False)
World_Scale_Label = Label(World_Scale_frame, text="Zoom:", bg = Default_BG_Color)
create_hint(World_Scale_Label,"Allows to select which scale factor (x1, x1.5 and x2) to use for displaying the world map. A new scale selection may take a moment to take effect.")
World_Scale_Combo_Val = StringVar(World_Scale_frame)     
World_Scale_Combo = ttk.Combobox(World_Scale_frame, width = 3, textvariable=World_Scale_Combo_Val)
World_Scale_Combo['values'] = ('1','1.5','2')
World_Scale_Combo['state'] = 'readonly'
World_Scale_Combo.set("1")
World_Scale_Combo.pack(side=RIGHT,expand=False,fill=BOTH, padx=4, pady=2)  #,expand=True,fill=BOTH
World_Scale_Label.pack(side=RIGHT,expand=False,fill=BOTH, padx=3, pady=2)
create_hint(World_Scale_Combo,"Allows to select which scale factor (x1, x1.5 and x2) to use for displaying the world map. A new scale selection may take a moment to take effect.")

#Creating the "Display Distance circles" checkmark
Distances_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
Distances_frame.pack(side=LEFT, expand=False)
Distances_Checkbutton_Val = IntVar(Distances_frame)
Distances_Checkbutton = Checkbutton(Distances_frame, text='Distances (Km)',variable=Distances_Checkbutton_Val, onvalue=1, offvalue=0, command=draw_dist_and_az_lines)
Distances_Checkbutton.pack(side=RIGHT,expand=False,fill=BOTH, padx=7, pady=2)
create_hint(Distances_Checkbutton,"Displays distance circles centered on your station location in increments of 500 kilometers")

#Creating the "Azimuth Lines" checkmark
Azimuth_frame = Frame(Grid_Map_Window, relief=RAISED, borderwidth=1)
Azimuth_frame.pack(side=LEFT, expand=False)
Azimuth_Checkbutton_Val  = IntVar(Azimuth_frame)
Azimuth_Checkbutton = Checkbutton(Azimuth_frame, text='Azimuths',variable=Azimuth_Checkbutton_Val, onvalue=1, offvalue=0, command=draw_dist_and_az_lines)
Azimuth_Checkbutton.pack(side=RIGHT,expand=False,fill=BOTH, padx=7, pady=2)
create_hint(Azimuth_Checkbutton,"Displays azimuth lines centered on your station location in increments of 15 degrees")
        
# (Re)draws the World Grid map and restores the center map position to the same position after scaling
def draw_map(event):
    global Lat_Grid_Pitch
    global Long_Grid_Pitch
    global X1_MAP_HEIGHT
    global X1_MAP_WIDTH
    global Map_Scale_Factor
    global Map_Height
    global World_Filename   # This is required otherwisew the map will not display
    global Own_Gridsquare

    Wait_For_Loading_Label.pack(expand=True, fill=None)
    # Save where the map is centered before changing the scale factor
    Old_Map_Scale_Factor = Map_Scale_Factor
    Old_Scrollbar_X = Map_Canvas.xview()[0]
    Old_Scrollbar_Y = Map_Canvas.yview()[0]
    Map_Scale_Factor = float(World_Scale_Combo.get()) # This is the new scaling factor
    Map_Width = X1_MAP_WIDTH * Map_Scale_Factor  # This is the correct sizes for the scaling factor
    Map_Height = X1_MAP_HEIGHT * Map_Scale_Factor
    Lat_Grid_Pitch = Map_Height / 180             # The correct grid pitch for the scaling factor
    Long_Grid_Pitch = Map_Width / 180
    Y_Offset = Map_Scale_Factor * 2   # Offset needed to correct color boxes centering vs. world map grids.
    Map_Canvas.delete("all")    # Erase everything on the canvas
    # Required maps is of equirectangular projection. Current map produced at https://www.simplemappr.net, and then touched up and scaled
    Grid_Map_Window.update()
    if (Map_Scale_Factor == 1): World_Filename = PhotoImage(file = "./images/WorldMap_5760x2880_Grid_Labels.gif")
    elif (Map_Scale_Factor == 2): World_Filename = PhotoImage(file = "./images/WorldMap_11520x5760_Grid_Labels.gif")
    else: World_Filename = PhotoImage(file = "./images/WorldMap_8640x4320_Grid_Labels.gif")
    Map_Canvas.Map_Image = Map_Canvas.create_image(0,-Y_Offset, anchor=NW, image=World_Filename)
    Map_Canvas.config(width=Map_Width, height=Map_Height, scrollregion=(0,0,Map_Width,Map_Height))
    # Calculate the scrollbars' new positions. This will keep the point in the center of the map in that position after the zoom
    if (Map_Scale_Factor / Old_Map_Scale_Factor > 1):  # for zoom in action
        Map_Canvas.xview_moveto(Old_Scrollbar_X + 0.5 * int(re.split("[x+]",Grid_Map_Window.geometry())[0]) / Map_Width * (Map_Scale_Factor / Old_Map_Scale_Factor - 1)) 
        Map_Canvas.yview_moveto(Old_Scrollbar_Y + 0.5 * int(re.split("[x+]",Grid_Map_Window.geometry())[1]) / Map_Height * (Map_Scale_Factor / Old_Map_Scale_Factor - 1)) 
    else:  # for zoom out action
        Map_Canvas.xview_moveto(Old_Scrollbar_X - 0.5 * int(re.split("[x+]",Grid_Map_Window.geometry())[0]) / Map_Width * (1 - Map_Scale_Factor / Old_Map_Scale_Factor)) #* (Map_Scale_Factor / Old_Map_Scale_Factor) 
        Map_Canvas.yview_moveto(Old_Scrollbar_Y - 0.5 * int(re.split("[x+]",Grid_Map_Window.geometry())[1]) / Map_Height * (1 - Map_Scale_Factor / Old_Map_Scale_Factor)) #* (Map_Scale_Factor / Old_Map_Scale_Factor)
    draw_dist_and_az_lines()
    update_grid_boxes_no_event()
    Wait_For_Loading_Label.pack_forget()
    Grid_Map_Window.update()

# Define the canvas translation action of a mouse button-1 move on the map
def scroll_start(event):
    Map_Canvas.scan_mark(event.x, event.y)

def map_mouse_move(event):
    Map_Canvas.scan_dragto(event.x, event.y, gain=1)

World_Scale_Combo.bind("<<ComboboxSelected>>", draw_map)    # Attach map scale combobox change actions to a map re-draw

# Attach the mouse click and move actions to a canvas translation
Map_Canvas.bind("<ButtonPress-1>", scroll_start)
Map_Canvas.bind("<B1-Motion>", map_mouse_move)

# Treats the Grid map exit.
def grid_map_window_exit():
    Grid_Map_Window.withdraw()
    
# Hints window creation.
Hints_Window = Toplevel(QSO_List_Window)
Hints_Window.withdraw()
Hints_Window.title("VCL - Help")    
Hints_Window.configure(bg = Default_BG_Color)
Hints_Window.iconphoto(True, PhotoImage(file = "./images/VCL_Icon_350x350.png"))  # Only accepts .PNG files
Hint_Text_Box = ScrolledText(Hints_Window, height=12, width=40, wrap=WORD, bg = Default_BG_Color)
Hint_Text_Box.pack(fill=BOTH, expand=True)
Hint_Text_Box.insert(END, "Hover the mouse pointer over the various elements of the program to get a hints of their function")
Hint_Text_Box.config(state='disabled')

# Load saved settings from config file at startup and apply them to the various widgets.
try:
    file = open("./config.sav",'r') # Open config file for reading
    Contest_File_Name = file.readline()[:-1]
    QSO_Entry_Window.geometry('{}x{}+{}+{}'.format(260,150,
                            int(file.readline()[:-1]),
                            int(file.readline()[:-1])))
    QSO_List_Window.geometry(file.readline()[:-1])
    Stats_Window_Geometry_X = int(file.readline()[:-1])
    Stats_Window_Geometry_Y = int(file.readline()[:-1])    
    QSO_Listbox.configure(font=("Consolas",file.readline()[:-1] , "")) 
    Contest_Number = int(file.readline()[:-1])
    Own_Callsign = file.readline()[:-1]
    Own_Gridsquare = file.readline()[:-1]
    Grid_Map_Window.geometry(file.readline()[:-1])
    Map_Canvas.xview_moveto(file.readline()[:-1])
    Map_Canvas.yview_moveto(file.readline()[:-1])
    Band1_Combo.set(file.readline()[:-1])
    Band2_Combo.set(file.readline()[:-1])
    Band3_Combo.set(file.readline()[:-1])
    Band4_Combo.set(file.readline()[:-1])
    Map_Scale_Factor = float(file.readline()[:-1])
    if (file.readline()[:-1] == 'True'): wsjt_1_logging_enabled = True
    else: wsjt_1_logging_enabled = False
    if (file.readline()[:-1] == 'True'): wsjt_2_logging_enabled = True
    else: wsjt_2_logging_enabled = False
    file.close()
    log_file_load()
    World_Scale_Combo_Val.set(Map_Scale_Factor)    
except IOError:     # Loading defaults
    showerror("Error: No Config found", "Error, no configuration file was found. Reverting to defaults")
    Contest_File_Name = "No Log loaded..."
    QSO_List_Window.geometry("+100+200")
    QSO_Entry_Window.geometry("+100+20")
    Grid_Map_Window.geometry("500x500+300+300")
    No_Log_Loaded_Label.pack(expand=True, fill=None) # This makes the label appear
    QSO_List_Window.title("VCL - No Log Loaded")
    Contest_Number = 0
    Own_Callsign = "NoCall"
    Own_Gridsquare = "FN00"
    
# Manage the window exits
QSO_List_Window.protocol('WM_DELETE_WINDOW', process_app_exit)
QSO_Entry_Window.protocol('WM_DELETE_WINDOW', process_app_exit)
Grid_Map_Window.protocol('WM_DELETE_WINDOW', grid_map_window_exit)
Hints_Window.protocol('WM_DELETE_WINDOW',lambda: Hints_Window.withdraw()) 

QSO_Entry_Window.after(100, update_datetime_and_misc)  # Initially calls the date and time function as a separate thread   

QSO_List_Window.deiconify()  # Show the QSO list window

QSO_Listbox.bind("<Delete>", erase_qso_event) # Attaches the delete key press to a QSO delete action.

# Display the splash screen centered on the list window at startup
x = round(int(QSO_List_Window.geometry().split("+")[1]) + int(re.split("[x+]",QSO_List_Window.geometry())[0])/2 - 150)
y = round(int(QSO_List_Window.geometry().split("+")[2]) + int(re.split("[x+]",QSO_List_Window.geometry())[1])/2 - 100)
Splash_Window.geometry("%dx%d+%d+%d" % (300,200,x,y))  # Place splash screen at center of screen
Splash_Window.deiconify()   # Show the splash window.

# Now update everything based on the loaded contest logbook.
update_qso_list()
draw_map(None)
update_grid_boxes_no_event()
Grid_Map_Window.update()
qso_listbox_dupe_check()
Splash_Window.withdraw()   # Hide the splash window.
Splash_Window.grab_release()
Callsign_Entry.focus_set()  # Send the focus to the QSO entry window.

# Define and bind UDP sockets whether the UDP monitoring is enabled or not.
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Internet and UDP
sock1.settimeout(0.1)
sock1.bind((UDP_IP, UDP_PORT1))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Internet and UDP
sock2.settimeout(0.1)
sock2.bind((UDP_IP, UDP_PORT2))
QSO_Entry_Window.after(100, check_and_save_qso_from_wsjt_thread)  # Launch the WSJT-X UDP monitoring thread

# Loop the main window
QSO_Entry_Window.mainloop()

# E_N_D__O_F__P_R_O_G_R_A_M__C_O_D_E
