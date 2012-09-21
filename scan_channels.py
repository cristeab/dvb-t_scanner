#!/usr/bin/env python

#Brief: Scans DVB-T channels in order to find the available stations for a specific location
#Author: Bogdan Cristea

#Uses 'scan' utility which must be in the system path. The scan utility receives as input a text file,
#so that on each line a DVB-T channel is defined.
#Each DVB-T channel is defined by the following parameters:
#T 474166000 8MHz 2/3 NONE QAM64 8k 1/32 NONE
#The output represents the detected DVB-T stations and can be used as input to VLC, for example.

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

#generate channels
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

#count the number of lines (number of channels found)
fd.seek(0)
nb_ch = 0
for line in fd:
  nb_ch = nb_ch+1
fd.close()

#show summary
print('*'*40)
print("Scanned DVB-T channels from "+str(ch_min)+" to "+str(ch_max))
print("Carrier frequency offset "+str(freq_offset_kHz)+" kHz")
print("Found "+str(nb_ch)+" channels")
print('*'*40)
