import ROOT
from ROOT import *
import sys
from math import *
import collections
import numpy as np
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)

### Layout settings here
gStyle.SetCanvasDefW(900)
gStyle.SetPaperSize(20, 30)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.13)
gStyle.SetPadBottomMargin(0.08)
gStyle.SetPadLeftMargin(0.09)
gStyle.SetPalette(kPastel)
gStyle.SetPaintTextFormat("1.4f");

canvas = TCanvas("tmpC", "tmpC")
canvas.cd()
heatmap = TH2F( '', '', 7, 1, 7, 13, 1, 13)
heatmap.SetMarkerSize(1.6)
heatmap.GetXaxis().SetTitle("Number of trees")
heatmap.GetYaxis().SetTitle("Learning rate")
heatmap.GetZaxis().SetTitle("Sensitivity")
heatmap.GetXaxis().SetTitleOffset(0.9)
heatmap.GetYaxis().SetTitleOffset(1.2)
heatmap.GetZaxis().SetTitleOffset(0.9)
heatmap.GetYaxis().SetLabelSize(0.05)
heatmap.GetXaxis().SetLabelSize(0.05)
heatmap.GetXaxis().SetTickLength(0.)
heatmap.GetYaxis().SetTickLength(0.)

### Get heatmap
file = open("MVAScripts/sigs_" + sys.argv[1] + ".txt")

values = {}
lrs = np.arange(0.1, 0.75, 0.05)
for i in range(0, len(lrs)):
    lr = "{:.2f}".format(lrs[i])
    values[lr] = range(1, 14)[i]

trees = range(200, 900, 100)
for j in range(0, len(trees)):
    tree = str(trees[j])
    values[tree] = range(1, 8)[j]

dict = collections.OrderedDict()
for line in file.readlines():
    if 'Eval.txt' in line:
        config = line.replace("_Eval.txt\n", "").replace("./Grad_", "")
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