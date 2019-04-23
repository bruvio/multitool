#!/bin/env python
#  -*- coding: utf-8 -*-
"""
Created on July 2017

# ----------------------------
__author__ = "bruvio"
__version__ = "1.1"

# ----------------------------
"""
import eproc as ep
import numpy as np
from class_geom import geom
import os
import csv
import stat
import math
import argparse, logging
import mpmath
import math
from time import gmtime, strftime
from ppf import *
from matplotlib.patches import Polygon
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.collections import PatchCollection
#from django.utils.datastructures import SortedDict
from collections import OrderedDict
pi=mpmath.pi

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
def write_hrts(pulse, dda,sequence=None,user=None,fit=None):
    if sequence is None:
        sequence =0
    else:
        sequence=sequence
    if user is None:
        # user = 'lfrassin'
        user = 'estefan'
    else:
        user=user
    ppfuid(user, "r")

    ihdat, iwdat, dense, x_dense, t_dense, ier = ppfget(pulse, dda, 'NE')
    ihdat, iwdat, ddense, x_ddense, t_ddense, ier = ppfget(pulse, dda, 'DNE')
    ihdat, iwdat, tempe, x_tempe, t_tempe, ier = ppfget(pulse, dda, 'TE')
    ihdat, iwdat, dtempe, x_dtempe, t_dtempe, ier = ppfget(pulse, dda, 'DTE')
    ihdat, iwdat, rmid, x_rmid, t_rmid, ier = ppfget(pulse, dda, 'rmde')
    ihdat, iwdat, psi, x_psi, t_psi, ier = ppfget(pulse, dda, 'PSIE')
    ihdat, iwdat, z, x_z, t_z, ier = ppfget(pulse, dda, 'Z')
    ppfuid('jetppf', "r")
    ihdat, iwdat, rlcfs, x_rlcfs, t_rlcfs, ier = ppfget(pulse, 'efit', 'rbnd')
    rmrsep = rmid - rlcfs[0]
    # data=Getdata(pulse, dda,dtype,sequence,user)
    ncol = 9
    nrow=len(rmid)
    # nrow=len(rmde)
    # print(t_dense)
    # raise SystemExit
    filename='hrts_'+str(pulse)+'_'+str(t_dense)+'_'+user + '_' + \
                     dda + '_' + \
                     str(sequence) +\
                     '_python.dat'


    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    path = '/u/bviola/work/Python/EDGE2D/exp_data'
    with  open(path + '/' + filename, 'wt') as ofile:
        writer = csv.writer(ofile, delimiter='\t')
        writer.writerow([str(pulse), str(t_dense), str(ncol), str(nrow),filename, str(time)])
        writer.writerow([dda,user, str(sequence)])
        writer.writerow(['m',
                         'm', 'm',
                         'n/a', 'm', 'm-3', 'm-3',
                         'eV', 'eV'])

        writer.writerow([
            'R',
            'Z', 'RMID', 'PSI',
            'RmRsep', 'NE', 'DNE', 'TE',
            'DTE'])
    with open(path + '/' + filename ,
              'a') as f:  # Just use 'w' mode in 3.x
        writer = csv.writer(f, delimiter='\t')
        for i in range(0, len(rmid)):
            writer.writerow([x_dense[i],
                 z[i],
                 rmid[i],
                 psi[i],
                 rmrsep[i],
                 dense[i],
                 ddense[i],
                 tempe[i],
                 dtempe[i]])



    print('HRTS profiles ' \
          ' written to ... ', path + '/' + filename )





def write_hrts_fit(pulse, dda,sequence=None,user=None):
    if sequence is None:
        sequence =0
    else:
        sequence=sequence
    if user is None:
        # user = 'lfrassin'
        user = 'estefan'
    else:
        user=user
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ppfuid(user, "r")
    ihdat, iwdat, dense, x_dense, t_dense, ier = ppfget(pulse, dda, 'NE')
    ihdat, iwdat, ddense, x_ddense, t_ddense, ier = ppfget(pulse, dda, 'DNE')
    ihdat, iwdat, tempe, x_tempe, t_tempe, ier = ppfget(pulse, dda, 'TE')
    ihdat, iwdat, dtempe, x_dtempe, t_dtempe, ier = ppfget(pulse, dda, 'DTE')
    ihdat, iwdat, rhoe, x_rhoe, t_rhoe, ier = ppfget(pulse, dda, 'RHOE')
    ihdat, iwdat, rmde, x_rmde, t_rmde, ier = ppfget(pulse, dda, 'RMDE')
    ihdat, iwdat, psie, x_psie, t_psie, ier = ppfget(pulse, dda, 'PSIE')
    ihdat, iwdat, z, x_z, t_z, ier = ppfget(pulse, dda, 'Z')
    ihdat, iwdat, nef1, x_nef1, t_nef1, ier = ppfget(pulse, dda, 'NEF1')
    ihdat, iwdat, nef3, x_nef3, t_nef3, ier = ppfget(pulse, dda, 'NEF3')
    ihdat, iwdat, tef1, x_tef1, t_tef1, ier = ppfget(pulse, dda, 'TEF1')
    ihdat, iwdat, tef3, x_tef3, t_tef3, ier = ppfget(pulse, dda, 'TEF3')
    ihdat, iwdat, tef5, x_tef5, t_tef5, ier = ppfget(pulse, dda, 'TEF5')
    ihdat, iwdat, rhof, x_rhof, t_rhof, ier = ppfget(pulse, dda, 'RHOF')
    ihdat, iwdat, rmdf, x_rmdf, t_rmdf, ier = ppfget(pulse, dda, 'RMDF')
    ihdat, iwdat, psif, x_psif, t_psif, ier = ppfget(pulse, dda, 'PSIF')
    ihdat, iwdat, rlcfs, x_lcfs, t_lcfs, ier = ppfget(pulse, dda, 'lcfs')
    ppfuid('jetppf', "r")
    ihdat, iwdat, rbnd, x_rbnd, t_rbnd, ier = ppfget(pulse, 'efit', 'rbnd')



    rmrsepe = rmde - rlcfs[0]


    rmrsepf = rmdf - rlcfs[0]
# data=Getdata(pulse, dda,dtype,sequence,user)
    ncol = 3
    nrow = len(rmde)
    filename='hrts_conv_'+str(pulse)+'_'+str(t_dense)+'_'+user + '_' + \
    dda + '_' + \
                     str(sequence) + \
                     '_python.dat'
    path = '/u/bviola/work/Python/EDGE2D/exp_data'
    with  open(path + '/' + filename, 'wt') as ofile:
        writer = csv.writer(ofile, delimiter='\t')
        writer.writerow([str(pulse), str(t_dense), str(ncol), str(nrow),filename, str(time)])
        writer.writerow([dda,user, str(sequence)])
        writer.writerow(['m',
                         'm-3','eV'])

        writer.writerow([
            'Rfit', 'nef3',
            'tef5'])
    with open(path + '/' + filename ,
              'a') as f:  # Just use 'w' mode in 3.x
        writer = csv.writer(f, delimiter='\t')
        for i in range(0, len(rmdf)):
            writer.writerow([rmrsepf[i],
                             nef3[i],
                             tef5[i]])



    print('HRTS fit profiles ' \
          ' written to ... ', path + '/' + filename )

if __name__=='__main__':

    # Parse the input arguments
    parser = argparse.ArgumentParser(description='Run write_HRTS')
    parser.add_argument('pulse',type=str, help="pulse to run.")
    parser.add_argument('dda',type=str, help="pulse to run.")
    parser.add_argument('--user', type=str, help="user.", required=False)
    parser.add_argument('--sequence', type=str, help="user.", required=False)


    parser.add_argument("-d", "--debug", type=int,
                        help="Debug level. 0: Error, 1: Warning, 2: Info, 3: Debug, 4: Debug Plus", default=1)

    args = parser.parse_args(sys.argv[1:])
    debug_map = {0: logging.ERROR,
                 1: logging.WARNING,
                 2: logging.INFO,
                 3: logging.DEBUG,
                 4: 5}
    logging.basicConfig(level=debug_map[args.debug])
    logger = logging.getLogger(__name__)




    write_hrts(args.pulse,args.dda,args.user,args.sequence)
    write_hrts_fit(args.pulse,args.dda,args.user,args.sequence)
