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
    EDGE2dfold = '/work/bviola/Python/EDGE2D/e2d_data'
    workfold = 'work/Python/EDGE2D'
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

    shot=84600



    owner='vparail'

    dda='JSP'



    sequence=1570
    dtype = 'R'
    r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1578
    dtype = 'R'
    r2, r2_x, r2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne2, ne2_x, ne2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII2, SDII2_x, SDII2_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1574
    dtype = 'R'
    r3, r3_x, r3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne3, ne3_x, ne3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII3, SDII3_x, SDII3_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1580
    dtype = 'R'
    r4, r4_x, r4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne4, ne4_x, ne4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII4, SDII4_x, SDII4_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1581
    dtype = 'R'
    r5, r5_x, r5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne5, ne5_x, ne5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII5, SDII5_x, SDII5_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)




    sim_1 = sim('84600', 'nov1219', '2', workfold,'vparail')
    sim_2 = sim('84600', 'nov1519', '3', workfold,'vparail')
    sim_3 = sim('84600', 'nov1419', '1', workfold,'vparail')
    sim_4 = sim('84600', 'nov1619', '2', workfold,'vparail')
    sim_5 = sim('84600', 'nov1719', '1', workfold,'vparail')

    timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
    tran1 = timesteps.index(53.1903)

    res1 = sim_1.read_profiles('omp',tran=tran1)

    timesteps = list(ep.timestep(sim_2.fullpath, ALL_TRANFILES=1))
    tran2 = timesteps.index(53.1903)
    res2 = sim_2.read_profiles('omp',tran=tran2)

    timesteps = list(ep.timestep(sim_3.fullpath, ALL_TRANFILES=1))
    tran3 = timesteps.index(53.1803)
    res3 = sim_3.read_profiles('omp',tran=tran3)

    timesteps = list(ep.timestep(sim_4.fullpath, ALL_TRANFILES=1))
    tran4 = timesteps.index(53.1603)
    res4 = sim_4.read_profiles('omp',tran=tran4)

    timesteps = list(ep.timestep(sim_5.fullpath, ALL_TRANFILES=1))
    tran5 = timesteps.index(53.1503)
    res5 = sim_5.read_profiles('omp',tran=tran5)

    fname = 'density profile OMP 11MW'
    plt.figure(num= fname)
    plt.title(fname)
    print(ne1_t[tran1])
    plt.plot(r1[tran1],ne1[tran1],label='1',color='red',linestyle=':')
    plt.plot(res1['dsrad'][0:]+r1[-1][-1],res1['ade'].yData[0:],color='red',linestyle=':')

    print(ne2_t[tran2])
    plt.plot(r2[tran2],ne2[tran2],label='2',color='blue',linestyle=':')
    plt.plot(res2['dsrad'][0:]+r2[-1][-1],res2['ade'].yData[0:],color='blue',linestyle=':')

    print(ne3_t[tran3])
    plt.plot(r3[tran3],ne3[tran3],label='3',color='magenta',linestyle=':')
    plt.plot(res3['dsrad'][0:]+r3[-1][-1],res3['ade'].yData[0:],color='magenta',linestyle=':')

    print(ne4_t[tran4])
    plt.plot(r4[tran4],ne4[tran4],label='4',color='green',linestyle=':')
    plt.plot(res4['dsrad'][0:]+r4[-1][-1],res4['ade'].yData[0:],color='green',linestyle=':')

    print(ne5_t[tran5])
    plt.plot(r5[tran5],ne5[tran5],label='5',color='black',linestyle=':')
    plt.plot(res5['dsrad'][0:]+r5[-1][-1],res5['ade'].yData[0:],color='black',linestyle=':')

    plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
    plt.savefig('./figures/' + fname, format='eps', dpi=300)
    plt.savefig('./figures/' + fname, dpi=300)  #

    ###ionization source
    fname = 'ionization source profile OMP 11MW'
    plt.figure(num= fname)
    plt.title(fname)
    print(ne1_t[tran1])
    plt.plot(r1[tran1][0:-1],SDII1[tran1][0:-1],label='1',color='red',linestyle=':')
    plt.plot(res1['dsrad'][1:]+r1[-1][-1],res1['asoun'].yData[1:],color='red',linestyle=':')

    print(ne2_t[tran2])
    plt.plot(r2[tran2][0:-1],SDII2[tran2][0:-1],label='2',color='blue',linestyle=':')
    plt.plot(res2['dsrad'][1:]+r2[-1][-1],res2['asoun'].yData[1:],color='blue',linestyle=':')

    print(ne3_t[tran3])
    plt.plot(r3[tran3][0:-1],SDII3[tran3][0:-1],label='3',color='magenta',linestyle=':')
    plt.plot(res3['dsrad'][1:]+r3[-1][-1],res3['asoun'].yData[1:],color='magenta',linestyle=':')

    print(ne4_t[tran4])
    plt.plot(r4[tran4][0:-1],SDII4[tran4][0:-1],label='4',color='green',linestyle=':')
    plt.plot(res4['dsrad'][1:]+r4[-1][-1],res4['asoun'].yData[1:],color='green',linestyle=':')

    print(ne5_t[tran5])
    plt.plot(r5[tran5][0:-1],SDII5[tran5][0:-1],label='5',color='black',linestyle=':')
    plt.plot(res5['dsrad'][1:]+r5[-1][-1],res5['asoun'].yData[1:],color='black',linestyle=':')

    plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
    plt.savefig('./figures/' + fname, format='eps', dpi=300)
    plt.savefig('./figures/' + fname, dpi=300)  #


    #####just core
    # plt.figure()
    # plt.title('11MW')
    # print(ne1_t[tran1])
    # plt.plot(ne1_x,ne1[tran1],label='1',color='red')
    # # plt.plot(res1['dsrad']+r1[-1][-1],res1['ade'].yData,color='red')
    #
    # print(ne2_t[tran2])
    # plt.plot(ne2_x,ne2[tran2],label='2',color='blue')
    # # plt.plot(res2['dsrad']+r2[-1][-1],res2['ade'].yData,color='blue')
    #
    # print(ne3_t[tran3])
    # plt.plot(ne3_x,ne3[tran3],label='3',color='magenta')
    # # plt.plot(res3['dsrad']+r3[-1][-1],res3['ade'].yData,color='magenta')
    #
    # print(ne4_t[tran4])
    # plt.plot(ne4_x,ne4[tran4],label='4',color='green')
    # # plt.plot(res4['dsrad']+r4[-1][-1],res4['ade'].yData,color='green')
    #
    # print(ne5_t[tran5])
    # plt.plot(ne5_x,ne5[tran5],label='5',color='black')
    # # plt.plot(res5['dsrad']+r5[-1][-1],res5['ade'].yData,color='black')
    #
    # plt.xlim(left=0.79,right=1.01)




    #####just edge
    # plt.figure()
    # plt.title('11MW')
    # print(ne1_t[tran1])
    # # plt.plot(r1[-2],ne1[-2],label='1',color='red')
    # plt.plot(res1['dsrad'],res1['ade'].yData,color='red')
    #
    # print(ne2_t[tran2])
    # # plt.plot(r2[-1],ne2[-1],label='2',color='blue')
    # plt.plot(res2['dsrad'],res2['ade'].yData,color='blue')
    #
    # print(ne3_t[tran3])
    # # plt.plot(r3[-1],ne3[-1],label='3',color='magenta')
    # plt.plot(res3['dsrad'],res3['ade'].yData,color='magenta')
    #
    # print(ne4_t[tran4])
    # # plt.plot(r4[-1],ne4[-1],label='4',color='green')
    # plt.plot(res4['dsrad'],res4['ade'].yData,color='green')
    #
    # print(ne5_t[tran5])
    # # plt.plot(r5[-1],ne5[-1],label='5',color='black')
    # plt.plot(res5['dsrad'],res5['ade'].yData,color='black')


    # plt.show(block=True)



######## 7 MW

    shot=84600



    owner='vparail'

    dda='JSP'

    sim_1 = sim('84600', 'nov1219', '1', workfold,'vparail')
    sim_2 = sim('84600', 'nov1419', '2', workfold,'vparail')
    sim_3 = sim('84600', 'nov1519', '2', workfold,'vparail')
    sim_4 = sim('84600', 'nov1319', '1', workfold,'vparail')


    timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
    tran1 = timesteps.index(53.1403)

    res1 = sim_1.read_profiles('omp',tran=tran1)

    timesteps = list(ep.timestep(sim_2.fullpath, ALL_TRANFILES=1))
    tran2 = timesteps.index(53.1902)
    res2 = sim_2.read_profiles('omp',tran=tran2)

    timesteps = list(ep.timestep(sim_3.fullpath, ALL_TRANFILES=1))
    tran3 = timesteps.index(53.1603)
    res3 = sim_3.read_profiles('omp',tran=tran3)

    timesteps = list(ep.timestep(sim_4.fullpath, ALL_TRANFILES=1))
    tran4 = timesteps.index(53.1903)
    res4 = sim_4.read_profiles('omp',tran=tran4)




    sequence=1569
    dtype = 'R'
    r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1575
    dtype = 'R'
    r2, r2_x, r2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne2, ne2_x, ne2_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII2, SDII2_x, SDII2_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1577
    dtype = 'R'
    r3, r3_x, r3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne3, ne3_x, ne3_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII3, SDII3_x, SDII3_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)

    sequence = 1573
    dtype = 'R'
    r4, r4_x, r4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne4, ne4_x, ne4_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII4, SDII4_x, SDII4_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)






    fname = 'density profile OMP 7MW'
    plt.figure(num= fname)
    plt.title(fname)
    print(ne1_t[tran1])
    plt.plot(r1[tran1],ne1[tran1],label='1',color='red',linestyle=':')
    plt.plot(res1['dsrad'][0:]+r1[-1][-1],res1['ade'].yData[0:],color='red',linestyle=':')

    print(ne2_t[tran2])
    plt.plot(r2[tran2],ne2[tran2],label='2',color='blue',linestyle=':')
    plt.plot(res2['dsrad'][0:]+r2[-1][-1],res2['ade'].yData[0:],color='blue',linestyle=':')

    print(ne3_t[tran3])
    plt.plot(r3[tran3],ne3[tran3],label='3',color='magenta',linestyle=':')
    plt.plot(res3['dsrad'][0:]+r3[-1][-1],res3['ade'].yData[0:],color='magenta',linestyle=':')

    print(ne4_t[tran4])
    plt.plot(r4[tran4],ne4[tran4],label='4',color='green',linestyle=':')
    plt.plot(res4['dsrad'][0:]+r4[-1][-1],res4['ade'].yData[0:],color='green',linestyle=':')


    plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
    plt.savefig('./figures/' + fname, format='eps', dpi=300)
    plt.savefig('./figures/' + fname, dpi=300)  #


    ###ionization source
    fname = 'ionization source profile OMP 7MW'
    plt.figure(num= fname)
    plt.title(fname)
    print(ne1_t[tran1])
    plt.plot(r1[tran1][0:-1],SDII1[tran1][0:-1],label='1',color='red',linestyle=':')
    plt.plot(res1['dsrad'][1:]+r1[-1][-1],res1['asoun'].yData[1:],color='red',linestyle=':')

    print(ne2_t[tran2])
    plt.plot(r2[tran2][0:-1],SDII2[tran2][0:-1],label='2',color='blue',linestyle=':')
    plt.plot(res2['dsrad'][1:]+r2[-1][-1],res2['asoun'].yData[1:],color='blue',linestyle=':')

    print(ne3_t[tran3])
    plt.plot(r3[tran3][0:-1],SDII3[tran3][0:-1],label='3',color='magenta',linestyle=':')
    plt.plot(res3['dsrad'][1:]+r3[-1][-1],res3['asoun'].yData[1:],color='magenta',linestyle=':')

    print(ne4_t[tran4])
    plt.plot(r4[tran4][0:-1],SDII4[tran4][0:-1],label='4',color='green',linestyle=':')
    plt.plot(res4['dsrad'][1:]+r4[-1][-1],res4['asoun'].yData[1:],color='green',linestyle=':')


    plt.xlim(left=3.795,right=max(res5['dsrad']+r5[-1][-1]))
    plt.savefig('./figures/' + fname, format='eps', dpi=300)
    plt.savefig('./figures/' + fname, dpi=300)  #


    #####just core
    # plt.figure()
    # plt.title('7MW')
    #
    # plt.plot(ne1_x,ne1[tran1],label='1',color='red')
    # # plt.plot(res1['dsrad']+r1[-1][-1],res1['ade'].yData,color='red')
    #
    # plt.plot(ne2_x,ne2[tran2],label='2',color='blue')
    # # plt.plot(res2['dsrad']+r2[-1][-1],res2['ade'].yData,color='blue')
    #
    # plt.plot(ne3_x,ne3[tran3],label='3',color='magenta')
    # # plt.plot(res3['dsrad']+r3[-1][-1],res3['ade'].yData,color='magenta')
    #
    # plt.plot(ne4_x,ne4[tran4],label='4',color='green')
    # # plt.plot(res4['dsrad']+r4[-1][-1],res4['ade'].yData,color='green')
    #
    #
    # plt.xlim(left=0.79,right=1.01)




    #####just edge
    # plt.figure()
    # plt.title('7MW')
    # # plt.plot(r1[-2],ne1[-2],label='1',color='red')
    # plt.plot(res1['dsrad'],res1['ade'].yData,color='red')
    #
    # # plt.plot(r2[-1],ne2[-1],label='2',color='blue')
    # plt.plot(res2['dsrad'],res2['ade'].yData,color='blue')
    #
    #
    # # plt.plot(r3[-1],ne3[-1],label='3',color='magenta')
    # plt.plot(res3['dsrad'],res3['ade'].yData,color='magenta')
    #
    #
    # # plt.plot(r4[-1],ne4[-1],label='4',color='green')
    # plt.plot(res4['dsrad'],res4['ade'].yData,color='green')












    logger.info('plotting HRTS NE')
    # %%


    fnorm = 1
    ftitle = 'Electron Density OMP'
    # fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
    fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'

    plt.figure(num=fname + "_" + pulse1.label)
    try:
        plt.errorbar(pulse1.hrts_profiles['R'] +0.035,
                     pulse1.hrts_profiles['NE'], label='_nolegend_',
                     yerr=pulse1.hrts_profiles['DNE'], fmt=None,
                     ecolor='black')
    except:
        logger.error('impossible to plot pulse1 NE from HRTS')
    # try:
    #     plt.scatter(pulse1.hrts_fit['Rfit'] + float(pulse1.shift_fit),
    #                 pulse1.hrts_fit['nef3'], label='_nolegend_',
    #                 color='black')
    # except:
    #     logger.error('impossible to plot pulse2 NE HRTS fit')



    try:
        plt.errorbar(pulse2.hrts_profiles['R'] +0.035,
                     pulse2.hrts_profiles['NE'], label='_nolegend_',
                     yerr=pulse2.hrts_profiles['DNE'], fmt=None,
                     ecolor='red')
    except:
        logger.error('impossible to plot pulse2 NE from HRTS')
    # try:
    #     plt.scatter(pulse2.hrts_fit['Rfit'] + float(pulse2.shift_fit),
    #                 pulse2.hrts_fit['nef3'], label='_nolegend_',
    #                 color='red')
    # except:
    #     logger.error('impossible to plot pulse2 NE HRTS fit')


    sim_1 = sim('84600', 'nov1219', '1', workfold,'vparail')
    timesteps = list(ep.timestep(sim_1.fullpath, ALL_TRANFILES=1))
    tran1 = timesteps.index(53.1403)


    sim_5 = sim('84600', 'nov1719', '1', workfold,'vparail')
    timesteps = list(ep.timestep(sim_5.fullpath, ALL_TRANFILES=1))
    tran5 = timesteps.index(53.1503)
    res5 = sim_5.read_profiles('omp',tran=tran5)


    sequence=1569
    dtype = 'R'
    r1, r1_x, r1_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne1, ne1_x, ne1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII1, SDII1_x, SDII1_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)


    sequence = 1581
    dtype = 'R'
    r5, r5_x, r5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'NE'
    ne5, ne5_x, ne5_t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppf.ppfdata(shot,dda,dtype, seq=sequence, uid=owner, reshape=1)
    dtype = 'SDII'
    SDII5, SDII5_x, SDII5_t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier= ppf.ppfdata(shot, dda, dtype, seq=sequence, uid=owner, reshape=1)


    plt.plot(r1[tran1],ne1[tran1]/1e19,label='1',color='black',linestyle=':',linewidth=3)
    data = [data/1e19 for data in res1['ade'].yData[0:]]
    plt.plot(res1['dsrad'][0:]+r1[-1][-1],data,color='black',linestyle=':',linewidth=3)

    plt.plot(r5[tran1],ne5[tran5]/1e19,label='5',color='red',linestyle=':',linewidth=3)
    data = [data / 1e19 for data in res5['ade'].yData[0:]]
    plt.plot(res5['dsrad'][0:]+r5[-1][-1],data,color='red',linestyle=':',linewidth=3)


    plt.xlim(left=3.75)

    plt.show(block=True)