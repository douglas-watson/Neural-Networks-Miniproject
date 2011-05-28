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
from toolset2 import *


# Create HH soma, a 18 um x 18 um
soma = DefaultSection('soma', 'hh')

# Attach a dendrite directly to the soma
dend1 = DefaultDendrite()
dend1.connect(soma, 0, 1)
dend1.insert('pas')
dend1.reset_synapses()

# Attach two dendrites to the first, forming a y, and add synapses at their
# other extremity
dend2 = DefaultDendrite()
dend2.connect(dend1, 0, 1)
dend2.insert_synapses(N=100)
dend2.insert('ix')
dend2.gkbar_ix = 2e-5
dend2.reset_synapses()

dend3 = DefaultDendrite()
dend3.connect(dend1, 0, 1)
dend3.insert_synapses()
dend3.insert('ixx')
dend3.reset_synapses()

# dend4 = DefaultDendrite()
# dend4.connect(dend1, 0, 1)
# dend4.insert_synapses(N=1000)

# 2.1 How many synapses for a spike?

def prob2_1():
    prob2_1_a()
    prob2_1_b()
    prob2_1_c()

def prob2_1_a(Ns):
    ax = newplot("Time [ms]", "Membrane voltage [mV]", "Synapses on Dendrite 2")
    col = colours(len(Ns))
    for i in Ns:
        # Reset synapses, then activate just the appropriate number
        dend2.reset_synapses()
        dend2.activate_synapses(N=i, onset=20, gmax=0.002)
        # no current injection
        data = run_IClamp(sec=soma, delay=0, dur=0, amp=0, tstop=80, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=col.pop(0), label=str(i))
    ax.legend()
    ax.set_ylim(0, 80)
    figsave("2.1-%s_synapse_number.pdf" % 'dend2')

def prob2_1_b(Ns):
    ax = newplot("Time [ms]", "Membrane voltage [mV]", "Synapses on Dendrite 3")
    col = colours(len(Ns))
    for i in Ns:
        # Reset synapses, then activate just the appropriate number
        dend3.reset_synapses()
        dend3.activate_synapses(N=i, onset=20)
        # no current injection
        data = run_IClamp(sec=soma, pos=1, delay=0, dur=0, amp=0, tstop=80, 
                dt=0.01, v_init=-70)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=col.pop(0), label=str(i))
    ax.legend()
    ax.set_ylim(0, 80)
    figsave("2.1-%s_synapse_number.pdf" % 'dend3')

def prob2_1_c(Ns):
    ax = newplot("Time [ms]", "Membrane voltage [mV]", 
            "Synapses on Dendrite 2 \& 3")
    col = colours(len(Ns))
    for i in Ns:
        # Reset synapses, then activate just the appropriate number
        dend2.reset_synapses()
        dend3.reset_synapses()
        dend2.activate_synapses(N=i, onset=20)
        dend3.activate_synapses(N=i, onset=20)
        # no current injection
        data = run_IClamp(sec=soma, delay=0, dur=20, amp=0, tstop=80, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=col.pop(0), label=str(i))
    ax.legend()
    figsave("2.1-%s_synapse_number.pdf" % 'dend2and3')

def prob2_1_d():
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
    figsave("2.1-spike_propagation.pdf")

def prob2_1_e():
    """ Just open 100'000 synapses """
    ax = newplot("Time [ms]", "Membrane voltage [mV]", "1'000 Synapses")
    # Reset synapses, then activate just the appropriate number
    dend4.reset_synapses()
    dend4.activate_synapses(N=1000, onset=30)
    # no current injection
    data = run_IClamp(sec=dend4, pos=0.5, delay=0, dur=20, amp=0, tstop=100, dt=0.01)
    t, v = np.transpose(data)
    ax.plot(t, v, '-', color=plt.cm.jet(1/40.))
    figsave("2.1-1000_synapses_measureDendrite.pdf") 

# 2.4 - Inhibitory synapse
def prob2_4():
    dend1.insert_inhibitory_synapse()
    # TODO how much gmax to veto a spike?

if __name__ == '__main__':
    # prob2_1_b()
    # prob2_1_a([0, 47, 50, 51, 53, 55])
    # prob2_1_b([0, 15, 17, 18, 19, 20])
    prob2_1_c([0, 6, 7, 8, 9, 10, 11])
    # prob2_4()
