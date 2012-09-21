dvb-t_scanner
=============

Scans DVB-T channels in order to find the available stations for a specific location

Usage: ./scan_channels.py -l <location>

Uses scan utility from http://www.linuxtv.org/wiki/index.php/LinuxTV_dvb-apps
The script creates a text file
 channels-<location>.conf
which can be opened with VLC, for example, to watch the available DVB-T channels.
It creates also an intermediate text file
 raw_channels-<location>.txt
with all channels to be scanned. This file can be used later to redo the scan with the command
 scan raw_channels-<location>.txt

