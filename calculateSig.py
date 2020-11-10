import sys
from math import *

file = open(sys.argv[1])

all_lines = file.readlines()

region = '2T_2J_150ptv_250ptv'
guess = 241
if region in all_lines[guess - 1]:
    j2_150250 = float(all_lines[guess - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess - 1 - 1]:
    j2_150250 = float(all_lines[guess - 1 - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess + 1 - 1]:
    j2_150250 = float(all_lines[guess + 1 - 1].split('\t')[1].split('\n')[0])
else:
    print "Need to locate ", region

region = '2T_2J_250ptv'
guess = 242
if region in all_lines[guess - 1]:
    j2_250 = float(all_lines[guess - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess - 1 - 1]:
    j2_250 = float(all_lines[guess - 1 - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess + 1 - 1]:
    j2_250 = float(all_lines[guess + 1 - 1].split('\t')[1].split('\n')[0])
else:
    print "Need to locate ", region

region = '2T_3J_150ptv_250ptv'
guess = 245
if region in all_lines[guess - 1]:
    j3_150250 = float(all_lines[guess - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess - 1 - 1]:
    j3_150250 = float(all_lines[guess - 1 - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess + 1 - 1]:
    j3_150250 = float(all_lines[guess + 1 - 1].split('\t')[1].split('\n')[0])
else:
    print "Need to locate ", region

region = '2T_3J_250ptv'
guess = 246
if region in all_lines[guess - 1]:
    j3_250 = float(all_lines[guess - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess - 1 - 1]:
    j3_250 = float(all_lines[guess - 1 - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess + 1 - 1]:
    j3_250 = float(all_lines[guess + 1 - 1].split('\t')[1].split('\n')[0])
else:
    print "Need to locate ", region

j2sig = sqrt((j2_150250**2) + (j2_250**2))
print "2J", j2sig

j3sig = sqrt((j3_150250**2) + (j3_250**2))
print "3J", j3sig

print "Sum", sqrt((j3sig**2) + (j2sig**2))