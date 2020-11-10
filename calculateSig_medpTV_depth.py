import sys
from math import *

file = open(sys.argv[1])

all_lines = file.readlines()

region = '2T_2J_75ptv_150ptv'
guess = 245
if region in all_lines[guess - 1]:
    j2_75 = float(all_lines[guess - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess - 1 - 1]:
    j2_75 = float(all_lines[guess - 1 - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess + 1 - 1]:
    j2_75 = float(all_lines[guess + 1 - 1].split('\t')[1].split('\n')[0])
else:
    print "Need to locate ", region

region = '2T_3J_75ptv_150ptv'
guess = 249
if region in all_lines[guess - 1]:
    j3_75 = float(all_lines[guess - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess - 1 - 1]:
    j3_75 = float(all_lines[guess - 1 - 1].split('\t')[1].split('\n')[0])
elif region in all_lines[guess + 1 - 1]:
    j3_75 = float(all_lines[guess + 1 - 1].split('\t')[1].split('\n')[0])
else:
    print "Need to locate ", region

print "Sum", sqrt((j3_75**2) + (j2_75**2))