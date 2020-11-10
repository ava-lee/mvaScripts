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
from array import array

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

file = ROOT.TFile(sys.argv[1])
region = sys.argv[2] #Signal or Background
label = sys.argv[3] #output comment for root file

def getSignalBackgroundBranches(file, label, region):
    tree = file.Get("Nominal")

    # Define new ROOT file and new tree
    new_root = ROOT.TFile("Evaluation" + region + "_" + label + ".root", "RECREATE")
    new_tree = ROOT.TTree(region, region)

    # Define branches to get:
    mva = array('d', [0])
    mBB = array('d', [0])
    pTV = array('d', [0])
    Mtop = array('d', [0])
    dRBB = array('d', [0])

    new_tree.Branch("mva", mva, 'mva/D')
    new_tree.Branch("mBB", mBB, 'mBB/D')
    new_tree.Branch("pTV", pTV, 'pTV/D')
    new_tree.Branch("Mtop", Mtop, 'Mtop/D')
    new_tree.Branch("dRBB", dRBB, 'dRBB/D')

    # Get signal/background events
    signalList = ["ggZllH125", "ggZvvH125", "qqWlvH125", "qqZllH125", "qqZvvH125"]  # signal samples
    # bkgList = ["Diboson","singletop","ttbar","Whf","Wcl","Wl","Zhf","Zcl","Zl"] # background samples

    print "Getting all events"
    tree.Draw(">>events") # get all events
    print "Getting signal events"
    for sampleName in signalList:
        cutString = TCut("EventWeight*(sample==\"" + sampleName + "\")")
        # put + after >> to add to existing TEventList
        tree.Draw(">>+ sig_events", cutString) # get signal events

    sig_events = gDirectory.Get("sig_events")
    if region == "Signal":
        events = sig_events
    elif region == "Background":
        print "Getting background events"
        events = gDirectory.Get("events")
        print events.GetN()
        events.Subtract(sig_events) # subtract signal events from all events to get background events
        print events.GetN()

    print "Filling new tree"
    # Fill new tree in new file
    for i in xrange(events.GetN()):
        entry = events.GetEntry(i) # get entry from TEventList
        tree.GetEntry(entry) # get entry from tree

        # Get values from branches of old tree
        mva[0] = tree.GetLeaf("mva").GetValue()
        mBB[0] = tree.GetLeaf("mBB").GetValue()
        pTV[0] = tree.GetLeaf("pTV").GetValue()
        Mtop[0] = tree.GetLeaf("Mtop").GetValue()
        dRBB[0] = tree.GetLeaf("dRBB").GetValue()
        new_tree.Fill()

    new_root.Write()
    new_root.Close()

getSignalBackgroundBranches(file, label, region)
