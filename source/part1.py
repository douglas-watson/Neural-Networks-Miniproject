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


# for i in np.arange(10, 100, 10):
    # data = run_IClamp(sec=HHx, delay=0, dur=100, amp=i, tstop=100)
    # ax = U_vs_t(data)
# plt.show()
# sys.exit(0)

# 1.2 - Type I or II?
for model in (HH, HHx, HHxx):
    data = []
    for I in np.arange(0, 2, 0.1):
        clampdata = run_IClamp(sec=model, delay=0, dur=100, amp=I, tstop=100)
        data.append([I, clampdata])
    ax = f_vs_I(data, '.', label=model.name, v_th=-40)
ax.legend()
plt.savefig("1-neuron_type.pdf")
