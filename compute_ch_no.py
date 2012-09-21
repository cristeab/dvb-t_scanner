#!/usr/bin/env python

#T 474166000 8MHz 2/3 NONE QAM64 8k 1/32 NONE

ch_min = 21
ch_max = 69
freq_shift_kHz = (-166, 166, 332, 498)
idx = 1 #doesn't need to be changed 
fec_up = (2, 3)
fec_low = (3, 4)
guard_up = (1, 1)
guard_low = (32, 8)
#idx2 = 1

#freq = input('F[MHz] = ')
for idx2 in range(0, 2):
    for ch_no in range(ch_min, ch_max+1):
#    ch_no = (freq-306)/8
        freq_MHz = 8*ch_no+306
        print 'T', int(freq_MHz*1e6+freq_shift_kHz[idx]*1e3), '8MHz '+\
        str(fec_up[idx2])+'/'+str(fec_low[idx2])+' NONE QAM64 8k '+\
        str(guard_up[idx2])+'/'+str(guard_low[idx2])+' NONE'
