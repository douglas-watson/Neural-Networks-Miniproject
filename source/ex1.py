#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   Exercice 1 of the NEURON miniproject, for the course "Neural networks and
#   biological modelling" 
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 14th April 2011
#
#   LICENSE: GNU GPL
#
#################################################

import neuron
import nrn

# The HH_traub and IM_cortex models should be imported automatically.

# Set temperature
h = neuron.h
h.celsius = 36

######################
# Model definitions
######################

# Create three models of a soma: HH, HHx, and HHxx, according to instructions
# given.

HH = nrn.Section()
# TODO check units of the following definitions.
HH.L = 67        # set length to 67 um
HH.diam = 67     # same for diameter
HH.Ra = 100      # intracellular resistivity

# Add passive membrane mechanism
HH.insert('pas')
HH(0.5).pas.g = 0.00015 # conductivity
HH(0.5).pas.e = -70.0   # reversal potential

# And H-H model, for a sodium and potassium channel.
HH.insert('hh2')
HH.insert('na_ion')
HH.insert('k_ion')

# And 40 alpha synapses equally distributed along the section:
for i in range(40):
    # TODO check units
    syn = h.AlphaSynapse(i/40.0, sec=HH)
    syn.tau = 2 # 2 ms
    syn.e = 0   # 0 mV reversal potential
    syn.gmax = 0.005 # uS

######################
# Testing
######################

# stimulate HH in the middle.
stim = h.IClamp(0.5, sec=HH)
stim.delay = 0 
stim.dur =  10 # 10 ms duration # TODO change to step
stim.amp = 10 # 10 nA 


######################
# Simulation control
######################

h.dt = 0.0025       # integration timestep

