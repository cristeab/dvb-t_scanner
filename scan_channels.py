#!/usr/bin/env python

# Brief: Scans DVB-T channels in order to find the available stations for a specific location
# Author: Bogdan Cristea

# Usage: ./scan_channels.py -l <location>

# Uses scan utility (http://www.linuxtv.org/wiki/index.php/LinuxTV_dvb-apps) which must be
# installed in your system path (most Linux distribution package already this utility).
# The script creates a text file
#  channels-<location>.conf
# which can be opened with VLC, for example, to watch the available DVB-T channels.
# It creates also an intermediate text file
#  raw_channels-<location>.txt
# with all channels to be scanned. This file can be used later to redo the scan with the command
#  scan raw_channels-<location>.txt
# Each line in the intermediate file represents a DVB-T channel to scan and has the format
# T 474166000 8MHz 2/3 NONE QAM64 8k 1/32 NONE
#
# ------------------------------------------------------------------------------------------
#
# Copyright (C) 2012 Bogdan Cristea
#
# You can redistribute and/or modify this script under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This script is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details (<http://www.gnu.org/licenses/>).
#
# ------------------------------------------------------------------------------------------

from optparse import OptionParser
from subprocess import Popen, PIPE
from sys import exit
from sys import stdout

#set input options
parser = OptionParser()
parser.add_option("-m", "--channel-min", dest="ch_min",
    help="DVB-T channel minimum index (default 21)",
    default=21)
parser.add_option("-M", "--channel-max", dest="ch_max",
    help="DVB-T channel maximum index (default 69)",
    default=69)
parser.add_option("-l", "--location", dest="location", 
    help="location (town, address, etc.) where the scan is realized (default empty string)",
    default="")
parser.add_option("-o", "--freq-offset-index", dest="freq_offset_idx", 
    help="DVB-T channel carrier frequency offset index (default 2)",
    default=2)
(options, args) = parser.parse_args()

#scan parameters
ch_min = int(options.ch_min) # default 21
ch_max = int(options.ch_max) # default 69
idx = int(options.freq_offset_idx) # doesn't need to be changed (default 2)
#constants
freq_offset_set_kHz = (-166, 0, 166, 332, 498)
fec_up = (2, 3)
fec_low = (3, 4)
guard_up = (1, 1)
guard_low = (32, 8)

#check inputs
if not(idx in range(0, len(freq_offset_set_kHz))):
  print("Carrier frequency offset index is out of range (min 0, max "+str(len(freq_offset_set_kHz)-1)+")")
  exit(1)
if 0 > ch_min or 0 > ch_max or ch_min > ch_max:
  print("Channel indices are wrong. Both should be positive integers and CH_MIN <= CH_MAX")
  exit(1)

#carrier frequency offset
freq_offset_kHz = freq_offset_set_kHz[idx]

#generate raw channels
raw_channels_file_name = "raw_channels-"+options.location+".txt"
fd = open(raw_channels_file_name, "w")
for idx2 in range(0, len(fec_up)):
    for ch_no in range(ch_min, ch_max+1):
        freq_MHz = 8*ch_no+306
        fd.write("T "+str(int(freq_MHz*1e6+freq_offset_kHz*1e3))+" 8MHz "+\
        str(fec_up[idx2])+"/"+str(fec_low[idx2])+" NONE QAM64 8k "+\
        str(guard_up[idx2])+"/"+str(guard_low[idx2])+" NONE\n")
fd.close()

#scan channels
fd = open("channels-"+options.location+".conf", "w+")
#call(["scan", "-q", raw_channels_file_name], stdout=fd)
proc = Popen(["scan", "-q", raw_channels_file_name], stdout=fd, stderr=PIPE)

#display progress
total_lines = 2*len(fec_up)*(ch_max-ch_min+1)
line_nb = 0
for line in iter(proc.stderr.readline,''):
  if "tune to:" in line:
    line_nb = line_nb+1
    progress = 100*line_nb/total_lines
    stdout.write("\r[{0}] {1}%".format('#'*(progress/5), progress))
stdout.write('\n')

#get the list of found channels
fd.seek(0)
ch_list = []
for line in fd:
  ch_list.append(line.split(':')[0])
fd.close()

#show summary
print('*'*40)
print("Scanned DVB-T channels from "+str(ch_min)+" to "+str(ch_max))
print("Carrier frequency offset "+str(freq_offset_kHz)+" kHz")
print("Found "+str(len(ch_list))+" channels")
for i in range(0, len(ch_list)):
  print("#"+str(i+1)+"\t"+ch_list[i])
print('*'*40)
