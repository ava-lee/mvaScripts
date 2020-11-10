#!/usr/bin/env python  

from ROOT import *
import sys
import os
import string
import collections

#get a tree from file (inFile)
#this checks first and second layer of input file
def getTree(inFile,treeName) :
	#get list of objects
	fileContent = inFile.GetListOfKeys()
	#first check if the matrix histogram is directly stored in file (old format)
	for obj_i in fileContent :
		objectName = obj_i.GetName() 
		if treeName in objectName : 
			tree = inFile.Get(objectName)
			return 1,tree #return success (1) and the histogram
	#now try if it is stored in a sub-directory (new format)
	for obj_i in fileContent :
		objectName2 = obj_i.GetName()
		className2 = obj_i.GetClassName()
		if className2 == "TDirectoryFile" :
			subdir = TDirectoryFile()	
			subdir = inFile.Get(objectName2)
			dirContent = subdir.GetListOfKeys()
			for subobj_i in dirContent :
				subobjectName = subobj_i.GetName()
				if treeName in subobjectName :
					tree = subdir.Get(subobjectName)
					return 1,tree #return success (1) and the histogram
	print "helpers.py \t <getTree> checked first and second layer of ROOT file for tree with name ", treeName, " but couldn't find it"
	return 0,0

#construct a histogram from specified file and tree for a given sample
# binning and selection can be specified
# 2D histo also supported if varName2 and binningString2 are specified
def getHisto(inputFile,fileName,treeName,varName,sampleName,binningString="",selectionString="",scaleFactors={},varName2="",binningString2="", ) :

	tmpC = TCanvas("tmpC", "tmpC")
	tmpC.cd()
	
	successTree, theTree = getTree(inputFile,treeName)

	if successTree < 1 : return 0

	cutString = ""

	#construct the cut strings for signal and background
	if selectionString=="" :
		cutString = TCut("weight*(className==\""+sampleName+"\")")		
	else :
		cutString = TCut("weight*(className==\""+sampleName+"\"&&"+selectionString+")")		

	#draw the histograms of the MVA output with fine bins
	histoName = "h_"+varName+"_"+getPlainFileName(fileName)+"_"+sampleName
	drawString = varName+">>"+histoName
	#for 2D histo: put first specified variable on x-axis
	if varName2 != "" : 
		histoName = histoName+"_"+varName2
		drawString = varName2+":"+varName+">>"+histoName
	if binningString != "" and binningString2 == "" : drawString = drawString+"("+binningString+")"
	if binningString != "" and binningString2 != "" : drawString = drawString+"("+binningString+","+binningString2+")"
	theTree.Draw(drawString,cutString)
	
	histo = gDirectory.Get(histoName)
	histo.SetDirectory(0)

	#if traintree scale by additional scale factor
	if treeName=="TrainTree" :
		if scaleFactors :
			histo.Scale(scaleFactors[sampleName])
		else :
			print "helpers.py \t <getHisto> you are using events from train tree but no scale factors -> histograms will probably have wrong sumOfWeights"

	theTree.Delete()
	tmpC.Close()

	return histo

#get a variable list and binning: default take all variables found in the specified tree of the specified inputFile
#if variable list was defined in options it will be taken
#exclude certain variables (exception: they are explicitly specified in the var list in the options) 
def constructVariableMap(inputFile,treeName="TestTree",predefinedVars="",excludedVars="") :
	variableMap = collections.OrderedDict()
	if predefinedVars != "" : 
		variableList = predefinedVars.split(":")
		successTree, theTree = getTree(inputFile,treeName)
		if successTree < 1 : return variableMap
		for var in variableList:
			#could specify mva, MVA or BDT to get output score
			if (var=="BDT") or (var=="MVA") or (var=="mva") :
				var = getNameOfBDTDistribution(inputFile,treeName)
			isVar = isLeafInTree(inputFile,treeName,var)
			if isVar == False : 
				continue
			else : 
				varName = var
				if "MV2" in varName :
					variableMap[varName] = "6,0,6"
				else : 
					variableMap[varName] = determineBinning(theTree.GetMinimum(var), theTree.GetMaximum(var))
	else :
		successTree, theTree = getTree(inputFile,treeName)
		if successTree < 1 : return variableMap
		#get list of leaves in tree and loop
		treeLeaves = theTree.GetListOfLeaves()
		for leaf_i in treeLeaves :
			leafName = leaf_i.GetName()
			#store names of all leaves stored in tree minus excludedVars
			if (leafName not in excludedVars) :
				leafType = leaf_i.GetTypeName()
				#only consider leaves that are float, double or int
				if ("Float" in leafType) or ("Double" in leafType) or ("Int" in leafType) :
					varName = leafName
					if "MV2" in varName :
						variableMap[varName] = "6,0,6"
					else : 
						variableMap[varName] = determineBinning(theTree.GetMinimum(leafName), theTree.GetMaximum(leafName))

	if not variableMap : return
	print "helpers.py \t <constructVariableMap> will produce histograms for the following variables: ", variableMap.keys()
	return variableMap

#get the name of the BDT output distribution as it is stored in training output file
#search for any variable that is called BDT* or mva* or MVA* 
def getNameOfBDTDistribution(inputFile,treeName="TestTree") :
	mvaName = ""
	mvaNameList = []
	successTree, theTree = getTree(inputFile,treeName)
	if successTree < 1 : return mvaName
	#get list of leaves in tree and loop
	treeLeaves = theTree.GetListOfLeaves()
	for leaf_i in treeLeaves :
		leafName = leaf_i.GetName()
		leafType = leaf_i.GetTypeName()
		if ("BDT" in leafName) and (("Float" in leafType) or ("Double" in leafType)) :
			mvaNameList.append(leafName) 
		if ("MVA" in leafName) and (("Float" in leafType) or ("Double" in leafType)) :
			mvaNameList.append(leafName) 
		if ("mva" in leafName) and (("Float" in leafType) or ("Double" in leafType)) :
			mvaNameList.append(leafName) 

	mvaName = mvaNameList[0]
	if mvaName=="" : 
		print "helpers.py \t <getNameOfBDTDistribution> couldn't find mva score distribution please specify it explicitly"
	if len(mvaNameList)>1 :
		print "helpers.py \t <getNameOfBDTDistribution> found multiple variables matching name pattern for mva output score -> will use: ", mvaName

	return mvaName

def isLeafInTree(inputFile,treeName,varName) :
	exists = False
	successTree, theTree = getTree(inputFile,treeName)
	if successTree < 1 : return exists
	if theTree.FindLeaf(varName) == None : 
		print "helpers.py \t <isLeafInTree> variable with name ", varName, "does not exist in tree ", treeName, " of file ", inputFile
	else : 
		exists = True
	return exists


#determine binning for variables
def determineBinning(minimum,maximum) :
	binningString = ""
	#use width=0.1 bins for everything smaller 10
	if maximum < 10 :
		#this should only be the case for the BDT output
		if minimum < 0 and minimum >= -1 and maximum <= 1 :
			binningString = "20,-1,1"
		else :
			theMin = 0
			theMax = round(maximum,1)
			if theMax < maximum : theMax = theMax+0.1
			nBins = (theMax-theMin)/0.1
			binningString = str(nBins)+","+str(theMin)+","+str(theMax)
	# use 1 GeV bins here
	elif (maximum > 10 and maximum < 50):
		theMin = 0
		theMax = round(maximum,-1)
		if theMax < maximum : theMax = theMax+1
		nBins = (theMax-theMin)/1	
		binningString = str(nBins)+","+str(theMin)+","+str(theMax)
	# use 5 GeV bins here
	elif (maximum > 50 and maximum < 102): #102 due to mLL going up to 101
		theMin = 0
		theMax = round(maximum,-1)
		if theMax < maximum : theMax = theMax+5
		nBins = (theMax-theMin)/5	
		binningString = str(nBins)+","+str(theMin)+","+str(theMax)	
	# use 10 GeV bins here
	elif (maximum > 102 and maximum < 500):
		theMin = 0
		theMax = round(maximum,-1)
		if theMax < maximum : theMax = theMax+10
		nBins = (theMax-theMin)/10	
		binningString = str(nBins)+","+str(theMin)+","+str(theMax)		
	# use 20 GeV bins here
	elif (maximum > 500):
		theMin = 0
		theMax = round(maximum,-1)
		if theMax < maximum : theMax = theMax+10
		if theMax%20 != 0 : theMax = theMax+10
		nBins = (theMax-theMin)/20	
		binningString = str(nBins)+","+str(theMin)+","+str(theMax)	

	return binningString

def getPlainFileName(fileName) :
	fileName = fileName.split("/")[-1]
	fileName = fileName.split(".root")[0]
	return fileName

def constructFilesDict(fileNames, labelNames) :
	filesDict = collections.OrderedDict()
	fileNames = fileNames.split(":")

	# hack to use same file multiple times

	if labelNames == "" :
		count_i = 0
		for file_i in fileNames :
			name = file_i
			if name in filesDict : name = name+">>"+str(count_i)
			label = getPlainFileName(file_i)
			filesDict[name] = label
			count_i += 1

	else :
		labelNames = labelNames.split(":")
		count_i = 0
		for file_i in fileNames :
			name = file_i
			if name in filesDict : name = name+">>"+str(count_i)
			filesDict[name] = labelNames[count_i]
			count_i +=1 

	return filesDict


# this is needed because TMVA internally reweights the training events 
# therefore an additional scale factor is needed to restore original sum of weights in train tree
def getScaleFactorForTrainTree(inputFile, fileName, selectionsDict={}) :

	c1 = TCanvas("c1", "c1")
	c1.cd()

	successTest, tree_test = getTree(inputFile,"TestTree")	
	successTrain, tree_train = getTree(inputFile,"TrainTree")	

	scaleFactors = {}
	cutS = ""
	cutB = ""

	if selectionsDict :
		addCut = selectionsDict[fileName]
		cutS = TCut("weight*(className==\"Signal\"&&"+addCut+")")		
		cutB = TCut("weight*(className==\"Background\"&&"+addCut+")")	
	else :
		cutS = TCut("weight*(className==\"Signal\")")	
		cutB = TCut("weight*(className==\"Background\")")


	if successTest < 1 or successTrain < 1 : 
		print "helpers.py \t <getScaleFactorForTrainTree> couldn't calculate scale factor -> will set to 1"
		scaleFactors["Signal"] = 1
		scaleFactors["Background"] = 1
		return scaleFactors

	else :
		tree_train.Draw("weight>>h_sig_train",cutS)
		tree_train.Draw("weight>>h_bg_train",cutB)
		tree_test.Draw("weight>>h_sig_test",cutS)
		tree_test.Draw("weight>>h_bg_test",cutB)

		h_sig_train = gDirectory.Get('h_sig_train')
		h_bg_train = gDirectory.Get('h_bg_train')
		h_sig_test = gDirectory.Get('h_sig_test')
		h_bg_test = gDirectory.Get('h_bg_test')

		scaleFactors["Signal"] = calculateScaleFactor(h_sig_test,h_sig_train)
		scaleFactors["Background"] = calculateScaleFactor(h_bg_test,h_bg_train)

	h_sig_train.Delete()
	h_bg_train.Delete()
	h_sig_test.Delete()
	h_bg_test.Delete()
	tree_train.Delete()
	tree_test.Delete()
	c1.Close()
	
	return scaleFactors
		
#calculate scale factors from training and test histogram
def calculateScaleFactor(h_test, h_train) :
	scaleFactor = 1
	sumWTest = h_test.GetSumOfWeights()
	entriesTest = h_test.GetEntries()
	sumWTrain = h_train.GetSumOfWeights()	 
	entriesTrain = h_train.GetEntries()

	scaleFactor = (sumWTest*entriesTrain)/(entriesTest*sumWTrain)
	return scaleFactor

