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

import numpy as np
import matplotlib.pyplot as plt

# The HH_traub and IM_cortex models should be imported automatically.

# Set temperature
h = neuron.h
h.celsius = 36

######################
# Model definitions
######################

# Create three models of a soma: HH, HHx, and HHxx, according to instructions
# given.

### HH
######################

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
    syn.e = -30   # 0 mV reversal potential
    syn.gmax = 0.005 # uS

######################
# Testing and simulation control
######################

def run_IClamp(sec, pos=0.5, delay=0, dur=100, amp=50, dt=25, tstop=5, 
        v_init=-70):
    # TODO again, make sure integration units are actually seconds.
    """ 
    Simulate a current clamp measurement on section *sec*. Returns an array of
    (time, voltage) pairs.

    Arguments for IClamp:
    * sec: section (HH, HHx, ...)
    * pos: position of electrode along section (typically 0.5)
    * delay: delay before step in ms
    * dur: duration of step in ms
    * amp: amplitude of current in nA

    Arguments for simulation:
    * dt: timestep in ms
    * tstop: endtime in SECONDS!
    * v_init: initial membrane potential in mV
    """
    # Define stimulate HH in the middle.
    stim = h.IClamp(pos, sec=sec)
    stim.delay = delay
    stim.dur =  dur
    stim.amp = amp

    # Simulation control
    # TODO make sure units are actually seconds
    h.dt = dt / 1000.0  # integration timestep: convert to seconds
    h.finitialize(v_init)
    h.fcurrent()
    
    # Run simulation: integrate and record data
    data = np.array([])  # array of (time, voltage) points
    while h.t < tstop:
        h.fadvance()
        data = np.reshape(np.append(data, [h.t, HH(0.5).v]), (-1, 2))
    return data

if __name__ == '__main__':
    # Run example simulation
    # Create a graph
    ax = plt.axes()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Membrane potential [mV]")

    # Run simulation and plot
    data = run_IClamp(sec=HH, delay=100, dur=100, amp=50, tstop=30)
    t, v = np.transpose(data)
    ax.plot(t, v, 'k-')
    plt.show()
