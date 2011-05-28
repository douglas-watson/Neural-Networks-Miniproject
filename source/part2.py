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
dend1 = DefaultDendrite("Dend. 1")
dend1.connect(soma, 0, 1)
dend1.insert('pas')
dend1.reset_synapses()

# Attach two dendrites to the first, forming a y, and add synapses at their
# other extremity
dend2 = DefaultDendrite("Dend. 2")
dend2.connect(dend1, 0, 1)
dend2.insert_synapses(N=100)
dend2.insert('ix')
dend2.gkbar_ix = 2e-5
dend2.reset_synapses()

dend3 = DefaultDendrite("Dend. 3")
dend3.connect(dend1, 0, 1)
dend3.insert_synapses()
dend3.insert('ixx')
dend3.reset_synapses()

# dend4 = DefaultDendrite("dend4")
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
    ax = newplot("Time [ms]", "Voltage [mV]", "Spike propagation along Dend. 1")
    col = colours(6)
    for x in [0, 0.5, 1]:
        dend1.reset_synapses()
        dend2.reset_synapses()
        dend3.reset_synapses()
        dend2.activate_synapses(onset=10, N=55)
        data = run_IClamp(sec=dend1, pos=0, rec_pos=x, amp=0, dur=100, 
                tstop=100)
        t, v = data.transpose()
        ax.plot(t, v, label=str(x), color=col.pop(2))
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

def prob2_2():
    """ Observe synaptic integration """
    ax = newplot("Number of activated synapses", "Max voltage [mV]")
    col = colours(4)
    for dend in (dend2, dend3):
        dend2.reset_synapses()
        dend3.reset_synapses()
        # reset synapses:
        max_v = []
        for i in range(len(dend.synapses)):
            # activate the synapses
            dend.reset_synapses()
            dend.activate_synapses(N=i)
            # Run current clamp subthreshold
            data = run_IClamp(sec=soma, delay=5, dur=0, amp=0, tstop=50,
                    dt=0.01)
            max_v.append([i, data[:,1].max()])
        n, v = np.transpose(max_v)
        ax.plot(n, v, '.', label=dend.name, color=col.pop(0))
    # on both at once
    for i in range(0, 30):
        dend2.reset_synapses()
        dend3.reset_synapses()
        dend2.activate_synapses(N=i)
        dend3.activate_synapses(N=i)
        data = run_IClamp(sec=soma, delay=5, dur=0, amp=0, tstop=50,
                dt=0.01)
        max_v.append([i, data[:,1].max()])
    n, v = np.transpose(max_v)
    ax.plot(n, v, '.', label="Dend. 2 \& 3", color=col.pop(0))

    ax.legend(loc="lower right")
    figsave("2.2-Synaptic_summation.pdf")

def prob2_2_b():
    """ 2D search, for number of neurons activated on each dendrite """
    max_v = [] # store maximum voltage of each run
    for i in range(0, 60):
        for j in range(0, 30):
            print i, j
            dend2.reset_synapses()
            dend3.reset_synapses()
            dend2.activate_synapses(N=i, onset=0)
            dend3.activate_synapses(N=j, onset=0)
            data = run_IClamp(sec=soma, delay=0, dur=0, amp=0, tstop=25,
                    dt=0.01)
            max_v.append([i, j, data[:,1].max()])
    np.savetxt('../data/synaptic_summation.dat', max_v)

# 2.3 - Inhibitory synapse
def prob2_3_a():
    """ Open inhibitory synapse, to observe its dynamics """
    ax = newplot("Time [ms]", "Voltage [mV]", "Inhibitory spike")
    dend1.insert_inhibitory_synapse()
    dend2.reset_synapses()
    dend3.reset_synapses()
    dend1.reset_inhibitory_synapse()
    dend1.activate_inhibitory_synapse(gmax=-0.05)
    data = run_IClamp(sec=dend1, rec_pos=0.5, amp=0, dur=0, tstop=100)
    t, v = data.transpose()
    ax.plot(t, v, '-')
    figsave("2.3-inhibitory_spike_alone.pdf")

def prob2_3_b():
    """ Thwart spike with inhibitory synapse 
    
    We know from the previous experiment (prob2_3_a) that the spike takes about
    10 ms to take full effect. Therefore, we must start it approx 10 ms before
    the expected peak of the EPSP (about 15 ms after synaptic opening). 
    
    On second note, this doesn't work, so we'll just do a big search on dt and
    gmax """

    dt = 10
    onset = 10

    # ax = newplot("Time [ms]", "Voltage [mV]", 
            # "Veto spike %d ms after synaptic onset" % dt)
    # Setup inhibitory synapse
    dend1.insert_inhibitory_synapse()

    # try a few values of gmax, see what works best.
    # col = colours(6)
    max_v = []
    for dt in range(-2, 15):
        for gmax in np.arange(-0.01, -0.10, -0.01):
            # reset everything
            dend1.reset_inhibitory_synapse()
            dend2.reset_synapses()
            dend3.reset_synapses()
            # activate 1.5 * N_max synapses on dend3  
            dend3.activate_synapses(onset=10, N=27)
            dend1.activate_inhibitory_synapse(gmax=gmax, onset=10+dt)
            data = run_IClamp(sec=soma, pos=0.5, rec_pos=0.5, amp=0, dur=0, 
                    tstop=30)
            # t, v = data.transpose()
            # ax.plot(t, v, '-', color=col.pop(0), label=str(gmax))
            max_v.append([dt, gmax, data[:,1].max()])
            print max_v[-1]
    # ax.legend()
    # figsave("2.3-veto_spike.pdf")
    np.savetxt("../data/inhibitory_synapse.dat", max_v)

def prob2_3_c():
    """ Thwart spike with inhibitory synapse 
    
    This func just plot the timeseries again. """

    ax = newplot("Time [ms]", "Voltage [mV]", 
            "Inhibitory spike, vary $g_{max}$")
    col = colours(13)

    dt = 10
    onset = 10

    # ax = newplot("Time [ms]", "Voltage [mV]", 
            # "Veto spike %d ms after synaptic onset" % dt)
    # Setup inhibitory synapse
    dend1.insert_inhibitory_synapse()

    # try a few values of gmax, see what works best.
    # col = colours(6)
    for gmax in np.arange(-0.04, -0.05, -0.001):
        # reset everything
        dend1.reset_inhibitory_synapse()
        dend2.reset_synapses()
        dend3.reset_synapses()
        # activate 1.5 * N_max synapses on dend3  
        dend3.activate_synapses(onset=10, N=27)
        dend1.activate_inhibitory_synapse(gmax=gmax, onset=10+dt)
        data = run_IClamp(sec=soma, pos=0.5, rec_pos=0.5, amp=0, dur=0, 
                tstop=100)
        t, v = data.transpose()
        ax.plot(t, v, '-', color=col.pop(0), label=str(gmax))
    ax.legend()
    figsave("2.3-veto_spike.pdf")

if __name__ == '__main__':
    # prob2_1_b()
    # prob2_1_a([0, 47, 50, 51, 53, 55])
    # prob2_1_b([0, 15, 17, 18, 19, 20])
    # prob2_1_c([0, 6, 7, 8, 9, 10, 11])
    # prob2_1_d()
    prob2_3_b()
