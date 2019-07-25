#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:08:45 2017

@author: bruvio
"""
import numpy as np
import sys
import math
import csv
import logging
import pandas as pd
from class_sim import *
from class_sim import Getdata
from class_sim import initread
from class_sim import find_indices
import matplotlib.pyplot as plt
from ppf import *
from matplotlib.patches import Polygon
import _eproc
import eproc as ep
import os
from matplotlib.pylab import yticks,xticks,ylabel,xlabel
from EDGE2DAnalyze import shot

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    EDGE2dfold = '/work/bviola/Python/bruvio_tool/e2d_data'
    workfold = 'work/Python/bruvio_tool'
    #

    del sys.modules['class_sim']
    # reload(class_sim)
    from class_sim import sim

    # os.system('run_write_HRTS.py  84598 T040 ')
    # os.system('run_write_HRTS.py  84599 T035 ')
    # os.system('run_write_HRTS.py  84600 T033 ')
    #tran='/u/bviola/cmg/catalog/edge2d/jet/92123/jul1717/seq#2/tran'
    # os.system('run_edge2danalysis.py  input_dict_84600.json -d 2 ')
    # raise SystemError
    # simlist=[]
    #
    #
    # sim_1 = sim('84600', 'aug0118', '3', workfold)
    #
    # simlist.append([sim_1, 'first'])
    # simlist.append([sim_2, 'first'])
    # simlist.append([sim_3, 'first'])
    # simlist.append([sim_4, 'first'])
    # simlist.append([sim_5, 'first'])
    # simlist.append([sim_6, 'first'])
    # result = sim_1.read_profiles1('IT')
    # result = sim_1.read_profiles('OMP')
    # result1 = sim_1.read_profiles1('OMP')
    # a = result['dsrad']
    # b = result1['dsrad']
    # len(result1['dsrad'])
    # len(result1['teve'].yData)
    # plt.scatter(result1['dsrad'],
    #             result1['teve'].yData)
    # plt.show(block=True)

    # print([i - j for i, j in zip(a, b)])

    # sim.write_edge2d_profiles1(simlist, 'e2dprofiles_python')
    # sim.write_edge2d_profiles(simlist, 'e2dprofiles_python')
    # raise SystemExit
    del sys.modules['EDGE2DAnalyze']
    
    from EDGE2DAnalyze import shot,read_json

    input_dict = read_json('input_dict_84600.json')
    pulse1 = shot(input_dict)
    # raise SystemExit
    # print(pulse1.profile_omp.columns.values)
    #
    # print(pulse1.profile_ot.columns.values)

    # profile_omp=  pd.read_csv(pulse1.profile_omp, skiprows=0,
    #                             delim_whitespace=True)
    # shot.compare_multi_shots('input_dict_84600.json','input_dict_84599.json','compare_dict_84598.json', ms=None, lw=None)
    # names = ep.getnames(pulse1.tranfile,1,1)
    names = ep.names(pulse1.tranfile,prof=1,time=0,flux=0,geom=0)
    # print(names.names)
    # print(names)

    # raise SystemExit
    # shot.compare_multi_shots_simdata('input_dict_84598.json',ms=None, lw=None,var = 'SOUN', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'input_dict_84598.json',ms=None, lw=None,var = 'SOUN', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'denel', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'teve', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'dm', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'da', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'sirec', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'eneutm', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'eneuta', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'sext', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'ripg', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'DENNI', loc = 'omp')
    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'riext', loc = 'omp')

    shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'DPERP', loc = 'omp')
    # shot.compare_multi_shots_simdata('input_dict_84600.json', 'compare_dict_84600.json',ms=None, lw=None,var = 'DPERP', loc = 'omp')


    # sim.write_edge2d_profiles(simlist, 'e2dprofiles_python')

    # #
    # os.system('run_edge2danalysis.py  input_dict_84600.json --input_dict2 compare_dict_84600.json -d 0 ')
    # os.system('run_edge2danalysis.py  input_dict_84599.json --input_dict2 compare_dict_84599.json -d 0 ')
    # os.system('run_edge2danalysis.py  input_dict_84598.json --input_dict2 compare_dict_84598.json -d 0 ')

    # os.system('run_edge2danalysis.py  input_dict_84598.json  -d 0 ')
    # os.system('run_edge2danalysis.py  input_dict_84599.json  -d 0 ')
    # os.system('run_edge2danalysis.py  input_dict_84600.json  -d 0 ')



        # os.system('run_edge2danalysis.py  input_dict_92121.json --input_dict2 input_dict_92123.json -d 2 ')

    # os.system('run_edge2danalysis.py  input_dict_84599.json  -d 2 ')

    # os.system('run_edge2danalysis.py  input_dict_84599.json  -d 2 ')


    # os.system('run_edge2danalysis.py  input_dict_84599.json  -d 2 ')

    # os.system('run_edge2danalysis.py  input_dict_92121.json --input_dict2 input_dict_92123.json -d 2 ')
    # os.system('run_edge2danalysis.py  input_dict_92121.json  -d 2 ')

    # raise SystemExit
    # print(sim_5e21.workingdir)

    plt.show(block=True)