import ROOT
import sys
from ROOT import *
import os
from math import  *
import argparse
import glob
import collections
import itertools
import string
import numpy as np
import time

from styleConfigurations import setStyle
from styleConfigurations import setLabel
from styleConfigurations import configureHisto
from styleConfigurations import defineHistoStyles
from styleConfigurations import setRatioStyle
from styleConfigurations import configurePads

from helpers import constructFilesDict
from helpers import getPlainFileName
#from helpers import getHisto
from helpers import getScaleFactorForTrainTree
from helpers import constructVariableMap
from helpers import getNameOfBDTDistribution
ROOT.gROOT.SetBatch()

# Can add more files to compare here
file = ROOT.TFile(sys.argv[1])
#file2 = ROOT.TFile(sys.argv[2])

def getCutValue(fileName, treeName, varName, cutFraction, sampleList=""):
    tree = fileName.Get(treeName)

    print "Calculating score corresponding to", cutFraction, "of S/B events in", varName, "dist:"
    start_time = time.time()

    print "Getting events in sample list"
    # Record index numbers of events ^= cuts
    if sampleList=="":
        tree.Draw(">>events") # get all events
    else:
        for sampleName in sampleList:
            cutString = TCut("EventWeight*(sample==\"" + sampleName + "\")")
            # put + after >> to add to existing TEventList
            tree.Draw(">>+ events", cutString)

    event_list = gDirectory.Get("events")  # Get TEventList
    entries = event_list.GetN()  # and number of entries in the list
    events_cut = int(round(entries * cutFraction))
    print "Number of events in sample list corresponding to cut:", events_cut

    print "Getting values for ", varName
    values = []
    for i in xrange(entries):
        entry = event_list.GetEntry(i)
        tree.GetEntry(entry)
        values.append(tree.GetLeaf(varName).GetValue())

    print "Sorting values"
    #values = np.array(values)
    #sorted = np.sort(values)
    sorted = sorted(values)
    cut_value = sorted[events_cut]

    print("Time taken: (%s) seconds" % (time.time() - start_time))

    return cut_value

def getCutValueFromGuess(fileName, treeName, varName, cutFraction, guessCut):
    tree = fileName.Get(treeName)

    print "Calculating score corresponding to", cutFraction, "according to guess score:"
    start_time = time.time()

    print "Getting events in guess score"
    cutString = TCut(varName + ">" + str(guessCut))
    tree.Draw(">>events", cutString)
    cut_events = gDirectory.Get("events")  # Get TEventList of events in cut
    guess_entries = cut_events.GetN()  # and number of entries in the list

    print "Compare number of events in guess cut to number of events in actual cut:"
    actual_entries = int(round(tree.GetEntries() * (1-cutFraction)))
    print "Guessed number of events", guess_entries
    print "Actual number of events", actual_entries
    if guess_entries < actual_entries:
        sys.exit('=========== Need more entries in guess ===========')

    elif guess_entries == actual_entries:
        sys.exit("=========== Guessed the correct cut ===========")

    elif guess_entries > actual_entries:
        print "Getting values for", varName
        values = []
        for i in xrange(guess_entries):
            entry = cut_events.GetEntry(i)
            tree.GetEntry(entry)
            values.append(tree.GetLeaf(varName).GetValue())

        print "Sorting values in descending order"
        reverse_sorted = sorted(values, reverse=True)
        cut_value = reverse_sorted[actual_entries]

    print("Time taken: (%s) seconds" % (time.time() - start_time))

    return cut_value

######################
# Set variables here (remember to add more if you added more files to argument)
label="Grad_0.50"

signalList = ["ggZllH125", "ggZvvH125", "qqWlvH125", "qqZllH125", "qqZvvH125"] # signal samples
# Getting background samples could take too long if you have many events
# Use getBackgroundBranches.py instead to get trees with relevant branches for bkg events
bkgList = ["Diboson","singletop","ttbar","Whf","Wcl","Wl","Zhf","Zcl","Zl"] # background samples

cutFraction=0.8
######################

# Example 1: get cut value for 80% signal events in highest mva dist
"""
cutFraction=0.8
sigMvaCut = getCutValue(file, "Nominal", "mva", cutFraction, signalList)
sigMvaCut2 = getCutValue(file2, "Nominal", "mva", cutFraction, signalList)
print "Signal MVA cut for", label1, "at", cutFraction, ":", sigMvaCut
print "Signal MVA cut for", label2, "at", cutFraction, ":", sigMvaCut2
"""

# Example 2: guessing to get cut value for 80% background events in mva
# Use for large number of events and remember to get the background tree for this first (saved as EvaluationBackground_...root)
guessCut=-0.3
bkgMvaCut = getCutValueFromGuess(file,"Background","mva",cutFraction,guessCut)
print "Background MVA cut for", label, "at", cutFraction, ":", bkgMvaCut