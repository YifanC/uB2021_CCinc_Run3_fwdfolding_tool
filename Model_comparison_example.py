#import stuff you eventually need
import numpy as np
import os
import ROOT
import math
from array import array

import imp
CC = imp.load_source('CC_inclusive_2D_lib','CC_inclusive_2D_lib.py')

data_POT = 2.144e+20

#change output path, input file corresponding to the generator name
generator_name = "GiBUU"


inputdir = "input/" # please give here path to inputfile
outputdir = "plots/" + generator_name + "/"

# make output dir if not existing
try:
    os.stat(outputdir)
except:
    os.mkdir(outputdir)

# load model prediction
# 'FF_generators.root' stores a few generator predictions, which one can read in as examples
f_pred = ROOT.TFile.Open(inputdir+'FF_pred.root', 'read')

# load file with uboone CV files + systematics
f_input = ROOT.TFile.Open(inputdir+'FF_input.root', 'read')

h_true_rate = f_pred.Get('h_true_rate_GiBUU')

frac_det = CC.return_detsys_covar(h_true_rate,data_POT)
frac_other = CC.return_other_covar(h_true_rate,data_POT)
frac_det_all,bkg_all = CC.return_all_covar(h_true_rate,data_POT)
frac_det_flux = CC.return_flux_covar(h_true_rate,data_POT)
frac_crt = CC.return_crt_covar(h_true_rate,data_POT)
frac_dirt = CC.return_dirt_covar(h_true_rate,data_POT)
frac_stat = CC.return_stat_covar(h_true_rate,data_POT)
frac_pot = CC.return_pot_covar(h_true_rate,data_POT)


frac_tot = frac_det+frac_other+frac_det_all+frac_det_flux+frac_crt+frac_dirt+frac_stat+frac_pot


h_data_rate = f_input.Get('h_data') # load data historgram

# compare data with the cross-section model prediction in the reconstructed phase space
CC.eventrate_comparison(h_data_rate,h_true_rate,data_POT,frac_tot, 'EventRate_'+generator_name, outputdir)

f_input.Close()
f_pred.Close()















