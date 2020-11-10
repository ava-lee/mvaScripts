#!/usr/bin/env python  

from ROOT import *
import sys
import os
import string
import collections

#set the label of a histogram at position x and y with up to 4 text strings in colour "colour"
def setLabel(x, y, text1="", text2="", text3="", text4="", colour=1):
	label = TLatex()
  	label.SetNDC()
	label.SetTextFont(72)
  	label.SetTextColor(colour)
	label.DrawLatex(x,y,text1)
	if text2 != "" : 
    		label2 = TLatex() 
		y2 = y-1.05*label.GetTextSize()
    		label2.SetNDC()
    		label2.SetTextFont(42)
    		label2.SetTextColor(colour)
    		label2.DrawLatex(x,y2,text2)
		if text3 != "" :
			label3 = TLatex()
			label3.SetNDC()
    			label3.SetTextFont(42)
    			label3.SetTextColor(colour)
			y3 = y2-1.05*label.GetTextSize()
	    		label3.DrawLatex(x,y3,text3)
			if text4 != "" :
				label4 = TLatex()
				label4.SetNDC()
	    			label4.SetTextFont(42)
	    			label4.SetTextColor(colour)
				y4= y2-1.05*label.GetTextSize()-1.2*label.GetTextSize()
		    		label4.DrawLatex(x,y4,text4)

#configure the style of a histogram ("histo")
def configureHisto(histo, colour=1, markerstyle=2, linestyle=1, markersize=0.8, linewidth=2, fillStyle=0) :
	histo.SetLineColor(colour)
	histo.SetLineStyle(linestyle)
	histo.SetMarkerSize(markersize)
	histo.SetMarkerColor(colour)
	histo.SetMarkerStyle(markerstyle)
	histo.SetFillColor(colour)
	histo.SetFillStyle(fillStyle)
	histo.SetLineWidth(linewidth)

#to configure the upper ("upper") and lower ("lower") Pad in a ratio plot
def configurePads(upper, lower) :
	upper.SetFrameFillColor(0)
	upper.SetFrameFillStyle(0)
	upper.SetFillColor(0)
	upper.SetFillStyle(0)
    	upper.SetBottomMargin(0.02/(1-(0.3+0.02)))
	lower.SetFrameFillColor(0)
	lower.SetFrameFillStyle(0)
	lower.SetFillColor(0)
	lower.SetFillStyle(0)
    	lower.SetTopMargin(0.02/(0.3+0.02))
    	lower.SetBottomMargin(0.36)
	lower.SetTicky()

#to configure the style of the ratio plot for a given histogram (h_down)
def setRatioStyle(h_down, titleX, titleY, yMin, yMax) :

	h_down.GetYaxis().SetNdivisions(503,kTRUE);
	h_down.GetYaxis().SetRangeUser(yMin,yMax);
	h_down.GetYaxis().SetLabelSize(0.105);
	h_down.GetYaxis().SetTitleSize(0.105);
	h_down.GetYaxis().SetTitle(titleY);
	h_down.GetYaxis().SetTitleOffset(0);            
	h_down.GetXaxis().SetTitle(titleX);
	h_down.GetYaxis().SetTitleOffset(0.6);            
	h_down.GetXaxis().SetLabelSize(0.105);
	h_down.GetXaxis().SetTitleOffset(1.4);            
	h_down.GetXaxis().SetTitleSize(0.105);
	h_down.SetTitle("")
	gPad.SetTicky()

#some general style settings 
def setStyle(textsize=0.04) :
	print "styleConfigurations.py \t <setStyle> setting global style"
	gStyle.SetCanvasColor(0)
	gStyle.SetCanvasBorderMode(0)
	gStyle.SetFrameFillColor(0)
	gStyle.SetFrameBorderMode(0)
	gStyle.SetPadColor(0)
	gStyle.SetPadBorderMode(0)
	gStyle.SetTitleFillColor(0)
	gStyle.SetStatColor(0)

	gStyle.SetCanvasDefW(700)
	gStyle.SetPaperSize(20, 30)
	gStyle.SetPadTopMargin(0.03)
	gStyle.SetPadRightMargin(0.03)
	gStyle.SetPadBottomMargin(0.1)
	gStyle.SetPadLeftMargin(0.1)
	gStyle.SetTitleXOffset(1)
	gStyle.SetTitleYOffset(1.2)
  
	font=42 #Helvetica
  	gStyle.SetTextFont(font)

  	gStyle.SetTextSize(textsize)
  	gStyle.SetLabelFont(font,"x")
  	gStyle.SetTitleFont(font,"x")
  	gStyle.SetLabelFont(font,"y")
  	gStyle.SetTitleFont(font,"y")
  	gStyle.SetLabelFont(font,"z")
  	gStyle.SetTitleFont(font,"z")
  
  	gStyle.SetLabelSize(textsize,"x")
  	gStyle.SetTitleSize(textsize,"x")
  	gStyle.SetLabelSize(textsize,"y")
  	gStyle.SetTitleSize(textsize,"y")
  	gStyle.SetLabelSize(textsize,"z")
  	gStyle.SetTitleSize(textsize,"z")

  	gStyle.SetErrorX(0.001)
  	gStyle.SetEndErrorSize(0.)

 	#gStyle.SetOptTitle(0)
  	gStyle.SetOptStat(0)
  	gStyle.SetOptFit(0)

def defineHistoStyles() :
	colors = [597,429,613,844,805,793]
	markerstyles = [26,28,24,25,27,30]
	linestyles = [1,3,2,9,8,10]
	return colors, markerstyles, linestyles

