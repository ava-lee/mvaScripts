import ROOT
from ROOT import *
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)

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

for i in range(heatmap.GetNbinsX()):
    heatmap.GetXaxis().SetBinLabel(i+1, str(200+i*100))
heatmap.GetXaxis().SetLabelSize(0.05)
for i in range(heatmap.GetNbinsY()):
    heatmap.GetYaxis().SetBinLabel(i+1, str(0.1+i*0.05))
heatmap.GetYaxis().SetLabelSize(0.05)
heatmap.GetXaxis().SetTickLength(0.)
heatmap.GetYaxis().SetTickLength(0.)

heatmap.SetBinContent(1,1,5.27993198)
heatmap.SetBinContent(2,1, 5.27731881192)
heatmap.SetBinContent(3,1, 5.312290141)
heatmap.SetBinContent(4,1, 5.331008286)
heatmap.SetBinContent(5,1, 5.343839043)
heatmap.SetBinContent(6,1, 5.354919528)
heatmap.SetBinContent(7,1, 5.366931156)

heatmap.SetBinContent(1,2, 5.276378404)
heatmap.SetBinContent(2,2, 5.314843453)
heatmap.SetBinContent(3,2, 5.335510612)
heatmap.SetBinContent(4,2, 5.35143662)
heatmap.SetBinContent(5,2, 5.363555792)
heatmap.SetBinContent(6,2, 5.376919905)
heatmap.SetBinContent(7,2, 5.38308966)

heatmap.SetBinContent(1,3, 5.313281447)
heatmap.SetBinContent(2,3, 5.34357638)
heatmap.SetBinContent(3,3, 5.366457029)
heatmap.SetBinContent(4,3, 5.384454736)
heatmap.SetBinContent(5,3, 5.403348927)
heatmap.SetBinContent(6,3, 5.412325488)
heatmap.SetBinContent(7,3, 5.422391583)

heatmap.SetBinContent(1,4, 5.300540794)
heatmap.SetBinContent(2,4, 5.340244241)
heatmap.SetBinContent(3,4, 5.367576961)
heatmap.SetBinContent(4,4, 5.375634133)
heatmap.SetBinContent(5,4, 5.39543264)
heatmap.SetBinContent(6,4, 5.400972137)
heatmap.SetBinContent(7,4, 5.414149117)

heatmap.SetBinContent(1,5, 5.340751674)
heatmap.SetBinContent(2,5, 5.360579817)
heatmap.SetBinContent(3,5, 5.384426374)
heatmap.SetBinContent(4,5, 5.407111085)
heatmap.SetBinContent(5,5, 5.416644155)
heatmap.SetBinContent(6,5, 5.42621783671)
heatmap.SetBinContent(7,5, 5.44781594386)

heatmap.SetBinContent(1,6, 5.34151804359)
heatmap.SetBinContent(2,6, 5.37252094647)
heatmap.SetBinContent(3,6, 5.3900009935)
heatmap.SetBinContent(4,6, 5.403689723)
heatmap.SetBinContent(5,6, 5.42721114251)
heatmap.SetBinContent(6,6, 5.435408845)
heatmap.SetBinContent(7,6, 5.454750308)

heatmap.SetBinContent(1,7, 5.337085885)
heatmap.SetBinContent(2,7, 5.381517996)
heatmap.SetBinContent(3,7, 5.406421343)
heatmap.SetBinContent(4,7, 5.417483857)
heatmap.SetBinContent(5,7, 5.427222507)
heatmap.SetBinContent(6,7, 5.4375456)
heatmap.SetBinContent(7,7, 5.442606185)

heatmap.SetBinContent(1,8, 5.350980704)
heatmap.SetBinContent(2,8, 5.381465804)
heatmap.SetBinContent(3,8, 5.401066006)
heatmap.SetBinContent(4,8, 5.41421359)
heatmap.SetBinContent(5,8, 5.427639693)
heatmap.SetBinContent(6,8, 5.4360)
heatmap.SetBinContent(7,8, 5.436902677)

heatmap.SetBinContent(1,9, 5.3428364)
heatmap.SetBinContent(2,9, 5.370757111)
heatmap.SetBinContent(3,9, 5.405948341)
heatmap.SetBinContent(4,9, 5.423716441)
heatmap.SetBinContent(5,9, 5.435471195)
heatmap.SetBinContent(6,9, 5.435302335)
heatmap.SetBinContent(7,9, 5.454744747)

heatmap.SetBinContent(1,10, 5.3634876)
heatmap.SetBinContent(2,10, 5.39258729246)
heatmap.SetBinContent(3,10, 5.409479771)
heatmap.SetBinContent(4,10, 5.417394925)
heatmap.SetBinContent(5,10, 5.437987183)
heatmap.SetBinContent(6,10, 5.448296795)
heatmap.SetBinContent(7,10, 5.455878108)

heatmap.SetBinContent(1,11, 5.326406629)
heatmap.SetBinContent(2,11, 5.375628681)
heatmap.SetBinContent(3,11, 5.39258729246)
heatmap.SetBinContent(4,11, 5.403945671)
heatmap.SetBinContent(5,11, 5.422595724)
heatmap.SetBinContent(6,11, 5.427291304)
heatmap.SetBinContent(7,11, 5.431306625)

heatmap.SetBinContent(1,12, 5.335409154)
heatmap.SetBinContent(2,12, 5.37966475488)
heatmap.SetBinContent(3,12, 5.40053225357)
heatmap.SetBinContent(4,12, 5.414787618)
heatmap.SetBinContent(5,12, 5.428793085)
heatmap.SetBinContent(6,12, 5.432166703)
heatmap.SetBinContent(7,12, 5.4323556)

heatmap.SetBinContent(1,13, 5.347938543)
heatmap.SetBinContent(2,13, 5.386915101)
heatmap.SetBinContent(3,13, 5.410239153)
heatmap.SetBinContent(4,13, 5.428824483)
heatmap.SetBinContent(5,13, 5.433752061)
heatmap.SetBinContent(6,13, 5.435106839)
heatmap.SetBinContent(7,13, 5.444345798)



heatmap.Draw("COLZ TEXT")

canvas.cd()
canvas.SaveAs('Ada_Sigs.png')
canvas.SaveAs('Ada_Sigs.pdf')
canvas.Close()
heatmap.Delete()