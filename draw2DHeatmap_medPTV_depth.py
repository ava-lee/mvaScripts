import ROOT
from ROOT import *
import sys
from math import *
import collections
import numpy as np
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)

from styleConfigurations import setStyle
from styleConfigurations import setLabel
from styleConfigurations import configureHisto
from styleConfigurations import defineHistoStyles
from styleConfigurations import setRatioStyle
from styleConfigurations import configurePads


### Layout settings here
gStyle.SetCanvasDefW(600)
gStyle.SetPaperSize(20, 30)
gStyle.SetPadTopMargin(0.02)
gStyle.SetPadRightMargin(0.14)
gStyle.SetPadBottomMargin(0.09)
gStyle.SetPadLeftMargin(0.08)
gStyle.SetPalette(kPastel)
gStyle.SetPaintTextFormat("1.4f");

canvas = TCanvas("tmpC", "tmpC")
canvas.cd()
heatmap = TH2F( '', '', 5, 1, 5, 4, 1, 4)
heatmap.SetMarkerSize(2)
heatmap.GetXaxis().SetTitle("Number of trees")
heatmap.GetYaxis().SetTitle("Maximum depth of trees")
heatmap.GetZaxis().SetTitle("Sensitivity")
heatmap.GetXaxis().SetTitleOffset(1.2)
heatmap.GetYaxis().SetTitleOffset(1.1)
heatmap.GetZaxis().SetTitleOffset(1.2)
labelsize = 0.05
heatmap.GetYaxis().SetLabelSize(labelsize)
heatmap.GetXaxis().SetLabelSize(labelsize)
heatmap.GetXaxis().SetTickLength(0.)
heatmap.GetYaxis().SetTickLength(0.)

setStyle(0.06)

### Get heatmap
file = open("MVAScripts/sigs_" + sys.argv[1] + ".txt")

# lr = depth
values = {}
lrs = np.arange(1, 5, 1)
for i in range(0, len(lrs)):
    lr = str(lrs[i])
    values[lr] = range(1, 5)[i]

trees = range(200, 1200, 200)
for j in range(0, len(trees)):
    tree = str(trees[j])
    values[tree] = range(1, 6)[j]

dict = collections.OrderedDict()
for line in file.readlines():
    if 'Eval.txt' in line:
        config = line.replace("_Eval.txt\n", "").replace("./Grad0.5_Depth", "")
        LR = config.split('_')[0]
        nTree = config.split('_')[1]
    if 'Sum' in line:
        dict[values[nTree], values[LR]] = line.split(" ")[1].replace("\n", "")

for n in range(heatmap.GetNbinsX()):
    heatmap.GetXaxis().SetBinLabel(n+1, str(trees[n]))
for n in range(heatmap.GetNbinsY()):
    heatmap.GetYaxis().SetBinLabel(n+1, str(lrs[n]))

for configs in dict.keys():
    heatmap.SetBinContent(configs[0],configs[1],float(dict[configs]))

heatmap.Draw("COLZ TEXT")

canvas.cd()
canvas.SaveAs(sys.argv[1]+'_Sigs.png')
canvas.SaveAs(sys.argv[1]+'_Sigs.pdf')
canvas.Close()
heatmap.Delete()