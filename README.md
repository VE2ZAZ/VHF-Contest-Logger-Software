# VHF & Microwave Contest Logger Software
### Version 1.5
### By Bert, VE2ZAZ / VA2IW (https://ve2zaz.net)

![The VHF & Microwave Contest Logger software windows](/images/All_Windows.png "The VHF & Microwave Contest Logger software windows")

This amateur radio software provides the ability to log and display the QSOs (radio contacts) made during one of the ARRL VHF, NA VHF Sprints or various NA Microwave contests. It offers a simple and efficient interface customized for these contests. The interface is distributed over several independent windows, which allows the user to better organize the desktop. The software performs continuous "dupe checks" and score calculation. It also displays the worked grid squares using color boxes on a zoom-able Maidenhead grid world map. Both 4-character and 6-character grid square logging is supported. Digital QSOs made on the WSJT-X software can be automatically logged. To save the contest information, the script uses a simple CSV (comma-separated text) file; no complex database is used. Since this software is a python script, it can be run on Linux, Windows and Mac, once the python-3 interpreter is installed. Another benefit of being a Python script is that it uses a simple text file as source code. It can thus be easily improved and customized by the user. Though it is customized for VHF and Microwave contesting, this software can also be used for general logging of VHF/UHF contacts. 

# Detailed Description
Please see the [Help.pdf](./Help.pdf) file for all the details on this software package, the installation procedure and  for some additional screenshots of the software windows.

# Release History
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
