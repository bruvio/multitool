#!/usr/bin/env python3
# ----------------------------
#Created on Wed Jul 26 21:08:45 2017

__author__ = "Bruno Viola"
__Name__ = "class EIRENE"
__version__ = "0.1"
__release__ = "0"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
__status__ = "Testing"
# __status__ = "Production"

# __credits__ = [""]
# -*- coding: utf-8 -*-
# from importlib import reload

import logging
logger = logging.getLogger(__name__)
import sys
import os
from importlib import import_module




libnames = ['eproc','ppf']
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

        lib = import_module(libr,package=package)
    except:
        exc_type, exc, tb = sys.exc_info()
        print(os.path.realpath(__file__))
        print(exc)
    else:
        globals()[libname] = lib
import argparse
import platform
from logging.handlers import RotatingFileHandler
from logging import handlers

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
import math
import csv
import pathlib
sys.path.append('../')
from custom_formatters import MyFormatter,QPlainTextEditLogger,HTMLFormatter
from class_sim import sim
from class_sim import Getdata
from class_sim import initread
from class_sim import find_indices

import pdb
try:
    ep = eproc
except:
    logger.error('failed to load EPROC')
    # raise SystemExit

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

    home = os.curdir

    # Ensure we are running on 64bit
    assert (platform.architecture()[0] == '64bit'), "Please log on Freja"

    # Ensure we are running python 3
    assert sys.version_info >= (
        3, 5), "Python version too old. Please use >= 3.5.X."

    parser = argparse.ArgumentParser(description='Run CORMAT_py')
    parser.add_argument("-d", "--debug", type=int,
                        help="Debug level. 0: Info, 1: Warning, 2: Debug,"
                             " 3: Error, 4: Debug Plus; \n default level is INFO", default=0)
    parser.add_argument("-doc", "--documentation", type=str,
                        help="Make documentation. yes/no", default='no')

    args = parser.parse_args(sys.argv[1:])


    debug_map = {0: logging.INFO,
                 1: logging.WARNING,
                 2: logging.DEBUG,
                 3: logging.ERROR,
                 4: 5}
    #this plots logger twice (black plus coloured)
    logging.addLevelName(5, "DEBUG_PLUS")
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=debug_map[args.debug])
    # logger.setLevel(debug_map[args.debug])

    fmt = MyFormatter()
    # hdlr = logging.StreamHandler(sys.stdout)


    # hdlr.setFormatter(fmt)
    # logging.root.addHandler(hdlr)
    fh = handlers.RotatingFileHandler('./LOGFILE.DAT', mode = 'w',maxBytes=(1048576*5), backupCount=7)
    fh.setFormatter(fmt)
    logging.root.addHandler(fh)

    if (args.documentation).lower() == 'yes':
        logger.info('creating documentation')
        os.chdir('../docs')
        import subprocess

        subprocess.check_output('make html', shell=True)
        subprocess.check_output('make latex', shell=True)
        os.chdir(home)




    EDGE2dfold='/work/bviola/Python/bruvio_tool/e2d_data'
    workfold='work/Python/bruvio_tool'
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
    # sim.write_edge2d_profiles1(sim_list,targetfilename)
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
    workfold='work/Python/bruvio_tool'
    #
    #import sys
    #del sys.modules['class_sim']
    #del sys.modules['class_eirene']
    
    from class_sim import sim
    from class_eirene import Eirene
    
    
    # sim_lfe = sim('92121', 'aug1717', '1', workfold)
    # sim_hfe = sim('92123', 'aug1717', '2', workfold)
    
    
    # sim_hfe_Nrad0 = sim('92123', 'oct1917', '1', workfold)
    sim_hfe_Nrad0 = sim('84600', 'oct1618', '1', workfold)
    sim_hfe_Nrad0 = sim('84599X', 'oct1618', '1', workfold)
    sim_hfe_Nrad0 = sim('84598X', 'oct1618', '1', workfold)
    simlist = []
    simlist.append([sim_hfe_Nrad0, 'first'])

    # sim.write_edge2d_profiles1(simlist, 'e2dprofiles_python')


    # pdb.set_trace()
    # sim_hfe_Nrad1 = sim('92123', 'aug1717', '6', workfold)
    #
    # sim_lfe_Nrad0 = sim('92121', 'aug1717', '3', workfold)
    # sim_lfe_Nrad1 = sim('92121', 'aug1717', '4', workfold)
    #
    # sim_lfe_81472 = sim('81472', 'may2316', '6', workfold)
    # sim_hfe_81472 = sim('81472', 'may2316', '1', workfold)
    #
    # # simlist=[]
    # # workfold = 'work/Python/EDGE2D'
    # # simu = sim('84598X', 'nov0518', '1',workfold);
    # # simlist.append([sim_lfe_Nrad0,'test'])
    # # for index1 in range(0, len(simlist)):
    # #     simu = simlist[index1][0]
    # #     label = simlist[index1][1]
    # #     simu.contour('DENEL', 'denel_' + label)
    # # raise SystemExit
    # simlist = []
    # simlist.append([sim_hfe_Nrad0, 'HFE_3MW'])
    # simlist.append([sim_hfe_Nrad1, 'HFE_5MW'])
    #
    # simlist.append([sim_lfe_Nrad0, 'LFE_2MW'])
    # simlist.append([sim_lfe_Nrad1, 'LFE_3MW'])
    #
    # omp_index = sim_lfe_Nrad0.find_omp_index()
    #
    # # first open cell on the OMP row
    # first_open_omp_cell_row = sim_lfe_Nrad0.find_omp_index_row()
    # # calculate connection length
    # l_lfe = sim_lfe_Nrad0.calc_connection_length(omp_index)
    # print(l_lfe)
    # # tpm_lfe_unseeded = sim_lfe_Nrad0.TPMscaling_Petrie(l_lfe)
    #
    # omp_index1 = sim_hfe_Nrad0.find_omp_index()
    #
    # # first open cell on the OMP row
    # first_open_omp_cell_row = sim_hfe_Nrad0.find_omp_index_row()
    # # calculate connection length
    # l_hfe = sim_hfe_Nrad0.calc_connection_length(omp_index1)
    # print(l_hfe)
    # ## tpm_hfe_unseeded = sim_hfe_Nrad0.TPMscaling_Petrie(l_hfe)
    # ## print(tpm_lfe_unseeded['ntar'], tpm_hfe_unseeded['ntar'])
    # ## print(tpm_lfe_unseeded['ttar'], tpm_hfe_unseeded['ttar'])
    # ## raise SystemExit
    #
    # ne1, te1 = sim_lfe_Nrad0.nete_omp()
    # #
    # ne2, te2 = sim_hfe_Nrad0.nete_omp()
    #
    # print(ne1, te1)
    # print(ne2, te2)
    #
    # #
    # contour = False
    # # contour = True
    # if contour is True:
    #     for index1 in range(0, len(simlist)):
    #         simu = simlist[index1][0]
    #         label= simlist[index1][1]
    #         var = ep.data(simu.fullpath, 'soun').data
    #         var = -np.trim_zeros(var, 'b')
    #         simu.contour(var, 'soun_' + label)
    #         plt.show(block=True)
    #
    #
    #
    # print_lfe= sim_lfe_Nrad0.read_print_file_edge2d()
    # print_hfe= sim_hfe_Nrad0.read_print_file_edge2d()
    #
    #
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
    # sim.bar_power_balance(lfe_pb,'LFE')
    # sim.bar_power_balance(hfe_pb,'HFE')

    sim_alexc = sim('84727', 'nov1015', '1', workfold,'alexc')
    sim_david = sim('81472', 'jan2215', '1', workfold,'dmoulton')
    # sim_bruvio_sd = sim('84599X', 'nov2818', '1', workfold)
    sim_bruvio_sd = sim('84599X', 'apr0519', '1', workfold)
    sim_bruvio = sim('92123', 'oct1917', '1', workfold)

    # simu = sim_bruvio
    # simu = sim_david
    # simu = sim_alexc
    simu = sim_bruvio_sd



    # simu.read_eirene(simu.fullpath[:-6])
    simu.read_eirene('/work/bviola/Python/bruvio_tool/EIRENE_FILES_UNCATALOGUED/')

    for i in range(0,9):
        simu.data.eirene.get_surface_name(i)


    simu.data.eirene.create_connected_eirene_surface(2)
    simu.data.eirene.assemble_eirene_surfaces(0, 2)

    simu.data.eirene.create_surface_start_end_poly()

    # plt.figure()
    simu.data.eirene.plot_eirene_grid()

    simu.data.eirene.plot_eirene_surface()




    simu.data.eirene.get_data_names(data='PLS')
    simu.data.eirene.get_data_names(data='MOl')
    simu.data.eirene.get_data_names(data='atm')
    simu.data.eirene.get_data_names(data='ion')

    simu.data.eirene.get_eirene_surface_data(data='PLS',var=0,species=0)

    simu.data.eirene.plot_eirere_surf_data(data='PLS',var=0,species=0)

    raise SystemExit
    # simu.read_eirene('/common/cmg/bviola/edge2d/runs/runsubdiv845981/')

    # simu.read_eirene('/home/alexc/cmg/catalog/edge2d/jet/84727/nov1015/seq#1/')
    # simu.data.eirene.plot_eirene_vol_data()
   #
   #
    # simu.data.eirene.plot_eirene_vol_data(data='MOL')
    # simu.data.eirene.plot_eirene_vol_data(data='ATM')




    #  #
    # simu.data.eirene.plot_subdivertor(simu.fullpath,'/work/bviola/matlab/subdivertor/E2DMATLAB/Substruc_VH_84599.txt')

    # simu.data.eirene.plot_eirene_grid('/work/bviola/Python/bruvio_tool/EIRENE_FILES_ALEX/puff.dat')
   #
   #  #
   #
   # #
   #  #
   #  #
   #
   #
   #
   #  #test to plot EIRENE PRESSURE AND TEMPERATURE
   #  triangnum = simu.data.eirene.geom.trimap.shape[0]
   #
   #
   #  mD2 = 2*2.01410178*1.660538921E-27; # kg
   #  vxD2 = np.asarray(simu.data.eirene.MOL.vol_avg_data[2]/1000/mD2/simu.data.eirene.MOL.vol_avg_data[1]/100); # m/s
   #  vyD2 = np.asarray(simu.data.eirene.MOL.vol_avg_data[3]/1000/mD2/simu.data.eirene.MOL.vol_avg_data[1]/100); # m/s
   #  vzD2 = np.asarray(simu.data.eirene.MOL.vol_avg_data[4]/1000/mD2/simu.data.eirene.MOL.vol_avg_data[1]/100); # m/s
   #  vxD2[np.isnan(vxD2)] = 0;
   #  vyD2[np.isnan(vyD2)] = 0;
   #  vzD2[np.isnan(vzD2)] = 0;
   #
   #  pD2 = np.asarray(2/3*(simu.data.eirene.MOL.vol_avg_data[5]*1.6022E-19*1E6 -
   #             0.5*mD2*simu.data.eirene.MOL.vol_avg_data[1]*1E6*(vxD2**2+vyD2**2+vzD2**2)));
   #  # pD2 = 2/3*(0.5*mD2*sim_alexc.data.eirene.MOL.data[1][0:triangnum]*1E6.*(vxD2.^2+vyD2.^2+vzD2.^2));
   #  TD2 = np.asarray(pD2/simu.data.eirene.MOL.vol_avg_data[1]/1E6/1.3806488E-23);
   #  TD2[np.isnan(TD2)] = 0;
   #  pD2[np.isnan(pD2)] = 0;
   #  #
   #  #
   #  # xv=linspace(2.003,2.547,100)';
   #  # yv=-2.3*ones(100,1);
   #  #
   #  #
   # #
   #  simu.data.eirene.plot_eirene_vol_data(data=pD2)
   #  simu.data.eirene.plot_eirene_vol_data(data=TD2)

    # simu.data.eirene.PLS.names
    # Out[12]: {0: 'D+', 1: 'Be1+', 2: 'Be2+', 3: 'Be3+', 4: 'Be4+'}
    # simu.data.eirene.MOL.names
    # Out[13]: {0: 'D2'}
    # simu.data.eirene.ATM.names
    # Out[14]: {0: 'D', 1: 'Be'}
    # simu.data.eirene.ION.names
    # Out[15]: {0: 'D2+'}



    # I want Be1+
    # species =1
    # data = simu.data.eirene.PLS.vol_avg_data
    # label = simu.data.eirene.PLS.names[species-1] + simu.data.eirene.PLS.VoldataName[26]
    # simu.data.eirene.plot_eirene_vol_data(data=data,species=species,label=label)
    #
    # # I want D
    # species = 0
    # var=0
    # species_name = simu.data.eirene.ATM.names[species]
    # data = simu.data.eirene.ATM.vol_avg_data
    # label = simu.data.eirene.ATM.names[var] + \
    #         simu.data.eirene.ATM.VoldataName[var]
    #
    # simu.data.eirene.plot_eirene_vol_data(data=data,species=species,label=label)
    # #
    # species = 0
    # var = 1
    # species_name = simu.data.eirene.ATM.names[species]
    # data = simu.data.eirene.ATM.vol_avg_data
    # label = simu.data.eirene.ATM.names[var] + \
    #         simu.data.eirene.ATM.VoldataName[var]
    #
    # simu.data.eirene.plot_eirene_vol_data(data=data,species=species,var=var,label=label)























    plt.show(block=True)
