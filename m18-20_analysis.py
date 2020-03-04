#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:08:45 2017

@author: bruvio
"""
import logging
logger = logging.getLogger(__name__)
import sys
import os
from importlib import import_module

libnames = ['ppf']
relative_imports = []


for libname in libnames:
    try:
        lib = import_module(libname)
    except:
        exc_type, exc, tb = sys.exc_info()
        print(os.path.realpath(__file__))
        print(exc)
    else:
        globals()[libname] = lib
for libname in relative_imports:
    try:
        anchor = libname.split('.')
        libr = anchor[0]
        package = anchor[1]

        lib = import_module(libr)
        # lib = import_module(libr,package=package)
    except:
        exc_type, exc, tb = sys.exc_info()
        print(os.path.realpath(__file__))
        print(exc)
    else:
        globals()[libr] = lib

import numpy as np
import sys
import pdb
from time import sleep
from scipy.signal import find_peaks
import math
import csv
import pandas as pd
from class_sim import *
from class_sim import Getdata
from class_sim import initread
from class_sim import find_indices
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from utility import *
from matplotlib.pylab import yticks,xticks,ylabel,xlabel
from EDGE2DAnalyze import shot
from ppf_write import *

try:
    ep = eproc
except:
    logger.error('failed to load EPROC')
    # raise SystemExit




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

# input_dict = read_json('input_dict_84600.json')
# pulse1 = shot(input_dict)
# raise SystemExit
# print(pulse1.profile_omp.columns.values)
#
# print(pulse1.profile_ot.columns.values)

# profile_omp=  pd.read_csv(pulse1.profile_omp, skiprows=0,
#                             delim_whitespace=True)
# shot.compare_multi_shots('input_dict_84600.json','input_dict_84599.json','compare_dict_84598.json', ms=None, lw=None)
# names = ep.getnames(pulse1.tranfile,1,1)
# names = ep.names(pulse1.tranfile,prof=1,time=0,flux=0,geom=0)
# print(names.names)
# print(names)

# raise SystemExit
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'SOUN', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'denel', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'teve', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'dm', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'da', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'sirec', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'eneutm', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'eneuta', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'sext', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'ripg', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'DENNI', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'riext', loc = 'omp')
#
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'input_dict_84599.json', 'compare_dict_84598.json',ms=None, lw=None,var = 'DPERP', loc = 'omp')
# shot.compare_multi_shots_simdata('input_dict_84600.json', 'compare_dict_84600.json',ms=None, lw=None,var = 'DPERP', loc = 'omp')

# plt.show(block=True)
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


### here follows a sequence of instructions to put togegher jetto profiles and edge2d profiles

input_dict = read_json('input_dict_84600.json')
pulse1 = shot(input_dict)

input_dict = read_json('input_dict_84598.json')
pulse2 = shot(input_dict)

import ppf

#     shot=84600
#
#
#
#     owner='vparail'
#
#     dda='JSP'
#
#
#
#     sequence=1570
#     dtype = 'R'
#     r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1578
#     dtype = 'R'
#     r2, r2_x, r2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne2, ne2_x, ne2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII2, SDII2_x, SDII2_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1574
#     dtype = 'R'
#     r3, r3_x, r3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne3, ne3_x, ne3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII3, SDII3_x, SDII3_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1580
#     dtype = 'R'
#     r4, r4_x, r4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne4, ne4_x, ne4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII4, SDII4_x, SDII4_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1581
#     dtype = 'R'
#     r5, r5_x, r5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne5, ne5_x, ne5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII5, SDII5_x, SDII5_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#
#
#
#     sim_1 = sim('84600', 'nov1219', '2', workfold,'vparail')
#     sim_2 = sim('84600', 'nov1519', '3', workfold,'vparail')
#     sim_3 = sim('84600', 'nov1419', '1', workfold,'vparail')
#     sim_4 = sim('84600', 'nov1619', '2', workfold,'vparail')
#     sim_5 = sim('84600', 'nov1719', '1', workfold,'vparail')
#
#     timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
#     tran_index1 = timesteps.index(53.1903)
#
#     res1 = sim_1.read_profiles('omp',tran=tran_index1)
#
#     timesteps = list(ep.timestep(sim_2.fullpath, ALL_TRANFILES=1))
#     tran_index2 = timesteps.index(53.1903)
#     res2 = sim_2.read_profiles('omp',tran=tran_index2)
#
#     timesteps = list(ep.timestep(sim_3.fullpath, ALL_TRANFILES=1))
#     tran_index3 = timesteps.index(53.1803)
#     res3 = sim_3.read_profiles('omp',tran=tran_index3)
#
#     timesteps = list(ep.timestep(sim_4.fullpath, ALL_TRANFILES=1))
#     tran_index4 = timesteps.index(53.1603)
#     res4 = sim_4.read_profiles('omp',tran=tran_index4)
#
#     timesteps = list(ep.timestep(sim_5.fullpath, ALL_TRANFILES=1))
#     tran_index5 = timesteps.index(53.1503)
#     res5 = sim_5.read_profiles('omp',tran=tran_index5)
#
#     fname = 'density profile OMP 11MW'
#     plt.figure(num= fname)
#     plt.title(fname)
#     print(ne1_t[tran_index1])
#     plt.plot(r1[tran_index1],ne1[tran_index1],label='1',color='red',linestyle=':')
#     plt.plot(res1['dsrad'][0:]+r1[-1][-1],res1['ade'].yData[0:],color='red',linestyle=':')
#
#     print(ne2_t[tran_index2])
#     plt.plot(r2[tran_index2],ne2[tran_index2],label='2',color='blue',linestyle=':')
#     plt.plot(res2['dsrad'][0:]+r2[-1][-1],res2['ade'].yData[0:],color='blue',linestyle=':')
#
#     print(ne3_t[tran_index3])
#     plt.plot(r3[tran_index3],ne3[tran_index3],label='3',color='magenta',linestyle=':')
#     plt.plot(res3['dsrad'][0:]+r3[-1][-1],res3['ade'].yData[0:],color='magenta',linestyle=':')
#
#     print(ne4_t[tran_index4])
#     plt.plot(r4[tran_index4],ne4[tran_index4],label='4',color='green',linestyle=':')
#     plt.plot(res4['dsrad'][0:]+r4[-1][-1],res4['ade'].yData[0:],color='green',linestyle=':')
#
#     print(ne5_t[tran_index5])
#     plt.plot(r5[tran_index5],ne5[tran_index5],label='5',color='black',linestyle=':')
#     plt.plot(res5['dsrad'][0:]+r5[-1][-1],res5['ade'].yData[0:],color='black',linestyle=':')
#
#     plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
#     plt.savefig('./figures/' + fname, format='eps', dpi=300)
#     plt.savefig('./figures/' + fname, dpi=300)  #
#
#     ###ionization source
#     fname = 'ionization source profile OMP 11MW'
#     plt.figure(num= fname)
#     plt.title(fname)
#     print(ne1_t[tran_index1])
#     plt.plot(r1[tran_index1][0:-1],SDII1[tran_index1][0:-1],label='1',color='red',linestyle=':')
#     plt.plot(res1['dsrad'][1:]+r1[-1][-1],res1['asoun'].yData[1:],color='red',linestyle=':')
#
#     print(ne2_t[tran_index2])
#     plt.plot(r2[tran_index2][0:-1],SDII2[tran_index2][0:-1],label='2',color='blue',linestyle=':')
#     plt.plot(res2['dsrad'][1:]+r2[-1][-1],res2['asoun'].yData[1:],color='blue',linestyle=':')
#
#     print(ne3_t[tran_index3])
#     plt.plot(r3[tran_index3][0:-1],SDII3[tran_index3][0:-1],label='3',color='magenta',linestyle=':')
#     plt.plot(res3['dsrad'][1:]+r3[-1][-1],res3['asoun'].yData[1:],color='magenta',linestyle=':')
#
#     print(ne4_t[tran_index4])
#     plt.plot(r4[tran_index4][0:-1],SDII4[tran_index4][0:-1],label='4',color='green',linestyle=':')
#     plt.plot(res4['dsrad'][1:]+r4[-1][-1],res4['asoun'].yData[1:],color='green',linestyle=':')
#
#     print(ne5_t[tran_index5])
#     plt.plot(r5[tran_index5][0:-1],SDII5[tran_index5][0:-1],label='5',color='black',linestyle=':')
#     plt.plot(res5['dsrad'][1:]+r5[-1][-1],res5['asoun'].yData[1:],color='black',linestyle=':')
#
#     plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
#     plt.savefig('./figures/' + fname, format='eps', dpi=300)
#     plt.savefig('./figures/' + fname, dpi=300)  #
#
#
#     #####just core
#     # plt.figure()
#     # plt.title('11MW')
#     # print(ne1_t[tran_index1])
#     # plt.plot(ne1_x,ne1[tran_index1],label='1',color='red')
#     # # plt.plot(res1['dsrad']+r1[-1][-1],res1['ade'].yData,color='red')
#     #
#     # print(ne2_t[tran_index2])
#     # plt.plot(ne2_x,ne2[tran_index2],label='2',color='blue')
#     # # plt.plot(res2['dsrad']+r2[-1][-1],res2['ade'].yData,color='blue')
#     #
#     # print(ne3_t[tran_index3])
#     # plt.plot(ne3_x,ne3[tran_index3],label='3',color='magenta')
#     # # plt.plot(res3['dsrad']+r3[-1][-1],res3['ade'].yData,color='magenta')
#     #
#     # print(ne4_t[tran_index4])
#     # plt.plot(ne4_x,ne4[tran_index4],label='4',color='green')
#     # # plt.plot(res4['dsrad']+r4[-1][-1],res4['ade'].yData,color='green')
#     #
#     # print(ne5_t[tran_index5])
#     # plt.plot(ne5_x,ne5[tran_index5],label='5',color='black')
#     # # plt.plot(res5['dsrad']+r5[-1][-1],res5['ade'].yData,color='black')
#     #
#     # plt.xlim(left=0.79,right=1.01)
#
#
#
#
#     #####just edge
#     # plt.figure()
#     # plt.title('11MW')
#     # print(ne1_t[tran_index1])
#     # # plt.plot(r1[-2],ne1[-2],label='1',color='red')
#     # plt.plot(res1['dsrad'],res1['ade'].yData,color='red')
#     #
#     # print(ne2_t[tran_index2])
#     # # plt.plot(r2[-1],ne2[-1],label='2',color='blue')
#     # plt.plot(res2['dsrad'],res2['ade'].yData,color='blue')
#     #
#     # print(ne3_t[tran_index3])
#     # # plt.plot(r3[-1],ne3[-1],label='3',color='magenta')
#     # plt.plot(res3['dsrad'],res3['ade'].yData,color='magenta')
#     #
#     # print(ne4_t[tran_index4])
#     # # plt.plot(r4[-1],ne4[-1],label='4',color='green')
#     # plt.plot(res4['dsrad'],res4['ade'].yData,color='green')
#     #
#     # print(ne5_t[tran_index5])
#     # # plt.plot(r5[-1],ne5[-1],label='5',color='black')
#     # plt.plot(res5['dsrad'],res5['ade'].yData,color='black')
#
#
#     # plt.show(block=True)
#
#
#
# ######## 7 MW
#
#     shot=84600
#
#
#
#     owner='vparail'
#
#     dda='JSP'
#
#     sim_1 = sim('84600', 'nov1219', '1', workfold,'vparail')
#     sim_2 = sim('84600', 'nov1419', '2', workfold,'vparail')
#     sim_3 = sim('84600', 'nov1519', '2', workfold,'vparail')
#     sim_4 = sim('84600', 'nov1319', '1', workfold,'vparail')
#
#
#     timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
#     tran_index1 = timesteps.index(53.1403)
#
#     res1 = sim_1.read_profiles('omp',tran=tran_index1)
#
#     timesteps = list(ep.timestep(sim_2.fullpath, ALL_TRANFILES=1))
#     tran_index2 = timesteps.index(53.1902)
#     res2 = sim_2.read_profiles('omp',tran=tran_index2)
#
#     timesteps = list(ep.timestep(sim_3.fullpath, ALL_TRANFILES=1))
#     tran_index3 = timesteps.index(53.1603)
#     res3 = sim_3.read_profiles('omp',tran=tran_index3)
#
#     timesteps = list(ep.timestep(sim_4.fullpath, ALL_TRANFILES=1))
#     tran_index4 = timesteps.index(53.1903)
#     res4 = sim_4.read_profiles('omp',tran=tran_index4)
#
#
#
#
#     sequence=1569
#     dtype = 'R'
#     r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1575
#     dtype = 'R'
#     r2, r2_x, r2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne2, ne2_x, ne2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII2, SDII2_x, SDII2_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1577
#     dtype = 'R'
#     r3, r3_x, r3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne3, ne3_x, ne3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII3, SDII3_x, SDII3_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#     sequence = 1573
#     dtype = 'R'
#     r4, r4_x, r4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne4, ne4_x, ne4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII4, SDII4_x, SDII4_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#
#
#
#
#
#     fname = 'density profile OMP 7MW'
#     plt.figure(num= fname)
#     plt.title(fname)
#     print(ne1_t[tran_index1])
#     plt.plot(r1[tran_index1],ne1[tran_index1],label='1',color='red',linestyle=':')
#     plt.plot(res1['dsrad'][0:]+r1[-1][-1],res1['ade'].yData[0:],color='red',linestyle=':')
#
#     print(ne2_t[tran_index2])
#     plt.plot(r2[tran_index2],ne2[tran_index2],label='2',color='blue',linestyle=':')
#     plt.plot(res2['dsrad'][0:]+r2[-1][-1],res2['ade'].yData[0:],color='blue',linestyle=':')
#
#     print(ne3_t[tran_index3])
#     plt.plot(r3[tran_index3],ne3[tran_index3],label='3',color='magenta',linestyle=':')
#     plt.plot(res3['dsrad'][0:]+r3[-1][-1],res3['ade'].yData[0:],color='magenta',linestyle=':')
#
#     print(ne4_t[tran_index4])
#     plt.plot(r4[tran_index4],ne4[tran_index4],label='4',color='green',linestyle=':')
#     plt.plot(res4['dsrad'][0:]+r4[-1][-1],res4['ade'].yData[0:],color='green',linestyle=':')
#
#
#     plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
#     plt.savefig('./figures/' + fname, format='eps', dpi=300)
#     plt.savefig('./figures/' + fname, dpi=300)  #
#
#
#     ###ionization source
#     fname = 'ionization source profile OMP 7MW'
#     plt.figure(num= fname)
#     plt.title(fname)
#     print(ne1_t[tran_index1])
#     plt.plot(r1[tran_index1][0:-1],SDII1[tran_index1][0:-1],label='1',color='red',linestyle=':')
#     plt.plot(res1['dsrad'][1:]+r1[-1][-1],res1['asoun'].yData[1:],color='red',linestyle=':')
#
#     print(ne2_t[tran_index2])
#     plt.plot(r2[tran_index2][0:-1],SDII2[tran_index2][0:-1],label='2',color='blue',linestyle=':')
#     plt.plot(res2['dsrad'][1:]+r2[-1][-1],res2['asoun'].yData[1:],color='blue',linestyle=':')
#
#     print(ne3_t[tran_index3])
#     plt.plot(r3[tran_index3][0:-1],SDII3[tran_index3][0:-1],label='3',color='magenta',linestyle=':')
#     plt.plot(res3['dsrad'][1:]+r3[-1][-1],res3['asoun'].yData[1:],color='magenta',linestyle=':')
#
#     print(ne4_t[tran_index4])
#     plt.plot(r4[tran_index4][0:-1],SDII4[tran_index4][0:-1],label='4',color='green',linestyle=':')
#     plt.plot(res4['dsrad'][1:]+r4[-1][-1],res4['asoun'].yData[1:],color='green',linestyle=':')
#
#
#     plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
#     plt.savefig('./figures/' + fname, format='eps', dpi=300)
#     plt.savefig('./figures/' + fname, dpi=300)  #
#
#
#     #####just core
#     # plt.figure()
#     # plt.title('7MW')
#     #
#     # plt.plot(ne1_x,ne1[tran_index1],label='1',color='red')
#     # # plt.plot(res1['dsrad']+r1[-1][-1],res1['ade'].yData,color='red')
#     #
#     # plt.plot(ne2_x,ne2[tran_index2],label='2',color='blue')
#     # # plt.plot(res2['dsrad']+r2[-1][-1],res2['ade'].yData,color='blue')
#     #
#     # plt.plot(ne3_x,ne3[tran_index3],label='3',color='magenta')
#     # # plt.plot(res3['dsrad']+r3[-1][-1],res3['ade'].yData,color='magenta')
#     #
#     # plt.plot(ne4_x,ne4[tran_index4],label='4',color='green')
#     # # plt.plot(res4['dsrad']+r4[-1][-1],res4['ade'].yData,color='green')
#     #
#     #
#     # plt.xlim(left=0.79,right=1.01)
#
#
#
#
#     #####just edge
#     # plt.figure()
#     # plt.title('7MW')
#     # # plt.plot(r1[-2],ne1[-2],label='1',color='red')
#     # plt.plot(res1['dsrad'],res1['ade'].yData,color='red')
#     #
#     # # plt.plot(r2[-1],ne2[-1],label='2',color='blue')
#     # plt.plot(res2['dsrad'],res2['ade'].yData,color='blue')
#     #
#     #
#     # # plt.plot(r3[-1],ne3[-1],label='3',color='magenta')
#     # plt.plot(res3['dsrad'],res3['ade'].yData,color='magenta')
#     #
#     #
#     # # plt.plot(r4[-1],ne4[-1],label='4',color='green')
#     # plt.plot(res4['dsrad'],res4['ade'].yData,color='green')
#
#
#
#
#
#
#
#
#
#
#
#
#     logger.info('plotting HRTS NE')
#     # %%
#
#
#     fnorm = 1
#     ftitle = 'Electron Density OMP'
#     # fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
#     fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'
#
#     plt.figure(num=fname + "_" + pulse1.label)
#     try:
#         plt.errorbar(pulse1.hrts_profiles['R'] +0.035,
#                      pulse1.hrts_profiles['NE'], label='_nolegend_',
#                      yerr=pulse1.hrts_profiles['DNE'], fmt=None,
#                      ecolor='black')
#     except:
#         logger.error('impossible to plot pulse1 NE from HRTS')
#     # try:
#     #     plt.scatter(pulse1.hrts_fit['Rfit'] + float(pulse1.shift_fit),
#     #                 pulse1.hrts_fit['nef3'], label='_nolegend_',
#     #                 color='black')
#     # except:
#     #     logger.error('impossible to plot pulse2 NE HRTS fit')
#
#
#
#     try:
#         plt.errorbar(pulse2.hrts_profiles['R'] +0.035,
#                      pulse2.hrts_profiles['NE'], label='_nolegend_',
#                      yerr=pulse2.hrts_profiles['DNE'], fmt=None,
#                      ecolor='red')
#     except:
#         logger.error('impossible to plot pulse2 NE from HRTS')
#     # try:
#     #     plt.scatter(pulse2.hrts_fit['Rfit'] + float(pulse2.shift_fit),
#     #                 pulse2.hrts_fit['nef3'], label='_nolegend_',
#     #                 color='red')
#     # except:
#     #     logger.error('impossible to plot pulse2 NE HRTS fit')
#
#
#     sim_1 = sim('84600', 'nov1219', '1', workfold,'vparail')
#     timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
#     tran_index1 = timesteps.index(53.1403)
#
#
#     sim_5 = sim('84600', 'nov1719', '1', workfold,'vparail')
#     timesteps = list(ep.timestep(sim_5.fullpath, ALL_TRANFILES=1))
#     tran_index5 = timesteps.index(53.1503)
#     res5 = sim_5.read_profiles('omp',tran=tran_index5)
#
#
#     sequence=1569
#     dtype = 'R'
#     r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#
#     sequence = 1581
#     dtype = 'R'
#     r5, r5_x, r5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'NE'
#     ne5, ne5_x, ne5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#     dtype = 'SDII'
#     SDII5, SDII5_x, SDII5_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#
#     plt.plot(r1[tran_index1],ne1[tran_index1]/1e19,label='1',color='black',linestyle=':',linewidth=3)
#     data = [data/1e19 for data in res1['ade'].yData[0:]]
#     plt.plot(res1['dsrad'][0:]+r1[-1][-1],data,color='black',linestyle=':',linewidth=3)
#
#     plt.plot(r5[tran_index1],ne5[tran_index5]/1e19,label='5',color='red',linestyle=':',linewidth=3)
#     data = [data / 1e19 for data in res5['ade'].yData[0:]]
#     plt.plot(res5['dsrad'][0:]+r5[-1][-1],data,color='red',linestyle=':',linewidth=3)
#
#
#     plt.xlim(left=3.75)


################################################# dec 6 2019 new simulations
def read_jetto_data(shot,sequence,dtype,dda,owner):
    data, x, t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(
        shot, dda, dtype, seq=sequence, uid=owner, reshape=1)


    return dict(zip(('data','x','t'), (data,x, t)))

def read_jetto_sequence(shot,sequence,dda,owner,dtypelist):
    dict_name = 'data_'+str(sequence)
    vars()[dict_name] = {}
    for dtype in dtypelist:
        vars()[dtype] = read_jetto_data(shot,sequence,dtype,dda,owner)
        vars()[dict_name][dtype] = vars()[dtype]
    return  vars()[dict_name]

def get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, simu,sequence, force_tran=None):
    dda_time = 'JST'
    wth = read_jetto_data(shot, sequence, 'WTH', dda_time, owner)
    data = read_jetto_sequence(shot, sequence, dda, owner,
                               ['R', 'NE', 'SDII', 'TE'])
    timesteps = list(ep.timestep(simu.fullpath, ALL_TRANFILES=1))
    index, dummy = find_peaks(wth['data'])
    last_peak_index = index[np.argmax(index)]
    value_closest = take_closest(timesteps, wth['t'][last_peak_index])
    peak_selected = wth['t'][last_peak_index]
    tran_index = timesteps.index(value_closest)
    if force_tran:
        tran_index = tran_index + force_tran
        sleep(1)
    res = simu.read_profiles('omp', tran=tran_index)



    plt.figure()
    ax1=plt.subplot(2,1,1)
    plt.plot(wth['t'],wth['data'],label='wth_'+str(sequence))
    plt.legend(loc='best', prop={'size': 6})
    plt.plot(wth['t'][index], wth['data'][index], "x")
    plt.axvline(x=peak_selected, color='r')
    plt.axvline(x=timesteps[tran_index], color='b')
    ax2=plt.subplot(2,1,2,sharex=ax1)
    plt.plot(data['TE']['t'],data['TE']['data'].T[-1],label='TE_'+str(sequence))
    plt.legend(loc='best', prop={'size': 6})
    plt.axvline(x=peak_selected,color='r')
    plt.axvline(x=timesteps[tran_index],color='b')
    plt.savefig('./figures/' + 'peak_selection'+str(sequence), dpi=300)  #
    plt.show(block=False)
    logger.info('Energy peak @ {}s / selected time is {}s'.format(peak_selected,
                                                                  timesteps[
                                                                      tran_index]))
    return res, tran_index, data,value_closest

# def rundec6simulations(allow_write_ppf):
#         logger = logging.getLogger(__name__)
#         EDGE2dfold = '/work/bviola/Python/EDGE2D/e2d_data'
#         workfold = 'work/Python/EDGE2D'
#         plt.close('all')
#
#         shot=84600
#         if allow_write_ppf:
#
#             err = open_ppf(shot, 'bviola')
#             if err != 0:
#                 logger.error('failed to open ppf')
#                 raise SystemExit
#
#         owner='vparail'
#
#         dda='JSP'
#
#         sim_1 = sim('84600', 'dec0419', '1', workfold,'vparail') # Extend  nov1719/1/1581 to 53.4s with D_flux=7.25e22s-1 + SUB_DIV_PUMP+11MW NBI+PUMP_A=0.92+NEW GRID+ DISCRETE. ELMS + NEW load module with IJETTO(26)=1
#         sim_2 = sim('84600', 'dec0519', '2', workfold,'vparail') #Extend  nov1219/1/1569 to 53.4s with D_flux=0.5e22s-1 + SUB_DIV_PUMP+7MW NBI+PUMP_A=0.92+NEW GRID+ DISCRETE. ELMS + NEW load module
#         sim_3 = sim('84600', 'dec0519', '1', workfold,'vparail') # Extend  nov1219/1/1569 to 53.4s with D_flux=0.5e22s-1 + SUB_DIV_PUMP+7MW NBI+PUMP_A=0.92+NEW GRID+ DISCRETE. ELMS + NEW load module
#
#
#
#         timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
#         tran_index1 = timesteps.index(53.3804)
#
#         res1 = sim_1.read_profiles('omp',tran=tran_index1)
#
#         timesteps = list(ep.timestep(sim_2.fullpath, ALL_TRANFILES=1))
#         tran_index2 = timesteps.index(53.3404)
#         res2 = sim_2.read_profiles('omp',tran=tran_index2)
#
#         timesteps = list(ep.timestep(sim_3.fullpath, ALL_TRANFILES=1))
#         tran_index3 = timesteps.index(53.3804)
#         res3 = sim_3.read_profiles('omp',tran=tran_index3)
#
#
#
#
#
#         sequence=1584
#         dtype = 'R'
#         r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'NE'
#         ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'SDII'
#         SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'TE'
#         TE1, TE1_x, TE1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#         sequence = 1586
#         dtype = 'R'
#         r2, r2_x, r2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'NE'
#         ne2, ne2_x, ne2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'SDII'
#         SDII2, SDII2_x, SDII2_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'TE'
#         TE1, TE1_x, TE1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#         sequence = 1585
#         dtype = 'R'
#         r3, r3_x, r3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'NE'
#         ne3, ne3_x, ne3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'SDII'
#         SDII3, SDII3_x, SDII3_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#         dtype = 'TE'
#         TE1, TE1_x, TE1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
#
#
#
#
#
#
#
#         fname = "NE  05e22 11MW"
#         plt.figure(num= fname)
#         plt.title(fname)
#         # print(ne1_t[tran_index1])
#         plt.plot(r1[tran_index1],ne1[tran_index1],label='1',color='red',linestyle=':')
#         plt.plot(res1['dsrad'][0:]+r1[-1][-1],res1['ade'].yData[0:],color='red',linestyle=':')
#         plt.xlim(left=3.795,right=max(res1['dsrad']+r1[-1][-1]))
#         plt.savefig('./figures/' + fname, format='eps', dpi=300)
#         plt.savefig('./figures/' + fname, dpi=300)  #
#         if allow_write_ppf:
#
#             write_err, itref_written = write_ppf(shot, 'edg2',
#                                              'den1',
#                                              np.concatenate([ne1[tran_index1],
#                                                              res1['ade'].yData[
#                                                              0:]]),
#                                              time=np.concatenate([r1[tran_index1],res1['dsrad'][0:] +r1[-1][-1]]),
#                                              status=np.concatenate([r1[tran_index1],res1['dsrad'][0:] +r1[-1][-1]]),
#                                              comment=fname,
#                                              unitd=" ", unitt=" ",
#                                              itref=-1,
#                                              nt=len(np.concatenate([r1[tran_index1],
#                                                             res1['dsrad'][0:] +
#                                                             r1[-1][-1]])))
#
#
#         fname = 'NE  725e22 11MW'
#         plt.figure(num= fname)
#         plt.title(fname)
#         # print(ne2_t[tran_index2])
#         plt.plot(r2[tran_index2],ne2[tran_index2],label='2',color='blue',linestyle=':')
#         plt.plot(res2['dsrad'][0:]+r2[-1][-1],res2['ade'].yData[0:],color='blue',linestyle=':')
#         plt.xlim(left=3.795,right=max(res2['dsrad']+r2[-1][-1]))
#         plt.savefig('./figures/' + fname, format='eps', dpi=300)
#         plt.savefig('./figures/' + fname, dpi=300)  #
#         if allow_write_ppf:
#
#             write_err, itref_written = write_ppf(shot, 'edg2',
#                                              'den2',
#                                              np.concatenate([ne2[tran_index2],
#                                                              res2['ade'].yData[
#                                                              0:]]),
#                                              time=np.concatenate([r2[tran_index2],
#                                                             res2['dsrad'][0:] +
#                                                             r2[-1][-1]]),
#                                              status=np.concatenate([r2[tran_index2],
#                                                             res2['dsrad'][0:] +
#                                                             r2[-1][-1]]),
#                                              comment=fname,
#                                              unitd=" ", unitt=" ",
#                                              itref=-1,
#                                              nt=len(np.concatenate([r2[tran_index2],
#                                                             res2['dsrad'][0:] +
#                                                             r2[-1][-1]])))
#
#
#         fname = 'NE  05e22 7MW'
#         plt.figure(num= fname)
#         plt.title(fname)
#         # print(ne3_t[tran_index3])
#         plt.plot(r3[tran_index3],ne3[tran_index3],label='3',color='magenta',linestyle=':')
#         plt.plot(res3['dsrad'][0:]+r3[-1][-1],res3['ade'].yData[0:],color='magenta',linestyle=':')
#         plt.xlim(left=3.795,right=max(res2['dsrad']+r2[-1][-1]))
#         plt.savefig('./figures/' + fname, format='eps', dpi=300)
#         plt.savefig('./figures/' + fname, dpi=300)  #
#         if allow_write_ppf:
#
#             write_err, itref_written = write_ppf(shot, 'edg2',
#                                              'den3',
#                                              np.concatenate([ne3[tran_index3],
#                                                              res3['ade'].yData[
#                                                              0:]]),
#                                              time=np.concatenate([r3[tran_index3],
#                                                             res3['dsrad'][0:] +
#                                                             r3[-1][-1]]),
#                                              status=np.concatenate([r3[tran_index3],
#                                                                   res3['dsrad'][
#                                                                   0:] +
#                                                                   r3[-1][-1]]),
#                                              comment=fname,
#                                              unitd=" ", unitt=" ",
#                                              itref=-1,
#                                              nt=len(np.concatenate([r3[tran_index3],
#                                                             res3['dsrad'][0:] +
#                                                             r3[-1][-1]])))
#
#         ###ionization source
#         fname = 'ION src  05e22 11MW'
#         plt.figure(num= fname)
#         plt.title(fname)
#         # print(ne1_t[tran_index1])
#         plt.plot(r1[tran_index1][0:-1],data1['SDII']['data'][tran_index1][0:-1],label='1',color='red',linestyle=':')
#         plt.plot(res1['dsrad'][1:]+r1[-1][-1],res1['asoun'].yData[1:],color='red',linestyle=':')
#         plt.xlim(left=3.795,right=max(res2['dsrad']+r2[-1][-1]))
#         plt.savefig('./figures/' + fname, format='eps', dpi=300)
#         plt.savefig('./figures/' + fname, dpi=300)  #
#
#         if allow_write_ppf:
#
#             write_err, itref_written = write_ppf(shot, 'edg2',
#                                              'ion1',
#                                              np.concatenate([ne1[tran_index1],
#                                                              res1['asoun'].yData[
#                                                              0:]]),
#                                              time=np.concatenate([r1[tran_index1],
#                                                             res1['dsrad'][0:] +
#                                                             r1[-1][-1]]),
#                                              status= np.concatenate([r1[tran_index1],
#                                                             res1['dsrad'][0:] +
#                                                             r1[-1][-1]]),
#                                              comment=fname,
#                                              unitd=" ", unitt=" ",
#                                              itref=-1,
#                                              nt=len(np.concatenate([r1[tran_index1],
#                                                             res1['dsrad'][0:] +
#                                                             r1[-1][-1]])))
#
#         fname = 'ION src  725e22 11MW'
#         plt.figure(num= fname)
#         plt.title(fname)
#         # print(ne2_t[tran_index2])
#         plt.plot(r2[tran_index2][0:-1],data2['SDII']['data'][tran_index2][0:-1],label='2',color='blue',linestyle=':')
#         plt.plot(res2['dsrad'][1:]+r2[-1][-1],res2['asoun'].yData[1:],color='blue',linestyle=':')
#         plt.xlim(left=3.795,right=max(res2['dsrad']+r2[-1][-1]))
#         plt.savefig('./figures/' + fname, format='eps', dpi=300)
#         plt.savefig('./figures/' + fname, dpi=300)  #
#
#         if allow_write_ppf:
#
#             write_err, itref_written = write_ppf(shot, 'edg2',
#                                              'ion2',
#                                              np.concatenate([ne2[tran_index2],
#                                                              res2['asoun'].yData[
#                                                              0:]]),
#                                              time=np.concatenate([r2[tran_index2],
#                                                             res2['dsrad'][0:] +
#                                                             r2[-1][-1]]),
#                                              status=np.concatenate([r2[tran_index2],
#                                                             res2['dsrad'][0:] +
#                                                             r2[-1][-1]]),
#                                              comment=fname,
#                                              unitd=" ", unitt=" ",
#                                              itref=-1,
#                                              nt=len(np.concatenate([r2[tran_index2],
#                                                             res2['dsrad'][0:] +
#                                                             r2[-1][-1]])))
#
#         fname = 'ION src  05e22 7MW'
#         plt.figure(num= fname)
#         plt.title(fname)
#         # print(ne3_t[tran_index3])
#         plt.plot(r3[tran_index3][0:-1],data3['SDII']['data'][tran_index3][0:-1],label='3',color='magenta',linestyle=':')
#         plt.plot(res3['dsrad'][1:]+r3[-1][-1],res3['asoun'].yData[1:],color='magenta',linestyle=':')
#         plt.xlim(left=3.795,right=max(res3['dsrad']+r3[-1][-1]))
#         plt.savefig('./figures/' + fname, format='eps', dpi=300)
#         plt.savefig('./figures/' + fname, dpi=300)  #
#         if allow_write_ppf:
#             write_err, itref_written = write_ppf(shot, 'edg2',
#                                              'ion3',
#                                              np.concatenate([ne3[tran_index3],
#                                                              res3['asoun'].yData[
#                                                              0:]]),
#                                              time=np.concatenate([r3[tran_index3],
#                                                             res3['dsrad'][0:] +
#                                                             r3[-1][-1]]),
#                                              status=np.concatenate([r3[tran_index3],
#                                                             res3['dsrad'][0:] +
#                                                             r3[-1][-1]]),
#                                              comment=fname,
#                                              unitd=" ", unitt=" ",
#                                              itref=-1,
#                                              nt=len(np.concatenate([r3[tran_index3],
#                                                             res3['dsrad'][0:] +
#                                                             r3[-1][-1]])))
#
#
#
#         #####just core
#         # plt.figure()
#         # plt.title('7MW')
#         #
#         # plt.plot(ne1_x,ne1[tran_index1],label='1',color='red')
#         # # plt.plot(res1['dsrad']+r1[-1][-1],res1['ade'].yData,color='red')
#         #
#         # plt.plot(ne2_x,ne2[tran_index2],label='2',color='blue')
#         # # plt.plot(res2['dsrad']+r2[-1][-1],res2['ade'].yData,color='blue')
#         #
#         # plt.plot(ne3_x,ne3[tran_index3],label='3',color='magenta')
#         # # plt.plot(res3['dsrad']+r3[-1][-1],res3['ade'].yData,color='magenta')
#         #
#         # plt.plot(ne4_x,ne4[tran_index4],label='4',color='green')
#         # # plt.plot(res4['dsrad']+r4[-1][-1],res4['ade'].yData,color='green')
#         #
#         #
#         # plt.xlim(left=0.79,right=1.01)
#
#
#
#
#         #####just edge
#         # plt.figure()
#         # plt.title('7MW')
#         # # plt.plot(r1[-2],ne1[-2],label='1',color='red')
#         # plt.plot(res1['dsrad'],res1['ade'].yData,color='red')
#         #
#         # # plt.plot(r2[-1],ne2[-1],label='2',color='blue')
#         # plt.plot(res2['dsrad'],res2['ade'].yData,color='blue')
#         #
#         #
#         # # plt.plot(r3[-1],ne3[-1],label='3',color='magenta')
#         # plt.plot(res3['dsrad'],res3['ade'].yData,color='magenta')
#         #
#         #
#         # # plt.plot(r4[-1],ne4[-1],label='4',color='green')
#         # plt.plot(res4['dsrad'],res4['ade'].yData,color='green')
#         if allow_write_ppf:
#
#             err = close_ppf(shot, 'bviola',
#                             '1')
#
#             if err != 0:
#                 logger.error('failed to close ppf')
#                 raise SystemExit
#
#
#         plt.show(block=False)
#
def plot_write_merged_sim(shot,fname,data,res,label_jetto,label_e2d,tran_index,label,allow_write_ppf,allow_plot,color,numb):
    fname = fname
    if allow_plot:
        plt.figure(num=fname)
        plt.title(fname)
        # print(ne5_t[tran_index])

        plt.plot(data['R']['data'][tran_index][0:-1], data[label_jetto]['data'][tran_index][0:-1], label=label,
                 linestyle=':', color=color)
        plt.plot(res['dsrad'][1:] + data['R']['data'][-1][-1], res[label_e2d].yData[1:],
                linestyle=':', color=color)
        plt.xlim(left=3.795, right=max(res['dsrad'] + data['R']['data'][-1][-1]))
        plt.legend(loc='upper right', prop={'size': 6})
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

    if allow_write_ppf:
        name = label_jetto+str(numb)
        if len(name) > 4:
            char2remove = len(name)-4
            name = name.replace(name[:char2remove],'')
        write_err, itref_written = write_ppf(shot, 'edg2',
                                         name,
                                         np.concatenate([data[label_jetto]['data'][tran_index],
                                                         res[label_e2d].yData[
                                                         0:]]),
                                         time=np.concatenate([data['R']['data'][tran_index],
                                                              res['dsrad'][0:] +
                                                              data['R']['data'][-1][-1]]),
                                         status=np.concatenate([data['R']['data'][tran_index],
                                                                res['dsrad'][0:] +
                                                                data['R']['data'][-1][-1]]),
                                         comment=fname,
                                         unitd=" ", unitt=" ",
                                         itref=-1,
                                         nt=len(np.concatenate([data['R']['data'][tran_index],
                                                                res['dsrad'][0:] +
                                                                data['R']['data'][-1][-1]])))
        
def runFebsimulations7MW(allow_write_ppf,allow_plot):
        logger = logging.getLogger(__name__)
        EDGE2dfold = '/work/bviola/Python/EDGE2D/e2d_data'
        workfold = 'work/Python/EDGE2D'

        plt.close('all')

        shot = 84600


        owner = 'vparail'

        dda = 'JSP'
        # EXTEND feb2319/2/1386 with discrete ELM model , ALL RUNS WITH 7MW NBI , 5 levels of GAS, same ALPH_crit=1.5
        sim_number =7


        sim_1 = sim('84600', 'nov1219', '1', workfold, 'vparail')
        sim_2 = sim('84600', 'nov1419', '2', workfold, 'vparail')
        sim_3 = sim('84600', 'nov1519', '2', workfold, 'vparail')
        sim_4 = sim('84600', 'nov1319', '1', workfold, 'vparail')
        sim_5 = sim('84600', 'nov1619', '1', workfold, 'vparail')
        sim_6 = sim('84600', 'nov1519', '1', workfold, 'vparail')
        sim_7 = sim('84600', 'dec0519', '1', workfold, 'vparail')

        force_index5 = -2


        res1, tran_index1, data1, time_used1 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_1,1569)
        res2, tran_index2, data2, time_used2 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_2,1575)
        res3, tran_index3, data3, time_used3 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_3,1577)
        res4, tran_index4, data4, time_used4 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_4,1573)
        res5, tran_index5, data5, time_used5 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_5,1579,force_tran=force_index5)
        res6, tran_index6, data6, time_used6 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_6,1576)
        res7, tran_index7, data7, time_used7 = get_combined_e2d_jetto_data_before_elm_crash(shot, owner, dda, sim_7,1585)

        sleep(1)




        logging.info('time used for simu {} is {}'.format(sim_1.date+'/'+sim_1.seq+'/'+str(1569),time_used1))
        logging.info('time used for simu {} is {}'.format(sim_2.date+'/'+sim_2.seq+'/'+str(1575),time_used2))
        logging.info('time used for simu {} is {}'.format(sim_3.date+'/'+sim_3.seq+'/'+str(1577),time_used3))
        logging.info('time used for simu {} is {}'.format(sim_4.date+'/'+sim_4.seq+'/'+str(1573),time_used4))
        logging.info('time used for simu {} is {}'.format(sim_5.date+'/'+sim_5.seq+'/'+str(1579),time_used5))
        logging.info('time used for simu {} is {}'.format(sim_6.date+'/'+sim_6.seq+'/'+str(1576),time_used6))
        logging.info('time used for simu {} is {}'.format(sim_7.date+'/'+sim_7.seq+'/'+str(1585),time_used7))

        if allow_write_ppf:

            err = open_ppf(shot, 'bviola')
            if err != 0:
                logger.error('failed to open ppf')
                raise SystemExit

        fname = "NE  1e22 7MW"
        label = 'NE-7MW'
        i = 1
        plot_write_merged_sim(shot,label, data1, res1, 'NE', 'ade',tran_index1, fname,
                              allow_write_ppf,allow_plot,'blue',i)
        fname = 'NE  225e20 7MW'
        i = i+1
        plot_write_merged_sim(shot,label, data2, res2, 'NE', 'ade', tran_index2, fname,
                              allow_write_ppf,allow_plot,'green',i)
        fname = 'NE  35e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data3, res3, 'NE', 'ade', tran_index3, fname,
                              allow_write_ppf,allow_plot,'red',i)
        fname = 'NE  47e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data4, res4, 'NE', 'ade', tran_index4, fname,
                              allow_write_ppf,allow_plot,'cyan',i)
        fname = 'NE  6e22 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data5, res5, 'NE', 'ade', tran_index5, fname,
                              allow_write_ppf,allow_plot,'magenta',i)
        fname = 'NE  225e200 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data6, res6, 'NE', 'ade', tran_index6, fname,
                              allow_write_ppf,allow_plot,'yellow',i)
        fname = 'NE  5e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data7, res7, 'NE', 'ade', tran_index7, fname,
                              allow_write_ppf,allow_plot,'black',i)
        #
        # ###ionization source
        fname = 'ION 1e22 7MW'
        label = 'ION-7MW'
        i = 1
        plot_write_merged_sim(shot,label, data1, res1, 'SDII', 'asoun', tran_index1, fname,
                              allow_write_ppf,allow_plot,'blue',i)
        fname = 'ION 225e20 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data2, res2, 'SDII', 'asoun', tran_index2, fname,
                              allow_write_ppf,allow_plot,'green',i)
        fname = 'ION 35e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data3, res3, 'SDII', 'asoun', tran_index3, fname,
                              allow_write_ppf,allow_plot,'red',i)
        fname = 'ION 47e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data4, res4, 'SDII', 'asoun', tran_index4, fname,
                              allow_write_ppf,allow_plot,'cyan',i)
        fname = 'ION 6e22 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data5, res5, 'SDII', 'asoun', tran_index5, fname,
                              allow_write_ppf,allow_plot,'magenta',i)
        fname = 'ION 225e200 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data6, res6, 'SDII', 'asoun', tran_index6, fname,
                              allow_write_ppf,allow_plot,'yellow',i)
        fname = 'ION 5e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data7, res7, 'SDII', 'asoun', tran_index7, fname,
                              allow_write_ppf,allow_plot,'black',i)
        ###temperature
        fname = 'TE 1e22 7MW'
        label = 'TE-7MW'
        i = 1
        plot_write_merged_sim(shot,label, data1, res1, 'TE', 'ate', tran_index1, fname,
                              allow_write_ppf,allow_plot,'blue',i)
        fname = 'TE 225e20 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data2, res2, 'TE', 'ate', tran_index2, fname,
                              allow_write_ppf,allow_plot,'green',i)
        fname = 'TE 35e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data3, res3, 'TE', 'ate', tran_index3, fname,
                              allow_write_ppf,allow_plot,'red',i)
        fname = 'TE 47e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data4, res4, 'TE', 'ate', tran_index4, fname,
                              allow_write_ppf,allow_plot,'cyan',i)
        fname = 'TE 6e22 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data5, res5, 'TE', 'ate', tran_index5, fname,
                              allow_write_ppf,allow_plot,'magenta',i)
        fname = 'TE 225e200 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data6, res6, 'TE', 'ate', tran_index6, fname,
                              allow_write_ppf,allow_plot,'yellow',i)
        fname = 'TE 5e21 7MW'
        i = i + 1
        plot_write_merged_sim(shot,label, data7, res7, 'TE', 'ate', tran_index7, fname,
                              allow_write_ppf,allow_plot,'black',i)
        if allow_write_ppf:

            err = close_ppf(shot, 'bviola',
                            '1')

            if err != 0:
                logger.error('failed to close ppf')
                raise SystemExit

        # plt.show(block=True)


def runFebsimulations11MW(allow_write_ppf,allow_plot):
    logger = logging.getLogger(__name__)
    EDGE2dfold = '/work/bviola/Python/EDGE2D/e2d_data'
    workfold = 'work/Python/EDGE2D'


    plt.close('all')

    shot = 84600


    owner = 'vparail'

    dda = 'JSP'
    # EXTEND feb2319/2/1386 with discrete ELM model , ALL RUNS WITH 11MW NBI , 5 levels of GAS, same ALPH_crit=1.5
    sim_1 = sim('84600', 'nov1219', '2', workfold, 'vparail')
    sim_2 = sim('84600', 'nov1519', '3', workfold, 'vparail')
    sim_3 = sim('84600', 'nov1419', '1', workfold, 'vparail')
    sim_4 = sim('84600', 'nov1619', '2', workfold, 'vparail')
    sim_5 = sim('84600', 'nov1719', '1', workfold, 'vparail')
    sim_6 = sim('84600', 'dec0419', '1', workfold, 'vparail')
    sim_7 = sim('84600', 'dec0519', '2', workfold, 'vparail')

    force_index4 = -2
    force_index5 = -2
    force_index6 = -2
    force_index7 = -2

    res1, tran_index1, data1, time_used1 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_1, 1570)
    res2, tran_index2, data2, time_used2 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_2, 1578)
    res3, tran_index3, data3, time_used3 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_3, 1574)
    res4, tran_index4, data4, time_used4 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_4, 1580,force_tran=force_index4)
    res5, tran_index5, data5, time_used5 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_5, 1581,force_tran=force_index5)
    res6, tran_index6, data6, time_used6 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_6, 1584,force_tran=force_index6)
    res7, tran_index7, data7, time_used7 = get_combined_e2d_jetto_data_before_elm_crash(
        shot, owner, dda, sim_7, 1586,force_tran=force_index7)



    sleep(1)



    logging.info(
        'time used for simu {} is {}'.format(sim_1.date + '/' + sim_1.seq+ '/' +str(1570),
                                             time_used1))
    logging.info(
        'time used for simu {} is {}'.format(sim_2.date + '/' + sim_2.seq+ '/' +str(1578),
                                             time_used2))
    logging.info(
        'time used for simu {} is {}'.format(sim_3.date + '/' + sim_3.seq+ '/' +str(1574),
                                             time_used3))
    logging.info(
        'time used for simu {} is {}'.format(sim_4.date + '/' + sim_4.seq+ '/' +str(1580),
                                             time_used4))
    logging.info(
        'time used for simu {} is {}'.format(sim_5.date + '/' + sim_5.seq+ '/' +str(1581),
                                             time_used5))

    logging.info(
        'time used for simu {} is {}'.format(sim_6.date + '/' + sim_6.seq+ '/' +str(1584),
                                             time_used6))

    logging.info(
        'time used for simu {} is {}'.format(sim_7.date + '/' + sim_7.seq+ '/' +str(1586),
                                             time_used7))

    if allow_write_ppf:

        err = open_ppf(shot, 'bviola')
        if err != 0:
            logger.error('failed to open ppf')
            raise SystemExit

    fname = "NE  1e22 11MW"
    label = 'NE-11MW'
    i = 1
    plot_write_merged_sim(shot,label, data1, res1, 'NE', 'ade', tran_index1, fname,
                          allow_write_ppf,allow_plot,'blue',i)
    fname = 'NE  225e20 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data2, res2, 'NE', 'ade', tran_index2, fname,
                          allow_write_ppf,allow_plot,'green',i)
    fname = 'NE  35e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data3, res3, 'NE', 'ade', tran_index3, fname,
                          allow_write_ppf,allow_plot,'red',i)
    fname = 'NE  47e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data4, res4, 'NE', 'ade', tran_index4, fname,
                          allow_write_ppf,allow_plot,'cyan',i)
    fname = 'NE  6e22 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data5, res5, 'NE', 'ade', tran_index5, fname,
                          allow_write_ppf,allow_plot,'magenta',i)
    fname = 'NE  5e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data6, res6, 'NE', 'ade', tran_index6, fname,
                          allow_write_ppf,allow_plot,'yellow',i)
    fname = 'NE  725e20 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data7, res7, 'NE', 'ade', tran_index7, fname,
                          allow_write_ppf,allow_plot,'black',i)

    ###ionization source
    fname = 'ION 1e22 11MW'
    label = 'ION-11MW'
    i = 1
    plot_write_merged_sim(shot,label, data1, res1, 'SDII', 'asoun', tran_index1, fname,
                          allow_write_ppf,allow_plot,'blue',i)
    fname = 'ION 225e20 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data2, res2, 'SDII', 'asoun', tran_index2, fname,
                          allow_write_ppf,allow_plot,'green',i)
    fname = 'ION 35e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data3, res3, 'SDII', 'asoun', tran_index3, fname,
                          allow_write_ppf,allow_plot,'red',i)
    fname = 'ION 47e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data4, res4, 'SDII', 'asoun', tran_index4, fname,
                          allow_write_ppf,allow_plot,'cyan',i)
    fname = 'ION 6e22 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data5, res5, 'SDII', 'asoun', tran_index5, fname,
                          allow_write_ppf,allow_plot,'magenta',i)
    fname = 'ION 5e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data6, res6, 'SDII', 'asoun', tran_index6, fname,
                          allow_write_ppf,allow_plot,'yellow',i)
    fname = 'ION 725e20 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data7, res7, 'SDII', 'asoun', tran_index7, fname,
                          allow_write_ppf,allow_plot,'black',i)
    ###temperature
    fname = 'TE 1e22 11MW'
    label = 'TE-11MW'
    i =  1
    plot_write_merged_sim(shot,label, data1, res1, 'TE', 'ate', tran_index1, fname,
                          allow_write_ppf,allow_plot,'blue',i)
    fname = 'TE 225e20 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data2, res2, 'TE', 'ate', tran_index2, fname,
                          allow_write_ppf,allow_plot,'green',i)

    fname = 'TE 35e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data3, res3, 'TE', 'ate', tran_index3, fname,
                          allow_write_ppf,allow_plot,'red',i)
    fname = 'TE 47e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data4, res4, 'TE', 'ate', tran_index4, fname,
                          allow_write_ppf,allow_plot,'cyan',i)
    fname = 'TE 6e22 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data5, res5, 'TE', 'ate', tran_index5, fname,
                          allow_write_ppf,allow_plot,'magenta',i)
    fname = 'TE 5e21 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data6, res6, 'TE', 'ate', tran_index6, fname,
                          allow_write_ppf,allow_plot,'yellow',i)
    fname = 'TE 725e20 11MW'
    i = i + 1
    plot_write_merged_sim(shot,label, data7, res7, 'TE', 'ate', tran_index7, fname,
                          allow_write_ppf,allow_plot,'black',i)
    if allow_write_ppf:

        err = close_ppf(shot, 'bviola',
                    '1')

        if err != 0:
            logger.error('failed to close ppf')
            raise SystemExit

    # plt.show(block=True)


def main():
    allow_write_ppf = True
    allow_plot = False
    runFebsimulations7MW(allow_write_ppf, allow_plot)
    runFebsimulations11MW(allow_write_ppf, allow_plot)
    plt.show(block=False)


if __name__ == "__main__":

    #
    debug_map = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        4: 5,
    }
    logging.basicConfig(level=debug_map[2])

    logging.addLevelName(5, "DEBUG_PLUS")

    logger = logging.getLogger(__name__)

    del sys.modules['class_sim']
    # reload(class_sim)
    from class_sim import sim

    main()
    # EDGE2dfold = '/work/bviola/Python/EDGE2D/e2d_data'
    # workfold = 'work/Python/EDGE2D'
    # simu = sim('84600', 'nov1219', '1', workfold, 'vparail')
    # merge_profiles(simu,1569)

