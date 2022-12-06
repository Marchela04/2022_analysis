#!/bin/bash

variables=("tau_sig_InvM" "tau_sig_deltaE" "tau_sigGamma_E" "tau_sigtrack_p_CMS" "tau_sig_CosBetweenCM" "thrust" "visibleEnergyOfEventCMS" "cos_lepton_pi_CM" "cos_miss_pi_CM")

#if var = "all", then make all the plots
var="visibleEnergyOfEventCMS" #all also via ${variables[1]}

python3 comparison_sbsignalregion.py ${var}
