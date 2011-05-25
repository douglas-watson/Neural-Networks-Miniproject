#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   Solutions to part 2 of the NEURON miniproject 
#
#   AUTHOR: Thibault Dupont <thibault.dupont@epfl.ch> & 
#           Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 23 May 2011
#
#   LICENSE: GNU GPL
#
#################################################

import sys
from toolset import *

# Create HH soma, a 18 um x 18 um
soma = DefaultSection('soma', 'hh')
soma.L = 18
soma.diam = 18

# Attach a dendrite directly to the soma
dend1 = DefaultDendrite()
dend1.connect(soma, 0, 1)

# Attach two dendrites to the first, forming a y, and add synapses at their
# other extremity
dend2 = DefaultDendrite()
dend2.connect(dend1, 0, 1)
dend2.insert_synapses()

dend3 = DefaultDendrite()
dend3.connect(dend1, 0, 1)
dend3.insert_synapses()

# 2.2 How many synapses for a spike?

def prob2_2():
    prob2_2_a()
    prob2_2_b()
    prob2_2_c()

def prob2_2_a():
    ax = newplot("Time [ms]", "Membrane voltage [mV]", "Synapses on Dendrite 2")
    for i in range(1, 50, 5):
        # Reset synapses, then activate just the appropriate number
        dend2.reset_synapses()
        dend2.activate_synapses(N=i, onset=30)
        # no current injection
        data = run_IClamp(sec=soma, delay=0, dur=20, amp=0, tstop=100, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=plt.cm.jet(i * 1/40.), label=str(i))
    ax.legend()
    figsave("2.2-%s_synapse_number.pdf" % 'dend2')

def prob2_2_b():
    ax = newplot("Time [ms]", "Membrane voltage [mV]", "Synapses on Dendrite 3")
    for i in np.arange(1, 50, 5):
        # Reset synapses, then activate just the appropriate number
        dend3.reset_synapses()
        dend3.activate_synapses(N=i, onset=30)
        # no current injection
        data = run_IClamp(sec=soma, delay=0, dur=20, amp=0, tstop=100, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=plt.cm.jet(i * 1/40.), label=str(i))
    ax.legend()
    figsave("2.2-%s_synapse_number.pdf" % 'dend3')

def prob2_2_c():
    ax = newplot("Time [ms]", "Membrane voltage [mV]", 
            "Synapses on Dendrite 2 & 3")
    for i in np.arange(1, 40, 4):
        # Reset synapses, then activate just the appropriate number
        dend2.reset_synapses()
        dend2.activate_synapses(N=i, onset=30)
        dend3.reset_synapses()
        dend3.activate_synapses(N=i, onset=30)
        # no current injection
        data = run_IClamp(sec=soma, delay=0, dur=20, amp=0, tstop=100, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=plt.cm.jet(i * 1/40.), label=str(i))
    ax.legend()
    figsave("2.2-%s_synapse_number.pdf" % 'dend2and3')

def prob2_2_d():
    """ Open 40 synapses, and observe peak propagation """
    dend2.reset_synapses()
    dend3.reset_synapses()
    dend2.activate_synapses(onset=30, N=40)
    ax = newplot("Time [ms]", "Voltage [mV]")

    for x in [0.2, 0.5, 1]:
        data = run_IClamp(dend2, pos=0, rec_pos=x, amp=0, dur=100, tstop=100)
        t, v = data.transpose()
        ax.plot(t, v, label=str(x))
    ax.legend()
    figsave("2.2-spike_propagation.pdf")


# 2.4 - Inhibitory synapse
def prob2_4():
    dend1.insert_inhibitory_synapse()
    # TODO how much gmax to veto a spike?

if __name__ == '__main__':
    prob2_2_b()
    # prob2_4()
