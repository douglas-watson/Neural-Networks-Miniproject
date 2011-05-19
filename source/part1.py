#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   Solutions to part 1 of the NEURON miniproject. 
#
#   AUTHORS: Thibault Dupont <thibault.dupont@epfl.ch>
#            Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 7 May 2010
#
#   LICENSE: GNU GPL
#
#################################################

import sys
from toolset import *

# 1.1 - Define the three different neuron models:
HH = DefaultSection("HH")
HHx = DefaultSection("HHx")
HHx.insert("ix")
HHxx = DefaultSection("HHxx")
HHxx.insert("ixx")

# data = run_IClamp(sec=HH, delay=15, dur=150, amp=.30, tstop=150, dt=0.01)
# ax = U_vs_t(data)
# plt.show()

# 1.2 - Type I or II?
def prob1_2():
    for model in (HH, HHx, HHxx):
        data = []
        for I in np.arange(0, 2, 0.1):
            clampdata = run_IClamp(sec=model, delay=0, dur=100, amp=I, 
                    tstop=100)
            data.append([I, clampdata])
        ax = f_vs_I(data, '.', label=model.name, v_th=-40)
    ax.legend()
    figsave("1.2-neuron_type.pdf")

# 1.3 - How many synapses need to be open for a spike?
def prob1_3():
    prob1_3_run(HH)
    prob1_3_run(HHx)
    prob1_3_run(HHxx)

def prob1_3_run(model):
    ax = plt.axes()
    ax.clear()
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Membrane voltage [mV]")
    ax.set_title("Effect of opening synapses")
    for i in range(1, 40):
        # Reset synapses, then activate just the appropriate number
        [ setattr(syn, 'gmax', 0) for syn in model.synapses ]
        [ setattr(syn, 'onset', 10) for syn in model.synapses ]
        [ setattr(syn, 'gmax', 0.005) for syn in model.synapses[:i] ]
        # no current injection
        data = run_IClamp(sec=model, delay=0, dur=20, amp=0, tstop=50, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=plt.cm.jet(i * 1/30.), label=str(i))
    ax.legend()
    figsave("1.3-%s_synapse_number.pdf" % model.name)

# 1.4 - Number of activated synapses vs EPSP in subthreshold regime
def prob1_4():
    ax = plt.axes()
    ax.clear()
    ax.set_xlabel("Number of activated synapses")
    ax.set_ylabel("Final voltage [mV]")
    for model in (HH, HHx, HHxx):
        # reset synapses:
        [ setattr(syn, 'gmax', 0) for syn in model.synapses ]
        final_v = []
        for i in range(len(model.synapses)):
            # activate the synapses
            model.synapses[i].gmax = 0.005 # uS
            model.synapses[i].onset = 0
            # Run current clamp subthreshold
            data = run_IClamp(sec=model, delay=5, dur=150, amp=.1, tstop=50,
                    dt=0.01)
            final_v.append([i, data[-1,1]])
        n, v = np.transpose(final_v)
        ax.plot(n, v, '.', label=model.name)
    ax.legend()
    figsave("1.4-number_of_synapses.pdf")

    # HHxx is interesting. Let's look deeper:
    ax = plt.axes()
    ax.clear()
    ax.set_xlabel("Number of activated synapses")
    ax.set_ylabel("Final voltage [mV]")
    for j in (.1, .15, .20): # different current amplitudes
        # reset synapses:
        [ setattr(syn, 'gmax', 0) for syn in HHxx.synapses ]
        final_v = []
        for i in range(len(HHxx.synapses)):
            # activate another synapses
            HHxx.synapses[i].gmax = 0.005 # uS
            HHxx.synapses[i].onset = 0
            # Run current clamp subthreshold
            data = run_IClamp(sec=HHxx, delay=5, dur=150, amp=j, tstop=50,
                    dt=0.01)
            final_v.append([i, data[-1,1]])
        n, v = np.transpose(final_v)
        ax.plot(n, v, '.', label="%.2f nA" % j)
    ax.legend()
    figsave("1.4-HHxx_number_of_synapses.pdf")

if __name__ == '__main__':
    prob1_3()
