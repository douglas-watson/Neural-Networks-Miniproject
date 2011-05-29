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

h.celsius = 36

# 1.1 - Define the three different neuron models:
HH = DefaultSection("HH")
HHx = DefaultSection("HHx")
HHx.insert("ix")
HHxx = DefaultSection("HHxx")
HHxx.insert("ixx")

# data = run_IClamp(sec=HH, delay=15, dur=150, amp=.30, tstop=150, dt=0.01)
# ax = U_vs_t(data)
# plt.show()

# 1 - Run Skander's example stimulations, for comparison
def skander_examples():
    data = run_IClamp(HH, delay=50, dur=500, amp=0.5, tstop=600)
    ax = U_vs_t(data)
    ax.set_xlim(0, 600)
    ax.set_ylim(-80, 60)
    ax.set_title("HH, I=0.5 nA")
    figsave("1-HH_skander-example.pdf")

    plt.clf()
    data = run_IClamp(HHx, delay=50, dur=500, amp=4.6, tstop=600)
    ax = U_vs_t(data)
    ax.set_xlim(0, 600)
    ax.set_ylim(-80, 60)
    ax.set_title("HHx, I = 4.6 nA")
    figsave("1-HHx_skander-example.pdf")

    plt.clf()
    data = run_IClamp(HHxx, delay=50, dur=500, amp=0.26, tstop=600)
    ax = U_vs_t(data)
    ax.set_xlim(0, 600)
    ax.set_ylim(-80, 60)
    ax.set_title("HHxx, I=0.26 nA")
    figsave("1-HHxx_skander-example.pdf")

# 1.2 - Type I or II?
def prob1_2():
    fig = plt.figure(figsize=[5.3, 3])
    fig.subplots_adjust(left=0.15, bottom=0.15)
    col = colours(4)

    for model in (HH, HHxx):
        data = []
        for I in np.arange(0, 1, 0.025):
            clampdata = run_IClamp(sec=model, delay=0, dur=100, amp=I, 
                    tstop=100)
            data.append([I, clampdata])
        ax = f_vs_I(data, '.', label=model.name, v_th=0, color=col.pop(0))

    # HHx requires more current
    data = []
    for I in np.arange(4, 5, 0.02):
        clampdata = run_IClamp(sec=HHx, delay=0, dur=100, amp=I, 
                tstop=100)
        data.append([I, clampdata])
    ax = f_vs_I(data, '.', label=HHx.name, v_th=0, color=col.pop(0))

    ax.legend(loc="upper right")
    figsave("1_2-neuron_type.pdf")

# 1.3 - How many synapses need to be open for a spike?
def prob1_3():
    prob1_3_run(HH, [1, 2, 3, 4, 5, 10, 40])
    prob1_3_run(HHx, [1, 10, 20, 23, 24, 25, 30, 40])
    prob1_3_run(HHxx, [1, 2, 3, 4, 10, 40])

def prob1_3_run(model, Ns):
    ax = newplot("Time [ms]", "Membrane voltage [mV]", 
            "Response to synaptic current")
    col = colours(len(Ns))
    for i in Ns:
        # Reset synapses, then activate just the appropriate number
        model.reset_synapses()
        model.activate_synapses(N=i, onset=10)
        # no current injection, we just want synaptic current
        data = run_IClamp(sec=model, delay=0, dur=20, amp=0, tstop=50, dt=0.01)
        t, v = np.transpose(data)
        ax.plot(t, v, '-', color=col.pop(0), label=str(i))
    ax.legend()
    figsave("1_3-%s_synapse_number.pdf" % model.name)

# 1.4 - Number of activated synapses vs EPSP in subthreshold regime
def prob1_4():
    ax = newplot("Number of activated synapses", "Max voltage [mV]")
    col = colours(5)
    for model in (HH, HHx, HHxx):
        # reset synapses:
        max_v = []
        for i in range(len(model.synapses)):
            # activate the synapses
            model.reset_synapses()
            model.activate_synapses(N=i, onset=10)
            # Run current clamp subthreshold
            data = run_IClamp(sec=model, delay=5, dur=150, amp=.0, tstop=50,
                    dt=0.01)
            max_v.append([i, data[:,1].max()])
        n, v = np.transpose(max_v)
        ax.plot(n, v, '.', label=model.name, color=col.pop(0))
    ax.legend(loc="lower right")
    figsave("1_4-number_of_synapses.pdf")

    ax.set_xlim(0, 6)
    ax.set_ylim(-80, -40)
    figsave("1_4-number_of_synapses_zoom.pdf")

if __name__ == '__main__':
    # skander_examples()
    prob1_2()
    #prob1_3()
    #prob1_3()
    #prob1_4()
    # prob1_3_run(HH, [1, 2, 3, 4, 5, 10, 40])
