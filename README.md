# VHF & Microwave Contest Logger Software
### Version 1.6 (June 2025)
### By Bert, VE2ZAZ / VA2IW (https://ve2zaz.net)

![The VHF & Microwave Contest Logger software windows](/images/All_Windows_1.6.png "The VHF & Microwave Contest Logger software windows")

This amateur radio software provides the ability to log and display the QSOs (radio contacts) made during one of the ARRL VHF, NA VHF Sprints, CQ VHF or various NA Microwave contests. Rover operation is also supported. It offers a simple and efficient interface customized for these contests. The interface is distributed over several independent windows, which allows the user to better organize the desktop. The software performs continuous "dupe checks" and score calculation. It also displays the worked grid squares using color boxes and the worked stations on a zoom-able Maidenhead grid world map. Both 4-character and 6-character grid square logging is supported. Digital QSOs made on the WSJT-X software can be automatically logged. To save the contest information, the script uses a simple CSV (comma-separated text) file; no complex database is used. A Cabrillo-formatted file is produced to export the contest activity. Since this software is a python script, it can be run on Linux, Windows and Mac, once the python-3 interpreter is installed. Another benefit of being a Python script is that it uses a simple text file as source code. It can thus be easily improved and customized by the user. Though it is customized for VHF and Microwave contesting, this software can also be used for general logging of VHF/UHF contacts. 

# Detailed Description
Please see the [Help.pdf](./Help.pdf) file for all the details on this software package, the installation procedure and  for some additional screenshots of the software windows.

# Release History
### Version 1.62 (September 2025):
- Corrected distance calculation between two grids for WSJT-X QSOs, when grids are of 4-character type.
### Version 1.61 (August 2025):
- Corrected misbehavior of logging a WSJT-X QSO. Logging a digital QSO would not include the distance between the two grid squares. This had the consequence of erasing the logbook file. It also caused grid square map misbehavior.
- For digital QSOs, both "DG" and "DIG" were used for the mode. Only "DG" is allowed in Cabrillo. Corrected.
- Corrected a score calculation error for the distance-based contests.
### Version 1.6 (June 2025):
- Added the CQ World Wide VHF Contests (both analog and digital). Made the ARRL June and September VHF Contests separate choices.
- Added support for Rovers contesting in more than one grid.
  - The operator's own gridsquare is now saved in QSO data and is listed in the QSO list.
  - Duplicates and scoring are processed accordingly.
  - A sort by operator gridsquare button is also added. 
- Stats window: Added number of activated grids (for rovers) and corrected total distance to exclude dupes.
- Added a QSO distance column in the QSO list, and added a distance sorting button in the header.
- Removed the 70 MHz band, which is not a valid band for any of the North American VHF contests.
- Added the contest name in the Cabrillo file. Value filled in based on selected contest.
- Added separate criteria checks for dupe QSOs in ARRL 10GHz+ contest: greater than 16 km position change of either station, otherwise it is a dupe.
- In QSO Capture window:
  - Band and Mode pulldown menus now get populated with appropriate choices based on contest selection.
  - Added bearing and distance information when a valid 4 or 6-character grid square is entered.
  - Improved gridsquare format checks in both 4-character and 6-character checks.
  - Added descriptive error and warning messages when a dupe QSO is found or when the grid square format is not met.
  - Added spacebar jump between the Call Sign Entry and Gridsquare Entry fields and vice versa.
  - Escape key now clears QSO data (same as clicking on Cancel button)
- Setup window: Improved format checks on the gridsquare, with enforcing of 6-character operator grid square entry when the selected contest required it.
- Gridsquare Map Window:
  - Brought all controls inside a popup window that show up when right clicking on map.
  - Added worked station position markers (diamonds) and callsigns. Callsign backgrounds use assigned band colors. Can be enabled/disabled with a checkmark.
### Version 1.5 (October 2023):
- Added support for several North-American microwave contests and the VHF/UHF Sprints.
- Added support for 6-character grid squares by selecting the proper contest description in the Setup window.
- The Statistics window now shows the total distance of all QSOs. Used in microwave contest score calculation.
- The Statistics window now shows the total distance multiplied by the Band factors of all QSOs. Used for the 222 MHz and Up Contest score calculation.
- Added the display of the latest QSO distance in kilometers at the bottom of the QSO Entry window.
- The QSO List banner now shows the Contest description along with the Logbook file name.
- Changed validation of grid square syntax. Now restricted to <A-R><A-R><0-9><0-9><A-X><A-X>. Follows allowed ranges.
- Now accepts call signs of up to 10 characters to allow special call sign stations.
- Renamed the software to "VCL - VHF & Microwave Contest Logger Software".
- Updated Splash screen information.
### Version 1.4 (October 2023):
- Added the logging of WSJT-X QSOs via local UDP ports 2237 and 2239. Two WSJT-X sessions can run concurrently, one per UDP port. Can be enabled in the Setup window. Settings are saved in config file.
- Added the default station values when there is no config.sav file available in the directory. Would crash at launch otherwise.
- Duplicated QSOs "Dupes": Corrected the score calculation algorithm to reject duplicate QSOs. A new stat of Dupes is displayed.
- Duplicated QSOs "Dupes": The QSO list now shows any subsequent dupe QSOs in red. The first QSO (valid) is shown in orange.
- Updated Splash screen information
### Version 1.3 (January 2023):
- Corrected the score calculation algorithm to accurately take into account the January VHF contest.
- Updated Splash screen information
### Version 1.2 (January 2023):
- Added "import sys", which was not needed on the author's computer in order to work. It should have been there...
### Version 1.1 (September 2021):
- In the QSO Capture window, corrected the date value to update based on UTC time, not on local time.
- In the Grid Map window, added Distance Circle and Azimuth Line display options, along with associated checkboxes.
- In the setup menu: 
-- Now converts operator's call sign and grid square to uppercase.
-- Now supports the operator's gridsquare in 6-character format, allowing for better location accuracy on the gridsquare map.
-- Now checks the operator's gridsquare for proper format (2-chars/2-digits/2-chars).
### Version 1.0 (July 2021):
- Initial release.    

# Legal Notice
This software, along with all accompanying files and scripts, is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>. When modifying the software, a mention of the original author, namely Bert-VE2ZAZ, would be a gracious consideration.

Note: This text is extracted from the "Help.pdf" file provided with this software.
