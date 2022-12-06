#!/usr/bin/env python
# coding: utf-8

# # Comparison train y test background and signal

import root_pandas
import glob, sys
import numpy as np
import ROOT as root
import sys

sys.path.append("../root_functions/")
import root_functions as rf

#from importlib import reload
#rf = reload(rf)

#samples train and test to be passed to the BDT 
train = glob.glob("../bdt_train_200fb_Signalregion.root")
test = glob.glob("../bdt_test_200fb_Signalregion.root")


nombre = ['train','test']
samples_path=[train,test]

#dic with the dataframe samples 
ruidos = {}
for i,n in enumerate(nombre):
    try:
        ruidos[n]={}
        ruidos[n]['df'] = root_pandas.read_root(samples_path[i],'treevpho').astype(float) 
        print(n, "bkg ok") #,globals()[n])
    except Exception as e:
        print('---->',n)
        print(e,'\n\n')
        del ruidos[n]

#specifications for the plot, units, ranges, name,
var_opt = {"tau_sig_InvM":{"namevar":"M_{Inv}", "units":"[GeV/c^{2}]", "a": 0.99,"b":2.01 ,"bines":100},
         "tau_sig_deltaE":{"namevar":"#Delta E", "units":"[GeV]","a": -1.5,"b":0.5, "bines":100}, 
         "tau_sigGamma_E":{"namevar":"E_{#gamma}", "units":"[GeV]","a": 0.0,"b":7.0,"bines":100},
         "tau_sigtrack_p_CMS":{"namevar":"P_{e}^{CMS}", "units":"[GeV/c]","a": 0.0,"b":6.0,"bines":100},
         "tau_sig_CosBetweenCM":{"namevar":r"cos #theta _{e-#gamma}^{CMS}", "units":" ","a": -1.0,"b":1.0,"bines":100},
         "thrust":{"namevar":"$thrust$", "units":" ","a": 0.6,"b":1.0,"bines":100},
         "visibleEnergyOfEventCMS":{"namevar":"E^{CMS}_{visible}", "units":"[GeV]","a": 0.3,"b":16.0,"bines":100},
         "cos_lepton_pi_CM":{"namevar":r"cos #theta _{e-#pi}^{CMS}", "units":" ","a": -1.0,"b":1.0,"bines":100},
         "cos_miss_pi_CM":{"namevar":r"cos #theta _{miss-#pi}^{CMS}", "units":" ","a": -1.0,"b":1.0,"bines":100},}

#style Belle 2 experiment
root.gROOT.LoadMacro('../belle2style/root/Belle2Style.C')
root.SetBelle2Style()

df1=ruidos[nombre[0]]['df']#train
df2=ruidos[nombre[1]]['df']#test

#Let's split into signal and bkg to compare the samples separately
def reduce(df,typo):
    if typo == "signal":
        cortesig = 'tau_sig_isSignal == 1' 
        df=df.query(cortesig)
    else:
        cortesbkg = 'tau_sig_isSignal != 1' 
        df=df.query(cortesbkg)
    return df
    
sb="signal"
df1_sig=reduce(df1,sb)
df2_sig=reduce(df2,sb)


sr="background"
df1_bkg=reduce(df1,sr)
df2_bkg=reduce(df2,sr)

#def of the function that include the ratio between the two distributions
def PlotEffy(variable, df_a, df_b, labelss, namevar, namefile,a,b,bins):
    hsr = rf.MakeTH1D("hsr","hsr",bins,a,b,namevar,"Events",linecolor=2)
    rf.FillHist1D(hsr,df_a,variable)
    hsb = rf.MakeTH1D("hsb","hsb",bins,a,b,"x2","y2",linecolor=4)
    rf.FillHist1D(hsb,df_b,variable)
    #hsr.Sumw2()
    #hsb.Sumw2()
    hdiv = rf.createRatio(hsr,hsb,0.8,1.2,namevar,"train/test",9)
    objects=[hsr,hsb]
    optionss=["f","f"]
    l = rf.MakeTLegend(tobjects=objects, labels=labelss, options=optionss)
    c, pad1, pad2 = rf.createCanvasPads()
    pad1.cd()
    root.gPad.SetLogy()
    hsr.Draw("HIST")
    hsb.Draw("sameHIST")
    rf.Belle2Label(0.4,0.88," ")
    rf.Belle2Lumi(0.44,0.78,"MC Simulation: #int L dt = 200 fb^{-1}");
    l.Draw("same")
    pad2.cd()
    hdiv.Draw("pe")
    c.Modified()
    c.Update()
    c.SaveAs(namefile)

# Let's choose the variable to be plotted via a bash file if the nanme of the variable is all, then plot all the distributions
variable= sys.argv[1]
if variable == "all":
    for elemento in var_opt:
        print(elemento)
        name = var_opt[elemento]["namevar"]
        units = var_opt[elemento]["units"]
        namevar = name+""+units
        namefile_sig = f"{elemento}_signal0.png"
        namefile_bkg = f"{elemento}_background0.png"
        labelss= ["train","test"]
        a = var_opt[elemento]["a"]
        b = var_opt[elemento]["b"]
        bins =var_opt[elemento]["bines"]
        print(elemento)
        PlotEffy(elemento,df1_sig, df2_sig, labelss, namevar, namefile_sig,a,b,bins)
        PlotEffy(elemento,df1_bkg, df2_bkg, labelss, namevar, namefile_bkg,a,b,bins)
else:
    print(variable)
    name = var_opt[variable]["namevar"]
    units = var_opt[variable]["units"]
    namevar = name+""+units
    namefile_sig = f"{variable}_signal1.png"
    namefile_bkg = f"{variable}_background1.png"
    labelss= ["train","test"]
    a = var_opt[variable]["a"]
    b = var_opt[variable]["b"]
    bins =var_opt[variable]["bines"]
    PlotEffy(variable,df1_sig, df2_sig, labelss, namevar, namefile_sig,a,b,bins)
    PlotEffy(variable,df1_bkg, df2_bkg, labelss, namevar, namefile_bkg,a,b,bins)
