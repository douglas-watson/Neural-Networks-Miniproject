#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   NEURON miniproject, for the course "Neural networks and
#   biological modelling" 
#
#   This file contains model definitions (neurons) and helper functions (such
#   as I Clamp tests and visualisation functions)
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 14th April 2011
#
#   LICENSE: GNU GPL
#
#################################################

import sys
import os
from copy import copy # copying of arrays

import neuron
import nrn

import numpy as np
import matplotlib.pyplot as plt

# The HH_traub and IM_cortex models should be imported automatically.

# Set temperature
h = neuron.h
h.celsius = 36

##############################
# Model definitions
##############################

# Define a generic section class, that will be used to initalize the three
# models HH, HHx, and HHxx, then customised.

class DefaultSection(nrn.Section):

    """ Defines the default values for all the somas we will use """

    def __init__(self, name, mechanism='hh2'):
        nrn.Section.__init__(self)
        self.name = name

        self.L = 67        # 67 um length
        self.diam = 67     # same for diameter
        self.Ra = 100      # intracellular resistivity
        self.cm = 1         # capacitance

        # Add passive membrane mechanism
        self.insert('pas')
        self(0.5).pas.g = 0.00015 # conductivity
        self(0.5).pas.e = -70.0   # reversal potential

        # And H-H model, with a sodium and potassium channel.
        self.insert(mechanism)
        self.ek = -100
        self.ena = 50
        if mechanism == 'hh2':
            self.vtraub_hh2 = -55
            self.gnabar_hh2 = 0.05
            self.gkbar_hh2 = 0.005

        # And 40 alpha synapses equally distributed along the section:
        self.synapses = []
        for i in range(40):
            # TODO check units
            syn = h.AlphaSynapse(0.5, sec=self)
            syn.tau = 2 # 2 ms
            syn.e = 0   # 0 mV reversal potential
            syn.gmax = 0.005*0 # uS, initially inactive
            self.synapses.append(syn)

    def reset_synapses(self):
        """ Inactivates all synapses. """
        [ setattr(syn, 'gmax', 0) for syn in self.synapses ]

    def activate_synapses(self, onset=0, N=-1, gmax=0.005):
        """ Activates N synapses at time 'onset', setting them to conductance
        gmax. 
        
        INPUT
        onset - time of activation, in ms
        N - number of synapses to activate. -1 to activate all
        gmax - maximum conductance when active
        """
        [ (setattr(syn, 'gmax', gmax), setattr(syn, 'onset', onset)) 
                for syn in self.synapses[:N] ]

class DefaultDendrite(DefaultSection):

    """ 
    Defines the default values for the dendrites we will use.
    
    This class just sets constants. Connections have to be established after
    instantiation. 

    All the methods from DefaultSection are inherited, therefore reset_synapses
    and activate_synapses also available.
    """

    def __init__(self):
        nrn.Section.__init__(self)

        self.Ra = 123       # ohm*cm intracellular resistivity
        self.cm = 2         # uF/cm^2 capacitance
        self.L = 500        # um length
        self.diam = 3       # um length

        # Passive mechanism
        self.insert('pas')
        self.nseg = 50
        self(0.5).pas.g = 0.0001   # S/cm^2 conductance
        self(0.5).pas.e = -70.0   # mV reversal potential 

        self.synapses = []  # no synapses initially.

    def insert_synapses(self, N=50, pos=0.5):
        """ Creates N synapses at pos """
        for i in range(N):
            syn = h.AlphaSynapse(pos, sec=self)
            syn.tau = 2 # ms
            syn.e = 0   # mV reversal potential
            syn.gmax = 0.002 # uS
            self.synapses.append(syn)

    def insert_inhibitory_synapse(self, pos=0.5, gmax=-0.01):
        """ Create an inhibitory synapse at position pos """
        syn = h.AlphaSynapse(pos, sec=self)
        syn.tau = 5 # ms
        syn.e = -70 # mV reversal potential
        syn.gmax = gmax
        self.inhib_synapse = syn

################################
# Testing and simulation control
################################

def run_IClamp(sec, pos=0.5, delay=0, dur=100, amp=10, dt=0.025, tstop=30, 
        v_init=-70, var='v', rec_pos=0.5):
    # TODO again, make sure integration units are actually seconds.
    """ 
    Simulate a current clamp measurement on section *sec*, stimulated by step
    current. Returns an array of (time, voltage) pairs.

    INPUT:

    Arguments for IClamp:
    sec - section (HH, HHx, ...)
    pos - position of electrode along section (typically 0.5)
    delay - delay before step in ms
    dur - duration of step in ms
    amp - amplitude of current in nA
    rec_pos - position to record voltage at

    Arguments for simulation:
    dt - timestep in ms
    tstop - endtime in ms!
    v_init - initial membrane potential in mV
    var - the variable to log

    """
    # Define stimulate HH in the middle.
    stim = h.IClamp(pos, sec=sec)
    stim.delay = delay
    stim.dur =  dur
    stim.amp = amp

    # Simulation control
    # TODO make sure units are actually seconds
    h.dt = dt
    h.finitialize(v_init)
    h.fcurrent()
    
    # Run simulation: integrate and record data
    data = np.array([])  # array of (time, voltage) points
    while h.t < tstop:
        h.fadvance()
        data = np.reshape(np.append(data, [h.t, getattr(sec(rec_pos), var)]), 
                (-1, 2))
    return data

def quick_IClamp(sec, pos=0.5, delay=0, dur=100, amp=10, dt=0.025, tstop=30,
        v_init=-70):
    """
    
    Quick "debug" run of a I clamp. Runs the simulation and displays a graph.
    Intented for interactive use.

    """

    data = run_IClamp(sec, pos, delay, dur, amp, dt, tstop, v_init)
    t, v = np.transpose(data)

    ax = plt.axes()
    ax.plot(t, v, 'k-')
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Membrane Potential [mV]")
    plt.show()

################################
# Helper functions
################################

def spiketimes(data, v_th=0.5):
    """Given voltage and time, returns array of spike times

    Note: Code ripped off from one of the python exercise examples.

    INPUT:

    data - 2D array of [time, voltage] pairs

    """

    t, v = np.transpose(data)
    v_above_th = v>v_th
    idx = np.nonzero((v_above_th[:-1]==False)&(v_above_th[1:]==True))
    return t[idx[0]+1]

def spikefreq(data, v_th=0.5):
    """Given voltage and time, returns spiking frequency

    INPUT:

    data - 2D array of [time, voltage] pairs

    """
    times = spiketimes(data, v_th=v_th)
    if len(times) > 1:
        freq = 1.0/np.mean(np.diff(times))
    else:
        freq = 0
    return freq


################################
# Visualisation
################################

def U_vs_t(data, linestyle='k-', ax=None):
    """ Returns a U vs t plot for data 
    
    INPUT
    
    data - an array of [t, v] pairs
    linestyle - matlab-style code for the linestyle
    """
    if ax is None: # no axes provided, set up some:
        ax = plt.axes()
        ax.set_xlabel("Time [ms]")
        ax.set_ylabel("Membrane potential [mV]")

    t, v = np.transpose(data)
    ax.plot(t, v, linestyle)
    ax.set_ylim(-80, 100)

    return ax

def f_vs_I(data, linestyle='-', label="", color="black", v_th=-40):
    """ Returns plot of spiking frequency versus stimulation current
    
    INPUT
    
    data - a list of [I, clampdata] pairs, where clampdata is an array of [t,
    v] pairs.
    linestyle - matlab-style code for the linestyle
    
    """
    ax = plt.axes()
    ax.set_xlabel("Current [nA]")
    ax.set_ylabel("Spiking Frequency [kHz]")

    points = [[I, spikefreq(d, v_th=v_th)] for I, d in data]
    I, f = np.transpose(points)
    ax.plot(I, f, linestyle, color=color, label=label)

    return ax

def figsave(filename, size=[20, 8], folder="../figures/"):
    """
    Saves the current graph. this is just a shortcut to avoid having to specify
    the folder and figure size everytime.

    INPUT

    filename - Name of the file. Extension determines filetype
    size - figsize, as a two-element list
    folder - folder to save the figures in.

    """

    plt.savefig(os.path.join(folder, filename), figsize=size)

def newplot(xlabel=None, ylabel=None, title=None):
    """
    Returns a new set of labelled axes for plotting.

    INPUT
    xlabel - x-axis label
    ylabel - y-axis label
    title - figure title
    """
    fig = plt.figure()
    fig.subplots_adjust(left=0.11)
    ax = plt.axes()
    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is not None: ax.set_ylabel(ylabel)
    if title  is not None: ax.set_title(title)

    return ax

colours = lambda N: [plt.cm.jet(i/float(N)) for i in range(N)]

if __name__ == '__main__':
    HH = DefaultSection("HH")
    # Run simulation and plot
    data = run_IClamp(sec=HH, delay=0, dur=20, amp=40, tstop=30)
    # ax = U_vs_t(data)

    # Type I or II?
    data = []
    for I in np.arange(5, 1000, 10):
        clampdata = run_IClamp(sec=HH, delay=0, dur=10, amp=I, tstop=30)
        data.append([I, clampdata])
    ax = f_vs_I(data, 'k.')
        
    plt.show()
