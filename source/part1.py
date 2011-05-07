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

from toolset import *

# 1.1 - Define the three different neuron models:
HH = DefaultSection("HH")
HHx = DefaultSection("HHx")
# HHx.insert("I_x")
HHxx = DefaultSection("HHxx")
# HHxx.insert("I_xx")


# 1.2 - Type I or II?
for model in (HH, HHx, HHxx):
    data = []
    for I in np.arange(5, 100, 10):
        clampdata = run_IClamp(sec=model, delay=0, dur=10, amp=I, tstop=30)
        data.append([I, clampdata])
    ax = f_vs_I(data, '.', label=model.name)
ax.legend()
plt.show()
