# -*- coding: utf-8 -*-
# ----------------------------
"""
__author__ = "Bruno Viola"
__Name__ = "class SIM"
__version__ = "0.1"
__release__ = "0"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
__status__ = "Testing"
# __status__ = "Production"
# __credits__ = [""]
"""
#Created on July 2017



# from importlib import reload
import sys
import os
import logging
logger = logging.getLogger(__name__)
from importlib import import_module
libnames = ['eproc']

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



import numpy as np
from class_geom import geom
from class_eirene import Eirene

import csv
import stat
import math

import pathlib
import mpmath
import math
from types import SimpleNamespace
import logging
from time import gmtime, strftime
from matplotlib.patches import Polygon
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.collections import PatchCollection
#from django.utils.datastructures import SortedDict
from collections import OrderedDict
# import Struct as st
import pdb;

pi=mpmath.pi

try:
    ep = eproc
except:
    logger.error('failed to load EPROC')
    # raise SystemExit

def slice_npts(array, physid):
    return_array = (array[physid])[0:array['npts']]
    return return_array


def interpolation_x(x0, y0, x1, y1, y):
    # we want to interpolate for x value not y
    x = ((x1 - x0) / (y1 - y0)) * (y - y0) + x0

    return x
def sqrt(s):
  """
    function that calculates square root
  """
  return math.sqrt(s)

def ln(x):
    return math.log1p(x)

def file_len(fname):
  """
    function that find the number of lines in a text file
  """
  with open(fname) as f:
      for i, l in enumerate(f):
         if l.strip():
          i=i+1
  return i

def find_indices(lst, condition):
  """
  function that find the indices within an array where condition is true

  Usage:
      iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)
  will return indices where the xdata[iy_OMP_SOL]>0
  """
  return [i for i, elem in enumerate(lst) if condition(elem)]


def count_string_occurrence(file_path, string):
  """
  function that counts the occurrences of a string within a text file 

  Usage:
  num=count_string_occurrence(file_path, string):

  """
  f = open(file_path)
  contents = f.read()
  f.close()
  return contents.count(string)
def initread(shot,userid,seq):
  """
  function that uses function of the ppf module
  it initialize the reading of a ppf file
  ppf file can be private, punlic or synthetic (coming from edge2d for example)

  Usage:
  initread(shot,userid,seq)

  """
  ppfsetdevice('JET')
  #print('ok')
  ppfuid(userid,'r')
  ier=ppfgo(int(shot),int(seq))
#@staticmethod
def Getdata(pulse, dda,dtype,sequence,user):

    '''
     function that reads a ppf file
    it can be used to read synthetic edge2d ppf files
    ARGS
    pulse1 :=  pulse

    dda := string e.g. 'kg1v'
    dtype:= string e.g. 'lid3'
    RETURNS
    '''
    #initialize pulse an sequence
    initread(int(pulse),user,int(sequence))
    data,x,t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier=ppfdata(int(pulse),dda,dtype,seq=int(sequence),uid=user,device="JET",fix0=0,reshape=0,no_x=0,no_t=0)
    #ihdat,iwdat,data,x,t,ier=ppfget(int(pulse),dda,dtype)
    #pulse,seq,iwdat,comment,numdda,ddalist,ier=ppfinf(comlen=50,numdda=50)
    # info,cnfo,ddal,istl,pcom,pdsn,ier=pdinfo(pulse,seq)
    # istat,ier = ppfgsf(pulse,seq,dda,dtype,mxstat=1)
    return{'dunits':dunits,
            'desc':desc,
          'xunits':xunits,
          'data':data,
          'x':x,
          't':t,
          'ier':ier,
          'sequence':seq}
###############################################
def readdata(filename,foldername):
  """

    read data stored using the download tool

    usage:
    simu=sim('92123','jul1717','2','bviola','edge2d')
    var=simu.read_data('TEVE','HFE')
    ExtraInput is the suffix used to store the simulation in its dedicated folder
  """


  pathT=foldername
  with open(foldername+filename, 'rb') as f:
      reader = csv.reader(f, delimiter=';')
      next(reader)
      # col = list(zip(*reader))[1]
      csv_dic = []

      for row in reader:
          csv_dic.append(row);
      col = []


      for row in csv_dic:
          col.append(row[0])
      dummy=np.array(col)
      dummy=[float(i) for i in dummy]
      data=np.asarray(dummy)
  f.close()
  return {'data':data}


class sim(geom):
  """"
  given a catalogues edge2d simulation it provides with tools to extract data

  a simulation is defined by
  owner
  date
  sequence
  machine
  shot number

the following functions are available:

Read_print_file_edge2d()
Write_print2file(simu_list,path,filename)
Read_ionrecom
Read_psol_pradpsol()
Read_time_data(var, interval)
Read_pow_lfs_div(interval)
Read_row_data(variable, region, Extrainput)
Read_data(variable, )
Read_edge2d_pedestal_fuel()
Read_radiation_split(interval,)
Read_qpeak_ot()
Read_prad_sol()
Read_imp_content()
Read_imp_content_core()
Read_n2(region)
Read_e()
Read_x_point()
Read_div_mol_atom_ratio()
Read_sirec_soun_lfs()
Read_power_balance()
Write_powerbalance2file(simu_list,path_filename)
Read_omp()
Read_netflux(surface_in,surface_out)
Eirene_netcur(surface_in,surface_out, )
Write_eirene_cur2fil(simu_list, path, filename)
Read_eirene_pump()
Eirene_pumpcur()
Write_pump_cur2file(simu_list,path,filename)
Read_e2d_ppf(dda,dtype, sequence, )
Contour(, var, fname, lowerbound=None,upperbound=None)
Execute_makeppf(simu_list, outputfile)
write_edge2d_profiles
read_eirene




  """


###############################################
  def __init__(self,shotIDArg,dateIDArg,seqNumArg, folder,ownerArg=None, codeArg=None, macArg=None, fileArg=None ):
    if ownerArg is None:
        ownerArg = os.getenv('USR')
    else:
        ownerArg = ownerArg


    geom.__init__(self,shotIDArg,dateIDArg,seqNumArg,ownerArg, codeArg, macArg, fileArg )
    self.path_e2d = os.getcwd()+'/e2d_data/runs'

    self.sim_folder='shotid_'+shotIDArg+'_'+dateIDArg+'_grid_' # deprecated

    catalogue=ep.cat(shotIDArg,dateIDArg,seqNumArg,ownerArg)
    owner=catalogue.owner
    code=catalogue.code
    machine=catalogue.machine
    date=catalogue.date
    sequence=catalogue.seq
    pulse=catalogue.shot
    # self.simfolder='/u/'+owner+
# /u/bviola/cmg/catalog/edge2d/jet
    self.folder=os.path.join(os.sep,'u',owner,'cmg','catalog',code,machine,pulse,date,'seq#',sequence)
    self.workingdir=folder
    self.initfolder(folder)
    self.data = SimpleNamespace()  # dictionary object that contains all data
    
    
    self.data.eirene = {}



    # self.pathT=self.path_e2d+'/'+self.sim_folder+'/'+'seq'+seqNumArg

###############################################
  def __str__(self):
    ret = "Structure Struct contains:\n"
    ret = ret+ "  .shot\n"
    ret = ret+ "  .date\n"
    ret = ret+ "  .seq\n"
    ret = ret+ "  .owner\n"
    ret = ret+ "  .code\n"
    ret = ret+ "  .machine\n"
    ret = ret+ "  .fullpath\n"

    return ret

  def initfolder(self,folder, owner=None):
      if owner is None:
          owner = os.getenv('USR')
      else:
          owner = owner
      homefold = os.path.join(os.sep, 'u', owner)
      # print(owner)
      # print(homefold)
      # print(homefold + os.sep+ folder)
      pathlib.Path(homefold + os.sep + folder).mkdir(parents=True,
                                                     exist_ok=True)
      pathlib.Path(homefold + os.sep + folder+ os.sep + 'e2d_data').mkdir(parents=True,
                                                     exist_ok=True)
      pathlib.Path(homefold + os.sep + folder+ os.sep +'e2d_data'+ os.sep + str(self.shot)).mkdir(parents=True,
                                                     exist_ok=True)
      pathlib.Path(homefold + os.sep + folder+ os.sep + 'exp_data').mkdir(parents=True,
                                                     exist_ok=True)
      pathlib.Path(homefold + os.sep + folder+ os.sep + 'figures').mkdir(parents=True,
                                                     exist_ok=True)

      self.workingdir=  homefold + os.sep + folder
      # print('Parent output folder will be')
      # print(homefold + os.sep + folder)


  # def init(self,folder, pulse):
  #     self.set_folder(folder)
  #
  #
  #     self.set_folder(folder + '/e2d_data')
  #     self.set_folder(folder + '/e2d_data/' + str(pulse))
  #
  #     self.set_folder(folder + '/exp_data')
  #     self.set_folder(folder + '/figures')
###############################################
  def read_print_file_edge2d(self):
    """
    reads edge2d print file of a catalogued simulation
    """
    if (self.fullpath[len(self.fullpath)-4:len(self.fullpath)] == "tran"):
        ffile = self.fullpath[0:len(self.fullpath)-5]

#  and add tran again
    prt = 'print'
    file = ffile+'/'+prt
    text1 = 'GENERAL RESULTS :-'

    # print(file)
    dummy=[]
    with open(file) as f:
        lines = f.readlines()
    # 	# print(lines)
        text = 'H0 RECL+RECOM+PUF'
        for index, line in enumerate(lines):
            if text in str(line):
                # print(line)
                dummy=lines[index].split()
                # print(dummy)
                # type(dummy)
                i_h0_reclrecpuf=float(dummy[2])
                # print(i_h0_reclrecpuf)
        text='H0 FLUX TO MP'
        for index, line in enumerate(lines):
            if text in str(line):
                dummy=lines[index].split()
                i_h0_main=float(dummy[5])
                # print(i_h0_main)
        text='H0 PUMPED FLUX'
        for index, line in enumerate(lines):
            if text in str(line):
                dummy=lines[index].split()
                i_h0_pump=float(dummy[4])
                # print(i_h0_pump)
        text = 'Z0 PUMPED FLUX'
        z1_pump = 0
        z2_pump = 0
        for index, line in enumerate(lines):
            if text in str(line):
                dummy = lines[index].split()
                # print(dummy)
                if len(dummy) > 4:
                    z1_pump=dummy[4]
                if len(dummy) > 5:
                    z2_pump=dummy[5]
                # print(z1_pump,z2_pump)
        text1 = ' CNTL H PUFF (S-1):'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)
                i_cntl_h0=float(dummy[4])
                # print(i_cntl_h0)
        text1 = ' EXT. H PUFFW(S-1):'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)
                i_ext_h0_wall=float(dummy[3])
                # print(i_ext_h0_wall)
        text1 = 'EXT. H PUFFT(S-1):'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)
                i_ext_h0_target=float(dummy[3])
                # print(i_ext_h0_target)
        text1 = 'CNTL Z PUFF (S-1):'
        i_cntl_z1 = 0
        i_cntl_z2 = 0
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)
                if len(dummy) > 4:
                    i_cntl_z1=dummy[4]
                if len(dummy) > 5:
                    i_cntl_z2=dummy[5]
                # print(i_cntl_z1,i_cntl_z2)

        text1 = 'CNTL Z RECY.(S-1):'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)
                z1_cntl_r = 0
                z2_cntl_r = 0
                if len(dummy) > 3:
                    z1_cntl_r=float(dummy[3])
                if len(dummy) > 4:
                    z2_cntl_r=float(dummy[4])
                # print(z1_cntl_r,z2_cntl_r)
        text1 = 'EXT. Z PUFFW(S-1):'
        z1_ext_puffw = 0
        z2_ext_puffw = 0
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)

                if len(dummy) > 3:
                    z1_ext_puffw=float(dummy[3])
                if len(dummy) > 4:
                    z2_ext_puffw=float(dummy[4])
                # print(z1_ext_puffw,z2_ext_puffw)
        text1 = 'EXT. Z PUFFT(S-1):'
        z1_ext_pufft = 0
        z2_ext_pufft = 0
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index].split()
                # print(dummy)
                if len(dummy) > 3:
                    z1_ext_pufft=float(dummy[3])
                if len(dummy) > 4:
                    z2_ext_pufft=float(dummy[4])
                # print(z1_ext_pufft,z2_ext_pufft)
        text1 = ' DIVERTOR RESULTS :-'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+4].split()
                # print(dummy)
                nisep_omp=float(dummy[3])
                nisep_imp=float(dummy[4])
                nisep_ot=float(dummy[5])
                nisep_it=float(dummy[6])
                dummy=lines[index+5].split()
                # print(dummy)
                nesep_omp=float(dummy[3])
                nesep_imp=float(dummy[4])
                nesep_ot=float(dummy[5])
                nesep_it=float(dummy[6])
                dummy=lines[index+6].split()
                # print(dummy)
                tisep_omp=float(dummy[3])
                tisep_imp=float(dummy[4])
                tisep_ot=float(dummy[5])
                tisep_it=float(dummy[6])
                dummy=lines[index+7].split()
                # print(dummy)
                tesep_omp=float(dummy[3])
                tesep_imp=float(dummy[4])
                tesep_ot=float(dummy[5])
                tesep_it=float(dummy[6])
                dummy=lines[index+8].split()
                # print(dummy)
                psep_omp=float(dummy[3])
                psep_imp=float(dummy[4])
                psep_ot=float(dummy[5])
                psep_it=float(dummy[6])
                dummy=lines[index+12].split()
                # print(dummy)
                niavg_omp=float(dummy[3])
                niavg_imp=float(dummy[4])
                niavg_ot=float(dummy[5])
                niavg_it=float(dummy[6])
                dummy=lines[index+13].split()
                # print(dummy)
                neavg_omp=float(dummy[3])
                neavg_imp=float(dummy[4])
                neavg_ot=float(dummy[5])
                neavg_it=float(dummy[6])
                dummy=lines[index+14].split()
                # print(dummy)
                tiavg_omp=float(dummy[3])
                tiavg_imp=float(dummy[4])
                tiavg_ot=float(dummy[5])
                tiavg_it=float(dummy[6])
                dummy=lines[index+15].split()
                # print(dummy)
                teavg_omp=float(dummy[3])
                teavg_imp=float(dummy[4])
                teavg_ot=float(dummy[5])
                teavg_it=float(dummy[6])
                dummy=lines[index+16].split()
                # print(dummy)
                pavg_omp=float(dummy[3])
                pavg_imp=float(dummy[4])
                pavg_ot=float(dummy[5])
                pavg_it=float(dummy[6])
                dummy=lines[index+18].split()
                # print(dummy)
                pdepinn=-float(dummy[3])
                dummy=lines[index+19].split()
                # print(dummy)
                pdepout=-float(dummy[3])

        text1 = ' POWER & PARTICLE GLOBAL CONSERVATION :-'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+4].split()
                # print(dummy)
                pcorei=float(dummy[2])*1.e6
                pcoree=float(dummy[3])*1.e6
                i_input=float(dummy[4])
                # i_imp_tot=float(buf[5])
                prec=float(dummy[5])
                i_imp1_tot = 0
                i_imp2_tot = 0
                # print(len(dummy))
                if len(dummy) > 6:
                    i_imp1_tot=float(dummy[6])
                if len(dummy) > 7:
                    i_imp2_tot=float(dummy[7])
                # print(i_imp1_tot,i_imp2_tot)


                i_ves_buf = lines[index+5].split()
                i_ves_odiv_buf = lines[index+8].split()
                i_ves_msol_buf = lines[index+11].split()
                i_ves_idiv_buf = lines[index+14].split()
                i_ves_pfr_buf = lines[index+17].split()
                i_idiv_buf = lines[index+20].split()
                i_odiv_buf = lines[index+23].split()
                i_ionis_buf = lines[index+27].split()
                i_atomic_buf = lines[index+28].split()
                i_molec_buf = lines[index+29].split()
                i_CX_buf = lines[index+30].split()
                i_hydrad_buf = lines[index+31].split()
                i_radiated_buf = lines[index+37].split()
                i_recomb_buf = lines[index+38].split()
                i_particle_buf = lines[index+39].split()
                i_eq_buf =  lines[index+42].split()
                i_compr_buf =  lines[index+43].split()
                i_dt_buf =  lines[index+45].split()

                i_ves=float(i_ves_buf[6])
                i_ves_msol=float(i_ves_msol_buf[6])
                i_ves_odiv=float(i_ves_odiv_buf[6])
                i_ves_idiv=float(i_ves_idiv_buf[6])
                i_ves_pfr=float(i_ves_pfr_buf[6])
                #
                # ;stop
                # print( i_ves,i_ves_msol,i_ves_odiv,i_ves_idiv,i_ves_pfr)
                #
                # ; total power to outer and inner targets
                p_idiv = float(i_idiv_buf[4]) + float(i_idiv_buf[5])
                p_odiv = float(i_odiv_buf[4]) + float(i_odiv_buf[5])
                p_rec_odiv  = float(i_odiv_buf[7])
                p_rec_idiv  = float(i_idiv_buf[7])
                p_rec_vessel  = float(i_ves_buf[7])
                #
                # print(p_idiv, p_odiv, p_rec_odiv, p_rec_idiv, p_rec_vessel)
                # ; total particle flux to inner and outer targets
                i_idiv = float(i_idiv_buf[6])
                i_odiv = float(i_odiv_buf[6])
                #
                # ; total power source due to neutral interactions
                # print(i_ionis_buf)
                pi_ions = float(i_ionis_buf[4])
                pe_ions = float(i_ionis_buf[5])
                #
                # # ; total power source due to atomic contribution
                pi_atomic = float(i_atomic_buf[3])
                pe_atomic = float(i_atomic_buf[4])
                # print(pi_atomic,pe_atomic)
                # #
                # # ; total power source due to molecular dissociation
                pi_mol = float(i_molec_buf[2])
                pe_mol = float(i_molec_buf[3])
                # print(pi_mol,pe_mol)
                # print( i_idiv, i_odiv, pi_ions, pe_ions, pi_atomic, pe_atomic, pi_mol, pe_mol)				#  # total power source due to CX
                pi_cx = float(i_CX_buf[4])
                # print(pi_cx)
                # #
                # # ; total power source due to hrad and zrad
                pe_hrad = float(i_hydrad_buf[3])
                pe_zrad = float(i_radiated_buf[3])
                # print(pe_hrad,pe_zrad)
                # #
                # ; total power source due to recombination
                pi_rec = float(i_recomb_buf[2])
                pe_rec = float(i_recomb_buf[3])
                # print(pi_rec)
                # #
                # # ; total power source due to equipartition
                pi_eq = float(i_eq_buf[2])
                pe_eq = float(i_eq_buf[3])
                # print(pi_eq,pe_eq)
                #
                # # ; total power source due to compression
                pi_com = float(i_compr_buf[2])
                pe_com = float(i_compr_buf[3])


                # ; total dt
                pi_dt = float(i_dt_buf[3])
                pe_dt = float(i_dt_buf[4])
                # print(pi_dt,pe_dt)

                # ; ------------------------------------------------------
        text1 = ' MISCELLANEOUS SUMMATIONS BY MACRO-ZONE :-'
                #
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+4].split()
                # print(dummy)
                part_core = dummy
                part_sol = lines[index+6].split()
                part_ods = lines[index+8].split()
                part_ids = lines[index+10].split()
                part_odp = lines[index+12].split()
                part_idp = lines[index+14].split()
                part_t = lines[index+16].split()
                #
                # ;stop
                #
                core_ioniz=float(part_core[5])
                core_recom=float(part_core[6])
                # print(core_ioniz)
                msol_ioniz=float(part_sol[5])
                msol_recom=float(part_sol[6])
                odiv_ioniz=float(part_ods[5])
                odiv_recom=float(part_ods[6])
                idiv_ioniz=float(part_ids[5])
                idiv_recom=float(part_ids[6])
                opfr_ioniz=float(part_odp[5])
                opfr_recom=float(part_odp[6])
                ipfr_ioniz=float(part_idp[5])
                ipfr_recom=float(part_idp[6])
                #
                sol_ioniz = (float(part_sol[5])+
                        float(part_ods[5])+float(part_ids[6])+
                                float(part_odp[5])+float(part_idp[6]))
                sol_recom= (float(part_sol[6])+
                        float(part_ods[6])+float(part_ids[6])+
                                float(part_odp[6])+float(part_idp[6]))

                tot_ioniz = core_ioniz + sol_ioniz
                tot_recom = core_recom + sol_recom
                #
                # ; ------------------------------------------------------
        text1 = ' ION POWER BALANCE BY MACRO-ZONE :-'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+4].split()
                # print(dummy)		#

                infocore = lines[index+5].split()
                infosol = lines[index+6].split()
                infoods =lines[index+7].split()
                infoids = lines[index+8].split()
                infoodp = lines[index+9].split()
                infoidp = lines[index+10].split()
                infot = lines[index+11].split()

                infocore2 = lines[index+14].split()
                infosol2 = lines[index+15].split()
                infoods2 =lines[index+16].split()
                infoids2 = lines[index+17].split()
                infoodp2 = lines[index+18].split()
                infoidp2 = lines[index+19].split()
                infot2 = lines[index+20].split()
                # print(infoidp2)
                i_dt_core = float(infocore2[2])*1.e6
                i_dt_sol = float(infosol2[2])*1.e6
                i_dt_ods = float(infoods2[2])*1.e6
                i_dt_ids = float(infoids2[2])*1.e6
                i_dt_odp = float(infoodp2[2])*1.e6
                i_dt_idp = float(infoidp2[2])*1.e6
                i_dt_tot = float(infot2[2])*1.e6

                i_AT_ELASTIC_core = float(infocore2[3])*1.e6
                i_AT_ELASTIC_sol = float(infosol2[3])*1.e6
                i_AT_ELASTIC_ods = float(infoods2[3])*1.e6
                i_AT_ELASTIC_ids = float(infoids2[3])*1.e6
                i_AT_ELASTIC_odp = float(infoodp2[3])*1.e6
                i_AT_ELASTIC_idp = float(infoidp2[3])*1.e6
                i_AT_ELASTIC_tot = float(infot2[3])*1.e6

                I_MOLE_ELASTIC_core = float(infocore2[4])*1.e6
                i_MOLE_ELASTIC_sol = float(infosol2[4])*1.e6
                i_MOLE_ELASTIC_ods = float(infoods2[4])*1.e6
                i_MOLE_ELASTIC_ids = float(infoids2[4])*1.e6
                i_MOLE_ELASTIC_odp = float(infoodp2[4])*1.e6
                i_MOLE_ELASTIC_idp = float(infoidp2[4])*1.e6
                i_MOLE_ELASTIC_tot = float(infot2[4])*1.e6

                i_KIN_EN_CORR_core = float(infocore2[5])*1.e6
                i_KIN_EN_CORR_sol = float(infosol2[5])*1.e6
                i_KIN_EN_CORR_ods = float(infoods2[5])*1.e6
                i_KIN_EN_CORR_ids = float(infoids2[5])*1.e6
                i_KIN_EN_CORR_odp = float(infoodp2[5])*1.e6
                i_KIN_EN_CORR_idp = float(infoidp2[5])*1.e6
                i_KIN_EN_CORR_tot = float(infot2[5])*1.e6

                i_VISCOUS_core = float(infocore2[6])*1.e6
                i_VISCOUS_sol = float(infosol2[6])*1.e6
                i_VISCOUS_ods = float(infoods2[6])*1.e6
                i_VISCOUS_ids = float(infoids2[6])*1.e6
                i_VISCOUS_odp = float(infoodp2[6])*1.e6
                i_VISCOUS_idp = float(infoidp2[6])*1.e6
                i_VISCOUS_tot = float(infot2[6])*1.e6

                i_EXT_core = float(infocore2[7])*1.e6
                i_EXT_sol = float(infosol2[7])*1.e6
                i_EXT_ods = float(infoods2[7])*1.e6
                i_EXT_ids = float(infoids2[7])*1.e6
                i_EXT_odp = float(infoodp2[7])*1.e6
                i_EXT_idp = float(infoidp2[7])*1.e6
                i_EXT_tot = float(infot2[7])*1.e6

                cx_core=float(infocore[7])*1.e6
                cx_msol=float(infosol[7])*1.e6
                cx_odiv=float(infoods[7])*1.e6
                cx_idiv=float(infoids[7])*1.e6
                cx_opfr=float(infoodp[7])*1.e6
                cx_ipfr=float(infoidp[7])*1.e6

                ati_core=float(infocore[5])*1.e6
                ati_msol=float(infosol[5])*1.e6
                ati_odiv=float(infoods[5])*1.e6
                ati_idiv=float(infoids[5])*1.e6
                ati_opfr=float(infoodp[5])*1.e6
                ati_ipfr=float(infoidp[5])*1.e6

                moli_core=float(infocore[6])*1.e6
                moli_msol=float(infosol[6])*1.e6
                moli_odiv=float(infoods[6])*1.e6
                moli_idiv=float(infoids[6])*1.e6
                moli_opfr=float(infoodp[6])*1.e6
                moli_ipfr=float(infoidp[6])*1.e6

                reci_core=float(infocore[8])*1.e6
                reci_msol=float(infosol[8])*1.e6
                reci_odiv=float(infoods[8])*1.e6
                reci_idiv=float(infoids[8])*1.e6
                reci_opfr=float(infoodp[8])*1.e6
                reci_ipfr=float(infoidp[8])*1.e6
                #
                cx_sol = (float(infosol[7])+
                          float(infoods[7])+float(infoids[7])+
                              float(infoodp[7])+float(infoidp[7]))*1.e6

                cx_div = (float(infoods[7])+float(infoids[7])+
                              float(infoodp[7])+float(infoidp[7]))*1.e6

                cx_tot = cx_core + cx_sol
                #

                infot = lines[index+24].split()
                pcore_out_ion = float(infot[3])*1.e6
                #
                infot = lines[index+25].split()
                # ; power to the outer divertor entrance
                pod_ion = float(infot[4])*1.e6
                # ; power to the inner divertor entracen
                pid_ion = float(infot[5])*1.e6
                # ; power to the vessel wall between X-points. Main sol.
                pves_ion = float(infot[3])*1.e6

                infot =  lines[index+26].split()
                pves_od_ion = float(infot[3])*1.e6

                infot =  lines[index+27].split()
                pves_id_ion = float(infot[3])*1.e6

                infot =  lines[index+28].split()
                pves_opfr_ion = float(infot[2])*1.e6

                infot =  lines[index+29].split()
                pves_ipfr_ion = float(infot[2])*1.e6
                #
                # ; ------------------------------------------------------
        text1 = ' ELECTRON POWER BALANCE BY MACRO-ZONE :-'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+4].split()


                infocore = dummy
                # print(infocore)

                infosol = lines[index+5].split()
                # print(infosol)

                infoods =lines[index+6].split()
                # print(infoods)

                infoids = lines[index+7].split()
                # print(infoids)

                infoodp = lines[index+8].split()
                # print(infoodp)

                infoidp = lines[index+9].split()
                # print(infoidp)

                infot = lines[index+10].split()
                # print(infot)

                infocore2 = lines[index+14].split()
                infosol2 = lines[index+15].split()
                infoods2 =lines[index+16].split()
                infoids2 = lines[index+17].split()
                infoodp2 = lines[index+18].split()
                infoidp2 = lines[index+19].split()
                infot2 = lines[index+20].split()

                e_dt_core = float(infocore2[2])*1.e6
                e_dt_sol = float(infosol2[2])*1.e6
                e_dt_ods = float(infoods2[2])*1.e6
                e_dt_ids = float(infoids2[2])*1.e6
                e_dt_odp = float(infoodp2[2])*1.e6
                e_dt_idp = float(infoidp2[2])*1.e6
                e_dt_tot = float(infot2[2])*1.e6

                e_OHM_HEAT_core = float(infocore2[3])*1.e6
                e_OHM_HEAT_sol = float(infosol2[3])*1.e6
                e_OHM_HEAT_ods = float(infoods2[3])*1.e6
                e_OHM_HEAT_ids = float(infoids2[3])*1.e6
                e_OHM_HEAT_odp = float(infoodp2[3])*1.e6
                e_OHM_HEAT_idp = float(infoidp2[3])*1.e6
                e_OHM_HEAT_tot = float(infot2[3])*1.e6

                i_MOLE_ELASTIC_core = float(infocore2[4])*1.e6
                i_MOLE_ELASTIC_sol = float(infosol2[4])*1.e6
                i_MOLE_ELASTIC_ods = float(infoods2[4])*1.e6
                i_MOLE_ELASTIC_ids = float(infoids2[4])*1.e6
                i_MOLE_ELASTIC_odp = float(infoodp2[4])*1.e6
                i_MOLE_ELASTIC_idp = float(infoidp2[4])*1.e6
                i_MOLE_ELASTIC_tot = float(infot2[4])*1.e6


                prad_core_z=float(infocore[2])*1.e6
                prad_core_h=float(infocore[7])*1.e6
                prad_msol_z=float(infosol[2])*1.e6
                prad_msol_h=float(infosol[7])*1.e6
                prad_odiv_z=float(infoods[2])*1.e6
                prad_odiv_h=float(infoods[7])*1.e6
                prad_idiv_z=float(infoids[2])*1.e6
                prad_idiv_h=float(infoids[7])*1.e6
                prad_opfr_z=float(infoodp[2])*1.e6
                prad_opfr_h=float(infoodp[7])*1.e6
                prad_ipfr_z=float(infoidp[2])*1.e6
                prad_ipfr_h=float(infoidp[7])*1.e6

                ate_core=float(infocore[5])*1.e6
                mole_core=float(infocore[6])*1.e6
                ate_msol=float(infosol[5])*1.e6
                mole_msol=float(infosol[6])*1.e6
                ate_odiv=float(infoods[5])*1.e6
                mole_odiv=float(infoods[6])*1.e6
                ate_idiv=float(infoids[5])*1.e6
                mole_idiv=float(infoids[6])*1.e6
                ate_opfr=float(infoodp[5])*1.e6
                mole_opfr=float(infoodp[6])*1.e6
                ate_ipfr=float(infoidp[5])*1.e6
                mole_ipfr=float(infoidp[6])*1.e6


                prad_sol_h = (float(infosol[7])+
                        float(infoods[7])+float(infoids[7])+
                                float(infoodp[7])+float(infoidp[7]))*1.e6
                prad_sol_z = (float(infosol[2])+
                        float(infoods[2])+float(infoids[2])+
                                float(infoodp[2])+float(infoidp[2]))*1.e6
                prad_sol = prad_sol_h + prad_sol_z

                prad_div_h = (float(infoods[7])+float(infoids[7])+
                                float(infoodp[7])+float(infoidp[7]))*1.e6
                prad_div_z = (float(infoods[2])+float(infoids[2])+
                                float(infoodp[2])+float(infoidp[2]))*1.e6
                prad_div = prad_div_h + prad_div_z

                prad_h = prad_core_h + prad_sol_h
                prad_z = prad_core_z + prad_sol_z
                prad_tot = prad_h + prad_z

                infot = lines[index+24].split()
                # print(infot)
                pcore_out_ele = float(infot[3])*1.e6


                infot =  lines[index+25].split()
                pod_ele = float(infot[4])*1.e6
                pid_ele = float(infot[5])*1.e6
                pves_ele = float(infot[3])*1.e6

                infot =  lines[index+26].split()
                pves_od_ele = float(infot[3])*1.e6

                infot = lines[index+27].split()
                pves_id_ele = float(infot[3])*1.e6

                infot =  lines[index+28].split()
                pves_opfr_ele = float(infot[2])*1.e6

                infot =  lines[index+29].split()
                # print(infot)
                pves_ipfr_ele = float(infot[2])*1.e6
                # #
                # ; ------------------------------------------------------
        # text1 = ' ION PARTICLE BALANCE BY MACRO-ZONE :-'
        text1 = ' * ION PARTICLE FLUX *'
        for index, line in enumerate(lines):
            if text1 in str(line):
                # dummy=lines[index+4].split()
                dummy=lines[index+2].split()
                #

                infocore = dummy
                # print(infocore)
                ionflux_core_out = float(infocore[3])
                #
                # #
                # infosol  =lines[index+5].split()
                infosol  =lines[index+3].split()
                ionflux_sol_wall = float(infosol[3])
                #
                # infosol  =lines[index+6].split()
                infosol  =lines[index+4].split()
                ionflux_sol_outdiv = float(infosol[4])
                #
                #
                # infoinsol  =lines[index+7].split()
                infoinsol  =lines[index+5].split()
                ionflux_sol_indiv = float(infoinsol[5])
                #
                # infooutprv  =lines[index+8].split()
                infooutprv  =lines[index+6].split()
                ionflux_prv_outdiv = float(infooutprv[4])
                #
                # infoinprv  =lines[index+9].split()
                infoinprv  =lines[index+7].split()
                ionflux_prv_indiv = float(infoinprv[5])
                #
                # print(ionflux_core_out)
                # print(ionflux_sol_wall)
                # print(ionflux_sol_outdiv)
                # print(ionflux_sol_indiv)
                # print(ionflux_prv_outdiv)
                # print(ionflux_prv_indiv)
                # ;

                #
                imp1flux_core_out = 0
                imp2flux_core_out = 0
        text1  = ' IMPURITY PARTICLE BALANCE BY MACRO-ZONE :-'
        for index, line in enumerate(lines):
            if text1 in str(line):
                # dummy=lines[index+3]

                text1  = ' * IMPURITY(1) SOURCES *'
                if text1 in str(line):
                    infocore =lines[index+3].split()
                    imp1flux_core_out = float(infocore[3])
                text1  = ' * IMPURITY(2) SOURCES *'
                if text1 in str(line):

                    infocore = lines[index+3].split()
                    imp2flux_core_out = float(infocore[3])
                # endif
                # endif
                #
                # ; ------------------------------------------------------
        text1 = ' ION MOMENTUM BALANCE BY MACRO-ZONE :-'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+4].split()
                #

                infocore = dummy

                infosol = lines[index+5].split()

                infoods = lines[index+6].split()

                infoids = lines[index+7].split()

                infoodp = lines[index+8].split()

                infoidp = lines[index+9].split()

                infot = lines[index+10].split()
                # print(infot)
                momsrc_core=float(infocore[3])*1.e5 * 1.67e-30 # unit in Newton
                momsrc_sol=float(infosol[3])*1.e5 * 1.67e-30
                momsrc_ods=float(infoods[3])*1.e5 * 1.67e-30
                momsrc_ids=float(infoids[3])*1.e5 * 1.67e-30
                momsrc_odp=float(infoodp[3])*1.e5 * 1.67e-30
                momsrc_idp=float(infoidp[3])*1.e5 * 1.67e-30
                momsrc_tot=float(infot[3])*1.e5 * 1.67e-30

                momsrc_odiv = momsrc_ods + momsrc_odp
                momsrc_idiv = momsrc_ids + momsrc_idp
                momsrc_tdiv = abs(momsrc_odiv) + abs(momsrc_idiv)

                gradpsrc_core=float(infocore[2])*1.e5 * 1.67e-30 # unit in Newton
                gradpsrc_sol=float(infosol[2])*1.e5 * 1.67e-30
                gradpsrc_ods=float(infoods[2])*1.e5 * 1.67e-30
                gradpsrc_ids=float(infoids[2])*1.e5 * 1.67e-30
                gradpsrc_odp=float(infoodp[2])*1.e5 * 1.67e-30
                gradpsrc_idp=float(infoidp[2])*1.e5 * 1.67e-30
                gradpsrc_tot=float(infot[2])*1.e5 * 1.67e-30
                gradpsrc_odiv = gradpsrc_ods + gradpsrc_odp
                gradpsrc_idiv = gradpsrc_ids + gradpsrc_idp
                gradpsrc_tdiv = abs(gradpsrc_odiv) + abs(gradpsrc_idiv)

                esrc_core=float(infocore[4])*1.e5 * 1.67e-30 # unit in Newton
                esrc_sol=float(infosol[4])*1.e5 * 1.67e-30
                esrc_ods=float(infoods[4])*1.e5 * 1.67e-30
                esrc_ids=float(infoids[4])*1.e5 * 1.67e-30
                esrc_odp=float(infoodp[4])*1.e5 * 1.67e-30
                esrc_idp=float(infoidp[4])*1.e5 * 1.67e-30
                esrc_tot=float(infot[4])*1.e5 * 1.67e-30
                esrc_odiv = esrc_ods + esrc_odp
                esrc_idiv = esrc_ids + esrc_idp
                esrc_tdiv = abs(esrc_odiv) + abs(esrc_idiv)

                ezfrcitsrc_core=float(infocore[5])*1.e5 * 1.67e-30 # unit in Newton
                ezfrictsrc_sol=float(infosol[5])*1.e5 * 1.67e-30
                ezfrictsrc_ods=float(infoods[5])*1.e5 * 1.67e-30
                ezfrictsrc_ids=float(infoids[5])*1.e5 * 1.67e-30
                ezfrictsrc_odp=float(infoodp[5])*1.e5 * 1.67e-30
                ezfrictsrc_idp=float(infoidp[5])*1.e5 * 1.67e-30
                ezfrictsrc_tot=float(infot[5])*1.e5 * 1.67e-30
                ezfrictsrc_odiv = ezfrictsrc_ods + ezfrictsrc_odp
                ezfrictsrc_idiv = ezfrictsrc_ids + ezfrictsrc_idp
                ezfrictsrc_tdiv = abs(ezfrictsrc_odiv) + abs(ezfrictsrc_idiv)

                ezthermsrc_core=float(infocore[6])*1.e5 * 1.67e-30 # unit in Newton
                ezthermsrc_sol=float(infosol[6])*1.e5 * 1.67e-30
                ezthermsrc_ods=float(infoods[6])*1.e5 * 1.67e-30
                ezthermsrc_ids=float(infoids[6])*1.e5 * 1.67e-30
                ezthermsrc_odp=float(infoodp[6])*1.e5 * 1.67e-30
                ezthermsrc_idp=float(infoidp[6])*1.e5 * 1.67e-30
                ezthermsrc_tot=float(infot[6])*1.e5 * 1.67e-30
                ezthermsrc_odiv = ezthermsrc_ods + ezthermsrc_odp
                ezthermsrc_idiv = ezthermsrc_ids + ezthermsrc_idp
                ezthermsrc_tdiv = abs(ezthermsrc_odiv) + abs(ezthermsrc_idiv)
                #
        text1 = ' * ION MOMENTUM FLUX *'
        for index, line in enumerate(lines):
            if text1 in str(line):
                dummy=lines[index+2].split()
                                #

                infocore = dummy
                # print(infocore)
                infosol = lines[index+3].split()

                infoods = lines[index+4].split()

                infoids = lines[index+5].split()

                infoodp = lines[index+6].split()
                # print(infoodp)
                infoidp = lines[index+7].split()

                # infot =lines[index+8].split()
                # print(infot)

                momflux_ods_l = float(infoods[2])*1.e5 * 1.67e-30
                momflux_ods_r = float(infoods[3])*1.e5 * 1.67e-30
                momflux_ods_d = float(infoods[4])*1.e5 * 1.67e-30
                momflux_ods_u = float(infoods[5])*1.e5 * 1.67e-30
                momflux_odp_l = float(infoodp[2])*1.e5 * 1.67e-30
                momflux_odp_r = float(infoodp[3])*1.e5 * 1.67e-30
                momflux_odp_d = float(infoodp[4])*1.e5 * 1.67e-30
                momflux_odp_u = float(infoodp[5])*1.e5 * 1.67e-30

                momflux_left_odiv=momflux_odp_l
                momflux_right_odiv=momflux_ods_r
                momflux_down_odiv=momflux_odp_d+momflux_ods_d
                momflux_up_odiv=momflux_odp_u+momflux_ods_u
    f.close()
    result=OrderedDict()
    name = str(self.owner) + '/' + str(self.shot) + '/' + str(
        self.date) + '/' + str(self.seq)
    result['name']=name
    result['pcoree']=pcoree
    result['pcorei']=pcorei
    result['i_cntl_h0']=i_cntl_h0
    result['i_cntl_z2']=i_cntl_z2
    result['i_h0_pump']=i_h0_pump
    result['i_h0_reclrecpuf']=i_h0_reclrecpuf
    result['i_ext_h0_wall']=i_ext_h0_wall
    result['i_ext_h0_target']=i_ext_h0_target
    result['i_h0_main']=i_h0_main
    result['z1_pump']=z1_pump
    result['z2_pump']=z2_pump
    result['z1_ext_pufft']=z1_ext_pufft
    result['z2_ext_pufft']=z2_ext_pufft
    result['z1_ext_puffw']=z1_ext_puffw
    result['z2_ext_puffw']=z2_ext_puffw
    result['p_rec_odiv']=p_rec_odiv
    result['p_rec_idiv']=p_rec_idiv
    result['p_rec_vessel']=p_rec_vessel
    result['core_ioniz']=core_ioniz
    result['core_recom']=core_recom
    result['msol_ioniz']=msol_ioniz
    result['msol_recom']=msol_recom
    result['odiv_ioniz']=odiv_ioniz
    result['odiv_recom']=odiv_recom
    result['idiv_ioniz']=idiv_ioniz
    result['idiv_recom']=idiv_recom
    result['opfr_ioniz']=opfr_ioniz
    result['opfr_recom']=opfr_recom
    result['ipfr_ioniz']=ipfr_ioniz
    result['ipfr_recom']=ipfr_recom
    result['sol_ioniz']=sol_ioniz
    result['sol_recom']=sol_recom
    result['tot_ioniz']=tot_ioniz
    result['tot_recom']=tot_recom
    result['cx_core']=cx_core
    result['cx_msol']=cx_msol
    result['cx_odiv']=cx_odiv
    result['cx_idiv']=cx_idiv
    result['cx_opfr']=cx_opfr
    result['cx_ipfr']=cx_ipfr
    result['ati_core']=ati_core
    result['ati_msol']=ati_msol
    result['ati_odiv']=ati_odiv
    result['ati_idiv']=ati_idiv
    result['ati_opfr']=ati_opfr
    result['ati_ipfr']=ati_ipfr
    result['moli_core']=moli_core
    result['moli_msol']=moli_msol
    result['moli_odiv']=moli_odiv
    result['moli_idiv']=moli_idiv
    result['moli_opfr']=moli_opfr
    result['moli_ipfr']=moli_ipfr
    result['reci_core']=reci_core
    result['reci_msol']=reci_msol
    result['reci_odiv']=reci_odiv
    result['reci_idiv']=reci_idiv
    result['reci_opfr']=reci_opfr
    result['reci_ipfr']=reci_ipfr
    result['prad_core_h']=prad_core_h
    result['prad_core_z']=prad_core_z
    result['prad_msol_h']=prad_msol_h
    result['prad_msol_z']=prad_msol_z
    result['prad_odiv_h']=prad_odiv_h
    result['prad_odiv_z']=prad_odiv_z
    result['prad_idiv_h']=prad_idiv_h
    result['prad_idiv_z']=prad_idiv_z
    result['prad_opfr_h']=prad_opfr_h
    result['prad_opfr_z']=prad_opfr_z
    result['prad_ipfr_h']=prad_ipfr_h
    result['prad_ipfr_z']=prad_ipfr_z
    result['prad_sol_h']=prad_sol_h
    result['prad_sol_z']=prad_sol_z
    result['prad_sol']=prad_sol
    result['prad_div_h']=prad_div_h
    result['prad_div_z']=prad_div_z
    result['prad_div']=prad_div
    result['prad_h']=prad_h
    result['prad_z']=prad_z
    result['prad_tot']=prad_tot
    result['ate_core']=ate_core
    result['ate_msol']=ate_msol
    result['ate_odiv']=ate_odiv
    result['ate_idiv']=ate_idiv
    result['ate_opfr']=ate_opfr
    result['ate_ipfr']=ate_ipfr
    result['mole_core']=mole_core
    result['mole_msol']=mole_msol
    result['mole_odiv']=mole_odiv
    result['mole_idiv']=mole_idiv
    result['mole_opfr']=mole_opfr
    result['mole_ipfr']=mole_ipfr
    result['i_ves']=i_ves
    result['i_ves_msol']=i_ves_msol
    result['i_ves_odiv']=i_ves_odiv
    result['i_ves_idiv']=i_ves_idiv
    result['i_ves_pfr']=i_ves_pfr
    result['i_idiv']=i_idiv
    result['i_odiv']=i_odiv
    result['p_idiv']=p_idiv
    result['p_odiv']=p_odiv
    result['momsrc_core']=momsrc_core
    result['momsrc_sol']=momsrc_sol
    result['momsrc_ids']=momsrc_ids
    result['momsrc_ods']=momsrc_ods
    result['momsrc_idp']=momsrc_idp
    result['momsrc_odp']=momsrc_odp
    result['momsrc_idiv']=momsrc_idiv
    result['momsrc_odiv']=momsrc_odiv
    result['momsrc_tdiv']=momsrc_tdiv
    result['nisep_omp']=nisep_omp
    result['nisep_imp']=nisep_imp
    result['nisep_ot']=nisep_ot
    result['nisep_it']=nisep_it
    result['nesep_omp']=nesep_omp
    result['nesep_imp']=nesep_imp
    result['nesep_ot']=nesep_ot
    result['nesep_it']=nesep_it
    result['tisep_omp']=tisep_omp
    result['tisep_imp']=tisep_imp
    result['tisep_ot']=tisep_ot
    result['tisep_it']=tisep_it
    result['tesep_omp']=tesep_omp
    result['tesep_imp']=tesep_imp
    result['tesep_ot']=tesep_ot
    result['tesep_it']=tesep_it
    result['psep_omp']=psep_omp
    result['psep_imp']=psep_imp
    result['psep_ot']=psep_ot
    result['psep_it']=psep_it
    result['niavg_omp']=niavg_omp
    result['niavg_imp']=niavg_imp
    result['niavg_ot']=niavg_ot
    result['niavg_it']=niavg_it
    result['neavg_omp']=neavg_omp
    result['neavg_imp']=neavg_imp
    result['neavg_ot']=neavg_ot
    result['neavg_it']=neavg_it
    result['tiavg_omp']=tiavg_omp
    result['tiavg_imp']=tiavg_imp
    result['tiavg_ot']=tiavg_ot
    result['tiavg_it']=tiavg_it
    result['teavg_omp']=teavg_omp
    result['teavg_imp']=teavg_imp
    result['teavg_ot']=teavg_ot
    result['teavg_it']=teavg_it
    result['pavg_omp']=pavg_omp
    result['pavg_imp']=pavg_imp
    result['pavg_ot']=pavg_ot
    result['pavg_it']=pavg_it
    result['pi_ions']=pi_ions
    result['pi_atomic']=pi_atomic
    result['pi_mol']=pi_mol
    result['pi_cx']=pi_cx
    result['pi_rec']=pi_rec
    result['pi_eq']=pi_eq
    result['pi_com']=pi_com
    result['pi_dt']=pi_dt
    result['pe_ions']=pe_ions
    result['pe_atomic']=pe_atomic
    result['pe_mol']=pe_mol
    result['pe_rec'] = pe_rec
    result['pe_hrad']=pe_hrad
    result['pe_zrad']=pe_zrad
    result['pe_eq']=pe_eq
    result['pe_com'] = pe_com
    result['pe_dt']=pe_dt
    result['ionflux_core_out']=ionflux_core_out
    result['ionflux_sol_wall']=ionflux_sol_wall
    result['ionflux_sol_outdiv']=ionflux_sol_outdiv
    result['ionflux_sol_indiv']=ionflux_sol_indiv
    result['ionflux_prv_outdiv']=ionflux_prv_outdiv
    result['ionflux_prv_indiv']=ionflux_prv_indiv
    result['pcore_out_ion']=pcore_out_ion
    result['pcore_out_ele']=pcore_out_ele
    result['pod_ion']=pod_ion
    result['pod_ele']=pod_ele
    result['pid_ion']=pid_ion
    result['pid_ele']=pid_ele
    result['pves_ion']=pves_ion
    result['pves_ele']=pves_ele
    result['pves_od_ion']=pves_od_ion
    result['pves_od_ele']=pves_od_ele
    result['pves_id_ion']=pves_id_ion
    result['pves_id_ele']=pves_id_ele
    result['pves_opfr_ion']=pves_opfr_ion
    result['pves_opfr_ele']=pves_opfr_ele
    result['pves_ipfr_ion']=pves_ipfr_ion
    result['pves_ipfr_ele']=pves_ipfr_ele
    result['imp1flux_core_out']=imp1flux_core_out
    result['imp2flux_core_out']=imp2flux_core_out
    result['gradpsrc_odiv']=gradpsrc_odiv
    result['esrc_odiv']=esrc_odiv
    result['ezfrictsrc_odiv']=ezfrictsrc_odiv
    result['ezthermsrc_odiv']=ezthermsrc_odiv
    result['momflux_left_odiv']=momflux_left_odiv
    result['momflux_right_odiv']=momflux_right_odiv
    result['momflux_down_odiv']=momflux_down_odiv
    result['momflux_up_odiv']=momflux_up_odiv
    result['e_dt_core'] =                e_dt_core
    result['e_dt_sol'] =                 e_dt_sol
    result['e_dt_ods'] =                e_dt_ods
    result['e_dt_ids'] =                 e_dt_ids
    result['e_dt_odp'] =                 e_dt_odp
    result['e_dt_idp'] =                 e_dt_idp
    result['e_dt_tot'] =                 e_dt_tot
    result['i_dt_core'] =                i_dt_core
    result['i_dt_sol'] =                 i_dt_sol
    result['i_dt_ods'] =                i_dt_ods
    result['i_dt_ids'] =                 i_dt_ids
    result['i_dt_odp'] =                 i_dt_odp
    result['i_dt_idp'] =                 i_dt_idp
    result['i_dt_tot'] =                 i_dt_tot
    result['e_OHM_HEAT_core'] =                 e_OHM_HEAT_core
    result['e_OHM_HEAT_sol'] =                 e_OHM_HEAT_sol
    result['e_OHM_HEAT_ods'] =                 e_OHM_HEAT_ods
    result['e_OHM_HEAT_ids'] =                 e_OHM_HEAT_ids
    result['e_OHM_HEAT_odp'] =                 e_OHM_HEAT_odp
    result['e_OHM_HEAT_idp'] =                 e_OHM_HEAT_idp
    result['e_OHM_HEAT_tot'] =                 e_OHM_HEAT_tot
    result['i_MOLE_ELASTIC_core'] =                i_MOLE_ELASTIC_core
    result['i_MOLE_ELASTIC_sol'] =                 i_MOLE_ELASTIC_sol
    result['i_MOLE_ELASTIC_ods'] =                 i_MOLE_ELASTIC_ods
    result['i_MOLE_ELASTIC_ids'] =                 i_MOLE_ELASTIC_ids
    result['i_MOLE_ELASTIC_odp'] =                 i_MOLE_ELASTIC_odp
    result['i_MOLE_ELASTIC_idp'] =                 i_MOLE_ELASTIC_idp
    result['i_MOLE_ELASTIC_tot'] =                 i_MOLE_ELASTIC_tot
    result['i_AT_ELASTIC_core'] =                i_AT_ELASTIC_core
    result['i_AT_ELASTIC_sol'] =                 i_AT_ELASTIC_sol
    result['i_AT_ELASTIC_ods'] =                 i_AT_ELASTIC_ods
    result['i_AT_ELASTIC_ids'] =                 i_AT_ELASTIC_ids
    result['i_AT_ELASTIC_odp'] =                 i_AT_ELASTIC_odp
    result['i_AT_ELASTIC_idp'] =                 i_AT_ELASTIC_idp
    result['i_AT_ELASTIC_tot'] =                 i_AT_ELASTIC_tot
    result['I_MOLE_ELASTIC_core'] =                I_MOLE_ELASTIC_core
    result['i_MOLE_ELASTIC_sol'] =                 i_MOLE_ELASTIC_sol
    result['i_MOLE_ELASTIC_ods'] =                 i_MOLE_ELASTIC_ods
    result['i_MOLE_ELASTIC_ids'] =                 i_MOLE_ELASTIC_ids
    result['i_MOLE_ELASTIC_odp'] =                 i_MOLE_ELASTIC_odp
    result['i_MOLE_ELASTIC_idp'] =                 i_MOLE_ELASTIC_idp
    result['i_MOLE_ELASTIC_tot'] =                 i_MOLE_ELASTIC_tot
    result['i_KIN_EN_CORR_core'] =                i_KIN_EN_CORR_core
    result['i_KIN_EN_CORR_sol'] =                 i_KIN_EN_CORR_sol
    result['i_KIN_EN_CORR_ods'] =                 i_KIN_EN_CORR_ods
    result['i_KIN_EN_CORR_ids'] =                 i_KIN_EN_CORR_ids
    result['i_KIN_EN_CORR_odp'] =                 i_KIN_EN_CORR_odp
    result['i_KIN_EN_CORR_idp'] =                 i_KIN_EN_CORR_idp
    result['i_KIN_EN_CORR_tot'] =                 i_KIN_EN_CORR_tot
    result['i_VISCOUS_core'] =                i_VISCOUS_core
    result['i_VISCOUS_sol'] =                 i_VISCOUS_sol
    result['i_VISCOUS_ods'] =                 i_VISCOUS_ods
    result['i_VISCOUS_ids'] =                 i_VISCOUS_ids
    result['i_VISCOUS_odp'] =                 i_VISCOUS_odp
    result['i_VISCOUS_idp'] =                 i_VISCOUS_idp
    result['i_VISCOUS_tot'] =                          i_VISCOUS_tot
    result['i_EXT_core'] =                i_EXT_core
    result['i_EXT_sol'] =                 i_EXT_sol
    result['i_EXT_ods'] =                 i_EXT_ods
    result['i_EXT_ids'] =                 i_EXT_ids
    result['i_EXT_odp'] =                 i_EXT_odp
    result['i_EXT_idp'] =                 i_EXT_idp
    result['i_EXT_tot'] =                   i_EXT_tot




    return result


###############################################
  @staticmethod
  def write_print2file(simu_list,path,filename):
    """
    writes to file the output of read_print_file_edge2d, it takes as input a list of simulations
    """
    with open(path+'/'+filename+'_print.csv', 'w') as f:  # Just use 'w' mode in 3.x
      simu=simu_list[0][0]
      result=simu.read_print_file_edge2d()
      w = csv.DictWriter(f, result.keys(), delimiter='\t')
      w.writeheader()
    with open(path+'/'+filename+'_print.csv', 'a') as f:  # Just use 'w' mode in 3.x
      writer = csv.writer(f, delimiter='\t')
      for index1 in range(0,len(simu_list)):
        simu=simu_list[index1][0]
        #print(simu)
        result=simu.read_print_file_edge2d()
        writer.writerow(result.values())
        
   
    f.close()
    print('print file written to ... ', path+'/'+filename+'_print.csv')

###############################################


  def read_ionrecom(self):
    """
    extracts information about ionization and recombination in the divertor
    """

    vol_correct=2.*np.pi *1e-6


    ixpt1=self.RHS_row
    ixpt2=self.LHS_row
    # ; read in radial profile at outer plate to determine
    # ; SOL radial width and index of separatrix
    # ; dummy parameter: ionisation source 'soun'

    temp_ot=ep.row(self.fullpath,'soun','OT')
    ny_ot=temp_ot.nPts
    dsrad_ot=temp_ot.xData[0:ny_ot]
    iy_sol_ot=np.greater(dsrad_ot, 0.0).nonzero()[0]
    iy_sep_ot=iy_sol_ot[0]

    temp_it=ep.row(self.fullpath,'soun','IT')
    ny_it=temp_it.nPts
    dsrad_it=temp_it.xData[0:ny_it]
    iy_sol_it=np.greater(dsrad_it, 0.0).nonzero()[0]
    iy_sep_it=iy_sol_it[0]
    #
    # # ; read in SOUN as representative parameter to calculate
    # # ; poloidal # of cells of SOL
    #
    soun_sol=ep.ring(self.fullpath,'soun','S1')
    nx_sol=soun_sol.nPts-1

    soun_pfr=ep.ring(self.fullpath,'soun','P1')
    nx_pfr=soun_pfr.nPts-1
    #
    # # ; read in poloidal rings across SOL and PFR up to x-point
    # # ; to build 2-D map of dspol
    #
    dspol_idiv=np.zeros(shape=(ixpt2,ny_it))
    dspol_idiv_norm=np.zeros(shape=(ixpt2,ny_it))
    rings_idiv_sol=[]
    for i in range(1,iy_sol_it.size+1):
        dummy='S'+str(i)
        rings_idiv_sol.append(dummy)

    rings_idiv_pfr=[]

    for i in range(1,iy_sol_it.size+1):
        dummy='P'+str(i)
        rings_idiv_pfr.append(dummy)

    #
    for i in range(0,len(rings_idiv_sol)):
        # print(i)
        temp=ep.ring(self.fullpath,'soun',rings_idiv_sol[i])
        dspol_idiv[0:ixpt2-1,iy_sep_it+i]= temp.xData[nx_sol-ixpt2+1:nx_sol]
        dspol_idiv_norm[0:ixpt2-1,iy_sep_it+i]=(temp.xData[nx_sol-ixpt2+1:nx_sol] -temp.xData[nx_sol-ixpt2+1]) / (temp.xData[nx_sol] - temp.xData[nx_sol-ixpt2+1])

    #
    #
    for i in range(len(rings_idiv_pfr)):
        temp=ep.ring(self.fullpath,'soun',rings_idiv_pfr[i])
        dspol_idiv[0:ixpt2-1,iy_sep_it-i-1]=temp.xData[nx_pfr-ixpt2+1:nx_pfr]
        dspol_idiv_norm[0:ixpt2-1,iy_sep_it-i-1]=(temp.xData[nx_pfr-ixpt2+1:nx_pfr] -temp.xData[nx_pfr-ixpt2+1]) /(temp.xData[nx_pfr] -	temp.xData[nx_pfr-ixpt2+1])
    #
    dspol_odiv=np.zeros(shape=(ixpt1,ny_ot))
    dspol_odiv_norm=np.zeros(shape=(ixpt1,ny_ot))
    rings_odiv_sol=[]
    for i in range(1,iy_sol_ot.size+1):
        dummy='S'+str(i)
        rings_odiv_sol.append(dummy)

    rings_odiv_pfr=[]

    for i in range(1,iy_sol_ot.size+1):
        dummy='P'+str(i)
        rings_odiv_pfr.append(dummy)

    #
    for i in range(len(rings_odiv_sol)):
        temp=ep.ring(self.fullpath,'soun',rings_odiv_sol[i])
        dspol_odiv[0:ixpt1-1,iy_sep_ot+i]=temp.xData[nx_sol-ixpt1+1:nx_sol]
        dspol_odiv_norm[0:ixpt1-1,iy_sep_ot+i]=(temp.xData[nx_sol-ixpt1+1:nx_sol] - temp.xData[nx_sol-ixpt1+1]) / (temp.xData[nx_sol] - temp.xData[nx_sol-ixpt1+1])
    # endfor
    #
    #
    for i in range(len(rings_odiv_pfr)):
        temp=ep.ring(self.fullpath,'soun',rings_odiv_pfr[i])
        dspol_odiv[0:ixpt2-1,iy_sep_ot-i-1]= temp.xData[nx_pfr-ixpt1+1:nx_pfr]
        dspol_odiv_norm[0:ixpt1-1,iy_sep_ot-i-1]= (temp.xData[nx_pfr-ixpt1+1:nx_pfr] -	temp.xData[nx_pfr-ixpt1+1]) /  (temp.xData[nx_pfr] - temp.xData[nx_pfr-ixpt1+1])
    #

    rows_idiv=range(nx_sol,nx_sol-ixpt2,-1)
    rows_odiv=range(ixpt1)
    # print(rows_idiv,rows_odiv)

    soun_idiv=np.zeros(shape=(ixpt2+1,ny_ot+1))
    soun_odiv=np.zeros(shape=(ixpt1+1,ny_ot+1))
    sirec_idiv=np.zeros(shape=(ixpt2+1,ny_ot+1))
    sirec_odiv=np.zeros(shape=(ixpt1+1,ny_ot+1))

    vol_idiv=np.zeros(shape=(ixpt2+1,ny_ot+1))
    vol_odiv=np.zeros(shape=(ixpt1+1,ny_ot+1))
    #
    for i in range(ixpt1):
    # i=0
    # 	print(rows_odiv[i])
    # 	print(i)
        temp=ep.row(self.fullpath,'soun',rows_odiv[i])
        soun_odiv[i,0:ny_ot]=temp.yData[0:ny_ot]
        temp=ep.row(self.fullpath,'sirec',rows_odiv[i])
        sirec_odiv[i,0:ny_ot]=temp.yData[0:ny_ot]
        temp=ep.row(self.fullpath,'DV',rows_odiv[i])
        vol_odiv[i,0:ny_ot]=np.asarray(temp.yData[0:ny_ot]) * vol_correct

    # print(vol_odiv)
    for i in range(ixpt2):

        temp=ep.row(self.fullpath,'soun',rows_idiv[i])
        soun_idiv[i,0:ny_it]=temp.yData[0:ny_it]
        temp=ep.row(self.fullpath,'sirec',rows_idiv[i])
        sirec_idiv[i,0:ny_it]=temp.yData[0:ny_it]
        temp=ep.row(self.fullpath,'DV',rows_idiv[i])
        vol_idiv[i,0:ny_it]=np.asarray(temp.yData[0:ny_it]) *  vol_correct
    # # # #
    # #
    # # # #
    i_ioniz_idiv=soun_idiv #; *vol_idiv
    i_ioniz_odiv=soun_odiv #; *vol_odiv
    i_recom_idiv=sirec_idiv #; *vol_idiv
    i_recom_odiv=sirec_odiv #; *vol_odiv


    max_i_ioniz_idiv,maxp_i_ioniz_idiv = i_ioniz_idiv.max(),i_ioniz_idiv.argmax(axis=0)
    # print(amax(i_ioniz_idiv,axis=0))
    # # indx_max_i_ioniz_idiv=array_indices(i_ioniz_idiv, maxp_i_ioniz_idiv)
    # print(unravel_index(i_ioniz_idiv.argmax(), i_ioniz_idiv.shape))
    max_i_ioniz_odiv,maxp_i_ioniz_odiv = i_ioniz_odiv.max(),i_ioniz_odiv.argmax(axis=0)
    # # indx_max_i_ioniz_odiv=array_indices(i_ioniz_odiv, maxp_i_ioniz_odiv)
    #
    max_i_recom_idiv,maxp_i_recom_idiv = abs(i_recom_idiv).max(),abs(i_recom_idiv).argmax(axis=0)
    # # indx_max_i_recom_idiv=array_indices(abs(i_recom_idiv), maxp_i_recom_idiv)
    #
    max_i_recom_odiv,maxp_i_recom_odiv = abs(i_recom_odiv).max(),abs(i_recom_odiv).argmax(axis=0)
    # # indx_max_i_recom_odiv=array_indices(abs(i_recom_odiv), maxp_i_recom_odiv)



    return{'i_ioniz_idiv':i_ioniz_idiv,
            'i_recom_idiv':i_recom_idiv,
            'max_i_ioniz_idiv':max_i_ioniz_idiv,
            'indx_max_i_ioniz_idiv':maxp_i_ioniz_idiv,
            'max_i_recom_idiv':max_i_recom_idiv,
            'indx_max_i_recom_idiv':maxp_i_recom_idiv,
            'i_ioniz_odiv':i_ioniz_odiv,
            'i_recom_odiv':i_recom_odiv,
            'max_i_ioniz_odiv':max_i_ioniz_odiv,
            'indx_max_i_ioniz_odiv':maxp_i_ioniz_odiv,
            'max_i_recom_odiv':max_i_recom_odiv,
            'indx_max_i_recom_odiv':maxp_i_recom_odiv,
            'dspol_idiv':dspol_idiv,
            'dspol_idiv_norm':dspol_idiv_norm,
            'dspol_odiv':dspol_odiv,
            'dspol_odiv_norm':dspol_odiv_norm}
###############################################
  def read_psol_pradpsol(self):

    """
    extracts information about the radiated power


    """
    #result=ep.time(self.fullpath,'POWSOL')
    #psol=result.yData
    psol=self.read_time_data('POWSOL',100)
    #print psol
    result1 = ep.volint(self.fullpath,'SQEHRAD','S01','S'+str(self.sol_ring))
    #print result1
    result2 = ep.volint(self.fullpath,'SQEHRAD','P01','P'+str(self.pr_ring))
    result3 = ep.volint(self.fullpath,'SQEHRAD','C01','C'+str(self.core_ring))
    sqehrad_sol = result1+result2
    #print(sqehrad_sol)
    sqehrad_core = result3
    sqehrad_tot = sqehrad_sol+sqehrad_core
    try:
      result1 = ep.volint(self.fullpath,'SQEZR_1','S01','S'+str(self.sol_ring))
      result2 = ep.volint(self.fullpath,'SQEZR_1','P01','P'+str(self.pr_ring))
      result3 = ep.volint(self.fullpath,'SQEZR_1','C01','C'+str(self.core_ring))
    except:
      result1 =0;result2=0;result3=0
    sqezr1_sol = result1+result2
    sqezr1_core = result3
    sqezr1_tot = sqezr1_sol+sqezr1_core
    try:
      result1 = ep.volint(self.fullpath,'SQEZR_2','S01','S'+str(self.sol_ring))
      result2 = ep.volint(self.fullpath,'SQEZR_2','P01','P'+str(self.pr_ring))
      result3 = ep.volint(self.fullpath,'SQEZR_2','C01','C'+str(self.core_ring))
    except:
      result1 =0;result2=0;result3=0
    sqezr2_sol = result1+result2
    sqezr2_core = result3
    sqezr2_tot = sqezr2_sol+sqezr2_core
    pradsol = sqehrad_sol+sqezr1_sol+sqezr2_sol
    #print(pradsol)
    pradtot = sqehrad_tot+sqezr1_tot+sqezr2_tot
    #print pradtot
    pradcore = pradtot - pradsol
    #print pradcore
    #print(pradsol,psol)
    fradsol = pradsol/psol
    fradsol2 = pradsol/pradtot
    rme = self.rme
    zme= self.zme
    # if ExtraInput is None:
    dve = ep.data(self.fullpath,'DV').data
    hra = ep.data(self.fullpath, 'SQEHRAD').data
    try:
        sqe1 = ep.data(self.fullpath, 'SQEZR_1').data
    except:
        sqe1 = 0
    try:
        sqe2 = ep.data(self.fullpath, 'SQEZR_2').data
    except:
        sqe2 = 0
    # else:
    #     dve= self.read_data('DV',ExtraInput)['data']
    #     hra =  self.read_data('SQEHRAD',ExtraInput)['data']
    #
    #     sqe1 =  self.read_data('SQEZR_1',ExtraInput)['data']
    #
    #     sqe2 =  self.read_data('SQEZR_2',ExtraInput)['data']

    hra = hra*dve
    sqe1=sqe1*dve
    sqe2=sqe2*dve
    rad_div_sum = 0

    for i in range(0,self.npts_m):
        if zme[i] < 1.2:
            rad_div_sum = rad_div_sum+hra[i]+sqe1[i]+sqe2[i]
    rad_div_sum = rad_div_sum
    fraddiv = rad_div_sum/psol
    return{'powsol':psol,
          'raddivsum':rad_div_sum,
          'pradcore':pradcore,
          'pradsol':pradsol,
          'pradtot':pradtot,
          'fradsol':fradsol,
          'fraddiv':fraddiv,
          'fradsol2':fradsol2,
          'hrad':sqehrad_tot,
          'brad':sqezr1_tot,
          'nrad':sqezr2_tot}
###############################################
  def read_time_data(self,var,interval):
    """
    extracts data time depentent, taking the median of an interval
    """
    result = ep.time(self.fullpath,var)
    data = result.yData
    data= data[-interval]

    return np.median(data)
###############################################
  def read_pow_lfs_div(self,interval):
    """
    extracts outer target power load
    """
    epowot=read_time_data(self,'epowot',interval)

    ipowit=read_time_data(self,'ipowot',interval)

    flxot=read_time_data(self,'FLXOT',interval)

    return {'pow':epowot*1e-6 + ipowot*1e-6 + flxot*1.6022e-19*1e-6*13.6}

# def read_row_data1(self,variable,region,ExtraInput):
# 	#ExtraInput is the suffix used to store the simulation in its dedicated folder
# 	pathT=self.path_e2d+'/'+self.sim_folder+ExtraInput+'/seq'+self.seq
# 	with open(pathT+'/'+region+'/'+variable+'_row.csv', 'rb') as f:
# 		reader = csv.reader(f, delimiter=';')
# 		next(reader)
# 		col = list(zip(*reader))[1]
# 	f.close()
# 	return np.array(col)

###############################################
  def read_row_data(self,variable,region,ExtraInput):
    """
    reads from stored csv files (created with the download tool)
    containing data along rows of the mesh
    usage:
    simu=sim('92123','jul1717','2','bviola','edge2d')
    dummy=read_row_data('DENEL','OT','HFE')

    variable and region must be given in capital letter

    HFE is the extrainput used to label the simulation during the download phase
    ExtraInput is the suffix used to store the simulation in its dedicated folder
    """

    pathT=self.path_e2d+'/'+self.sim_folder+ExtraInput+'/seq'+self.seq
    with open(pathT+'/'+region+'/'+variable+'_row.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        # col = list(zip(*reader))[1]
        csv_dic = []

        for row in reader:
            csv_dic.append(row);
        col1 = []
        col2 = []

        for row in csv_dic:
            col1.append(row[0])
            col2.append(row[1])
        dummy=np.array(col1)
        dummy2=np.array(col2)
        dummy2=[float(i) for i in dummy2]
        y_data=np.asarray(dummy2)
        dummy=[float(i) for i in dummy]
        x_data=np.asarray(dummy)
    f.close()
    return {'xData':x_data,
            'yData':y_data}

###############################################
  def read_data(self,variable,ExtraInput):
    """

    read data stored using the download tool

    usage:
    simu=sim('92123','jul1717','2','bviola','edge2d')
    var=simu.read_data('TEVE','HFE')
    ExtraInput is the suffix used to store the simulation in its dedicated folder
    """


    pathT=self.path_e2d+'/'+self.sim_folder+ExtraInput+'/seq'+self.seq
    with open(pathT+'/data/'+variable+'.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        # col = list(zip(*reader))[1]
        csv_dic = []

        for row in reader:
            csv_dic.append(row);
        col = []


        for row in csv_dic:
            col.append(row[0])
        dummy=np.array(col)
        dummy=[float(i) for i in dummy]
        data=np.asarray(dummy)
    f.close()
    return {'data':data}
###############################################
  def read_edge2d_pedestal_fuel(self):
#read pedestalfuel


    triggervalue = ep.ring(self.fullpath,'TEVE','C99')
    triggervalue = triggervalue.yData
    triggervalue = triggervalue[0]
    triggerind = 0
    pedestalfuel = 0
    i = 0
    while triggerind == 0:
        i = i+1
        if i < 10:
            dv = ep.ring(self.fullpath,'DV','C0'+str(i))
            dv = np.array(dv.yData)

            soun = ep.ring(self.fullpath,'SOUN','C0'+str(i))
            soun = np.array(soun.yData)

            pedestalfuel = np.array(pedestalfuel) + np.sum(dv*soun)

            trigger = ep.ring(self.fullpath,'TEVE', 'C0'+str(i))
            trigger = trigger.yData

            if trigger[0] == triggervalue:
                triggerind = 1

        else:
            dv = ep.ring(self.fullpath,'DV','C'+str(i))
            dv = np.array(dv.yData)

            soun = ep.ring(self.fullpath,'SOUN','C'+str(i))
            soun = np.array(soun.yData)

            pedestalfuel =np.array(pedestalfuel) + np.sum(dv*soun)

            trigger = ep.ring(self.fullpath,'TEVE', 'C'+str(i))
            trigger = trigger.yData

            if trigger[0] == triggervalue:
                triggerind = 1
    return pedestalfuel
###############################################
  def read_radiation_split(self,interval):
    """
    extracts radiation in different divertor zones:
    total divertor radiation
    low field side radiation
    high field side radiation
    below xpoint radiation
    """
    # if ExtraInput is None:
    dve = ep.data(self.fullpath,'DV').data
    hra = ep.data(self.fullpath, 'SQEHRAD').data
    try:
        sqe1 = ep.data(self.fullpath,'SQEZR_1').data
    except:
        sqe1=0
    try:
        sqe2 = ep.data(self.fullpath,'SQEZR_2').data
    except:
        sqe2=0
    try:
        sqe= ep.data(self.fullpath,'SQEZRAD').data
    except:
        sqe=0
    # else:
    #     dve = self.read_data('DV',ExtraInput)['data']
    #     hra = self.read_data('SQEHRAD',ExtraInput)['data']
    #     try:
    #         sqe1 = self.read_data('SQEZR_1',ExtraInput)['data']
    #     except:
    #         sqe1 = 0
    #     try:
    #         sqe2 = self.read_data('SQEZR_2', ExtraInput)['data']
    #     except:
    #         sqe2 = 0
    #     try:
    #         sqe = self.read_data('SQEZRAD', ExtraInput)['data']
    #     except:
    #         sqe = 0



    hra=(hra*dve)
    if (np.sum(sqe)) ==0 :

        sqe1=(sqe1*dve)
        sqe2=(sqe2*dve)
        # rad_div_sum = 0
        rad_div_lfs = 0
        rad_div_hfs = 0
        rad_div_bxp=0
        rad_axp=0
        for i in range(0,self.npts_m):
            if self.zme[i] > self.zxp:
                rad_axp = rad_axp+hra[i]+sqe1[i]+sqe2[i]
            else:
                rad_div_bxp = rad_div_bxp + hra[i] + sqe1[i] + sqe2[i]
            # print(rad_div_sum)
                if self.rme[i] > 2.634:
                    rad_div_lfs = rad_div_lfs+hra[i]+sqe1[i]+sqe2[i]
                else:
                    rad_div_hfs = rad_div_hfs+hra[i]+sqe1[i]+sqe2[i]
        rad_div_bxp=rad_div_bxp/1e6
        lfsrad=rad_div_lfs/1e6
        hfsrad=rad_div_hfs/1e6
        rad_axp=rad_axp/1e6
        output = {'rad_div_bxp':rad_div_bxp,
                  'lfsrad':lfsrad,
                  'hfsrad':hfsrad,
                  'rad_axp':rad_axp}
        return output
    else:
        sqe=(sqe*dve)
        rad_axp=0
        # rad_div_sum = 0
        rad_div_lfs = 0
        rad_div_hfs = 0
        rad_div_bxp=0
        for i in range(0,self.npts_m):
            if self.zme[i] > self.zxp:
                rad_axp = rad_axp+hra[i]+sqe1[i]+sqe2[i]
            else:
                rad_div_bxp = rad_div_bxp + hra[i] + sqe1[i] + sqe2[i]
            # print(rad_div_sum)
                if self.rme[i] > 2.634:
                    rad_div_lfs = rad_div_lfs+hra[i]+sqe1[i]+sqe2[i]
                else:
                    rad_div_hfs = rad_div_hfs+hra[i]+sqe1[i]+sqe2[i]
        rad_div_bxp=rad_div_bxp/1e6
        lfsrad=rad_div_lfs/1e6
        hfsrad=rad_div_hfs/1e6
        rad_axp=rad_axp/1e6
        output = {'rad_div_bxp':rad_div_bxp,
                  'lfsrad':lfsrad,
                  'hfsrad':hfsrad,
                  'rad_axp':rad_axp}
        return output

###############################################
  def read_qpeak_ot(self):
    """
    extracts maximum outer target load

    """
    # if ExtraInput is None:
    qiflxd = ep.row(self.fullpath,'QIFLXD', 'OT').yData
    qeflxd = ep.row(self.fullpath,'QEFLXD', 'OT').yData
    Row = ep.row(self.fullpath,'PFLXD', 'OT').yData
    pflxd = ep.row(self.fullpath,'PFLXD', 'OT').yData
    rmesh = ep.row(self.fullpath,'RMESH', 'OT').yData

    # else:
    #     qiflxd=self.read_row_data('QIFLXD','OT',ExtraInput)['yData']
    #     qeflxd=self.read_row_data('QEFLXD','OT',ExtraInput)['yData']
    #     Row=self.read_row_data('PFLXD','OT',ExtraInput)['xData']
    #     pflxd=self.read_row_data('PFLXD','OT',ExtraInput)['yData']
    #     rmesh=self.read_row_data('RMESH','OT',ExtraInput)['yData']
    out = np.zeros(len(Row))
    area = np.zeros(len(Row))
    for i in range(0,len(Row)):
        if i < len(Row):
            if i > 0:
                out[i] = (abs(qiflxd[i])+abs(qeflxd[i]))/((Row[i]-Row[i-1])*2*3.14*rmesh[i-1])
                area[i] = (Row[i]-Row[i-1])*2*3.14*rmesh[i-1]
            else:
                out[i] = (abs(qiflxd[i])+abs(qeflxd[i]))/((Row[i+1]-Row[i])*2*3.14*rmesh[i])
                area[i] = (Row[i+1]-Row[i])*2*3.14*rmesh[i]

        else:
            out[i] = (abs(qiflxd[i])+abs(qeflxd[i])+abs(pflxd[i])*13.6*1.6022e-19)/((Row[i]-Row[i-1])*2*3.14*rmesh[i-1])
            area[i]	 = (Row[i]-Row[i-1])*2*3.14*rmesh[i-1]


    return {'qpeak':out,
            'area':area}
###############################################
  def read_prad_sol(self):
    """
    extracts radiated power and radiated power below x point

    """

    triggervalue = ep.ring(self.fullpath,'TEVE','C99')
    triggervalue = triggervalue.yData
    triggervalue = triggervalue[0]
    triggerind = 0
    pedestalfuel = 0


    # if ExtraInput is None:
    hra = ep.data(self.fullpath,'SQEHRAD').data
    dv = ep.data(self.fullpath,'DV')

    try:
        sqe1=ep.data(self.fullpath,'SQEZR_1').data
      # sqe1 = self.read_data('SQEZR_1',ExtraInput)['data']
    except:
        sqe1=0
    #
    try:
        sqe2 = ep.data(self.fullpath, 'SQEZR_2').data
      # sqe2 = self.read_data('SQEZR_2',ExtraInput)['data']
    except:
      sqe2=0
    # sqezr=ep.data(self.fullpath,'sqezrad')
    try:
      sqe= ep.data(self.fullpath,'SQEZRAD').data
      # sqe= self.read_data('sqezrad',ExtraInput)['data']
    except:
      sqe=0
    # else:
    #     dve = self.read_data('DV', ExtraInput)['data']
    #     hra = self.read_data('SQEHRAD', ExtraInput)['data']
    #     try:
    #       sqe1 = self.read_data('SQEZR_1',ExtraInput)['data']
    #     except:
    #         sqe1=0
    #     #
    #     try:
    #       sqe2 = self.read_data('SQEZR_2',ExtraInput)['data']
    #     except:
    #       sqe2=0
    #     try:
    #       sqe= self.read_data('SQEZRAD',ExtraInput)['data']
    #     except:
    #       sqe=0
        
        
        
        
    hra=(hra*dve)
    if (np.sum(sqe)) ==0 :

        sqe1=(sqe1*dve)
        sqe2=(sqe2*dve)
        rad_sum = 0
        rad_sum_below=0
        for i in range(0,self.npts_m):
            rad_sum = rad_sum-hra[i]-sqe1[i]-sqe2[i]
            if self.zme[i] <0:
                rad_sum_below = rad_sum_below-hra[i]-sqe1[i]-sqe2[i]
        i = 0
        corerad = 0
        while triggerind == 0:
            i = i+1
            if i < 10:
                dv = ep.ring(self.fullpath,'DV','C0'+str(i))
                dv = np.array(dv.yData)

                hrad = ep.ring(self.fullpath,'SQEHRAD','C0'+str(i))
                hrad = -np.array(hrad.yData)
                try:
                  sqe1 = ep.ring(self.fullpath,'SQEZR_1','C0'+str(i))
                  sqe1 = -np.array(sqe1.yData)
                except:
                  sqe1=0
                try:
                  sqe2 = ep.ring(self.fullpath,'SQEZR_2','C0'+str(i))
                  sqe2 = -np.array(sqe2.yData)
                except:
                  sqe2=0
                corerad = corerad + np.sum(dv*(hrad+sqe1+sqe2))

                trigger = ep.ring(self.fullpath,'TEVE', 'C0'+str(i))
                trigger = trigger.yData

                if trigger[0] == triggervalue:
                    triggerind = 1

            else:
                dv = ep.ring(self.fullpath,'DV','C'+str(i))
                dv = np.array(dv.yData)

                hrad = ep.ring(self.fullpath,'SQEHRAD','C'+str(i))
                hrad = -np.array(hrad.yData)
                try:
                  sqe1 = ep.ring(self.fullpath,'SQEZR_1','C'+str(i))
                  sqe1 = -np.array(sqe1.yData)
                except:
                  sqe1=0
                try:
                  sqe2 = ep.ring(self.fullpath,'SQEZR_2','C'+str(i))
                  sqe2 = -np.array(sqe2.yData)
                except:
                  sqe2=0
                corerad = corerad + np.sum(dv*(hrad+sqe1+sqe2))

                trigger = ep.ring(self.fullpath,'TEVE', 'C'+str(i))
                trigger = trigger.yData

                if trigger[0] == triggervalue:
                    triggerind = 1

        psol_rad_below = rad_sum_below - corerad/2
        psol_rad= rad_sum -corerad
        return {'psol_rad_below':psol_rad_below,
                'psol_rad':psol_rad}
    else:


        sqe=sqe*dve

        rad_sum_below=0
        for i in range(0,self.npts_m):
            rad_sum = rad_sum-hra[i]-sqe1[i]-sqe2[i]
            if self.zme[i] <0:
                rad_sum_below = rad_sum_below-hra[i]-sqe1[i]-sqe2[i]
        i = 0
        corerad = 0
        while triggerind == 0:
            i = i+1
            if i < 10:
                dv = ep.ring(self.fullpath,'DV','C0'+str(i))
                dv = np.array(dv.yData)

                hrad = ep.ring(self.fullpath,'SQEHRAD','C0'+str(i))
                hrad = -np.array(hrad.yData)
                sqe1 = ep.ring(self.fullpath,'SQEZR_1','C0'+str(i))
                sqe1 = -np.array(sqe1.yData)
                sqe2 = ep.ring(self.fullpath,'SQEZR_2','C0'+str(i))
                sqe2 = -np.array(sqe2.yData)
                corerad = corerad + np.sum(dv*(hrad+sqe1+sqe2))

                trigger = ep.ring(self.fullpath,'TEVE', 'C0'+str(i))
                trigger = trigger.yData

                if trigger[0] == triggervalue:
                    triggerind = 1

            else:
                dv = ep.ring(self.fullpath,'DV','C'+str(i))
                dv = np.array(dv.yData)

                hrad = ep.ring(self.fullpath,'SQEHRAD','C'+str(i))
                hrad = -np.array(hrad.yData)
                sqe1 = ep.ring(self.fullpath,'SQEZR_1','C'+str(i))
                sqe1 = -np.array(sqe1.yData)
                sqe2 = ep.ring(self.fullpath,'SQEZR_2','C'+str(i))
                sqe2 = -np.array(sqe2.yData)
                corerad = corerad + np.sum(dv*(hrad+sqe1+sqe2))

                trigger = ep.ring(self.fullpath,'TEVE', 'C'+str(i))
                trigger = trigger.yData

                if trigger[0] == triggervalue:
                    triggerind = 1

        psol_rad_below = rad_sum_below - corerad/2
        psol_rad= rad_sum -corerad
        return {'psol_rad_below':psol_rad_below,
                'psol_rad':psol_rad}

###############################################
  def read_imp_content(self):

      dve = ep.data(self.fullpath,'DV').data

      zmesh  = ep.data(self.fullpath,'ZMESH').data

      try:
          # den5 = self.read_data('DENZ05', ExtraInput)['data']
          den6 = ep.data(self.fullpath,'DENZ06').data
          # den6 = self.read_data('DENZ06', ExtraInput)['data']
          den7 = ep.data(self.fullpath,'DENZ07').data
          # den7 = self.read_data('DENZ07', ExtraInput)['data']
          den8 = ep.data(self.fullpath,'DENZ08').data
          # den8 = self.read_data('DENZ08', ExtraInput)['data']
          den9 = ep.data(self.fullpath,'DENZ09').data
          # den9 = self.read_data('DENZ09', ExtraInput)['data']
          den10 = ep.data(self.fullpath,'DENZ10').data
          # den10 = self.read_data('DENZ10', ExtraInput)['data']
          den11 = ep.data(self.fullpath,'DENZ11').data
          # den11 = self.read_data('DENZ11', ExtraInput)['data']
      except:
          den5, den6, den7, den8, den9, de10, den11 = 0, 0, 0, 0, 0, 0, 0

      # else:
      #
      #
      #     # dv = ep.data(self.fullpath,'DV')
      #     dve = self.read_data('DV',ExtraInput)['data']
      #     # zmesh = ep.data(self.fullpath,'ZMESH')
      #     zmesh = self.read_data('ZMESH',ExtraInput)['data']
      #     # den5 = ep.data(self.fullpath,'DENZ05')
      #     try:
      #       den5 = self.read_data('DENZ05',ExtraInput)['data']
      #       # den6 = ep.data(self.fullpath,'DENZ06')
      #       den6 = self.read_data('DENZ06',ExtraInput)['data']
      #       # den7 = ep.data(self.fullpath,'DENZ07')
      #       den7 = self.read_data('DENZ07',ExtraInput)['data']
      #       # den8 = ep.data(self.fullpath,'DENZ08')
      #       den8 = self.read_data('DENZ08',ExtraInput)['data']
      #       # den9 = ep.data(self.fullpath,'DENZ09')
      #       den9 = self.read_data('DENZ09',ExtraInput)['data']
      #       # den10 = ep.data(self.fullpath,'DENZ10')
      #       den10 = self.read_data('DENZ10',ExtraInput)['data']
      #       # den11 = ep.data(self.fullpath,'DENZ11')
      #       den11 = self.read_data('DENZ11',ExtraInput)['data']
      #     except:
      #       den5,den6,den7,den8,den9,de10,den11=0,0,0,0,0,0,0

      dentot = den5+den6+den7+den8+den9+den10+den11
      out=np.sum(dentot*dve)
      return out
###############################################
  #def read_imp_content_core(self,coreindex,CF,ExtraInput):
  # def read_imp_content_core(self):
  #     #densum=0
  #     #index=coreindex-CF
  #     # dv = ep.data(self.fullpath,'DV')dv = dv.(3)
  #       dv = dv[0:index]
  #
  #     if ExtraInput is None:
  #
  #     else:
  #     dve = self.read_data('DV',ExtraInput)['data']
  #     # zmesh = ep.data(self.fullpath,'ZMESH')
  #     zmesh = read_data(self,'ZMESH',ExtraInput)['data']
  #     # den5 = ep.data(self.fullpath,'DENZ05')
  #     try:
  #       den5 = read_data(self,'DENZ05',ExtraInput)['data']
  #       # den6 = ep.data(self.fullpath,'DENZ06')
  #       den6 = read_data(self,'DENZ06',ExtraInput)['data']
  #       # den7 = ep.data(self.fullpath,'DENZ07')
  #       den7 = read_data(self,'DENZ07',ExtraInput)['data']
  #       # den8 = ep.data(self.fullpath,'DENZ08')
  #       den8 = read_data(self,'DENZ08',ExtraInput)['data']
  #       # den9 = ep.data(self.fullpath,'DENZ09')
  #       den9 = read_data(self,'DENZ09',ExtraInput)['data']
  #       # den10 = ep.data(self.fullpath,'DENZ10')
  #       den10 = read_data(self,'DENZ10',ExtraInput)['data']
  #       # den11 = ep.data(self.fullpath,'DENZ11')
  #       den11 = read_data(self,'DENZ11',ExtraInput)['data']
  #     except:
  #       den5,den6,den7,den8,den9,de10,den11=0,0,0,0,0,0,0
  #
  #     dentot = den5+den6+den7+den8+den9+den10+den11
  #     out=np.sum(dentot*dve)
  #     return out
###############################################
  def read_n2(self,region):
    """
    extract nitrogen concentration (imp2)
    """
    try:
      for i in range(5,12):#ionisation states considered
          if i < 10:
              emid = ep.row(self.fullpath,'DENZ0'+str(i),region)
          else:
              emid = ep.row(self.fullpath,'DENZ'+str(i),region)
          row = emid.xData
          idx = np.argmin(np.abs(np.asarray(row) - 0))
          # ind = ind+1
          values = emid.yData
          output = output+values[idx+1]
    except:
      output = 0
    return output
###############################################
  def read_e(self):
    """
    extract electron concentration (imp2)
    """
    # if ExtraInput is None:
    dv = ep.data(self.fullpath,'DV').data
    # dve = self.read_data('DV', ExtraInput)['data']
    den = ep.data(self.fullpath,'DENEL').data
    # den = self.read_data('DENEL', ExtraInput)['data']
    # else:
    #     # dv = ep.data(self.fullpath,'DV')
    #     dve = self.read_data('DV',ExtraInput)['data']
    #     # den = ep.data(self.fullpath,'DENEL')
    #     den = self.read_data('DENEL',ExtraInput)['data']
    out=np.sum(den*dve)
    return out
###############################################
  def read_x_point(self):
    """
    extract atom, molecules, ionization, charge exchange, and recombination data close to x-point
    """
    da = ep.ring(self.fullpath,'DA','C01')
    da = da.yData
    dm = ep.ring(self.fullpath,'DM','C01')
    dm = dm.yData
    soun = ep.ring(self.fullpath,'SOUN','C01')
    soun = soun.yData
    cx = ep.ring(self.fullpath,'SQICX','C01')
    cx = cx.yData
    sirec = ep.ring(self.fullpath,'SIREC','C01')
    sirec = sirec.yData

    da = (da[0]+da[self.non_div_row+1])/2
    dm = (dm[0]+dm[self.non_div_row+1])/2
    soun = (soun[0]+soun[self.non_div_row+1])/2
    cx = (cx[0]+cx[self.non_div_row+1])/2
    sirec = (sirec[0]+sirec[self.non_div_row+1])/2

    return {'da':da,
          'dm':dm,
          'soun':soun,
          'cx':cx,
          'sirec':sirec}

###############################################
  def read_div_mol_atom_ratio(self):
    """
    extract atomic, molecular and neutral concentration
    returns ration atoms/(mol+ato)
    """
    # if ExtraInput is None:
    zmesh = ep.data(self.fullpath,'ZMESH').data
    # zmesh = self.read_data('ZMESH', ExtraInput)['data']
    dv = ep.data(self.fullpath,'DV').data
    # dv = self.read_data('DV', ExtraInput)['data']
    da=ep.data(self.fullpath,'DA').data
    # da = self.read_data('DA', ExtraInput)['data']
    dm=ep.data(self.fullpath,'DM').data
    # dm = self.read_data('DM', ExtraInput)['data']
    ta=ep.data(self.fullpath,'ENEUTA').data
    # ta = self.read_data('ENEUTA', ExtraInput)['data']
    tm= ep.data(self.fullpath,'ENEUTM').data
    # tm = self.read_data('ENEUTM', ExtraInput)['data']

    # else:
    #     # zmesh = ep.data(self.fullpath,'ZMESH')
    #     zmesh = self.read_data('ZMESH',ExtraInput)['data']
    #     # dv = ep.data(self.fullpath,'DV')
    #     dv = self.read_data('DV',ExtraInput)['data']
    #     # da=ep.data(self.fullpath,'DA')
    #     da = self.read_data('DA',ExtraInput)['data']
    #     # dm=ep.data(self.fullpath,'DM')
    #     dm = self.read_data('DM',ExtraInput)['data']
    #     # ta=ep.data(self.fullpath,'ENEUTA')
    #     ta = self.read_data('ENEUTA',ExtraInput)['data']
    #     # tm= ep.data(self.fullpath,'ENEUTM')
    #     tm= self.read_data('ENEUTM',ExtraInput)['data']



    dasum = 0
    pasum = 0
    dmsum = 0
    pmsum=0
    for i in range(0,self.npts_m):
        if self.zme[i] < 1.2:
            dasum = dasum+da[i]*dv[i]
            dmsum = dmsum+dm[i]*dv[i]
            pasum = pasum+da[i]*ta[i]*dv[i]
            pmsum = pmsum+dm[i]*tm[i]*dv[i]

    densityrat=dmsum/(dasum+dmsum)
    pressurerate= pmsum/(pasum+pmsum)


    return {'dasum':dasum,
      'pasum':pasum,
      'dmsum':dmsum,
      'pmsum':pmsum,
      'densityrat':densityrat,
      'pressurerate':pressurerate}
###############################################
  def read_sirec_soun_lfs(self):
    """
    function that extracts total ionization and total recombination
    """
    sumsoun = 0
    sumsirec = 0
    for j in range(1,self.pr_ring+1):
        # i= self.LHS_row - j
        if j > 9:
            ring = 'P'+str(j)
        if j < 10:
            ring = 'P0'+str(j)
        print(ring)
        soun = ep.ring(self.fullpath,'SOUN',ring)
        soun = soun.yData
        sirec = ep.ring(self.fullpath,'SIREC',ring)
        sirec = sirec.yData
        dv = ep.ring(self.fullpath,'DV',ring)
        dv = dv.yData
        sumsoun = sumsoun + np.sum(np.asarray(soun[0:self.RHS_row])*np.asarray(dv[0:self.RHS_row]))
        sumsirec = sumsirec + np.sum(np.asarray(sirec[0:self.RHS_row])*np.asarray(dv[0:self.RHS_row]))

    for j in range(1,self.sol_ring+1):
        # i= self.LHS_row - j
        if j > 9:
            ring = 'S'+str(j)
        if j < 10:
            ring = 'S0'+str(j)
        soun = ep.ring(self.fullpath,'SOUN',ring)
        soun = soun.yData
        sirec = ep.ring(self.fullpath,'SIREC',ring)
        sirec = sirec.yData
        dv = ep.ring(self.fullpath,'DV',ring)
        dv = dv.yData

        sumsoun = sumsoun + np.sum(np.asarray(soun[0:self.RHS_row])*np.asarray(dv[0:self.RHS_row]))
        sumsirec = sumsirec + np.sum(np.asarray(sirec[0:self.RHS_row])*np.asarray(dv[0:self.RHS_row]))

    # for j in range(1,self.core_ring):
    # 	# i= self.LHS_row - j
    # 	if j > 9:
    # 		ring = 'C'+str(i)
    # 	if j < 10:
    # 		ring = 'C0'+str(i)
    # 	soun = ep.ring(self.fullpath,'SOUN',ring)
    # 	soun = soun.yData
    # 	sirec = ep.ring(self.fullpath,'SIREC',ring)
    # 	sirec = sirec.yData
    # 	dv = ep.ring(self.fullpath,'DV',ring)
    # 	dv = dv.yData
    # 	sumsoun = sumsoun + np.sum(soun(0:21)*dv(0:21))
    #  	sumsirec = sumsirec + np.sum(sirec(0:21)*dv(0:21))



    return {'sumsoun':sumsoun,
            'sumsirec':sumsirec}

# ###############################################
#   def read_power_balance(self):
#     """
#     reads print file and return power balance
#
#     TBD:
#     this should be converted in a static method and have as input a list of simulations
#     """
#     if (self.fullpath[len(self.fullpath)-4:len(self.fullpath)] == "tran"):
#         ffile = self.fullpath[0:len(self.fullpath)-5]
#
#     #  and add tran again
#         prt = 'print'
#         file = ffile+'/'+prt
#         text1 = ' POWER & PARTICLE GLOBAL CONSERVATION :-'
#         with open(file) as f:
#             lines = f.readlines()
#             for index, line in enumerate(lines):
#                 if text1 in str(line):
#                     dummy=lines[index+4].split()
#                     # #print(dummy)
#                     pinion=float(dummy[2])*1.e6
#                     pinelectron=float(dummy[3])*1.e6
#                     info=lines[index+5].split()
#
#
#                     pvesion = -float(info[4])
#                     pveselectron = -float(info[5])
#                     pvesrec = -float(info[7])
#                     info=lines[index+20].split()
#                     piti = -float(info[4])
#                     pite = -float(info[5])
#                     pitrec = -float(info[7])
#                     info=lines[index+23].split()
#                     # #print(info)
#                     poti = -float(info[4])
#                     pote = -float(info[5])
#                     potrec = -float(info[7])
#
#             text1 = 'ION POWER BALANCE BY MACRO-ZONE :-'
#             for index, line in enumerate(lines):
#                             if text1 in str(line):
#                                 info=lines[index+4].split()
#                                 pi_core_ioniz = -float(info[5])
#                                 pi_core_molec = -float(info[6])
#                                 pi_core_CX = -float(info[7])
#                                 pi_core_rec = -float(info[8])
#                                 # #print(pi_core_ioniz,pi_core_molec,pi_core_CX,pi_core_rec)
#                                 info=lines[index+5].split()
#                                 # print(info)
#
#                                 pi_ms_ioniz = -float(info[5])
#                                 pi_ms_molec = -float(info[6])
#                                 pi_ms_CX = -float(info[7])
#                                 pi_ms_rec = -float(info[8])
#                                 info=lines[index+6].split()
#                                 pi_ods_ioniz = -float(info[5])
#                                 pi_ods_molec = -float(info[6])
#                                 pi_ods_CX = -float(info[7])
#                                 pi_ods_rec = -float(info[8])
#                                 info=lines[index+7].split()
#                                 pi_ids_ioniz = -float(info[5])
#                                 pi_ids_molec = -float(info[6])
#                                 pi_ids_CX = -float(info[7])
#                                 pi_ids_rec = -float(info[8])
#                                 info=lines[index+8].split()
#                                 pi_opfr_ioniz = -float(info[5])
#                                 pi_opfr_molec = -float(info[6])
#                                 pi_opfr_CX = -float(info[7])
#                                 pi_opfr_rec = -float(info[8])
#                                 info=lines[index+9].split()
#                                 # #print(pi_opfr_ioniz,pi_opfr_molec,pi_opfr_CX,pi_opfr_rec)
#                                 pi_ipfr_ioniz = -float(info[5])
#                                 pi_ipfr_molec = -float(info[6])
#                                 pi_ipfr_CX = -float(info[7])
#                                 pi_ipfr_rec = -float(info[8])
#                                 info=lines[index+24].split()
#                                 # print(info)
#                                 psepi = -float(info[3])
#                                 info=lines[index+25].split()
#                                 podi=-float(info[4])
#                                 pidi=-float(info[5])
#                                 # print(pidi,podi,psepi)
#
#
#             text1 = 'ELECTRON POWER BALANCE BY MACRO-ZONE :-'
#             for index, line in enumerate(lines):
#                             if text1 in str(line):
#                                 info=lines[index+4].split()
#
#                                 prad_core = -float(info[2])
#                                 pation_core=-float(info[5])
#                                 pmoldis_core=-float(info[6])
#                                 phrad_core=-float(info[7])
#                                 info=lines[index+5].split()
#                                 prad_ms = -float(info[2])
#                                 pation_ms=-float(info[5])
#                                 pmoldis_ms=-float(info[6])
#                                 phrad_ms=-float(info[7])
#                                 info=lines[index+6].split()
#                                 prad_ods = -float(info[2])
#                                 pation_ods=-float(info[5])
#                                 pmoldis_ods=-float(info[6])
#                                 phrad_ods=-float(info[7])
#                                 info=lines[index+7].split()
#                                 prad_ids = -float(info[2])
#                                 pation_ids=-float(info[5])
#                                 pmoldis_ids=-float(info[6])
#                                 phrad_ids=-float(info[7])
#                                 info=lines[index+8].split()
#                                 prad_opfr = -float(info[2])
#                                 pation_opfr=-float(info[5])
#                                 pmoldis_opfr=-float(info[6])
#                                 phrad_opfr=-float(info[7])
#                                 info=lines[index+9].split()
#                                 prad_ipfr = -float(info[2])
#                                 pation_ipfr=-float(info[5])
#                                 pmoldis_ipfr=-float(info[6])
#                                 phrad_ipfr=-float(info[7])
#                                 info=lines[index+24].split()
#                                 psepe = -float(info[3])
#                                 info=lines[index+25].split()
#                                 pode = -float(info[4])
#                                 pide = -float(info[5])
#                                 # print(pode,pide,psepe)
#         #
#         #
#         #
#         powbalancearr = np.zeros(56)
#         powbalancearr[0]=pinion
#         powbalancearr[1]=pinelectron
#         powbalancearr[2]=psepi
#         powbalancearr[3]=psepe
#         powbalancearr[4]=pvesion
#         powbalancearr[5]=pveselectron
#         powbalancearr[6]=pvesrec
#         powbalancearr[7]=poti
#         powbalancearr[8]=pote
#         powbalancearr[9]=potrec
#         powbalancearr[10]=piti
#         powbalancearr[11]=pite
#         powbalancearr[12]=pitrec
#         powbalancearr[13]=podi
#         powbalancearr[14]=pode
#         powbalancearr[15]=pidi
#         powbalancearr[16]=pide
#
#         powbalancearr[17]=pi_core_ioniz
#         powbalancearr[18]=pi_core_molec
#         powbalancearr[19]=pi_core_CX
#         powbalancearr[20]=pi_core_rec
#
#         powbalancearr[21]=pi_ms_ioniz
#         powbalancearr[22]=pi_ms_molec
#         powbalancearr[23]=pi_ms_CX
#         powbalancearr[24]=pi_ms_rec
#
#         powbalancearr[25]=pi_ods_ioniz + pi_opfr_ioniz
#         powbalancearr[26]=pi_ods_molec + pi_opfr_molec
#         powbalancearr[27]=pi_ods_CX + pi_opfr_CX
#         powbalancearr[28]=pi_ods_rec + pi_opfr_rec
#
#         powbalancearr[29]=pi_ids_ioniz + pi_ipfr_ioniz
#         powbalancearr[30]=pi_ids_molec + pi_ipfr_molec
#         powbalancearr[31]=pi_ids_CX + pi_ipfr_CX
#         powbalancearr[32]=pi_ids_rec + pi_ipfr_rec
#
#         powbalancearr[33]=prad_core
#         powbalancearr[34]=pation_core
#         powbalancearr[35]=pmoldis_core
#         powbalancearr[36]=phrad_core
#
#         powbalancearr[37]=prad_ms
#         powbalancearr[38]=pation_ms
#         powbalancearr[39]=pmoldis_ms
#         powbalancearr[40]=phrad_ms
#
#         powbalancearr[41]=prad_ods + prad_opfr
#         powbalancearr[42]=pation_ods + pation_opfr
#         powbalancearr[43]=pmoldis_ods + pmoldis_opfr
#         powbalancearr[44]=phrad_ods + phrad_opfr
#
#
#         powbalancearr[45]=prad_ids + prad_ipfr
#         powbalancearr[46]=pation_ids + pation_ipfr
#         powbalancearr[47]=pmoldis_ids + pmoldis_ipfr
#         powbalancearr[48]=phrad_ids + phrad_ipfr
#
#
#         hrad=powbalancearr[48]+powbalancearr[44]+powbalancearr[40]+powbalancearr[36]
#         ion_ioniz=powbalancearr[29]+powbalancearr[25]+powbalancearr[21]+powbalancearr[17]
#         ele_ioniz=powbalancearr[46]+powbalancearr[42]+powbalancearr[38]+powbalancearr[34]
#         ion_molec=powbalancearr[18]+powbalancearr[22]+powbalancearr[26]+powbalancearr[30]
#         ele_molec=powbalancearr[35]+powbalancearr[39]+powbalancearr[43]+powbalancearr[47]
#         ion_ch_ex=powbalancearr[31]+powbalancearr[27]+powbalancearr[23]+powbalancearr[19]
#         p_rad    =powbalancearr[33]+powbalancearr[37]+powbalancearr[41]+powbalancearr[45]
#
#         powbalancearr[49]=hrad
#         powbalancearr[50]=ion_ioniz
#         powbalancearr[51]=ele_ioniz
#         powbalancearr[52]=ion_molec
#         powbalancearr[53]=ele_molec
#         powbalancearr[54]=ion_ch_ex
#         powbalancearr[55]=p_rad
#
#
#         result = OrderedDict()
#         result['pinion']=pinion
#         result['pinelectron']=pinelectron
#         result['psepi']=psepi
#         result['psepe']=psepe
#         result['pvesion']=pvesion
#         result['pveselectron']=pveselectron
#         result['pvesrec']=pvesrec
#         result['poti']=poti
#         result['pote']=pote
#         result['potrec']=potrec
#         result['piti']=piti
#         result['pite']=pite
#         result['pitrec']=pitrec
#         result['podi']=podi
#         result['pode']=pode
#         result['pidi']=pidi
#         result['pide']=pide
#         result['pi_core_ioniz']=pi_core_ioniz
#         result['pi_core_molec']=pi_core_molec
#         result['pi_core_CX']=pi_core_CX
#         result['pi_core_rec']=pi_core_rec
#         result['pi_ms_ioniz']=pi_ms_ioniz
#         result['pi_ms_molec']=pi_ms_molec
#         result['pi_ms_CX']=pi_ms_CX
#         result['pi_ms_rec']=pi_ms_rec
#         result['pi_od_ioniz']=pi_ods_ioniz+pi_opfr_ioniz
#         result['pi_od_molecc']=pi_ods_molec+pi_opfr_molec
#         result['pi_od_CX']=pi_ods_CX+pi_opfr_CX
#         result['pi_od_rec']=pi_ods_rec+pi_opfr_rec
#         result['pi_id_ioniz']=pi_ids_ioniz+pi_ipfr_ioniz
#         result['pi_id_molec']=pi_ids_molec+pi_ipfr_molec
#         result['pi_id_CX']=pi_ids_CX+pi_ipfr_CX
#         result['pi_id_rec']=pi_ids_rec+pi_ipfr_rec
#         result['pi_opfr_ioniz']=pi_opfr_ioniz
#         result['pi_opfr_molecc']=pi_opfr_molec
#         result['pi_opfr_CX']=pi_opfr_CX
#         result['pi_opfr_rec']=pi_opfr_rec
#         result['pi_ipfr_ioniz']=pi_ipfr_ioniz
#         result['pi_ipfr_molec']=pi_ipfr_molec
#         result['pi_ipfr_CX']=pi_ipfr_CX
#         result['pi_ipfr_rec']=pi_ipfr_rec
#         result['pi_ods_ioniz']=pi_ods_ioniz
#         result['pi_ods_molecc']=pi_ods_molec
#         result['pi_ods_CX']=pi_ods_CX
#         result['pi_ods_rec']=pi_ods_rec
#         result['pi_ids_ioniz']=pi_ids_ioniz
#         result['pi_ids_molec']=pi_ids_molec
#         result['pi_ids_CX']=pi_ids_CX
#         result['pi_ids_rec']=pi_ids_rec
#         result['prad_core']=prad_core
#         result['pation_core']=pation_core
#         result['pmoldis_core']=pmoldis_core
#         result['phrad_core']=phrad_core
#         result['prad_ms']=prad_ms
#         result['pation_ms']=pation_ms
#         result['pmoldis_ms']=pmoldis_ms
#         result['phrad_ms']=phrad_ms
#         result['prad_od']=prad_ods+prad_opfr
#         result['pation_od']=pation_ods+pation_opfr
#         result['pmoldis_od']=pmoldis_ods+pmoldis_opfr
#         result['phrad_od']=phrad_ods+phrad_opfr
#         result['prad_id']=prad_ids+prad_ipfr
#         result['pation_id']=pation_ids+pation_ipfr
#         result['pmoldis_id']=pmoldis_ids+pmoldis_ipfr
#         result['phrad_id']=phrad_ids+phrad_ipfr
#         result['prad_ods']=prad_ods
#         result['pation_ods']=pation_ods
#         result['pmoldis_ods']=pmoldis_ods
#         result['phrad_ods']=phrad_ods
#         result['prad_ids']=prad_ids
#         result['pation_ids']=pation_ids
#         result['pmoldis_ids']=pmoldis_ids
#         result['phrad_ids']=phrad_ids
#         result['prad_opfr']=prad_opfr
#         result['pation_opfr']=pation_opfr
#         result['pmoldis_opfr']=pmoldis_opfr
#         result['phrad_opfr']=phrad_opfr
#         result['prad_ipfr']=prad_ipfr
#         result['pation_ipfr']=pation_ipfr
#         result['pmoldis_ipfr']=pmoldis_ipfr
#         result['phrad_ipfr']=phrad_ipfr
#         result['hrad']=hrad
#         result['ion_ioniz']=ion_ioniz
#         result['ele_ioniz']=ele_ioniz
#         result['ion_molec']=ion_molec
#         result['ele_molec']=ele_molec
#         result['ion_ch_ex']=ion_ch_ex
#         result['p_rad']=p_rad
#
#         return result
# ###############################################
#   @staticmethod
#   def write_powerbalance2file(simu_list,path,filename):
#     """
#     writes to file the output of read_power_balance, it takes as input a list of simulations
#     """
#     with open(path+'/'+filename+'_power.csv', 'w') as f:  # Just use 'w' mode in 3.x
#       simu=simu_list[0][0]
#       result=simu.read_power_balance()
#       w = csv.DictWriter(f, result.keys(), delimiter='\t')
#       w.writeheader()
#     with open(path+'/'+filename+'.csv', 'a') as f:  # Just use 'w' mode in 3.x
#       writer = csv.writer(f, delimiter='\t')
#       for index1 in range(0,len(simu_list)):
#         simu=simu_list[index1][0]
#         #print(simu)
#         result=simu.read_power_balance()
#         writer.writerow(result.values())
#
#     f.close()
#     print('power balance written to ... ', path+'/'+filename+'_power.csv')

###############################################

###############################################
  def read_profiles(self,Region,tran=None):
    """
    reads outer mid plane data
printf,lun4,format='(A)',' psi_omp dsrad_omp dsrad_face_omp  ds_omp r_omp z_omp hrho_omp sh_omp bfi_omp jpar_omp jpari_omp jtarg_omp jtargi_omp gam_omp gamro_omp gamroe_omp pflxd_omp denel_omp te_omp ti_omp vi_omp mach_omp da_omp dm_omp dha_omp soun_omp sirec_omp pre_omp preel_omp prestat_omp pretot_omp qeflxd_omp qiflxd_omp qepcd_omp qepcdd_omp qepcv_omp qipcd_omp qipcdd_omp qipcv_omp qpare_omp qpari_omp qpartot_omp denpe_omp denpi_omp totpden_omp dperp_omp chii_omp chie_omp'

    """


    # if ExtraInput is None:
    if tran is None:
        pass
    else:
        self.fullpath = self.fullpath+str(tran)

    ade = ep.row(self.fullpath,'DENEL', Region)
    adi = ep.row(self.fullpath,'DEN', Region)
    asoun = ep.row(self.fullpath,'SOUN', Region)
    asirec = ep.row(self.fullpath,'SIREC', Region)
    psi = ep.row(self.fullpath,'PSI', Region)
    ate = ep.row(self.fullpath,'TEVE', Region)
    ati = ep.row(self.fullpath,'TEV', Region)
    apot = ep.row(self.fullpath,'POT', Region)
    rsepx = ep.row(self.fullpath,'RSEPX', Region)
    pre = ep.row(self.fullpath,'PRE', Region)
    preel = ep.row(self.fullpath,'PREEL', Region)
    pretot = ep.row(self.fullpath,'PREHYD', Region)
    prestat = ep.row(self.fullpath,'PRETOT', Region)
    vpi = ep.row(self.fullpath,'VPI', Region)
    vpe = ep.row(self.fullpath,'VPE', Region)
    mach = ep.row(self.fullpath,'PMACH', Region)
    pflxd = ep.row(self.fullpath,'PFLXD', Region)
    agamroe = ep.row(self.fullpath,'GAMROE', Region)
    jpar = ep.row(self.fullpath,'JPAR', Region)
    jpari = ep.row(self.fullpath,'JPARI', Region)
    jtarg = ep.row(self.fullpath,'JTARG', Region)
    jtargi = ep.row(self.fullpath,'JTARGI', Region)
    agam = ep.row(self.fullpath,'GAM', Region)
    agamro = ep.row(self.fullpath,'GAMRO', Region)
    ada = ep.row(self.fullpath,'DA', Region)
    adm = ep.row(self.fullpath,'DM', Region)
    adha = ep.row(self.fullpath,'DHA', Region)
    qeflxd = ep.row(self.fullpath,'QEFLXD', Region)
    qepcd = ep.row(self.fullpath,'QEPCD', Region)
    qepcdd = ep.row(self.fullpath,'QEPCDD', Region)
    qepcv = ep.row(self.fullpath,'QEPCV', Region)
    qiflxd = ep.row(self.fullpath,'QIFLXD', Region)
    qipcd = ep.row(self.fullpath,'QIPCD', Region)
    qipcdd = ep.row(self.fullpath,'QIPCDD', Region)
    qipcv = ep.row(self.fullpath,'QIPCV', Region)
    bfi = ep.row(self.fullpath,'BFI', Region)
    sh = ep.row(self.fullpath,'SH', Region)
    rmesh = ep.row(self.fullpath,'RMESH', Region)
    zmesh = ep.row(self.fullpath,'ZMESH', Region)
    hrho = ep.row(self.fullpath,'HRHO', Region)
    dperp = ep.row(self.fullpath,'DPERP', Region)
    chii = ep.row(self.fullpath,'CHII', Region)
    chie = ep.row(self.fullpath,'CHIE', Region)
    denpe = ep.row(self.fullpath,'DENPE', Region)
    denpi = ep.row(self.fullpath,'DENPI', Region)
    totpden = ep.row(self.fullpath,'TOTPDEN', Region)
    qpare = ep.row(self.fullpath,'QPARE', Region)
    qpari = ep.row(self.fullpath,'QPARI', Region)
    qpartot = ep.row(self.fullpath,'QPARTOT', Region)

    # arcx=ep.row(self.fullpath,'RCX',Region)
    # asqicx=ep.row(self.fullpath,'SQICX',Region)
    # aripg=ep.row(self.fullpath,'RIPG',Region)
    # ava0r=ep.row(self.fullpath,'VA0R',Region)
    # aeneuta=ep.row(self.fullpath,'ENEUTA',Region)

    # aqeflxl=ep.row(self.fullpath,'QEFLXL',Region)
    # aqiflxl=ep.row(self.fullpath,'QIFLXL',Region)
    # aqeflxd=ep.row(self.fullpath,'QEFLXD',Region)
    # aqiflxd=ep.row(self.fullpath,'QIFLXD',Region)
    # apflxd=ep.row(self.fullpath,'PFLXD',Region)
    #
    # aqirocdl=ep.row(self.fullpath,'QIROCDL',Region)
    # aqirocvl=ep.row(self.fullpath,'QIROCVL',Region)
    # aqerocdl=ep.row(self.fullpath,'QEROCDL',Region)
    # aqerocvl=ep.row(self.fullpath,'QEROCVL',Region)
    # else:
    #     ade=self.read_row_data('DENEL',Region,ExtraInput)
    #     adi=self.read_row_data('DEN',Region, ExtraInput)
    #     asoun=self.read_row_data('SOUN',Region, ExtraInput)
    #     asirec=self.read_row_data('SIREC',Region, ExtraInput)
    #     psi=self.read_row_data('PSI',Region, ExtraInput)
    #     ate=self.read_row_data('TEVE',Region, ExtraInput)
    #     ati=self.read_row_data('TEV',Region, ExtraInput)
    #     apot=self.read_row_data('POT',Region, ExtraInput)
    #     rsepx=self.read_row_data('RSEPX',Region, ExtraInput)
    #     pre=self.read_row_data('PRE',Region, ExtraInput)
    #     preel=self.read_row_data('PREEL',Region, ExtraInput)
    #     pretot=self.read_row_data('PREHYD',Region, ExtraInput)
    #     prestat=self.read_row_data('PRETOT',Region, ExtraInput)
    #     vpi=self.read_row_data('VPI',Region, ExtraInput)
    #     vpe=self.read_row_data('VPE',Region, ExtraInput)
    #     mach=self.read_row_data('PMACH',Region, ExtraInput)
    #     pflxd = self.read_row_data( 'PFLXD', Region, ExtraInput)
    #     agamroe=self.read_row_data('GAMROE',Region, ExtraInput)
    #     jpar=self.read_row_data('JPAR',Region, ExtraInput)
    #     jpari=self.read_row_data('JPARI',Region, ExtraInput)
    #     jtarg=self.read_row_data('JTARG',Region, ExtraInput)
    #     jtargi=self.read_row_data('JTARGI',Region, ExtraInput)
    #     agam=self.read_row_data('GAM',Region, ExtraInput)
    #     agamro=self.read_row_data('GAMRO',Region, ExtraInput)
    #     ada=self.read_row_data('DA',Region, ExtraInput)
    #     adm=self.read_row_data('DM',Region, ExtraInput)
    #     adha = self.read_row_data('DHA', Region, ExtraInput)
    #     qeflxd=self.read_row_data('QEFLXD',Region, ExtraInput)
    #     qepcd=self.read_row_data('QEPCD',Region, ExtraInput)
    #     qepcdd=self.read_row_data('QEPCDD',Region, ExtraInput)
    #     qepcv=self.read_row_data('QEPCV',Region, ExtraInput)
    #     qiflxd=self.read_row_data('QIFLXD',Region, ExtraInput)
    #     qipcd=self.read_row_data('QIPCD',Region, ExtraInput)
    #     qipcdd=self.read_row_data('QIPCDD',Region, ExtraInput)
    #     qipcv=self.read_row_data('QIPCV',Region, ExtraInput)
    #     bfi=self.read_row_data('BFI',Region, ExtraInput)
    #     sh=self.read_row_data('SH',Region, ExtraInput)
    #     rmesh=self.read_row_data('RMESH',Region, ExtraInput)
    #     zmesh=self.read_row_data('ZMESH',Region, ExtraInput)
    #     hrho=self.read_row_data('HRHO',Region, ExtraInput)
    #     dperp = self.read_row_data('DPERP',Region, ExtraInput)
    #     chii = self.read_row_data('CHII',Region, ExtraInput)
    #     chie = self.read_row_data('CHIE',Region, ExtraInput)
    #     denpe=self.read_row_data('DENPE',Region, ExtraInput)
    #     denpi=self.read_row_data('DENPI',Region, ExtraInput)
    #     totpden=self.read_row_data('TOTPDEN',Region, ExtraInput)
    #     qpare=self.read_row_data('QPARE',Region, ExtraInput)
    #     qpari=self.read_row_data('QPARI',Region, ExtraInput)
    #     qpartot=self.read_row_data('QPARTOT',Region, ExtraInput)
    #
    #     # arcx=self.read_row_data('RCX',Region, ExtraInput)
    #     # asqicx=self.read_row_data('SQICX',Region, ExtraInput)
    #     # aripg=self.read_row_data('RIPG',Region, ExtraInput)
    #     # ava0r=self.read_row_data('VA0R',Region, ExtraInput)
    #     # aeneuta=self.read_row_data('ENEUTA',Region, ExtraInput)
    #
    #     # aqeflxl=self.read_row_data('QEFLXL',Region, ExtraInput)
    #     # aqiflxl=self.read_row_data('QIFLXL',Region, ExtraInput)
    #     # aqeflxd=self.read_row_data('QEFLXD',Region, ExtraInput)
    #     # aqiflxd=self.read_row_data('QIFLXD',Region, ExtraInput)
    #     # apflxd=self.read_row_data('PFLXD',Region, ExtraInput)
    #     #
    #     # aqirocdl=self.read_row_data('QIROCDL',Region, ExtraInput)
    #     # aqirocvl=self.read_row_data('QIROCVL',Region, ExtraInput)
    #     # aqerocdl=self.read_row_data('QEROCDL',Region, ExtraInput)
    #     # aqerocvl=self.read_row_data('QEROCVL',Region, ExtraInput)
    # ds=np.zeros(len(rmesh['xData']))
    # for i in range(1,len(rmesh['xData'])-1)  :
    #     ds[i] = ds[i - 1] + 0.5 * (sqrt((zmesh['yData'][i - 1] -
    #     zmesh['yData'][i]) ** 2. +
    #     (rmesh['yData'][i - 1] -
    #     rmesh['yData'][i]) ** 2.) +
    #     sqrt((zmesh['yData'][i + 1] -
    #     zmesh['yData'][i]) ** 2. +
    #     (rmesh['yData'][i + 1] -
    #     rmesh['yData'][i]) ** 2.))
    #
    # npts = len(ade['xData'])
    # dsrad = ade['xData'][0:npts]
    ds=np.zeros(len(rmesh.xData))
    for i in range(1,len(rmesh.xData)-1)  :
        ds[i] = ds[i - 1] + 0.5 * (sqrt((zmesh.yData[i - 1] -
        zmesh.yData[i]) ** 2. +
        (rmesh.yData[i - 1] -
        rmesh.yData[i]) ** 2.) +
        sqrt((zmesh.yData[i + 1] -
        zmesh.yData[i]) ** 2. +
        (rmesh.yData[i + 1] -
        rmesh.yData[i]) ** 2.))

    npts = len(ade.xData)
    dsrad = ade.xData[0:npts]
    dsrad_face = np.zeros(npts)
    dsrad_face[0] = dsrad[0] - 0.5 * (dsrad[0] - 0.)


    return{'dsrad':dsrad,'dsrad_face':dsrad_face,'ds':ds,
        'ade'    :ade,
           'adi'    :adi,
            'asoun'  :  asoun,
            'asirec'  :  asirec,
            'psi'    :psi,
    'ate'    :ate,
    'ati'    :ati,
    'apot'   : apot,
    'rsepx'  :  rsepx,
    'pre'    :pre,
    'preel'  :  preel,
    'pretot' :   pretot,
    'prestat':    prestat,
    'vpi'    :vpi,
    'vpe'    :vpe,
    'mach'   : mach,
    'pflxd'  :  pflxd,
    'agamroe':    agamroe,
    'jpar'   : jpar,
    'jpari'  :  jpari,
    'jtarg'  :  jtarg,
    'jtargi' :   jtargi,
    'agam'   : agam,
    'agamro' :   agamro,
    'ada'    :ada,
    'adm'    :adm,
    'adha'   : adha,
    'qeflxd' :   qeflxd,
    'qepcd'  :  qepcd,
    'qepcdd' :   qepcdd,
    'qepcv'  :  qepcv,
    'qiflxd' :   qiflxd,
    'qipcd'  :  qipcd,
    'qipcdd' :   qipcdd,
    'qipcv'  :  qipcv,
    'bfi'    :bfi,
    'sh'    :sh,
    'rmesh'  :  rmesh,
    'zmesh'  :  zmesh,
    'hrho'   : hrho,
    'dperp'  :  dperp,
    'chii'   : chii,
    'chie'   : chie,
    'denpe'  :  denpe,
    'denpi'  :  denpi,
    'totpden':    totpden,
    'qpare'  :  qpare,
    'qpari'  :  qpari,
    'qpartot':    qpartot }
###############################################

  def read_profiles1(self,Region):


      names1 = ep.getnames(self.fullpath, 1)  # profile data
      names2 = ep.getnames(self.fullpath, 4)  # geometry data
      listnames = []
      for i in (range(names1.nNames)):
          listnames.append(names1.names[i].decode('utf-8').strip().lower())
      for i in (range(names2.nNames)):
          listnames.append(names2.names[i].decode('utf-8').strip().lower())

      for i in (range(len(listnames))):
          var = listnames[i]
          vars()[var] = ep.row(self.fullpath, var, Region)

      ds = np.zeros(len(vars()['rmesh'].xData))
      for i in range(1, len(vars()['rmesh'].xData) - 1):
          ds[i] = ds[i - 1] + 0.5 * (sqrt((vars()['zmesh'].yData[i - 1] -
                                           vars()['zmesh'].yData[i]) ** 2. +
                                          (vars()['rmesh'].yData[i - 1] -
                                           vars()['rmesh'].yData[i]) ** 2.) +
                                     sqrt((vars()['zmesh'].yData[i + 1] -
                                           vars()['zmesh'].yData[i]) ** 2. +
                                          (vars()['rmesh'].yData[i + 1] -
                                           vars()['rmesh'].yData[i]) ** 2.))

      npts = len(vars()['denel'].xData)
      dsrad = vars()['denel'].xData[0:npts]
      dsrad_face = np.zeros(npts)
      dsrad_face[0] = dsrad[0] - 0.5 * (dsrad[0] - 0.)

      result = OrderedDict()
      # result = dict()
      result['dsrad'] = dsrad
      result['dsrad_face'] = dsrad_face
      result['ds'] = ds
      for j in (range(len(listnames))):
          var = listnames[j]
          result[var] = vars()[var]



      return result

###############################################
  def read_neutflux(self,surface_in,surface_out):
    """
    before using this routine run
    /u/dharting/edge2d_scripts/perl/gen_e2deir_neutral_fluxes.perl  .
    /u/dharting/edge2d_scripts/perl/gen_e2deir_neutral_fluxes_Mol.perl  .
    in the simulation folder (catalogue)

    and store the information about the last closed core surfaces

    this routine reads the the neutral flux across the specified surfaces
    the output is then used by eirene_netcur

    """
    dirp=self.fullpath[0:-4]
#     ; ------------------------------------------------------------
# ; read in flux through inner flux surface
    fname='eirene_nondefaultsur' + str(surface_in) +'_neutflux.plt'
    # pwd=os.getcwd()
    # print(pwd)
    #os.chdir(dirp)
    # print(os.getcwd())
    lines= file_len(dirp+fname)
    # print(lines)
    ndata=lines-2
    r1_in=np.zeros(ndata)
    z1_in=np.zeros(ndata)
    r2_in=np.zeros(ndata)
    z2_in=np.zeros(ndata)
    neutcurrent_in=np.zeros(ndata)
    neutcurrent_in2=np.zeros(ndata)
    neutflux_in=np.zeros(ndata)
    neutflux_in2=np.zeros(ndata) #; impurity flux!
    spol_in=np.zeros(ndata)
    sy_in=np.zeros(ndata)
    dspol_in=np.zeros(ndata+1)
    # dspol_in[0]=0.0
    flag=0
    with open(dirp+fname) as f:
        lines = f.readlines()
        #len(lines)
        # for i, line in enumerate(ndata):
        for i in range(ndata):
            dummy=lines[i+2].split()
            # print(dummy[1],i)
            r1_in[i]=float(dummy[1])/100.  # convert to m
            z1_in[i]=float(dummy[2])/100.
            r2_in[i]=float(dummy[3])/100.
            z2_in[i]=float(dummy[4])/100.
            # print(r1_in[i])
            neutcurrent_in[i]=float(dummy[5]) / 1.602e-19 # in part/s
            # print(neutcurrent_in[i])
            if(len(dummy) == 7):
                flag = 1
                neutcurrent_in2[i]=float(dummy[6]) / 1.602e-19 # in part/s
                # print(neutcurrent_in2[i])
            else:
                neutcurrent_in2[i]=0

            spol_in[i]=sqrt((z2_in[i]-z1_in[i])**2+(r2_in[i]-r1_in[i])**2)
            # print(spol_in[i])
            sy_in[i]=spol_in[i]*2.*np.pi*(r1_in[i]+0.5*(r2_in[i]-r1_in[i]))
            dspol_in[i+1]=dspol_in[i]+sy_in[i]
            # print(dspol_in[i])
            # print(sy_in[i])
    # print(neutcurrent_in,sy_in)
    # print(spol_in)
    # print(np.asarray(neutcurrent_in)/np.asarray(sy_in))
    neutflux_in=np.asarray(neutcurrent_in)/np.asarray(sy_in)
    if(flag == 1):
        neutflux_in2=np.asarray(neutcurrent_in2)/np.asarray(sy_in)
    else:
        neutflux_in2=0

    dspol_in_norm=dspol_in / max(dspol_in)
    # print(dspol_in_norm)
    # print(dspol_in)

#     ; ------------------------------------------------------------
# ; read in flux through outer flux surface
    fname='eirene_nondefaultsur' + str(surface_out) +'_neutflux.plt'
    # pwd=os.getcwd()
    # os.chdir(dirp)
    lines= file_len(dirp+fname)
    # print(lines)
    ndata=lines-2
    r1_out=np.zeros(ndata)
    z1_out=np.zeros(ndata)
    r2_out=np.zeros(ndata)
    z2_out=np.zeros(ndata)
    neutcurrent_out=np.zeros(ndata)
    neutcurrent_out2=np.zeros(ndata)
    neutflux_out=np.zeros(ndata)
    neutflux_out2=np.zeros(ndata)
    spol_out=np.zeros(ndata)
    sy_out=np.zeros(ndata)
    dspol_out=np.zeros(ndata+1)
    # dspol_out[0]=0.0
    flag=0
    with open(dirp+fname) as f:
        lines = f.readlines()
    # 	# #print(lines)
        for i in range(ndata):
            dummy=lines[i+2].split()
            r1_out[i]=float(dummy[1])/100.  # convert to m
            z1_out[i]=float(dummy[2])/100.
            r2_out[i]=float(dummy[3])/100.
            z2_out[i]=float(dummy[4])/100.

            neutcurrent_out[i]=float(dummy[5]) / 1.602e-19 # in part/s
            if(len(dummy) > 6):
                flag = 1
                neutcurrent_out2[i]=float(dummy[6]) / 1.602e-19 # in part/s
            else:
                neutcurrent_out2[i]=0

            spol_out[i]=sqrt((z2_out[i]-z1_out[i])**2+
                            (r2_out[i]-r1_out[i])**2)
            sy_out[i]=spol_out[i]*2.*np.pi*(r1_out[i]+
                      0.5*(r2_out[i]-r1_out[i]))
            dspol_out[i+1]=dspol_out[i]+sy_out[i]
    # print(dspol_out)
    if(flag == 1):
        neutcurrent_out2_net=neutcurrent_out-neutcurrent_out2
    else:
        neutcurrent_out2_net=0
    neutflux_out=np.asarray(neutcurrent_out)/np.asarray(sy_out)
    # print(neutflux_out)
    if(flag == 1):
        neutflux_out2=np.asarray(neutcurrent_out2)/np.asarray(sy_out)
    else:
        neutflux_out2=0
    dspol_out_norm=dspol_out / max(dspol_out)

# ---------------------------------------------------------

    #os.chdir('/u/bviola/work/Python/EDGE2D')
#stop

    neutcurrent_net=neutcurrent_in-neutcurrent_out
    neutflux_net=neutflux_in-neutflux_out
    neutcurrent_net2=neutcurrent_in2-neutcurrent_out2
    neutflux_net2=neutflux_in2-neutflux_out2
    # print(neutcurrent_net)
    # print('')
    # print(neutflux_net)
    # print('')
    # print(neutcurrent_net2)
    # print('')
    # print(neutflux_net2)
    # print('')

    return{'r1_in':r1_in,'z1_in':z1_in,
        'r2_in':r2_in,'z2_in':z2_in,
        'sy_in':sy_in,'spol_in':spol_in,
        'dspol_in':dspol_in,'dspol_in_norm':dspol_in_norm,
        'neutcurrent_in':neutcurrent_in,
        'neutcurrent_in2':neutcurrent_in2,
        'neutflux_in':neutflux_in,
        'neutflux_in2':neutflux_in2,
        'r1_out':r1_out,'z1_out':z1_out,
        'r2_out':r2_out,'z2_out':z2_out,
        'sy_out':sy_out,'spol_out':spol_out,
        'dspol_out':dspol_out,'dspol_out_norm':dspol_out_norm,
        'neutcurrent_out':neutcurrent_out,
        'neutcurrent_out2':neutcurrent_out2,
        'neutflux_out':neutflux_out,
        'neutflux_out2':neutflux_out2,
        'neutcurrent_net':neutcurrent_net,
        'neutflux_net':neutflux_net,
        'neutcurrent_net2':neutcurrent_net2,
        'neutflux_net2':neutflux_net2 }
###############################################
  def eirene_netcur(self,surface_in, surface_out):

    """	pro write_eirene_neutcur,edge2d_cases,targetfilename, $
            surface_in, surface_out
          

    """
      # ; set constants
    ev=1.60217646e-19
    #print(surface_in, surface_out)
    # ; ------------------------------------------------------------------------
    # ; read in list of EDGE2D cases, create and fill structures




    # ; set up arrays for EGDE2D, then read in catalogue parameters
    omp=self.read_profiles('OMP')
    #
    #
    neut=self.read_neutflux(surface_in,surface_out)
    #
    #
    printfile=self.read_print_file_edge2d()



    # ; calculate separatrix and ranges for LP/IRTV
    xdata=omp['ate'].xData
    # iy_OMP_SOL=xdata[xdata > 0.0]

    iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)
    # print(iy_OMP_SOL)
    iy_sep_OMP=min(iy_OMP_SOL)
    iy_ny_OMP=max(iy_OMP_SOL)

    # ; -------------------------------------------------------------------------
    # ; calculate the total neutral current across the separatrix



    neutcurrent_in_tot=np.sum(neut['neutcurrent_in'])
    neutcurrent_in2_tot=np.sum(neut['neutcurrent_in2'])
    neutcurrent_in2_net_tot=np.sum(neut['neutcurrent_in2'])

    neutcurrent_out_tot=np.sum(neut['neutcurrent_out'])
    neutcurrent_out2_tot=np.sum(neut['neutcurrent_out2'])
    neutcurrent_out2_net_tot= np.sum(neut['neutcurrent_out2'])

    neutcurrent_net_tot=np.sum(neut['neutcurrent_net'])
    #




    name=str(self.owner)+'/'+str(self.shot)+'/'+str(self.date)+'/'+str(self.seq)
    return{'name':name,'pcoree':printfile['pcoree'],'pcorei':printfile['pcorei'],
                'pcore':printfile['pcoree']+printfile['pcorei'],
                'omp_ade_sep':omp['ade'].yData[iy_sep_OMP],
                'omp_adi_sep':omp['adi'].yData[iy_sep_OMP],
                'omp_ate_sep':omp['ate'].yData[iy_sep_OMP],
                'omp_ati_sep':omp['ati'].yData[iy_sep_OMP],
                'neutcurrent_in_tot':neutcurrent_in_tot,
                'neutcurrent_in2_tot':neutcurrent_in2_tot,
                'neutcurrent_in2_net_tot':neutcurrent_in2_net_tot,
                'neutcurrent_out_tot':neutcurrent_out_tot,
                'neutcurrent_out2_tot':neutcurrent_out2_tot,
                'neutcurrent_out2_net_tot':neutcurrent_out2_net_tot,
                'neutcurrent_net_tot':neutcurrent_net_tot}

###############################################
  @staticmethod
  def write_eirene_cur2file(simu_list,path,filename):
    """
    writes to file the output of eirene_netcur, it takes as input a list of simulations
    """
    #with open(path+'/'+filename+'.csv', 'w') as f:  # Just use 'w' mode in 3.x
      #simu=simu_list[0]
      #result=simu.eirene_netcur()
    ncol=19
    simu=simu_list[0]
    #print(dir(simu))
    surface_in=simu_list[0][1]
    # print(surface_in)
    surface_out=simu_list[0][2]
    # print(surface_out)
    # if simu_list[0][3] is None:
    #     ExtraInput = None
    # else:
    #     ExtraInput = simu_list[0][3]
    # print(ExtraInput)
      # ;ofile='eirene_neutcur_sep.dat'
      # ;targetfilename
    time=strftime("%Y-%m-%d", gmtime())
    with  open(path+'/'+filename+'_current.csv','wt') as ofile:
        writer = csv.writer(ofile, delimiter='\t')
        writer.writerow([str(ncol),filename,str(time)])
        writer.writerow([
            'Neutral current across: ',str(surface_in) ,str(surface_out)])
        writer.writerow(['n/a',
                'W','W','W',
                'm^-3','m^-3','eV','eV',
                'm^-3','m^-3','eV','eV',
                's-1','s-1','s-1',
                's-1','s-1','s-1',
                's-1'])

        writer.writerow([
            'EDGE2D',
            'pcore_e','pcore_i','pcore_tot',
            'ne_core','ni_core','Te_core','Ti_core',
            'ne_sep','ni_sep','Te_sep','Ti_sep',
            'I_neut_in','I_neut_in2',
            'I_neut_in_net2',
            'I_neut_out','I_neut_out2',
            'I_neut_out_net2',
            'I_neut_net'])
    with open(path+'/'+filename+'_current.csv', 'a') as f:  # Just use 'w' mode in 3.x
      writer = csv.writer(f, delimiter='\t')
      for index1 in range(0,len(simu_list)):
        simu=simu_list[index1][0]
        #print(simu)
        surface_in=simu_list[index1][1]
        #print(surface_in)
        surface_out=simu_list[index1][2]
        # if simu_list[index1][2] is None:
        #     ExtraInput = None
        # else:
        #     ExtraInput = simu_list[index1][3]
        result=simu.eirene_netcur(surface_in,surface_out)
        print(result['name'])
        writer.writerow([result['name'],result['pcoree'],result['pcorei'],
                result['pcore'],
                result['omp_ade_sep'],
                result['omp_adi_sep'],
                result['omp_ate_sep'],
                result['omp_ati_sep'],
                result['neutcurrent_in_tot'],
                result['neutcurrent_in2_tot'],
                result['neutcurrent_in2_net_tot'],
                result['neutcurrent_out_tot'],
                result['neutcurrent_out2_tot'],
                result['neutcurrent_out2_net_tot'],
                result['neutcurrent_net_tot']])








    f.close()

    print('Neutral currents across surfaces ', surface_in, surface_out,' written to ... ', path+'/'+filename+'_print.csv')

###############################################

  def read_eirene_pump(self):
    """
    function that reads eirene.output file
    extracting data related to the pumping surfaces

    returns a file containing
    total 
    atom and molecules incident and reemiteed fluxes
    """
    cwd=os.getcwd()
    #print(cwd)
    dirp=self.fullpath[0:-4]
    fname='eirene.output'
    print(dirp+fname)
    # os.chdir(dirp)
    # ----------------------------------------------------------------------------
    # read in fort.598 file to determine # of pump surfaces

    text =  '*  * pump surface'
    dummytext=' NO FLUXES INCIDENT ON THIS SURFACE'
    # n_pump = 0
    n_pump=count_string_occurrence(dirp+fname,text)


    print('# of pump surfaces: ',n_pump)


    # ----------------------------------------------------------------------------
    # define parameters
    surface_area=np.zeros(n_pump)
    d0_inc=np.zeros(n_pump)
    d2_inc=np.zeros(n_pump)
    d0_rem=np.zeros(n_pump)
    d2_rem=np.zeros(n_pump)
    total_atom=np.zeros(n_pump)
    removed_atom=np.zeros(n_pump)
    reemitted_atom=np.zeros(n_pump)
    # print('here1')
    #openr,lun,'fort.598', /get_lun

    #cd, dir
    #openr,lun,'fort.598', /get_lun
    index1 = 0
    with open(str(dirp+fname)) as f:
        lines = f.readlines()
        # print('here21')
        for index, line in enumerate(lines):
            # print(line)
            if text in str(line):
                # print(line)
                info=lines[index+6].split()
                # print(info)
                surface_area[index1] = float(info[3])
                if surface_area[index1] > 0:
                    # print(surface_area)
                    info=lines[index+11].split()
                    d0_inc[index1] = float(info[1])

                    info=lines[index+16].split()
                    d2_inc[index1] = float(info[1])

                    info=lines[index+21].split()
                    total_atom[index1] = float(info[1])

                    info=lines[index+27].split()
                    d0_rem[index1] = float(info[1])

                    info=lines[index+31].split()
                    darem = float(info[1])

                    info=lines[index+37].split()
                    d2_rem[index1] = float(info[1])

                    info=lines[index+41].split()
                    d2rem = float(info[1])
                    # print(d2rem,darem)
                    reemitted_atom[index1] = darem+d2rem
                    removed_atom[index1] = total_atom[index1] - reemitted_atom[index1]

                    index1 = index1 +1

                if dummytext in lines[index+8]:
                    # print('here')
                    d0_inc[index1] =0
                    d2_inc[index1] =0
                    total_atom[index1]=0
                    total_atom[index1]=0
                    d0_rem[index1]=0
                    darem=0
                    d2_rem[index1]=0
                    d2rem=0
                    print('NO FLUXES INCIDENT ON THIS SURFACE ', index1+1)
                    reemitted_atom[index1] = darem+d2rem
                    removed_atom[index1] = total_atom[index1] - reemitted_atom[index1]

                    index1 = index1 +1


    #stop
    # read in incident neutral fluxes







    return{'n_pump':n_pump, 'surface_area':surface_area,
          'd0_inc':d0_inc,
          'd0_rem':d0_rem,
          'd2_inc':d2_inc,
          'd2_rem':d2_rem,
          'total_atom':total_atom,
          'reemitted_atom':reemitted_atom,
          'removed_atom':removed_atom}
###############################################
  def eirene_pumpcur(self):
    """	 write_eirene_neutcur,edge2d_cases,targetfilename, $
                surface_in, surface_out

        uses read_eirene_pump function to extrac the total pumped current

    """
    # ; set constants
    ev=1.60217646e-19
    # print(surface_in, surface_out)
    # ; ------------------------------------------------------------------------
    # ; read in list of EDGE2D cases, create and fill structures




    # ; set up arrays for EGDE2D, then read in catalogue parameters
    omp=self.read_profiles('OMP')
    #
    #
    neut=self.read_eirene_pump()
    #
    #
    printfile=self.read_print_file_edge2d()



    # ; calculate separatrix and ranges for LP/IRTV
    xdata=omp['ate'].xData
    # iy_OMP_SOL=xdata[xdata > 0.0]

    iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)
    # print(iy_OMP_SOL)
    iy_sep_OMP=min(iy_OMP_SOL)
    iy_ny_OMP=max(iy_OMP_SOL)

    # ; -------------------------------------------------------------------------
    # ; calculate the total neutral current across the separatrix

    # form to total pumped flux for cross-comparison to PRINTFILE

    total_current=np.sum(neut['removed_atom']) / ev
    total_pump_area=np.sum(neut['surface_area']) /1.e4
    total_d0_inc=np.sum(neut['d0_inc'] / ev)
    total_d2_inc=np.sum(neut['d2_inc'] / ev)
    total_d0_rem=np.sum(neut['d0_rem'] / ev)
    total_d2_rem=np.sum(neut['d2_rem'] / ev)
    total_atom= np.sum(neut['total_atom'] / ev)
    total_reemitted_atom=  np.sum(neut['reemitted_atom']) / ev
# ; -------------------------------------------------------------------------
    # ; write results to -delimited file


    ncol=20
    name=str(self.owner)+'/'+str(self.shot)+'/'+str(self.date)+'/'+str(self.seq)
    print(str(name))
    # ;ofile='eirene_neutcur_sep.dat'
    # ;targetfilename


    return{'name':name,'pcoree':printfile['pcoree'],'pcorei':printfile['pcorei'],
          'pcore':printfile['pcoree']+printfile['pcorei'],
          'omp_ade_sep':omp['ade'].yData[iy_sep_OMP],
          'omp_adi_sep':omp['adi'].yData[iy_sep_OMP],
          'omp_ate_sep':omp['ate'].yData[iy_sep_OMP],
          'omp_ati_sep':omp['ati'].yData[iy_sep_OMP],
          'total_pump_area':total_pump_area,
          'total_d0_inc':total_d0_inc ,
          'total_d2_inc':total_d2_inc,
          'total_d0_rem':total_d0_rem ,
          'total_d2_rem':total_d2_rem ,
          'total_atom':total_atom,
          'total_reemitted_atom':total_reemitted_atom ,
          'total_current':total_current}



###############################################
  @staticmethod
  def write_pump_cur2file(simu_list,path,filename):
    """
    writes to file the output of eirene_pumpcur, it takes as input a list of simulations
    """
    #with open(path+'/'+filename+'.csv', 'w') as f:  # Just use 'w' mode in 3.x
      #simu=simu_list[0]
      #result=simu.eirene_pumpcur()
    ncol=20
      
      # ;ofile='eirene_neutcur_sep.dat'
      # ;targetfilename
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    with  open(path+'/'+filename+'_pump.csv','w') as ofile:
      writer = csv.writer(ofile, delimiter='\t')
      writer.writerow([str(ncol),filename,str(time)])
      writer.writerow([
        'Pump current across: '])
      writer.writerow(['n/a',
            'W','W','W',
            'm^-3','m^-3','eV','eV',
            'm^-3','m^-3','eV','eV',
            's-1','s-1','s-1',
            's-1','s-1','s-1',
            's-1'])

      writer.writerow([
        'EDGE2D',
        'pcore_e','pcore_i','pcore_tot',
        'ne_core','ni_core','Te_core','Ti_core',
        'ne_sep_e19','ni_sep','Te_sep','Ti_sep',
        'Asurf','I_H0_inc','I_H2_inc',
        'I_H0_rem','I_H2_rem',
        'I_tot_inc','I_tot_rem','I_tot_pump'])
    with open(path+'/'+filename+'_pump.csv', 'a') as f:  # Just use 'w' mode in 3.x
      writer = csv.writer(f, delimiter='\t')
      for index1 in range(0,len(simu_list)):      
        simu=simu_list[index1][0]
        ##print(simu['name'])
        # ExtraInput=simu_list[index1][1]
        #print(simu,ExtraInput)
        result=simu.eirene_pumpcur()
        #print(result.values())
        writer.writerow([result['name'],result['pcoree'],result['pcorei'],
                result['pcore'],
                result['omp_ade_sep'],
                result['omp_adi_sep'],
                result['omp_ate_sep'],
                result['omp_ati_sep'],
                result['total_pump_area'],
                result['total_d0_inc'],
                result['total_d2_inc'],
                result['total_d0_rem'],
                result['total_d2_rem'],
                result['total_atom'],
                result['total_reemitted_atom'],result['total_current']])



        ##print('ok')
    f.close()

    print('Pump currents written to ... ', path+'/'+filename+'_pump.csv')



###############################################
  def read_e2d_ppf(self,dda, dtype,sequence):

    """
    useful function to get data from synthetic ppf
    usage:
    simu.read_e2d_ppf('PY4D','TEI',325,'HFE')

    must be used after running
    execute_makeppf
    #and then the batch script to run the makeppf script

    """
    #initread()
    dire='e2d_data'
    # sim.init('testbruvio', '92123')
    pathlib.Path(
        self.workingdir + os.sep + folder + os.sep + str(self.shot)).mkdir(parents=True, exist_ok=True)
    filename=os.path.join(self.workingdir,dire,ppp.shot,str(sequence)+dda+dtype+'_python.dat')

    # filename=self.workingdir+os.sep+dire+os.sep+self.shot+'/'+str(sequence)+'_'+dda+dtype+'_python.dat'
    #print(filename)
    data=Getdata(int(self.shot), dda,dtype,int(sequence),self.owner)
    with  open(filename,'wt') as ofile:
      writer = csv.writer(ofile, delimiter='\t')
      writer.writerow([dda+'_x',dda+'_y',data['xunits'],data['dunits']])
      for i in range(0,len(data['x'])):
          writer.writerow([data['x'][i],data['data'][i]])
    print(data['desc']+' written to ... ', filename)
###############################################
  def contour(self,vari,fname, lowerbound=None,upperbound=None,label=None):
    """
    function to get a contour plot

    usage:

    
    if you want to set upper and lower bound to normalize the contour plot, use:
  simu.contour('LFE',var,'prad'+str(index1),upperbound=8e6)

    """
    # filename = os.path.join(self.workingdir, dire, ppp.shot,
    #                         str(sequence) + dda + dtype + '_python.dat')
    with open(self.workingdir+'/e2d_data/vessel_JET_csv.txt', 'rt') as f:
      reader = csv.reader(f, delimiter=';')
      next(reader)
      # col = list(zip(*reader))[1]
      csv_dic = []

      for row in reader:
          csv_dic.append(row);
      # print(csv_dic)
      col1 = []
      col2 = []

      for row in csv_dic:
          col1.append(row[0])
          col2.append(row[1])
      dummy=np.array(col1)
      # print(dummy)
      dummy2=np.array(col2)
      dummy2=[float(i) for i in dummy2]
      z_ves=-np.asarray(dummy2)
      dummy=[float(i) for i in dummy]
      r_ves=np.asarray(dummy)
    f.close()

    # if ExtraInput is None:
    rvert = ep.data(self.fullpath,'RVERTP').data
    rvert = np.trim_zeros(rvert, 'b')
    zvert = ep.data(self.fullpath,'ZVERTP').data
    zvert = -np.trim_zeros(zvert, 'b')
    rmesh = ep.data(self.fullpath,'RMESH').data
    rmesh = np.trim_zeros(rmesh, 'b')
    zmesh = ep.data(self.fullpath,'ZMESH').data
    zmesh = -np.trim_zeros(zmesh, 'b')
    r_sep = ep.data(self.fullpath,'RSEPX').data
    r_sep = np.trim_zeros(r_sep, 'b')
    z_sep = ep.data(self.fullpath,'ZSEPX').data
    z_sep = -np.trim_zeros(z_sep, 'b')
    # else:
    # rvert=self.read_data('RVERTP',ExtraInput)
    # rvert=np.trim_zeros(rvert['data'],'b')
    # zvert=self.read_data('ZVERTP',ExtraInput)
    # zvert=-np.trim_zeros(zvert['data'],'b')
    # rmesh=self.read_data('RMESH',ExtraInput)
    # rmesh=np.trim_zeros(rmesh['data'],'b')
    # zmesh=self.read_data('ZMESH',ExtraInput)
    # zmesh=-np.trim_zeros(zmesh['data'],'b')
    # r_sep=self.read_data('RSEPX',ExtraInput)
    # r_sep=np.trim_zeros(r_sep['data'],'b')
    # z_sep=self.read_data('ZSEPX',ExtraInput)
    # z_sep=-np.trim_zeros(z_sep['data'],'b')
    var=vari
    # var = -np.trim_zeros(var, 'b')
    #var=self.read_data(vari,ExtraInput)
    #var=np.trim_zeros(var['data'],'b')
    sep=[r_sep,z_sep]
    mesh=[rmesh,zmesh]
    max_jj=self.npts_m
    for ii in range(0,max_jj-1):      
        for jj in range(ii+1,max_jj):
            if (rmesh[jj]==rmesh[ii]) & (zmesh[jj]==zmesh[ii]):
                #print(jj)
                rmesh[jj]= 0
                zmesh[jj]=0
      
    #find_indices(zmesh, lambda e: e == 0)    
# and removing duplicate points
    rmesh_new = np.delete(rmesh, find_indices(rmesh, lambda e: e == 0))
    zmesh_new = np.delete(zmesh, find_indices(zmesh, lambda e: e == 0))
    #var = np.delete(var, find_indices(rmesh, lambda e: e == 0))
    var = np.delete(var, find_indices(zmesh, lambda e: e == 0))
#finding cell centers
    rvert_size=len(rvert)+5
    #print(rvert_size)
    dummy=list(range(1,int(rvert_size/5)))
    #print(dummy)
    #sys.exit('raise')
    #raise SystemExit('')
    dummy1=list(map(lambda x:5*x,dummy))
    dummy2=list(map(lambda x:x-1,dummy1))

    rvert_cent=rvert[dummy2[:]]

    zvert_size=len(zvert)+5
    dummy=list(range(1,int(zvert_size/5)))
    dummy1=list(map(lambda x:5*x,dummy))
    dummy2=list(map(lambda x:x-1,dummy1))
    zvert_cent=zvert[dummy2[:]]


    k=0
    ind=list()
#removing duplicate point in rmesh 
    for ii in list(range(0,len(rvert_cent))):
        for jj in list(range(0,len(rmesh_new))):
          dist=sqrt((rmesh_new[jj]-rvert_cent[ii])**2+(zmesh_new[jj]-zvert_cent[ii])**2)
          #print(dist)
          if dist==0.0:      
            ind.append(jj)
            k=k+1

#assembling mesh cells
    leng=len(rvert)
    dummy=list(range(0,int(leng/5)))
    #print(dummy)
    #dummy=list(range(0,len(int(rvert)/5)))
    dummy1=list(map(lambda x:5*x+1,dummy))
    dummy2=list(map(lambda x:5*x+2,dummy))
    dummy3=list(map(lambda x:5*x+3,dummy))
    dummy4=list(map(lambda x:5*x+4,dummy))

    dummy1=list(map(lambda x:x-1,dummy1))
    dummy2=list(map(lambda x:x-1,dummy2))
    dummy3=list(map(lambda x:x-1,dummy3))
    dummy4=list(map(lambda x:x-1,dummy4))


    A=rvert[dummy1]
    B=rvert[dummy2]
    C=rvert[dummy3]
    D=rvert[dummy4]
    dummy=list(range(0,int(leng/5)))
    #dummy=list(range(0,len(int(zvert)/5)))
    dummy1=list(map(lambda x:5*x+1,dummy))
    dummy2=list(map(lambda x:5*x+2,dummy))
    dummy3=list(map(lambda x:5*x+3,dummy))
    dummy4=list(map(lambda x:5*x+4,dummy))


    dummy1=list(map(lambda x:x-1,dummy1))
    dummy2=list(map(lambda x:x-1,dummy2))
    dummy3=list(map(lambda x:x-1,dummy3))
    dummy4=list(map(lambda x:x-1,dummy4))


    A1=zvert[dummy1]
    B1=zvert[dummy2]
    C1=zvert[dummy3]
    D1=zvert[dummy4]




    if lowerbound is None:
      lower = min(var[ind])
    else:
      lower=lowerbound
    if upperbound is None:
      upper = max(var[ind])
    else:
      upper=upperbound

    patches=[]
    for i in list(range(0,len(A))):
      #print(i)
      polygon = Polygon([[A[i],A1[i]],[B[i],B1[i]],[C[i],C1[i]],[D[i],D1[i]]],
        edgecolor='none',alpha=0.1,linewidth=0, closed=True)
      patches.append(polygon)
          #



    norm = mpl.colors.Normalize(vmin=lower,vmax=upper)
    collection = PatchCollection(patches, match_original=True)
    collection.set(array=var[ind], cmap='jet',norm=norm)


    fig,ax = plt.subplots()
    ax.add_collection(collection)

    #collection.set_color(colors)

    # ax.autoscale_view()


    sfmt=ScalarFormatter(useMathText=True)
    sfmt.set_powerlimits((0,0))
    # # old normalization
    sm = plt.cm.ScalarMappable(cmap="jet", norm=plt.Normalize(vmin=lower, vmax=upper))
    # norm = mpl.colors.Normalize(vmin=lower,vmax=upper)
    # sm = plt.cm.ScalarMappable(cmap="jet", norm=norm)
    sm.set_array([])
    plt.xlabel('R [m]')
    plt.ylabel('Z [m]')

    cbar=plt.colorbar(sm,format=sfmt)
    cbar.set_label(label)
    # plt.scatter(rvert_cent,zvert_cent)
    # plt.scatter(rmesh_new,zmesh_new,color='green');
    plt.plot(r_ves,z_ves,'k');plt.plot(r_sep,z_sep,'r')
    plt.xlim(2.2,3)
    plt.ylim(-1.77,-1.2)

    #plt.axis('equal')
    plt.savefig('./figures/'+fname, format='eps', dpi=600)
    plt.savefig('./figures/'+fname,  dpi=600) #


  @staticmethod  
  def execute_makeppf(simu_list,path,outfile):
    with open(path+'/'+outfile, 'w') as f_out:
        f_out.write('#!/bin/bash\n\n')
        for index1 in range(0,len(simu_list)):
          simu=simu_list[index1][0]
          f_out.write('echo {}\n'.format(simu.shot))
          batch_command = 'mkppf -c/home/jsimpson/eproc/input_files_mkppf_git/bviola_pb5_issue/cntl -g/home/jsimpson/eproc/input_files_mkppf_git/bviola_pb5_issue/geomfile1.txt -d/home/jsimpson/eproc/input_files_mkppf_git/bviola_pb5_issue/ddafile1.txt -o{} edge2d {} {} {} aaro_pb5_temp jsimpson\n'.format((simu.owner),int(simu.shot),(simu.date), int(simu.seq))  
          f_out.write(batch_command)
    f_out.close()
    st = os.stat(path+'/'+outfile)
    os.chmod(path+'/'+outfile, st.st_mode | stat.S_IEXEC)

  @staticmethod
  def write_edge2d_profiles(simu_list, filename):
      """
      writes to file mid plane and targets profiles, it takes as input a list of simulations
      """
      # with open(path+'/'+filename+'.csv', 'w') as f:  # Just use 'w' mode in 3.x
      # simu=simu_list[0]
      # result=simu.eirene_pumpcur()

      for index1 in range(0, len(simu_list)):
          simu = simu_list[index1][0]
          ##print(simu['name'])
          # ExtraInput = simu_list[index1][1]
          # dire='e2d_data'
          # print(simu.workingdir)
          # print(simu.shot)
          # print(simu.workingdir + os.sep + dire + os.sep + simu.shot)
          # pathlib.Path(simu.workingdir + os.sep + dire + os.sep + simu.shot).mkdir(parents=True, exist_ok=True)
          odir = simu.workingdir+'/e2d_data/' + simu.shot + "/"

          time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
          Region = ['IT', 'OT', 'IMP', 'OMP']
          for i, word in enumerate(Region):
              oname = '_' +word + '_' + simu.shot + '_' + simu.date + \
                      '_seq#' + simu.seq + '.dat'
              outfile = odir + filename + oname
              result=simu.read_profiles(word)
              with  open(outfile, 'w') as ofile:
                  writer = csv.writer(ofile, delimiter='\t')
                  # writer.writerow([str(49), filename, str(time)])
                  # writer.writerow(['Pump current across: '])
                  writer.writerow(['psi',
                  'dsrad',
                  'dsrad_face',
                  'ds',
                  'rmesh',
                  'zmesh',
                  'hrho',
                  'sh',
                  'bfi',
                  'jpar',
                  'jpari',
                  'jtarg',
                  'jtargi',
                  'gam',
                  'gamro',
                  'gamroe',
                  'pflxd',
                  'denel',
                  'te',
                  'ti',
                  'vi',
                  'mach',
                  'da',
                  'dm',
                  'dha',
                  'soun',
                  'sirec',
                  'pre',
                  'preel',
                  'prestat',
                  'pretot',
                  'qeflxd',
                  'qiflxd',
                  'qepcd',
                  'qepcdd',
                  'qepcv',
                  'qipcd',
                  'qipcdd',
                  'qipcv',
                  'qpare',
                  'qpari',
                  'qpartot',
                  'denpe',
                  'denpi',
                  'totpden',
                  'dperp',
                  'chii',
                  'chie'])

                  for i in range(0, len(result['ade'].xData)):
                      writer.writerow([result['psi'].yData[i],
                                          result['dsrad'][i],
                                          result['dsrad_face'][i],
                                          result['ds'][i],
                                          result['rmesh'].yData[i],
                                          result['zmesh'].yData[i],
                                          result['hrho'].yData[i],
                                          result['sh'].yData[i],
                                          result['bfi'].yData[i],
                                          result['jpar'].yData[i],
                                          result['jpari'].yData[i],
                                          result['jtarg'].yData[i],
                                          result['jtargi'].yData[i],
                                          result['agam'].yData[i],
                                          result['agamro'].yData[i],
                                          result['agamroe'].yData[i],
                                          result['pflxd'].yData[i],
                                          result['ade'].yData[i],
                                          result['ate'].yData[i],
                                          result['ati'].yData[i],
                                          result['vpi'].yData[i],
                                          result['mach'].yData[i],
                                          result['ada'].yData[i],
                                          result['adm'].yData[i],
                                          result['adha'].yData[i],
                                          result['asoun'].yData[i],
                                          result['asirec'].yData[i],
                                          result['pre'].yData[i],
                                          result['preel'].yData[i],
                                          result['prestat'].yData[i],
                                          result['pretot'].yData[i],
                                          result['qeflxd'].yData[i],
                                          result['qiflxd'].yData[i],
                                          result['qepcd'].yData[i],
                                          result['qepcdd'].yData[i],
                                          result['qepcv'].yData[i],
                                          result['qipcd'].yData[i],
                                          result['qipcdd'].yData[i],
                                          result['qipcv'].yData[i],
                                          result['qpare'].yData[i],
                                          result['qpari'].yData[i],
                                          result['qpartot'].yData[i],
                                          result['denpe'].yData[i],
                                          result['denpi'].yData[i],
                                          result['totpden'].yData[i],
                                          result['dperp'].yData[i],
                                          result['chii'].yData[i],
                                          result['chie'].yData[i]
                                       ])

                  ofile.close()

                  print('EDGE2D ' + word + ' profiles written to ... ',
                        odir  + filename + oname)
          print('\n')

  @staticmethod
  def write_edge2d_profiles1(simu_list, filename):
      """
        writes to file mid plane and targets profiles, it takes as input a list of simulations
      """
      # with open(path+'/'+filename+'.csv', 'w') as f:  # Just use 'w' mode in 3.x
      # simu=simu_list[0]
      # result=simu.eirene_pumpcur()
      simu = simu_list[0][0]
      filename=filename+'_new'
      names1 = ep.getnames(simu.fullpath, 1)  # profile data
      names2 = ep.getnames(simu.fullpath, 4)  # geometry data
      listnames = []
      for i in (range(names1.nNames)):
          listnames.append(names1.names[i].decode('utf-8').strip().lower())
      for i in (range(names2.nNames)):
          listnames.append(names2.names[i].decode('utf-8').strip().lower())
      listnames.append('dsrad')
      listnames.append('dsrad_face')
      listnames.append('ds')

      for index1 in range(0, len(simu_list)):
          simu = simu_list[index1][0]
          ##print(simu['name'])
          # ExtraInput = simu_list[index1][1]
          # dire='e2d_data'
          # print(simu.workingdir)
          # print(simu.shot)
          # print(simu.workingdir + os.sep + dire + os.sep + simu.shot)
          # pathlib.Path(simu.workingdir + os.sep + dire + os.sep + simu.shot).mkdir(parents=True, exist_ok=True)
          odir = simu.workingdir + '/e2d_data/' + simu.shot + "/"

          time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
          Region = ['IT', 'OT', 'IMP', 'OMP']
          for i, word in enumerate(Region):
              oname = '_' + word + '_' + simu.shot + '_' + simu.date + \
                      '_seq#' + simu.seq + '.dat'
              outfile = odir + filename + oname
              result1 = simu.read_profiles1(word)


                  # w.writerow(result1)
              # result = simu.read_profiles(word)
              # a = result['dsrad']
              # b = result1['dsrad']
              # print([i - j for i, j in zip(a, b)])
              rows = len(result1['denel'].xData)
              columns = len(result1.keys())
              # # columns = len(result)
              #
              bigdata = np.zeros((rows, columns))
              for i, var in enumerate(result1.keys()):
              #     # print(i,var)
                  for j in range(0, rows):
                      if var == 'dsrad' or var == 'ds' or var == 'dsrad_face':
                          bigdata[j, i] = result1[var][j]
                      else:
                        bigdata[j, i] = result1[var].yData[j]

              # for i in (range(0,columns-3)):
              #     var = listnames[i]
              #     for j in range(0, rows):
              #         bigdata[j, i] = result1[var].yData[j]
              #
              # for j in range(0, rows):
              #
              #       bigdata[j,columns-3]=result1['dsrad'][j]
              #       bigdata[j,columns-2]=result1['dsrad_face'][j]
              #       bigdata[j,columns-1]=result1['ds'][j]

              # listnames = []
              # for var in result1.keys():
              #     listnames.append(var)
              #
              with open(outfile, 'w') as f:  # Just use 'w' mode in 3.x
                  w = csv.DictWriter(f, result1.keys(), delimiter='\t')
                  w.writeheader()
              f.close()
              with open(outfile, 'a') as ofile:  # Just use 'w' mode in 3.x
                  writer = csv.writer(ofile, delimiter='\t')
                  writer.writerows(bigdata)

              f.close()
              # with  open(outfile, 'w') as ofile:
              #     writer = csv.writer(ofile, delimiter='\t')
              #     # writer.writerow([str(49), filename, str(time)])
              #     # writer.writerow(['Pump current across: '])
              #     writer.writerow(listnames)
              #     writer.writerows(bigdata)
              # ofile.close()

              print('EDGE2D ' + word + ' profiles written to ... ',
                    odir + filename + oname)
          print('\n')


  @staticmethod
  def calc_lambda_q(power_flux):
        #qiflxd
        #qeflxd
        
      # set npts
      #    power_flux['xData'] = (power_flux['xData'])[0:power_flux['npts']]
      #    power_flux.yData = (power_flux.yData)[0:power_flux['npts']]


      # print(power_flux['xData'])
      # print('\n')
      # print(power_flux.yData)
      # find seperatrix index
      sep = 0
      sep_idx = np.abs(np.asarray(power_flux.xData)-sep).argmin()
          # (np.abs(np.array(power_flux['xData']) - sep)).argmin()

      # TODO put check for negative x value for seperatrix
      if (power_flux.xData)[sep_idx] < 0:
          # check we are on th correct side of the seperatrix
          sep_idx += 1
      # slice data such that we only see from the seperatrix onwards
      power_flux.yData = np.asarray(power_flux.yData)[sep_idx:power_flux.nPts]
      power_flux.xData = np.asarray(power_flux.xData)[sep_idx:power_flux.nPts]

      cum_power_flux = np.cumsum([power_flux.yData])
      print('cum power ', cum_power_flux)
      # lambda q defined roughly as 60% of the cumlative sum of the power flux density
      end_cum_val_60 = cum_power_flux[len(cum_power_flux) - 1] * (
      1 - (1 / np.e))

      # interpolation of the powerflux if on grid scale will provide more accurate answer





      print('END = ', end_cum_val_60)
      lambda_q_idx = (np.abs(cum_power_flux - end_cum_val_60)).argmin()

      # decides which cells to interpolate between
      if cum_power_flux[lambda_q_idx] < cum_power_flux[lambda_q_idx + 1]:

          # do the interpolation
          x0 = (power_flux.xData)[lambda_q_idx]
          y0 = cum_power_flux[lambda_q_idx]
          x1 = (power_flux.xData)[lambda_q_idx + 1]
          y1 = cum_power_flux[lambda_q_idx + 1]
          y = end_cum_val_60
          lambda_q = interpolation_x(x0, y0, x1, y1, y)

      else:
          # between lambda_q_idx and previous index
          # do the interpolation
          x0 = (power_flux.xData)[lambda_q_idx - 1]
          y0 = cum_power_flux[lambda_q_idx - 1]
          x1 = (power_flux.xData)[lambda_q_idx]
          y1 = cum_power_flux[lambda_q_idx]
          y = end_cum_val_60
          lambda_q = interpolation_x(x0, y0, x1, y1, y)

      print(' GRID RESOLUTION ', (x1 - x0))
      #
      print('Power flux at lambda q para', cum_power_flux[lambda_q_idx])
      print('index = ', lambda_q_idx)
      print('lambda_q = ',lambda_q)
      return lambda_q

  # THE INDEX PROVIDED HERE IS THE OMP INDEX ON RING NOT A ROW!!!
  # THE ROW INDEX NEED TO BE WORKED OUT!
  # def find_omp_index1(self):
  #     geom = ep.geom(self.fullpath)
  #
  #     open_ring = geom.firstOpenRing  # first open ring
  #     last_ring = geom.wallRing  # last open ring (i.e. wall ring)
  #     last_ring = open_ring + 4  # this is for debugging purpouses
  #
  #     # Locate the outer mid plane index
  #
  #     omp_loc_data = ep.ring(self.fullpath, 'RMESH',
  #                               's01')  # READ FIRST OPEN RING
  #     #    omp_loc_xData = np.array(slice_npts(omp_loc_data,'ydata'))
  #     omp_loc_xData = omp_loc_data.yData
  #
  #     # find maximum or the r data
  #
  #     omp_index = np.argmax(omp_loc_xData)
  #
  #     # confirm the index is correct by using known built in function of OMP in EprocRow
  #
  #     omp_loc_row = ep.row(self.fullpath, 'RMESH', 'OMP')
  #     #     omp_loc_row_xData = np.array(slice_npts(omp_loc_row,'ydata'))
  #     omp_loc_row_xData = omp_loc_row.yData
  #     safety_flag = True  # indicates that OMP location could not be found
  #     for i in range(0, len(omp_loc_row_xData)):
  #
  #         if omp_loc_row_xData[i] == omp_loc_xData[omp_index]:
  #             print(i)
  #             print('FOUND')
  #             print('OUTER MIDPLANE COORD CONFIMRED')
  #             safety_flag = False
  #
  #     print(omp_index)
  #     if safety_flag == True:
  #         sys.exit(
  #             "Outer midplane index cannot be verified. Max R on first seperatrix ring does not match outer mid-plane row location.")
  #     return omp_index
  #
  # # this finds the first open cell on the omp row
  def find_omp_index_row(self):
      rmesh = ep.row(self.fullpath, 'rmesh', 'omp')
      rmesh_x = rmesh.xData
      npts = rmesh.nPts

      # slice the x data
      rmesh_x = rmesh_x[0:npts]

      omp_row_index = (np.abs(np.asarray(rmesh_x) - 0)).argmin()

      if rmesh_x[omp_row_index] < 0:
          # we want the x axis to be open and this the value of rmesh_x[omp_row_index] needs to be positive
          omp_row_index = omp_row_index + 1

      # debug purpouse
      # print('omp cell =',omp_row_index)
      return omp_row_index
  #
  def find_omp_index(self):
      geom=ep.geom(self.fullpath)
      open_ring = geom.firstOpenRing
      last_ring =geom.wallRing
      last_ring = last_ring+4

      omp_loc_data = ep.ring(self.fullpath,'RMESH','s01')
      omp_loc_x_data = np.asarray(omp_loc_data.yData)
      omp_index = np.argmax((omp_loc_x_data))



      omp_loc_row  = ep.row(self.fullpath,'RMESH','OMP')
      omp_loc_row_x_data = np.asarray(omp_loc_row.yData)
      safety_flag = True # indicates that OMP location could not be found
      for i in range(0,len(omp_loc_row_x_data)):

          if omp_loc_row_x_data[i] == omp_loc_x_data[omp_index]:
               print(i)
               print('FOUND')
               print('OUTER MIDPLANE COORD CONFIMRED')
               safety_flag = False


      print(omp_index)
      if safety_flag == True:
          sys.exit("Outer midplane index cannot be verified. \
          Max R on first seperatrix ring does not match outer mid-plane row location. " )
      return omp_index

  def calc_connection_length(self, end_pos):

      # note: end_pos should be the index of the row on the ring which to end
      # calc the connection length as distance between cells / sin(pitch angle)

      # get ring data

      sh = ep.ring(self.fullpath, 'sh', 's01', 0)
      rmesh = ep.ring(self.fullpath, 'rmesh','s01', 0)
      zmesh = ep.ring(self.fullpath, 'zmesh','s01', 0)

      connection_length = 0
      # use all the centre points for the calculation of the distance between cells and the sin of the pitch angle
      # then calculate the connection length using those two
      for i in range(0, end_pos - 1):
          r1 = (rmesh.yData)[i + 1] - (rmesh.yData)[i]
          z1 = (zmesh.yData)[i + 1] - (zmesh.yData)[i]
          # sh is calculated at teh centre point of each cell
          avg_sh = ((sh.yData)[i] + (sh.yData)[i + 1]) / 2
          length = (r1 ** 2 + z1 ** 2) ** (1 / 2)
          delta_connection = length / avg_sh
          connection_length = connection_length + delta_connection

      return connection_length
  # #
  def div_idx_ring_value(self, div_row_idx, ring_position):

      # uses the result from below to match it to a ring a value

      rmesh = ep.ring(self.fullpath, 'rmesh', ring_position)
      zmesh = ep.ring(self.fullpath, 'zmesh', ring_position)

  def div_idx_value(self):

      geom = ep.geom(self.fullpath)

      # get first core row index
      first_core_row_idx = geom.firstCoreRow
      # obviously the first row in divertor is going to be one less than this
      first_div_row_idx = first_core_row_idx - 1

      # find the value of the cell with the first positive r value
      # xddata
      first_div_row = ep.row(self.fullpath, 'denel',first_div_row_idx)
      npts = first_div_row.nPts
      first_div_row=np.asarray(first_div_row.xData)


      # # find value cloest to zero but remember to slice array with npts all you will get all the reduntant 0's
      # first_div_row = first_div_row[0:npts]
      first_open_cell_idx = (np.abs(first_div_row - 0)).argmin()
      # TODO check that first open cell doesnt lie on a negative x point
      # for debugging
      # for l in first_div_row:
      #     print(l)
      # print(first_open_cell_idx)
      # print(npts)
      if first_div_row[first_open_cell_idx] < 0:
          # this means that its the cell just before the first open cell, i.e. its x value is negative
          first_open_cell_idx = first_open_cell_idx + 1
      # print(first_div_row[first_open_cell_idx])

      return first_open_cell_idx, first_div_row_idx
  # # #
  # # #
  # # #     # for testing
  # # #
  # # #     # if __name__ == "__main__":
  # # #     #     # quick testing function
  # # #     #
  # # #     #     self.fullpath = "/common/cmg/jsimpson/edge2d/runs/run1606091/tran"
  # # #     #
  # # #     #     idx =  div_idx_value(self.fullpath)
  # # #     #
  # # #     #     print(idx)
  # # #
  def calculate_upstream_t(self,l):
        # # omp index this give the index for the omp row or omp on a ring
        # omp_index = self.find_omp_index()
        #
        # # first open cell on the OMP row
        # first_open_omp_cell_row = self.find_omp_index_row()
        # # print(first_open_omp_cell_row)
        # # calculate connection length
        # l = self.calc_connection_length(omp_index)
        # print('connection length = ', l)
        #
        # # find the first open cell entering the divertor
        #
        # first_open_cell_row_div, first_div_row = self.div_idx_value()
        # # print(type(first_open_cell_row_div))
        # # type(first_div_row)
        # # print(first_open_cell_row_div, first_div_row)
        # # get the variables you need from the tran file
        #
        # # weight them for there area to remap to outer midplane
        # rmesh = ep.row(self.fullpath, 'rmesh', first_div_row)
        # dvol = ep.row(self.fullpath, 'dv', first_div_row)
        # rmesh = np.asarray(rmesh.yData)
        # dvol = np.asarray(dvol.yData)
        # # print(len(dvol))
        # # print(int(first_open_omp_cell_row))
        # # print(dvol[21])
        # # print()
        # area_div = dvol[first_open_cell_row_div] / (2 * np.pi * rmesh[first_open_cell_row_div])
        # #
        # # # OMP area
        # rmesh = ep.row(self.fullpath, 'rmesh', 'omp')
        # npts = rmesh.nPts
        # dvol = ep.row(self.fullpath, 'dv', 'omp')
        # rmesh = np.asarray(rmesh.yData)
        # dvol = np.asarray(dvol.yData)
        # # print(dvol[first_open_omp_cell_row])
        # #
        # #
        # area_omp = dvol[first_open_omp_cell_row] / (2 * np.pi * rmesh[first_open_omp_cell_row])
        # # print('omp = ', npts)
        # # upstream_te, upstream_ti=0,0
        # # print(dvol[omp_index])
        # #
        # # # area at x point should be larger than at the OMP and q parallel should be larger at the OMP than at the x point hence why the ratio is this way around
        # area_ratio = area_div / area_omp
        # #
        # # # need to calculate q paralell i.e. the energy flux density
        # #
        # # # for electrons read from a row because we have that index
        # q_para_e = ep.row(self.fullpath, 'qepcdd', first_div_row)
        # q_para_e = np.asarray(q_para_e.yData)
        # # # get the values at the divertor and remap for area
        # q_para_e_omp = q_para_e[first_open_cell_row_div] * area_ratio
        # #
        # # # for ions read from a row because we that index
        # q_para_i = ep.row(self.fullpath, 'qipcdd', first_div_row)
        # q_para_i = np.asarray(q_para_i.yData)
        # # # remap for area
        # q_para_i_omp = q_para_i[first_open_cell_row_div] * area_ratio
        qpar=self.Qpara()

        q_para_e_omp = qpar['q_para_e_omp']
        q_para_i_omp = qpar['q_para_i_omp']
        # q_para_i = qpar.q_para_i
        # q_para_e = qpar.q_para_e

        #
        q_para_e_omp_neg_flag = False
        if q_para_e_omp < 0:
          # we can't take a negative root. so needs changing, the sign just represents the direction.
          q_para_e_omp = q_para_e_omp * (-1)
          q_para_e_omp_neg_flag = True

        q_para_i_omp_neg_flag = False
        if q_para_i_omp < 0:
          # we can't take a negative root. so needs changing, the sign just represents the direction.
          q_para_i_omp = q_para_i_omp * (-1)
          q_para_i_omp_neg_flag = True
        #
        # # get miplane value of q_para_i
        kapa_0e = 2000  # CHECK THESE!!!
        kapa_0i = 70  # CHECK THESE!!!

        upstream_te = ((7 * q_para_e_omp * l) / (2 * kapa_0e)) ** (2. / 7)
        upstream_ti = ((7 * q_para_i_omp * l) / (2 * kapa_0i)) ** (2. / 7)

        # sign checking
        if q_para_e_omp_neg_flag == True:
          # upstream_te = upstream_te*(-1)
          print('WARNING Q PARALLEL ELECTRON IS NEGATIVE')

        if q_para_i_omp_neg_flag == True:
          # upstream_ti = upstream_ti*(-1)
          print('WARNING Q PARALLEL ION IS NEGATIVE')

        return upstream_te, upstream_ti

  def TPMscaling_Petrie(self,lconn):
          # following Petrie et al., NF 53 2013
        import mpmath
        R=ep.row(self.fullpath,'RMESH','OT')
        ii=np.argmax(list(map(lambda x: x>0, R.xData)))
        Rosp=R.yData[ii]
        omp=self.read_profiles('OMP')
        xdata=omp['ate'].xData
        # iy_OMP_SOL=xdata[xdata > 0.0]

        iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)

        # print(iy_OMP_SOL)
        iy_sep_OMP=min(iy_OMP_SOL)
        iy_ny_OMP=max(iy_OMP_SOL)
        Romp=R.yData[iy_sep_OMP]
        fr=Rosp/Romp
        frad=abs(self.read_psol_pradpsol()['fraddiv'])
        Pin =self.read_time_data('POWSOL',100)
        nsep=omp['ade'].yData[iy_sep_OMP]
        # print('frad',frad)
        # print(Pin)
        # print(fr)
        # print(Romp)
        # print(nsep)
        # ntar = pow(Rosp,2) * pow(lconn,6/7) * pow(nsep,3)
        # ttar = pow(Rosp,-2) * pow(lconn,-4/7) * pow(nsep,-2)
        dummy=(lconn*ln(fr) / (fr-1))

        ntar =  pow(Rosp,2) * pow(nsep,3) * pow(Pin/1e6 * (1-frad),-8./7) * mpmath.power(dummy,-6./7)

        ttar = mpmath.power(Pin/1e6,10./7) * mpmath.power(1-frad,10./7) *  pow(Rosp,-2)  * pow(nsep,-2) * mpmath.power((fr-1) * (lconn*ln(fr)),-4./7)
        return{'ntar':ntar,'ttar':ttar}

  def nete_omp(self):
        omp=self.read_profiles('OMP')
        xdata=omp['ate'].xData
        # iy_OMP_SOL=xdata[xdata > 0.0]

        iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)
        # print(iy_OMP_SOL)
        iy_sep_OMP=min(iy_OMP_SOL)
        iy_ny_OMP=max(iy_OMP_SOL)
        nsep=omp['ade'].yData[iy_sep_OMP]
        tsep=omp['ate'].yData[iy_sep_OMP]
        return nsep,tsep

  def Qpara(self):
        # # omp index this give the index for the omp row or omp on a ring
        omp_index = self.find_omp_index()

        # first open cell on the OMP row
        first_open_omp_cell_row = self.find_omp_index_row()
        # print(first_open_omp_cell_row)
        # calculate connection length
        l = self.calc_connection_length(omp_index)
        print('connection length = ', l)

        # find the first open cell entering the divertor

        first_open_cell_row_div, first_div_row = self.div_idx_value()
        # print(type(first_open_cell_row_div))
        # type(first_div_row)
        # print(first_open_cell_row_div, first_div_row)
        # get the variables you need from the tran file

        # weight them for there area to remap to outer midplane
        rmesh = ep.row(self.fullpath, 'rmesh', first_div_row)
        dvol = ep.row(self.fullpath, 'dv', first_div_row)
        rmesh = np.asarray(rmesh.yData)
        dvol = np.asarray(dvol.yData)
        # print(len(dvol))
        # print(int(first_open_omp_cell_row))
        # print(dvol[21])
        # print()
        area_div = dvol[first_open_cell_row_div] / (2 * np.pi * rmesh[first_open_cell_row_div])
        #
        # # OMP area
        rmesh = ep.row(self.fullpath, 'rmesh', 'omp')
        npts = rmesh.nPts
        dvol = ep.row(self.fullpath, 'dv', 'omp')
        rmesh = np.asarray(rmesh.yData)
        dvol = np.asarray(dvol.yData)
        # print(dvol[first_open_omp_cell_row])
        #
        #
        area_omp = dvol[first_open_omp_cell_row] / (2 * np.pi * rmesh[first_open_omp_cell_row])
        # print('omp = ', npts)
        # upstream_te, upstream_ti=0,0
        # print(dvol[omp_index])
        #
        # # area at x point should be larger than at the OMP and q parallel should be larger at the OMP than at the x point hence why the ratio is this way around
        area_ratio = area_div / area_omp
        #
        # # need to calculate q paralell i.e. the energy flux density
        #
        # # for electrons read from a row because we have that index
        q_para_e = ep.row(self.fullpath, 'qepcdd', first_div_row)
        q_para_e = np.asarray(q_para_e.yData)
        # # get the values at the divertor and remap for area
        q_para_e_omp = q_para_e[first_open_cell_row_div] * area_ratio
        #
        # # for ions read from a row because we that index
        q_para_i = ep.row(self.fullpath, 'qipcdd', first_div_row)
        q_para_i = np.asarray(q_para_i.yData)
        # # remap for area
        q_para_i_omp = q_para_i[first_open_cell_row_div] * area_ratio
        return{'q_para_e':q_para_e,
             'q_para_e_omp': q_para_e_omp,
             'q_para_i': q_para_i,
             'q_para_i_omp': q_para_i_omp}



  def TPMscaling(self,lconn):
          # following Petrie et al., NF 53 2013
        import mpmath
          # omp index this give the index for the omp row or omp on a ring
        R=ep.row(self.fullpath,'RMESH','OT')
        ii=np.argmax(list(map(lambda x: x>0, R.xData)))
        Rosp=R.yData[ii]
        omp=self.read_profiles('OMP')
        xdata=omp['ate'].xData
        # iy_OMP_SOL=xdata[xdata > 0.0]

        iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)

        # print(iy_OMP_SOL)
        iy_sep_OMP=min(iy_OMP_SOL)
        iy_ny_OMP=max(iy_OMP_SOL)
        Romp=R.yData[iy_sep_OMP]
        fr=Rosp/Romp
        frad=abs(self.read_psol_pradpsol()['fraddiv'])
        Pin =self.read_time_data('POWSOL',100)
        nsep=omp['ade'].yData[iy_sep_OMP]
        print('frad',frad)
        qpar=self.Qpara()
        Qparallel_up=qpar['q_para_e_omp'] #+ qpar.q_para_i_omp
        # print(Pin)
        # print(fr)
        # print(Romp)
        # print(nsep)


        ntar =  mpmath.power(Qparallel_up,-8./7) *pow(Rosp,2) * pow(nsep,3) * pow((1-frad),2) * mpmath.power(lconn,6./7)

        ttar = mpmath.power(Qparallel_up,10./7) * mpmath.power(1-frad,2)*  pow(nsep,-2) *  pow(Rosp,-2)  * pow(Romp,2) * mpmath.power(lconn,-4./7)

        return{'ntar':ntar,'ttar':ttar}


  def read_eirene(self,path):

      """
    % Function to read EIRENE output data from a run directory. Mimicks the
    % behaviour of Derek Harting's plote2deir reading routines.
    % Input  : rundir          = Full path of run directory
    % Output : geom.xv       = x coordinates of distinct EIRENE triangle vertices.
    %          geom.yv       = y coordinates of distinct EIRENE triangle vertices.
    %          geom.trimap   = indices into xv and yv giving triangle coordinates.
    %                          Has dimension: (ntriangles,3). Triangle
    %                          coordinates are then
    %                          (geom.xv(geom.trimap),geom.yv(geom.trimap)).
    %          PLS.names     = Names of bulk plasma ions in eirene.input.
    %          PLS.dataName  = Data names for bulk plasma ions.
    %          PLS.unitName  = Unit names for bulk plasma ions.
    %          PLS.data      = 3D array containing data for each bulk plasma ion
    %                          species, for each data name and at each EIRENE
    %                          triangle. Has dimension:
    %               (length(PLS.names),length(PLS.dataName),size(geom.trimap,1)).
    %          ATM           = Same for atoms.
    %          MOL           = Same for molecules.
    %          ION           = Same for test ions.
    %          MISC          = Same for miscelaneous.
      :param path: 
      :return: 
      """
      self.data.eirene=Eirene(path)
      logger.log(5,dir(self.data.eirene))








    



  @staticmethod
  def plot_profiles(simlist,var,Region):
          for index1 in range(0, len(simlist)):
              simu = simlist[index1][0]
              label = simlist[index1][1]
              data=ep.row(simu.fullpath,var,Region)
              fname = data.yDesc.decode('utf-8')
              ftitle = data.yDesc.decode('utf-8')
              fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
              fylabel = str(data.yUnits.decode('utf-8'))

              # print(fylabel)
              plt.figure(num=fname)
              # if self.plot_exp == "True":
              plt.scatter(data.xData,data.yData,
                              label=label)

              axes = plt.axes()
              plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
              plt.legend(loc='upper right', prop={'size': 18})
              plt.xlabel(fxlabel)
              plt.ylabel(fylabel)
          plt.show()
          # %%

          # plt.savefig('./figures/' + fname, format='eps', dpi=300)
          # plt.savefig('./figures/' + fname, dpi=300)  #

  @staticmethod
  def contour_rad_power(simlist,upper):
          for index1 in range(0, len(simlist)):
              simu = simlist[index1][0]
              label = simlist[index1][1]
              # print(simu)
              var_H = ep.data(simu.fullpath, 'SQEHRAD').data
              # var_H=-np.trim_zeros(var_H['data'],'b')
              try:
                  var_SQERZ_1 = ep.data(simu.fullpath, 'SQEZR_1').data
                  # var_SQERZ_1=-np.trim_zeros(var_SQERZ_1['data'],'b')
              except:
                  print('no SQEZR_1')
                  var_SQERZ_1 = 0
              try:
                  var_SQERZ_2 = ep.data(simu.fullpath, 'SQEZR_2').data
                  # var_SQERZ_2=-np.trim_zeros(var_SQERZ_2['data'],'b')
              except:
                  print('no SQEZR_2')
                  var_SQERZ_2 = 0
              #
              var = var_H + var_SQERZ_1 + var_SQERZ_2
              # var=var_H+var_SQERZ_1+var_SQERZ_2
              var = -np.trim_zeros(var, 'b')
              simu.contour(var, 'Prad_' + label, upperbound=upper,
                           label='MW/m^3')

          
  @staticmethod
  def bar_power_balance(pb,label):
      import pandas as pd
      from matplotlib import pyplot as plt
      N = 8

      ion = (0, pb['pi_eq'], pb['pi_com'], pb['pi_atomic'], pb['pi_mol'],0, pb['pi_rec'],
      pb['pi_cx'])
      electronn = (pb['pe_zrad'], pb['pe_eq'], pb['pe_com'], pb['pe_atomic'],
      pb['pe_mol'], pb['pe_hrad'], pb['pe_rec'], 0)
      # menStd = (2, 3, 4, 1, 2)
      # womenStd = (3, 5, 2, 3, 3)
      ind = np.arange(N)  # the x locations for the groups
      width = 0.15  # the width of the bars: can also be len(x) sequence
      plt.figure()
      p1 = plt.bar(ind, ion, width)
      # p2 = plt.bar(ind, electronn, width, bottom=ion)
      p2 = plt.bar(ind, electronn, width)

      plt.ylabel('MW')
      plt.title('power balance ' + label)
      plt.xticks(ind, (
      'radiation', 'equipartition', 'compression', 'recombination',
      'atomic_ionisation', 'molecular_ionisation', 'hydrogen_radiation',
      'charge_exchange'), rotation=30)
      # plt.yticks(np.arange(0, 81, 10))

      plt.legend((p1[0], p2[0]), ('ION', 'ELECTRON'))
      plt.tight_layout()
      plt.show()
        ##impurity rad
        #pb['pe_zrad']
          
        ## #equipartition
        #pb['pi_eq']
        #pb['pe_eq']
        ## #compression
        #pb['pe_com']
        #pb['pi_com']
        ## # atomic ioni
        #pb['pe_atomic']
        #pb['pi_atomic']
        ## #molec ion
        #pb['pe_mol']
        #pb['pi_mol']
        ## #hydro rad
        #pb['pe_hrad']
        ## #recombination
        #pb['pe_rec']
        #pb['pi_rec']
        ## #charge exchange
        #pb['pi_cx']
        ##
        #data1 = [100,120,140]
        #data2 = [150,120,190]
        #data3 = [100,150,130]

        # df = pd.DataFrame({'data1': data1, 'data2': data2, 'data3': data3})
          
          
          #main_impurity_radiation = []
          #equipartition = []
          #compression = []
          #recombination = []
          #atomic_ionisation = []
          #molecular_ionisation = []
          #charge_exchange = []
          #hydrogen_radiation = []
          
          #main_impurity_radiation.append()
          #equipartition.append()
          #compression.append()
          #recombination.append()
          #atomic_ionisation.append()
          #molecular_ionisation.append()
          #charge_exchange.append()
          #hydrogen_radiation.append()
          
          #ion_power_balance=pd.DataFrame({'main impurity radiation':[0],
          #'equipartition':[pb['pi_eq']],
                               #'compression':[pb['pi_com']],
                               #'recombination':[pb['pi_rec']],
                               #'atomic ionisation':[pb['pi_atomic']],
                               #'molecular ionisation':[pb['pi_mol']],
                               #'charge exchange':[pb['pi_cx']],
                               #'hydrogen radiation':[0]
                               #})
          #ion_power_balance.plot(kind='bar', stacked=True)
          #plt.show()
          

                                
                                # elec_power_balance=pd.DataFrame({'main impurity radiation':pb['pe_zrad'],
                                #                                 'equipartition':pb['pe_eq'],
                                #                                 'compression':pb['pe_com'],
                                #                                 'recombination':pb['pe_rec'],
                                #                                 'atomic ionisation':pb['pe_atomic'],
                                #                                 'molecular ionisation':pb['pe_mol'],
                                #                                 'charge exchange':0,
                                #                                 'hydrogen radiation':pb['pe_hrad']
                                #                                 })
          #
          # df.plot(kind='bar', stacked=True)
        



