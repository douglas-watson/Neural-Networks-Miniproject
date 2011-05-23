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

def prob2_2_a():
    ax = plt.axes()
    ax.clear()
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Membrane voltage [mV]")
    ax.set_title("Effect of opening synapses")
    for i in range(1, 40):
        # Reset synapses, then activate just the appropriate number
        dend2.reset_synapses()
        dend2.activate_synapses(N=i, onset=30)
        # for syn in dend2.synapses:
            # print syn.gmax, syn.onset
        # if i > 2:
            # sys.exit(0)
        # no current injection
        data = run_IClamp(sec=soma, delay=0, dur=20, amp=0, tstop=100, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=plt.cm.jet(i * 1/40.), label=str(i))
    ax.legend()
    figsave("2.1-%s_synapse_number.pdf" % 'dend2')

if __name__ == '__main__':
    prob2_2_a()
