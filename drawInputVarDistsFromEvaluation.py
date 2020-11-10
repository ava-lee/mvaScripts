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

def getHisto(fileName, treeName, varName, sampleName="", selectionString="", binningString=""):
    tmpC = TCanvas("tmpC", "tmpC")
    tmpC.cd()

    tree = fileName.Get(treeName)

    if selectionString == "" and sampleName == "": cutString = TCut("")
    if selectionString == "" and sampleName != "": cutString = TCut("EventWeight*(sample==\"" + sampleName + "\")")
    if selectionString != "" and sampleName != "": cutString = TCut("EventWeight*(sample==\"" + sampleName + "\"&&" + selectionString + ")")
    if selectionString != "" and sampleName == "": cutString = TCut(selectionString)

    # draw the histograms of the MVA output with fine bins
    histoName = "h_" + varName
    if sampleName != "":
        histoName = histoName + "_" + sampleName
    drawString = varName + ">>" + histoName
    if binningString != "" : drawString = drawString+"("+binningString+")"
    tree.Draw(drawString, cutString)

    histo = gDirectory.Get(histoName)
    histo.SetDirectory(0)

    print histoName

    tree.Delete()
    tmpC.Close()

    return histo

def drawHighBDTInputVarHistos(file, file2, folderName, treeName, selectionString, selectionString2, region, varName, binningString):
    #style settings
    colours, markerstyles, linestyles = defineHistoStyles()

    #get histograms from signal/background evaluation root files
    tmpHisto = getHisto(file, treeName, varName, "", selectionString, binningString)
    tmpHisto.SetDirectory(0)
    tmpHisto.Scale(1/tmpHisto.Integral())
    configureHisto(tmpHisto,colours[1],markerstyles[0], 1,0.8)

    tmpHisto2 = getHisto(file2, treeName, varName, "", selectionString2, binningString)
    tmpHisto2.SetDirectory(0)
    tmpHisto2.Scale(1/tmpHisto2.Integral())
    configureHisto(tmpHisto2,colours[2],markerstyles[3],1,0.8)

    canvas = TCanvas("canvas", "canvas")
    canvas.cd()
    #Add legend
    leg = TLegend(0.5,0.8,0.9,0.95)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    if varName == "dRBB":
        varLabel = varName
    else:
        varLabel = varName + " [GeV]"
    #Draw first histogram
    refHisto = tmpHisto.Clone("ref")
    refHisto.Draw("HISTE")
    refHisto.SetTitle("")
    refHisto.GetYaxis().SetTitle("Arbitrary units")
    refHisto.GetXaxis().SetTitle(varLabel)
    maximum = refHisto.GetMaximum()*1.5
    leg.AddEntry(tmpHisto,label1,"ple")

    #Draw second histogram
    canvas.cd()
    tmpHisto2.Draw("HISTE,same")
    if tmpHisto2.GetMaximum() > maximum: maximum = tmpHisto2.GetMaximum() * 1.5
    leg.AddEntry(tmpHisto2,label2,"ple")
    refHisto.GetYaxis().SetRangeUser(0,maximum)

    canvas.cd()
    leg.Draw()

    if region == "Signal":
        setLabel(0.15, 0.9, "Signal")
    if region == "Background":
        setLabel(0.15, 0.9, "Background")

    canvas.cd()
    outName = folderName+"/"+region + "_" + varName
    canvas.SaveAs(outName + '.png') #for preview
    canvas.SaveAs(outName+'.pdf')
    canvas.Close()

###################### This is basically the int main ######################
gROOT.SetBatch(kTRUE)
setStyle()
file = ROOT.TFile(sys.argv[1])
file2 = ROOT.TFile(sys.argv[2])

### Set variables here:
# Legend:
label1="AdaBoost 0.10, 200 trees"
label2="GradBoost 0.50, 600 trees"
folderName="MVAPlots_highBDT"
if not os.path.exists(folderName):
    os.makedirs(folderName)

# Signal MVA cut score:
mva_cut = 0.462944239378
mva_cut2 = 0.837719559669
selectionString = "mva>(%s)" % mva_cut
selectionString2 = "mva>(%s)" % mva_cut2

if "Background" in sys.argv[1]:
    region = "Background"
    mBBbinningString = "50,10,200"
    pTVbinningString = "50,50,650"
    MtopbinningString = "50,50,700"
    dRBBbinningString = "50,0.2,4"
elif "Signal" in sys.argv[1]:
    region = "Signal"
    mBBbinningString="50,60,160"
    pTVbinningString="50,50,650"
    MtopbinningString="50,50,700"
    dRBBbinningString="50,0.2,4"

else:
    print "You probably have to get the background or signal branches first, use get...Branches.py"

drawHighBDTInputVarHistos(file, file2, folderName, region, selectionString, selectionString2, region, "mBB", mBBbinningString)
drawHighBDTInputVarHistos(file, file2, folderName, region, selectionString, selectionString2, region, "pTV", pTVbinningString)
drawHighBDTInputVarHistos(file, file2, folderName, region, selectionString, selectionString2, region, "Mtop", MtopbinningString)
drawHighBDTInputVarHistos(file, file2, folderName, region, selectionString, selectionString2, region, "dRBB", dRBBbinningString)

##### Old function for signal #####
def compareInputDistHighBDT(file, file2, folderName, selectionString, selectionString2, sampleList, region, varName, binningString):
    # Formatting and create canvas and legend
    colours, markerstyles, linestyles = defineHistoStyles()
    canvas = TCanvas("canvas", "canvas")
    canvas.cd()
    # leg = TLegend(0.75,0.63,0.83,0.8) #x1,y1,x2,y2
    leg = TLegend(0.2, 0.4, 0.6, 0.6)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    nBins = int(binningString.split(",")[0])
    xMin = float(binningString.split(",")[1])
    xMax = float(binningString.split(",")[2])

    h = TH1D("","", nBins,xMin,xMax)
    h2 = TH1D("","", nBins,xMin,xMax)
    #h3 = TH1D("", "", nBins,xMin,xMax) # To adjust legend

    print "Drawing", varName, "histograms using calculated mva scores for", region
    start_time = time.time()

    # Not using this for bkg since this cutting takes too long
    #if region=="Signal":
        #sampleList = ["ggZllH125", "ggZvvH125", "qqWlvH125", "qqZllH125", "qqZvvH125"]
    # elif region=="Background":
        # sampleList= ["Diboson","singletop","ttbar","Whf","Wcl","Wl","Zhf","Zcl","Zl"]

    for sample in sampleList:
        h_tmp = getHisto(file, "Nominal", varName, sample, selectionString, binningString)
        h_tmp2 = getHisto(file2, "Nominal", varName, sample, selectionString2, binningString)
        h.Add(h_tmp)
        h2.Add(h_tmp2)

    # Scaling and other setups of new histograms
    h.Draw("HISTE")
    h2.Draw("HISTE, same")
    h.Scale(1 / h.Integral())
    h2.Scale(1 / h2.Integral())

    print("Time taken: (%s) seconds" % (time.time() - start_time))
    print "Number of entries", h.GetEntries()

    varLabel = varName
    # hack to identify variables with unit GeV
    h.SetTitle("")
    maximum = h.GetMaximum() * 1.5
    if h.GetMaximum() < h2.GetMaximum(): maximum = h2.GetMaximum() * 1.5
    h.GetYaxis().SetRangeUser(0, maximum)
    h.GetYaxis().SetTitle("Arbitrary units")
    h.GetXaxis().SetTitle(varName)
    h.SetStats(0)

    # Set colours and markers for histograms
    configureHisto(h, colours[1], markerstyles[1], 1, 0.8, 2, 0)
    configureHisto(h2, colours[2], markerstyles[3], 1, 0.8, 2, 0)

    # Label legend
    leg.AddEntry(h, label1, "ple")
    leg.AddEntry(h2, label2, "ple")
    #leg.AddEntry(h3, " ", "1")
    leg.Draw()
    if region=="Signal":
        setLabel(0.2, 0.80, "Signal")
    if region=="Background":
        setLabel(0.2, 0.80, "Background")

    canvas.cd()
    outName = folderName + "/highBDT_" + region + "_" + varName +".png"
    canvas.SaveAs(outName)
    outName = folderName + "/highBDT_" + region + "_" + varName + ".pdf"
    canvas.SaveAs(outName)
    canvas.Close()
    h.Delete()
    h2.Delete()
    #h3.Delete()
