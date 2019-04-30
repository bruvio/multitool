#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:08:45 2017

@author: bruvio
"""
# from importlib import reload
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
import sys
import math
import csv
import pathlib
import os
from class_sim import sim
from class_sim import Getdata
from class_sim import initread
from class_sim import find_indices
import eproc as ep
from ppf import *

def e2d_variables(file):
    with open(file) as f:
        lines = f.readlines()
    variables = []
    for line in lines[0:]:
        # print('line', line)
        columns = line.split()
        variables.append(columns[0])
    f.close()
    return variables
from matplotlib.collections import PatchCollection
def sqrt(s):
    return math.sqrt(s)
#def initread(shot,userid,seq):
	#ppfsetdevice('JET')
	#print('ok')
	#ppfuid(userid,'r')
	#ier=ppfgo(int(shot),int(seq))
	##print('ok')

#def Getdata(pulse, dda,dtype,sequence,user):
	#'''
	#ARGS
	#pulse1 :=  pulse

	#dda := string e.g. 'kg1v'
	#dtype:= string e.g. 'lid3'
	#RETURNS
	#'''
	#initread(int(pulse),user,int(sequence))
	##print('ok1')
	#data,x,t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier=ppfdata(int(pulse),dda,dtype,seq=int(sequence),uid=user,device="JET",
                        #fix0=0,reshape=0,no_x=0,no_t=0)
	##ihdat,iwdat,data,x,t,ier=ppfget(int(pulse),dda,dtype)
	##pulse,seq,iwdat,comment,numdda,ddalist,ier=ppfinf(comlen=50,numdda=50)
	## info,cnfo,ddal,istl,pcom,pdsn,ier=pdinfo(pulse,seq)
	## istat,ier = ppfgsf(pulse,seq,dda,dtype,mxstat=1)
	#return{'dunits':dunits,
			#'desc':desc,
		  #'xunits':xunits,
		  #'data':data,
		  #'x':x,
		  #'t':t,
		  #'ier':ier,
		  #'sequence':seq}
#def contour_plots(self,var,ExtraInput):





if __name__ == "__main__":

    EDGE2dfold='/work/bviola/Python/EDGE2D/e2d_data'
    workfold='work/Python/EDGE2D'
    #

    del sys.modules['class_sim']
    from class_sim import sim
    # from class_sim import set_folder

    # ppp=sim('92123','jul1717','2',workfold)
    # # print(ppp.workingdir)
    # # ppp.initfolder('work/Python/EDGE2D')
    # # dire='e2d_data'
    # # pathlib.Path(ppp.workingdir + os.sep + dire + os.sep + ppp.shot).mkdir(parents=True, exist_ok=True)
    # # reload(class_sim)
    #
    # simu1=sim('92123','jul1717','2','bviola','edge2d')
    # lfe=sim('92121','feb0218','1','bviola','edge2d')
    # hfe=sim('92123','feb0218','1','bviola','edge2d')
    #
    # #simu2=sim('92123','aug1717','1','bviola','edge2d')
    # #simu3=sim('92123','aug1717','2','bviola','edge2d')
    # simu4=sim('92123','aug1717','3','bviola','edge2d')
    # simlist=[]
    # simlist.append([simu4])
    # sim_lfe_unseeded = sim('92121', 'apr1618', '5', 'bviola', 'edge2d')
    #
    #
    #
    # sim_hfe_unseeded =sim('92123', 'apr1618', '5', 'bviola', 'edge2d')


    #sim_hfe_Nrad0 = sim('92123', 'oct1917', '1',workfold)
    #sim_hfe_Nrad1= sim('92123', 'aug1717', '6',workfold)


    #sim_lfe_Nrad0 = sim('92121', 'aug1717', '2',workfold)
    #sim_lfe_Nrad1= sim('92121', 'aug1717', '3',workfold)
    #simlist = []
    #simlist.append([sim_hfe_Nrad0,'HFE_3MW'])
    #simlist.append([sim_hfe_Nrad1,'HFE_5MW'])
    #simlist.append([sim_lfe_Nrad0,'LFE_2MW'])
    #simlist.append([sim_lfe_Nrad1,'LFE_3MW'])




    #omp_index = sim_lfe_Nrad0.find_omp_index()
    ##
    # # first open cell on the OMP row
    ## first_open_omp_cell_row = lfe.find_omp_index_row()
    # # calculate connection length
    #l_lfe = sim_lfe_Nrad0.calc_connection_length(omp_index)
    #print(l_lfe)
    #tpm_lfe_unseeded=sim_lfe_Nrad0.TPMscaling_Petrie(l_lfe)





    #omp_index1 = sim_hfe_Nrad0.find_omp_index()
    ##
    ## # first open cell on the OMP row
    ## first_open_omp_cell_row = hfe.find_omp_index_row()
    ## # calculate connection length
    #l_hfe = sim_hfe_Nrad0.calc_connection_length(omp_index1)
    #print(l_hfe)
    #tpm_hfe_unseeded  = sim_hfe_Nrad0.TPMscaling_Petrie(l_hfe)
    #print(tpm_lfe_unseeded['ntar'],tpm_hfe_unseeded['ntar'])
    #print(tpm_lfe_unseeded['ttar'],tpm_hfe_unseeded['ttar'])
    ## raise SystemExit

    #ne1,te1=sim_lfe_Nrad0.nete_omp()

    #ne2, te2 = sim_hfe_Nrad0.nete_omp()



    #print(ne1,te1)
    #print(ne2,te2)
    #print(ne3,te3)
    #print(ne4,te4)
    #print(ne5,te5)


    #raise SystemExit
    ## for index1 in range(0,len(simlist)):
    ##   simu=simlist[index1][0]
    ##   #print(simu)
    ##   var_H=simu.read_data('SQEHRAD','HFE')
    ##   #var_H=-np.trim_zeros(var_H['data'],'b')
    ##   try:
    ##     var_SQERZ_1=simu.read_data('SQEZR_1','HFE')
    ##     #var_SQERZ_1=-np.trim_zeros(var_SQERZ_1['data'],'b')
    ##   except:
    ##     print('no SQEZR_1')
    ##     var_SQERZ_1['data']=0
    ##   try:
    ##     var_SQERZ_2=simu.read_data('SQEZR_2','HFE')
    ##     #var_SQERZ_2=-np.trim_zeros(var_SQERZ_2['data'],'b')
    ##   except:
    ##     print('no SQEZR_2')
    ##     var_SQERZ_2['data']=0
    ##   #
    ##   var=var_H['data']+var_SQERZ_1['data']+var_SQERZ_2['data']
    ##   #var=var_H+var_SQERZ_1+var_SQERZ_2
    ##   var=-np.trim_zeros(var,'b')
    ##   simu.contour(var,'testprad'+str(index1),'HFE',upperbound=3.5e6,label='MW/m^3')
    ## raise SystemExit
    ## for index1 in range(0, len(simlist)):
    ##       simu = simlist[index1][0]
    ##       # print(simu)
    ##       var_H = ep.data(simu.fullpath,'SQEHRAD').data
    ##       # var_H=-np.trim_zeros(var_H['data'],'b')
    ##       try:
    ##           var_SQERZ_1 = ep.data(simu.fullpath,'SQEZR_1').data
    ##           # var_SQERZ_1=-np.trim_zeros(var_SQERZ_1['data'],'b')
    ##       except:
    ##           print('no SQEZR_1')
    ##           var_SQERZ_1 = 0
    ##       try:
    ##           var_SQERZ_2 = ep.data(simu.fullpath,'SQEZR_2').data
    ##           # var_SQERZ_2=-np.trim_zeros(var_SQERZ_2['data'],'b')
    ##       except:
    ##           print('no SQEZR_2')
    ##           var_SQERZ_2 = 0
    ##       #
    ##       var = var_H + var_SQERZ_1 + var_SQERZ_2
    ##       # var=var_H+var_SQERZ_1+var_SQERZ_2
    ##       var = -np.trim_zeros(var, 'b')
    ##       simu.contour(var, 'testprad' + str(index1), upperbound=3.5e6,
    ##                    label='MW/m^3')
    ## raise SystemExit

    ##sim_list=[]
    ##sim_list.append([simu1,'HFE'])
    ##sim_list.append([simu1,'HFE'])
    ##sim_list.append([simu1,'HFE'])
    ##sim_list.append([simu1,'HFE'])
    ##targetfilename='test_pump_cur'

    ##raise SystemExit

    ##sim_list=[]
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##targetfilename='test_eirene_cur'
    ##simu1.write_eirene_cur2file(sim_list,EDGE2dfold,targetfilename)
    ##raise SystemExit

    #sim_list=[]
    ## sim_list.append([lfe,84, 85,'LFE'])
    ## sim_list.append([hfe,84, 85,'HFE'])
    ## #sim_list.append([simu1,84, 85,'HFE'])
    ## #sim_list.append([simu1,84, 85,'HFE'])
    #simu1 = sim('92123', 'apr1118', '1', 'bviola', 'edge2d')
    ## simu1=sim('92123','jul1717','2','bviola','edge2d')
    #sim_list.append([simu1, 85, 86])
    ## sim_list.append(simu1)
    #targetfilename='92123_DC_us_2018'
    #sim.write_print2file(sim_list,EDGE2dfold,targetfilename)
    #sim.write_pump_cur2file(sim_list, EDGE2dfold, targetfilename)
    ## raise SystemExit
    ## omp = simu1.read_profiles('OMP')
    #sim.write_edge2d_profiles(sim_list,targetfilename)
    ## print(omp)
    ## result=simu1.read_print_file_edge2d()
    ## print(result.values())


    ##sim_list=[]
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##sim_list.append([simu1,84, 85,'HFE'])
    ##targetfilename='test_powerbalance'
    #sim.write_powerbalance2file(sim_list,EDGE2dfold,targetfilename)
    ##result1=simu1.read_power_balance()
    ##print(result1.values())
    ## raise SystemExit
    ## sim_list.append([simu1, 84, 85, 'LFE'])
    #sim.write_eirene_cur2file(sim_list, EDGE2dfold, targetfilename)
    ##raise SystemExit
    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    ##aa=simu.read_neutflux(84, 85)
    ##print(aa['neutcurrent_net'])
    ##ppp1=simu.eirene_netcur(84,85,'HFE')
    ##print(ppp1)
    ## raise SystemExit

    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    #ddd21=simu1.read_profiles('OMP')
    #print(ddd21['ade'].yData)
    #print(ddd21['adi'].yData)
    #print(ddd21['ate'].yData)
    #print(ddd21['ati'].yData)
    ## raise SystemExit
    #sim.execute_makeppf(sim_list, EDGE2dfold, 'makeppf.h')
    ## simu=sim('92123','jul1717','2','bviola','edge2d')
    ## neut=simu1.read_eirene_pump()
    #raise SystemExit


    ##aa=simu1.eirene_pumpcur('HFE')
    ##raise SystemExit


    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    ##simu.read_e2d_ppf('PY4D','ISI',325,'HFE')
    ##simu.read_e2d_ppf('PY4D','ISO',325,'HFE')
    ##simu.read_e2d_ppf('PY4D','TEO',325,'HFE')
    ##simu.read_e2d_ppf('PY4D','TEI',325,'HFE')
    ##simu.read_e2d_ppf('PY4D','NEO',325,'HFE')
    ##simu.read_e2d_ppf('PY4D','NEI',325,'HFE')
    ##simu.read_e2d_ppf('PB5','VERT',325,'HFE')
    ##simu.read_e2d_ppf('PB5','HORI',325,'HFE')
    ##simu.read_e2d_ppf('PS3','H0MO',325,'HFE')
    ##simu.read_e2d_ppf('PS3','H0MI',325,'HFE')
    ##raise SystemExit

    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    ##print(simu.shot)
    ##data=Getdata(simu.shot, 'PY4D','ISI',325,simu.owner)
    ##print(data['desc'])
    ##print(data['sequence'])
    ##print(data['ier'])
    ##print(data['data'])
    ###print(data['x'])
    ##sys.exit()
    ##raise SystemExit

    ###var=simu.read_data('SOUN','HFE')
    ###var=np.trim_zeros(var['data'],'b')
    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    ###simu.contour('HFE',var,'test_SOUN')
    ##sim_lfe=[]
    ##simu2_lfe=sim('92121','aug1717','2','bviola','edge2d')
    ##simu3_lfe=sim('92121','aug1717','3','bviola','edge2d')
    ##simu=sim('92121','aug1717','4','bviola','edge2d')
    ##sim_lfe.append([simu2_lfe])
    ##sim_lfe.append([simu3_lfe])
    ###sim_lfe=[]
    ###sim_lfe.append([simu])  



    ##sim_hfe=[]
    ##simu2_hfe=sim('92123','oct1917','1','bviola','edge2d')
    ##simu3_hfe=sim('92123','aug1717','6','bviola','edge2d')
    ##sim_hfe.append(simu2_hfe)
    ##sim_hfe.append(simu3_hfe)

    ###getdes=e2d_variables("./getdes_row.txt")
    ###getdes2=e2d_variables("./getdes_data.txt")
  


    ##for index1 in range(0,len(sim_lfe)):
      ##simu=sim_lfe[index1][0] 
      ###print(simu)
      ##var_H=simu.read_data('SQEHRAD','HFE')
      ###var_H=-np.trim_zeros(var_H['data'],'b')
      ##try:
        ##var_SQERZ_1=simu.read_data('SQEZR_1','HFE')
        ###var_SQERZ_1=-np.trim_zeros(var_SQERZ_1['data'],'b')
      ##except:  
        ##print('no SQEZR_1')
        ##var_SQERZ_1['data']=0
      ##try:
        ##var_SQERZ_2=simu.read_data('SQEZR_2','HFE')
        ###var_SQERZ_2=-np.trim_zeros(var_SQERZ_2['data'],'b')
      ##except:
        ##print('no SQEZR_2')
        ##var_SQERZ_2['data']=0

      ##var=var_H['data']+var_SQERZ_1['data']+var_SQERZ_2['data']
      ###var=var_H+var_SQERZ_1+var_SQERZ_2
      ##var=-np.trim_zeros(var,'b')
      ##simu.contour('LFE',var,'prad'+str(index1),upperbound=5e6)


    ##raise SystemExit

    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    ##var=simu.read_data('DENEL','HFE')
    ##var=np.trim_zeros(var['data'],'b')
    ##simu.contour('HFE',var,'denel')


    ##var_H=simu.read_data('SQEHRAD','HFE')
    ##var_SQERZ_1=simu.read_data('SQEZR_1','HFE')
    ##var_SQERZ_2=simu.read_data('SQEZR_2','HFE')
    ##var=var_H['data']+var_SQERZ_1['data']+var_SQERZ_2['data']
    ##var=-np.trim_zeros(var,'b')
    ##simu.contour('HFE',var,'prad',upperbound=3.55e6)
    ##raise SystemExit

    #simu=sim('92123','jul1717','2','bviola','edge2d')
    #bb=simu.read_radiation_split(30,'HFE')
    #print('hfsrad', bb['hfsrad'])
    #simu1=sim('92123','jul1717','2','bviola','edge2d')
    #bb=simu1.read_radiation_split(30)
    #print('hfsrad', bb['hfsrad'])
    #raise SystemExit
    #print('lfsrad', bb['lfsrad'])
    #print('rad_div_bxp', bb['rad_div_bxp'])
    #print('rad_axp', bb['rad_axp'])
    #aa=simu.read_psol_pradpsol('HFE')
    ## print(aa)
    #print('raddivsum',    aa['raddivsum'])
    #print(   'pradcore',  aa['pradcore'])
    #print(  'pradsol' ,  aa['pradsol'])
    #print(   'pradtot',  aa['pradtot'])
    #print(  'fradsol'  , aa['fradsol'])
    #print( 'fraddiv'  ,  aa['fraddiv'])
    #print(  'fradsol2',   aa['fradsol2'])
    #print(  'hrad' ,  aa['hrad'])
    #print(   'brad',  aa['brad'])
    #print(   'nrad',  aa['nrad'])
    #raise SystemExit
    #qiflx=ep.row(lfe.fullpath,'qiflxd','OT')
    #qeflx=ep.row(lfe.fullpath,'qeflxd','OT')

    ## sim.calc_lambda_q(qiflx)
    #omp_index = lfe.find_omp_index()
    ##
    ## # first open cell on the OMP row
    ## first_open_omp_cell_row = lfe.find_omp_index_row()
    ## # calculate connection length
    #l = lfe.calc_connection_length(omp_index)
    #print(l)
    #omp_index1 = hfe.find_omp_index()
    ##
    ## # first open cell on the OMP row
    ## first_open_omp_cell_row = hfe.find_omp_index_row()
    ## # calculate connection length
    #l = simu4.calc_connection_length(omp_index1)
    #print(l)
    #te,ti=lfe.calculate_upstream_t()
    #print(te,ti)
    #raise SystemExit


    ##def testtt(nome,eta=None,paese=None):
      ##if eta is None:
        ##eta=30
      ##if paese is None:
        ##paese='Italia'
      ##print(nome+' ha '+str(eta)+' anni'+' ed viene da '+paese)
  
    ##testtt('Marco')      
    ##testtt('Bruno',eta=35)      
    ##testtt('Maria',eta=24,paese='Spagna')
    ##testtt('Lucia',paese='Grecia')
      

      
    ##simu=sim_lfe[0][0]]
    ##simu=sim('92123','jul1717','2','bviola','edge2d')
    ##var=simu.read_data('SQEZR_2','HFE')
    ##var=-np.trim_zeros(var['data'],'b')
    ##simu.contour('HFE',var,'test')

    ##simul=sim('92123','jul1717','2','bviola','edge2d')
    ##outfile = 'test_makeppf.sh'
    ##simu_list=[]
    ##simu_list.append(simul)
    ##simu_list.append(simul)
    ##outfile = 'test_makeppf.sh'

    ##simu.execute_makeppf(simu_list,outfile)

##plt.savefig('./figures/'+fname, format='eps', dpi=600)
#plt.savefig('./figures/'+fname,  dpi=600) #



    EDGE2dfold='./e2d_data'
    workfold='work/Python/EDGE2D'
    #
    #import sys
    #del sys.modules['class_sim']
    #del sys.modules['class_eirene']
    
    from class_sim import sim
    from class_eirene import Eirene
    
    
    # sim_lfe = sim('92121', 'aug1717', '1', workfold)
    # sim_hfe = sim('92123', 'aug1717', '2', workfold)
    
    
    sim_hfe_Nrad0 = sim('92123', 'oct1917', '1', workfold)
    sim_hfe_Nrad1 = sim('92123', 'aug1717', '6', workfold)
    
    sim_lfe_Nrad0 = sim('92121', 'aug1717', '3', workfold)
    sim_lfe_Nrad1 = sim('92121', 'aug1717', '4', workfold)
    
    sim_lfe_81472 = sim('81472', 'may2316', '6', workfold)
    sim_hfe_81472 = sim('81472', 'may2316', '1', workfold)
    
    # simlist=[]
    # workfold = 'work/Python/EDGE2D'
    # simu = sim('84598X', 'nov0518', '1',workfold);
    # simlist.append([sim_lfe_Nrad0,'test'])
    # for index1 in range(0, len(simlist)):
    #     simu = simlist[index1][0]
    #     label = simlist[index1][1]
    #     simu.contour('DENEL', 'denel_' + label)
    # raise SystemExit
    simlist = []
    simlist.append([sim_hfe_Nrad0, 'HFE_3MW'])
    # simlist.append([sim_hfe_Nrad1, 'HFE_5MW'])
    #
    # simlist.append([sim_lfe_Nrad0, 'LFE_2MW'])
    # simlist.append([sim_lfe_Nrad1, 'LFE_3MW'])
    
    # omp_index = sim_lfe_Nrad0.find_omp_index()
    #
    # # first open cell on the OMP row
    # first_open_omp_cell_row = lfe.find_omp_index_row()
    # # calculate connection length
    # l_lfe = sim_lfe_Nrad0.calc_connection_length(omp_index)
    # print(l_lfe)
    # tpm_lfe_unseeded = sim_lfe_Nrad0.TPMscaling_Petrie(l_lfe)
    
    # omp_index1 = sim_hfe_Nrad0.find_omp_index()
    #
    # # first open cell on the OMP row
    # first_open_omp_cell_row = hfe.find_omp_index_row()
    # # calculate connection length
    # l_hfe = sim_hfe_Nrad0.calc_connection_length(omp_index1)
    # print(l_hfe)
    # tpm_hfe_unseeded = sim_hfe_Nrad0.TPMscaling_Petrie(l_hfe)
    # print(tpm_lfe_unseeded['ntar'], tpm_hfe_unseeded['ntar'])
    # print(tpm_lfe_unseeded['ttar'], tpm_hfe_unseeded['ttar'])
    # raise SystemExit
    
    # ne1, te1 = sim_lfe_Nrad0.nete_omp()
    
    # ne2, te2 = sim_hfe_Nrad0.nete_omp()
    
    # print(ne1, te1)
    # print(ne2, te2)
    # print(ne3, te3)
    # print(ne4, te4)
    # print(ne5, te5)
    #
    # # contour = False
    # contour = True
    # if contour is True:
    #     # sim.(simlist,3.5e6)
    #     # plt.show(block=True)
    #
    #     for index1 in range(0, len(simlist)):
    #         simu = simlist[index1][0]
    #         label= simlist[index1][1]
    #         var = ep.data(simu.fullpath, 'soun').data
    #         var = -np.trim_zeros(var, 'b')
    #         simu.contour(var, 'soun_' + label)
    #         plt.show(block=True)
    # sim_hfe_Nrad0.contour()
    
    
    # print_lfe= sim_lfe_Nrad0.read_print_file_edge2d()
    # print_hfe= sim_hfe_Nrad0.read_print_file_edge2d()
    
    
    # print(print_lfe['ionflux_sol_outdiv'])
    # print(print_lfe['ionflux_sol_indiv'])
    #
    # print(print_hfe['ionflux_sol_outdiv'])
    # print(print_hfe['ionflux_sol_indiv'])
    #
    #
    # lfe_pb = sim_lfe_Nrad1.read_print_file_edge2d()
    # hfe_pb = sim_hfe_Nrad1.read_print_file_edge2d()
    #
    # sim.bar_power_balance(lfe_pb,'LFE')
    # sim.bar_power_balance(hfe_pb,'HFE')
    #
    # lfe_pb = sim_lfe_81472.read_print_file_edge2d()
    # hfe_pb = sim_hfe_81472.read_print_file_edge2d()
    #
    # sim.bar_power_balance(sim_lfe_81472,'LFE')
    # sim.bar_power_balance(sim_hfe_81472,'HFE')
    
    sim_hfe_Nrad0.read_eirene('/home/alexc/cmg/catalog/edge2d/jet/84727/nov1015/seq#1/')
    sim_hfe_Nrad0.data.eirene.plot_eirene()
    raise SystemExit

    # sim_hfe_Nrad0.data.eirene.plot_eirene()

    x = [sim_hfe_Nrad0.data.eirene.geom.xv[i] for i in
         sim_hfe_Nrad0.data.eirene.geom.trimap]
    y = [sim_hfe_Nrad0.data.eirene.geom.yv[i] for i in
         sim_hfe_Nrad0.data.eirene.geom.trimap]

    # matplotlib.pyplot.tricontourf(x, y, sim_hfe_Nrad0.data.eirene.MOL.data)





    # plt.tricontourf(sim_hfe_Nrad0.data.eirene.geom.xv,sim_hfe_Nrad0.data.eirene.geom.yv,sim_hfe_Nrad0.data.eirene.geom.trimap,sim_hfe_Nrad0.data.eirene.MOL.data[1])

    var=sim_hfe_Nrad0.data.eirene.MOL.data[1]
    label = 'MOL m^{-3}'
    # if lowerbound is None:
    lower = min(var)
    # else:
    #   lower=lowerbound
    # if upperbound is None:
    upper = max(var)
    # else:
    #   upper=upperbound
    x1=[]
    x2=[]
    x3=[]
    for i,value in enumerate(x):
        x1.append(x[i][0])
        x2.append(x[i][1])
        x3.append(x[i][2])
    y1=[]
    y2=[]
    y3=[]
    for i,value in enumerate(y):
        y1.append(y[i][0])
        y2.append(y[i][1])
        y3.append(y[i][2])

    patches=[]
    for i in list(range(0,len(x1))):
      #print(i)
      polygon = Polygon([[x1[i],y1[i]],[x2[i],y2[i]],[x3[i],y3[i]]],
        edgecolor='none',alpha=0.1,linewidth=0, closed=True)
      patches.append(polygon)


    norm = mpl.colors.Normalize(vmin=lower,vmax=upper)
    collection = PatchCollection(patches, match_original=True)
    collection.set(array=var, cmap='jet',norm=norm)

    fig,ax = plt.subplots()
    ax.add_collection(collection)

    ax.autoscale_view()


    sfmt=ScalarFormatter(useMathText=True)
    sfmt.set_powerlimits((0,0))
    sm = plt.cm.ScalarMappable(cmap="jet", norm=plt.Normalize(vmin=lower, vmax=upper))
    sm.set_array([])
    plt.xlabel('R [m]')
    plt.ylabel('Z [m]')

    cbar=plt.colorbar(sm,format=sfmt)
    cbar.set_label(label)
    plt.show(block=True)