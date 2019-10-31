#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017

@author: bruvio
modified by tmp
final version
"""
from class_sim import *
import os.path
import csv
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import yticks,xticks,ylabel,xlabel
import logging
import json
import argparse
import sys
import eproc as ep
# import pylab
from utility import *
#sys.path.append('/Users/bruvio/Work/Python/fit_langmu/lib_langmu/')
#from langmu_routines import myplot, myfigure,savitzky_golay
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import AutoMinorLocator
import pdb
logger = logging.getLogger(__name__)

#import plot_e2d
#%%
plt.ion()


def read_json(input_dict_str1):
    with open(input_dict_str1, mode='r', encoding='utf-8') as f:
        # Remove comments
        with open("temp.json", 'w') as wf:
            for line in f.readlines():
                if line[0:2] == '//' or line[0:1] == '#':
                    continue
                wf.write(line)

    with open("temp.json", 'r') as f:
        input_dict = json.load(f)
    os.remove("temp.json")

    return input_dict


def normalize(y):
    return y / sum(y)
def plot_e2d(dataname,x,y,labelname,colorname,**kwargs):
    fnorm=kwargs.pop('fnorm',1)
    linew=kwargs.pop('linew',2)
    plt.scatter(dataname[x],dataname[y],label=labelname,s=50, color=colorname)



    #plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
    #plt.axhline(y=3, xmin=-.15, xmax=500, linewidth=2, color = 'k')

    axes = plt.axes()
#    axes.set_xlim([-.02, .02])
    #axes.set_ylim([0, 50.0])
    #axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
    #axes.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])
    #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=14)
    plt.legend(loc=2,prop={'size':8})
#    locs,labels = xticks()
#    xticks(locs, list(map(lambda x: "%g" % x, locs)))
#    locs,labels = yticks()
#    yticks(locs, list(map(lambda x: "%.3f" % x, locs*fnorm)))
    # plt.tight_layout()
    plt.xlabel(fxlabel,{'color': 'k','size': 16})
    plt.ylabel(fylabel,{'color': 'k','size': 16})
    #    plt.ioff()
    # plt.tight_layout()
    #plt.savefig('./figures/'+fname,dpi=300) #

    #plt.show()

#%%
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
#%%
#get_ipython().magic(u'matplotlib inline')
#get_ipython().magic(u'matplotlib qt5')
#matplotlib.use('TkAgg')
# self.pulse= input('pulse to analyze')
# read_conf = input(' or hfe?')
# def main(self.pulse, read_conf, plot_sim, plot_exp):
class shot:
    """
    Main function to run the code.

    :param self.pulse_no: self.pulse_nonumber to use
    :param read_conf:  or HFE read_conf to plot
    :param plot_sim: Determines if simulations will be plotted
    :param plot_exp: Determines if experimental data will be plotted

    """
    def __init__(self,input_dict):
        # logger.info("Reading simulation data.")
        self.color = input_dict['color']
        self.pulse = (input_dict['pulse'])
        self.conf =  input_dict['conf']
        self.sim_user =input_dict['sim_user']
        self.reload = input_dict['reload']
        # self.profile_omp= input_dict['omp_profiles']
        self.profile_omp= "/u/bviola/work/Python/EDGE2D/e2d_data/"+self.pulse+"/e2dprofiles_python_new_OMP_"+self.pulse+'_'+self.conf+'.dat'
        # self.profile_ot= input_dict['ot_profiles']
        self.profile_ot= "/u/bviola/work/Python/EDGE2D/e2d_data/"+self.pulse+"/e2dprofiles_python_new_OT_"+self.pulse+'_'+self.conf+'.dat'
        self.plot_sim = input_dict['plot_sim']
        self.plot_exp = input_dict['plot_exp']
        self.label = input_dict['label']
        self.plot_bolo = input_dict['plot_bolo']
        self.plot_spectro = input_dict['plot_spectro']
        self.unseeded = input_dict['unseeded']
        self.compare = input_dict['compare']
        self.shift = float(input_dict['shift'])
        self.shift_fit = float(input_dict['shift_fit'])
        self.ne_omp_factor = float(input_dict['ne_omp_factor'])
        self.te_omp_factor_exp = float(input_dict['te_omp_factor_exp'])
        self.ne_omp_factor_exp = float(input_dict['ne_omp_factor_exp'])
        self.te_omp_factor = float(input_dict['te_omp_factor'])
        self.ne_ot_factor = float(input_dict['ne_ot_factor'])
        self.te_ot_factor = float(input_dict['te_ot_factor'])


        # ==============================================================================
        self.filename_hrts_data = input_dict['filename_hrts_data']
        self.filename_hrts_fit = input_dict['filename_hrts_fit']
        # %%
        # ==============================================================================
        # LP experimental
        self.filename_lp_data = input_dict['filename_lp_data']

        # other exp signals
        self.hrts_ppf = input_dict['hrts_ppf']
        self.hrts_uid = input_dict['hrts_uid']
        self.filename_HRTS_Ne = input_dict['filename_HRTS_Ne']
        self.filename_HRTS_Pe = input_dict['filename_HRTS_Pe']
        self.filename_HRTS_Te = input_dict['filename_HRTS_Te']
        self.filename_ECM1_Te = input_dict['filename_ECM1_Te']
        self.filename_KG10_Ne = input_dict['filename_KG10_Ne']
        self.filename_LIDR_Ne = input_dict['filename_LIDR_Ne']
        self.filename_LIDR_Te = input_dict['filename_LIDR_Te']
        self.filename_LIDR_Pe = input_dict['filename_LIDR_Pe']
        self.filename_boloh_unseeded = input_dict['filename_boloh_unseeded']
        self.filename_boloh_medN = input_dict['filename_boloh_medN']
        self.filename_boloh_highN = input_dict['filename_boloh_highN']
        self.filename_boloh_unseeded_e2d = input_dict['filename_boloh_unseeded_e2d']
        self.filename_boloh_lowN_e2d = input_dict['filename_boloh_lowN_e2d']
        self.filename_boloh_medN_e2d = input_dict['filename_boloh_medN_e2d']
        self.filename_boloh_highN_e2d = input_dict['filename_boloh_highN_e2d']
        self.filename_bolov_unseeded = input_dict['filename_bolov_unseeded']
        self.filename_bolov_medN = input_dict['filename_bolov_medN']
        self.filename_bolov_highN = input_dict['filename_bolov_highN']
        self.filename_bolov_unseeded_e2d = input_dict['filename_bolov_unseeded_e2d']
        self.filename_bolov_lowN_e2d = input_dict['filename_bolov_lowN_e2d']
        self.filename_bolov_medN_e2d = input_dict['filename_bolov_medN_e2d']
        self.filename_bolov_highN_e2d = input_dict['filename_bolov_highN_e2d']

        self.filename_spectroh_highN = input_dict['filename_spectroh_highN']
        self.filename_spectroh_medN = input_dict['filename_spectroh_medN']
        self.filename_spectroh_highN_e2d = input_dict['filename_spectroh_highN_e2d']
        self.filename_spectroh_medN_e2d = input_dict['filename_spectroh_medN_e2d']
        workfold = 'work/Python/EDGE2D'
        conf = self.conf
        date = conf.split('_')[0]
        seq = (conf.split('_')[1]).split('#')[1]
        self.sim_1 = sim(str((self.pulse)), str(date), str(seq), workfold)
        eproccat = ep.cat;
        self.tranfile = (eproccat(str((self.pulse)), str(date), str(seq),
                                  OWNER=self.sim_user,
                                  CODE='edge2d',
                                  MACHINE='jet')).__str__();
        if os.path.isfile(self.profile_omp) & os.path.isfile(
                self.profile_ot):
            logger.info('profile files exist')
        elif self.reload.lower() == 'yes':
            logger.info('profile files do NOT exist \n')
            logger.info('recalculating profiles \n')
            try:


                simlist = []
                simlist.append([self.sim_1, 'first'])
                sim.write_edge2d_profiles1(simlist, 'e2dprofiles_python')
                logger.info('profile created')

            except:
                logger.info('using user provided profiles')

                self.profile_omp= input_dict['omp_profiles']
                self.profile_ot = input_dict['ot_profiles']


        else:
            logger.info('profile files do NOT exist')
            try:


                simlist = []
                simlist.append([self.sim_1, 'first'])
                sim.write_edge2d_profiles1(simlist, 'e2dprofiles_python')
                logger.info('profile created')

            except:
                logger.info('using user provided profiles')

                self.profile_omp= input_dict['omp_profiles']
                self.profile_ot = input_dict['ot_profiles']


        try:
            self.e2d_profiles = pd.read_csv(self.profile_omp,skiprows=0,delim_whitespace=True)
        except:
            logger.info('no e2d omp data!')
        try:
            # ot profiles
            self.e2d_profiles_ot = pd.read_csv(self.profile_ot,skiprows=0,delim_whitespace=True)
        except:
            logger.info('no e2d ot data!')
        try:
            self.spectro_profiles_medN = pd.read_csv(
                self.filename_spectroh_medN, skiprows=6,
                delim_whitespace=True)
            self.spectro_profiles_highN = pd.read_csv(
                self.filename_spectroh_highN, skiprows=6,
                delim_whitespace=True)
            # e2d
            self.spectro_profiles_medN_e2d = pd.read_csv(
                self.filename_spectroh_medN_e2d, skiprows=6,
                delim_whitespace=True)
            self.spectro_profiles_highN_e2d = pd.read_csv(
                self.filename_spectroh_highN_e2d, skiprows=6,
                delim_whitespace=True)
        except:
            logger.info('no spectroscopy data')

        try:
            self.boloh_profiles_unseeded = pd.read_csv(self.filename_boloh_unseeded,
                                             skiprows=2,
                                             delim_whitespace=True)

            self.boloh_profiles_medN = pd.read_csv(self.filename_boloh_medN,
                                         skiprows=2, delim_whitespace=True)

            self.boloh_profiles_highN = pd.read_csv(self.filename_boloh_highN,
                                          skiprows=2, delim_whitespace=True)
        # e2d

            self.boloh_profiles_unseeded_e2d = pd.read_csv(
            self.filename_boloh_unseeded_e2d, skiprows=0,
            delim_whitespace=True)

            self.boloh_profiles_unseeded_e2d = pd.read_csv(
            self.filename_boloh_unseeded_e2d, skiprows=0,
            delim_whitespace=True)

            self.boloh_profiles_lowN_e2d = pd.read_csv(self.filename_boloh_lowN_e2d,
                                             skiprows=0,
                                             delim_whitespace=True)

            self.boloh_profiles_medN_e2d = pd.read_csv(self.filename_boloh_medN_e2d,
                                             skiprows=0,
                                             delim_whitespace=True)

            self.boloh_profiles_highN_e2d = pd.read_csv(self.filename_boloh_highN_e2d,
                                              skiprows=0,
                                              delim_whitespace=True)

            self.bolov_profiles_unseeded = pd.read_csv(self.filename_bolov_unseeded,
                                             skiprows=2, delim_whitespace=True)

            self.bolov_profiles_medN = pd.read_csv(self.filename_bolov_medN, skiprows=2,
                                         delim_whitespace=True)

            self.bolov_profiles_highN = pd.read_csv(self.filename_bolov_highN, skiprows=2,
                                          delim_whitespace=True)
        # e2d

            self.bolov_profiles_unseeded_e2d = pd.read_csv(
            self.filename_bolov_unseeded_e2d, skiprows=0, delim_whitespace=True)

            self.bolov_profiles_lowN_e2d = pd.read_csv(self.filename_bolov_lowN_e2d,
                                             skiprows=0, delim_whitespace=True)

            self.bolov_profiles_medN_e2d = pd.read_csv(self.filename_bolov_medN_e2d,
                                             skiprows=0, delim_whitespace=True)

            self.bolov_profiles_highN_e2d = pd.read_csv(self.filename_bolov_highN_e2d,
                                              skiprows=0, delim_whitespace=True)


        except:
            logger.info('no bolometric data')
        try:
            self.hrts_profiles = pd.read_csv(self.filename_hrts_data,skiprows=3,delim_whitespace=True)
        except:
            logger.info('no hrts data')


        try:
            self.hrts_fit = pd.read_csv(self.filename_hrts_fit, skiprows=3,
                                        delim_whitespace=True)
        except:
            logger.info('no hrts fit data')

        try:
            self.lp_profiles = pd.read_csv(self.filename_lp_data, skiprows=1,
                                      delim_whitespace=True)
        except:
            logger.info('no LPs data')
        try:
            self.ecm1_profiles = pd.read_csv(self.filename_ECM1_Te, skiprows=0,
                                        delim_whitespace=True)
        except:
            logger.info('no ECM1 data')
        try:
            self.hrtstecore_profiles = pd.read_csv(self.filename_HRTS_Te, skiprows=0,
                                              delim_whitespace=True)
            self.hrtsnecore_profiles = pd.read_csv(self.filename_HRTS_Ne, skiprows=0,
                                              delim_whitespace=True)
            self.hrtspecore_profiles = pd.read_csv(self.filename_HRTS_Pe, skiprows=0,
                                              delim_whitespace=True)
        except:
            logger.info('no HRTS core data')
        try:
            self.kg10_profiles = pd.read_csv(self.filename_KG10_Ne,skiprows=0,delim_whitespace=True)
        except:
            logger.info('no KG10 data')
        try:
            self.lidrte_profiles = pd.read_csv(self.filename_LIDR_Te,skiprows=0,delim_whitespace=True)
            self.lidrne_profiles = pd.read_csv(self.filename_LIDR_Ne,skiprows=0,delim_whitespace=True)
            self.lidrpe_profiles = pd.read_csv(self.filename_LIDR_Pe,skiprows=0,delim_whitespace=True)
        except:
            logger.info('no LIDAR data')
        # except :
        #     # logger.error("Could not read in simulation data")
        #     logger.error("Could not read in simulation data")

    def unseeded_analysis(self,ms = None, lw = None,color1=None):
        logger.debug('inside compare profiles')
        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw
        if color1 is None:
            color1 = 'black'
        else:
            color1 = color1

        try:
            fieldnames = list(self.e2d_profiles.columns.values)
            fieldnames = [x.strip() for x in fieldnames]
            fieldnames_ot = list(self.e2d_profiles_ot.columns.values)
            fieldnames_ot = [x.strip() for x in fieldnames_ot]

            # logger.info("Reading experimental data.")


            fieldnames_hrts = list(self.hrts_profiles.columns.values)
            fieldnames_hrts = [x.strip() for x in fieldnames_hrts]
            #
            fieldnames_hrts_fit = list(self.hrts_fit.columns.values)
            fieldnames_hrts_fit = [x.strip() for x in fieldnames_hrts_fit]
            logger.info(fieldnames)
            logger.info(fieldnames_ot)
            logger.info(fieldnames_hrts)
            logger.info(fieldnames_hrts_fit)
            logger.info(self.filename_hrts_data)


        except:
            logger.info('no HRTS data')
        try:
            fieldnames_lp = list(self.lp_profiles.columns.values)
            fieldnames_lp = [x.strip() for x in fieldnames_lp]
            logger.info(fieldnames_lp)
            logger.info(self.filename_lp_data)
        except:
            logger.info('no LP data')
            #==============================================================================


        try:
            fieldnames_ecm1 = list(self.ecm1_profiles.columns.values)
            fieldnames_ecm1 = [x.strip() for x in fieldnames_ecm1]
            logger.info(fieldnames_ecm1)
        except:
            logger.info('no ECM1 data')
        #==============================================================================


        try:
            fieldnames_hrtscore = list(self.hrtstecore_profiles.columns.values)
            fieldnames_hrtscore = [x.strip() for x in fieldnames_hrtscore]
            logger.info(fieldnames_hrtscore)
        except:
            logger.info('no HRTS core data')

            #==============================================================================


        try:
            fieldnames_kg10 = list(self.kg10_profiles.columns.values)
            fieldnames_kg10 = [x.strip() for x in fieldnames_kg10]
            logger.info(fieldnames_kg10)
        except:
            logger.info('no KG10 data')
            #==============================================================================


        try:
            fieldnames_lidr = list(self.lidrpe_profiles.columns.values)
            fieldnames_lidr = [x.strip() for x in fieldnames_lidr]
            logger.info(fieldnames_lidr)
        except:
            logger.info('no LIDAR data')
        try:
            fieldnames_spectro = list(self.spectro_profiles_highN.columns.values)
            fieldnames_spectro = [x.strip() for x in fieldnames_spectro]

            fieldnames_spectro_e2d = list(
                self.spectro_profiles_highN_e2d.columns.values)
            fieldnames_spectro_e2d = [x.strip() for x in fieldnames_spectro_e2d]
        except:
            logger.info('no SPECTRO data')
            #
            # logger.info(fieldnames_spectro)
            # logger.info(fieldnames_spectro_e2d)
        # except :
        #         logger.error("Could not read in experimental data")
                # logger.error("Could not read in experimental data")

        logger.info(self.pulse)
        logger.info(self.conf)






        # logger.info(hrtstecore_profiles)

        
        logger.info('filename simulation')
        logger.info(self.profile_omp)
        logger.info(self.profile_ot)
        


        # logger.info('plotting HRTS')
        # logger.info('plotting HRTS TE')
        # pdb.set_trace()

        try:

            logger.info('plotting HRTS TE')
            # logger.debug('%s',str(self.pulse))

            # print(self)

            fname = str(self.pulse) +'_'+str(self.label) + 'Te_omp'

            fnorm = 1
            ftitle = 'Electron Temperature OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$T_{e,OMP}\quad keV$'

            plt.figure(num=fname + "_" + self.label)

            

            if self.plot_sim == "True":
                try:

                    plt.scatter(self.e2d_profiles['dsrad_omp'],
                                self.e2d_profiles['te_omp'] / self.te_omp_factor,
                                label=self.conf+'_sim', color=color1)
                    logger.debug('try plotting e2d te self')

                except:

                    plt.scatter(self.e2d_profiles['dsrad'],self.e2d_profiles['teve'] / self.te_omp_factor,label=self.conf+'_sim', color=color1)
                    logger.debug('except plotting e2d ne self')
            #
            if self.plot_exp == "True":
                try:

                    plt.errorbar(self.hrts_profiles['RmRsep']+float(self.shift),self.hrts_profiles['TE'],label='_nolegend_', yerr=self.hrts_profiles['DTE'], fmt=None, ecolor=color1)
                except:
                    logger.error('no HRTS exp data')
                try:
                    plt.scatter(self.hrts_fit['Rfit']+float(self.shift_fit),self.hrts_fit['tef5']/self.te_omp_factor_exp,label='_nolegend_',color=color1)
                except:
                    logger.error('no HRTS fit data')



            plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
            # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color='k')
            axes = plt.axes()
            axes.set_xlim([-.15, .1])
            axes.set_ylim([0, 1.0])
            # axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            plt.legend(loc=0, prop={'size': 8})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs)))
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
            
            plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
            plt.ylabel(fylabel, {'color': 'k', 'size': 16})
            plt.savefig('./figures/' + fname+'_'+self.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+self.label, dpi=300)  #
            
            # raise SystemExit
        except :
            # logger.info("Could not plot HRTS Te")
            logger.error("Could not plot HRTS te")
    # %%

        #    logger.info('plotting HRTS NE')
        try:
            logger.info('plotting HRTS NE')
            # %%
            
            fname = str(self.pulse) +'_'+str(self.label) +   'ne_omp'
            fnorm = 1
            ftitle = 'Electron Density OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname + "_" + self.label)
            if self.plot_sim == "True":
                try:

                    plt.scatter(self.e2d_profiles['dsrad_omp'],
                                self.e2d_profiles['denel_omp'] / self.ne_omp_factor,
                                label=self.conf+'_sim', color=color1)
                    logger.debug('try plotting e2d ne self')

                except:

                    plt.scatter(self.e2d_profiles['dsrad'],
                                self.e2d_profiles['denel'] / self.ne_omp_factor,
                                label=self.conf+'_sim', color=color1)
                    logger.debug('except plotting e2d ne self')

            if self.plot_exp == "True":
                try:
                    plt.errorbar(self.hrts_profiles['RmRsep']+float(self.shift),self.hrts_profiles['NE'],label='_nolegend_', yerr=self.hrts_profiles['DNE'], fmt=None, ecolor=color1)
                except:
                    logger.error('impossible to plot HRTS NE data')
                try:
                    plt.scatter(self.hrts_fit['Rfit']+float(self.shift_fit),self.hrts_fit['nef3']/self.ne_omp_factor_exp,label='_nolegend_',color=color1)
                except:
                    logger.error('impossible to plot HRTS NE fit data')



            plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
            # plt.axhline(y=3.5, xmin=-.15, xmax=500, linewidth=2, color = 'k')

            axes = plt.axes()
            axes.set_xlim([-.15, .1])
            axes.set_ylim([0, 10.0])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])
            plt.legend(loc=2,prop={'size':8})



            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs)))
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
            plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
            plt.ylabel(fylabel, {'color': 'k', 'size': 16})
            plt.savefig('./figures/' + fname+'_'+self.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+self.label, dpi=300)  #
        except :
            logger.info("Could not plot HRTS ne")
            # logger.error("Could not plot HRTS ne")
        # logger.info('plotting ne_ot')
        try:
            logger.info('plotting ne_ot')
            fname = str(self.pulse) +'_'+str(self.label) +  +'ne_ot'
            fnorm=1
            ftitle='Electron Density OT'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$n_{e,OT}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname+"_"+self.label)
            # plt.suptitle(ftitle, fontsize=11)
            if self.plot_exp == "True":
                logger.debug('plot exp self true')
                try:
                    plt.scatter(self.lp_profiles['dSsep'],self.lp_profiles['ne'],label=self.conf+'_exp',color=color1)
                    logger.debug('here ne_ot')
                except:
                    logger.error('no ne LP exp data for self')
            if self.plot_sim == "True":
                logger.debug('plot sim self true')
                try:
                    plt.plot(self.e2d_profiles_ot['dsrad_ot'],self.e2d_profiles_ot['denel_ot'],'-',label=self.conf+'_sim',color=color1)
                    logger.debug('try plotting e2d ne self')
                except:
                    plt.plot(self.e2d_profiles_ot['dsrad'],self.e2d_profiles_ot['denel'],'-',label=self.conf+'_sim',color=color1)
                    logger.debug('except plotting e2d ne self')




            axes = plt.axes()
            axes.set_ylim(bottom=0)
            plt.legend(loc =0,prop={'size':18})




            plt.savefig('./figures/'+fname+'_'+self.label, format='eps', dpi=300)
            plt.savefig('./figures/'+fname+'_'+self.label,  dpi=300) #
        except :
            logger.error("Could not plot ne ot")
            # logger.error("Could not plot ne ot")
        #     logger.info('plotting te_ot')
        try:
            logger.info('plotting te_ot')
            fname = str(self.pulse) +'_'+str(self.label) +  'te_ot'
            fnorm=1
            ftitle='Electron Temperature OT'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$T_{e,OT}\quad keV$'

            plt.figure(num=fname+"_"+self.label)
            if self.plot_exp == "True":
                logger.debug('plot exp self true')
                try:
                    plt.scatter(self.lp_profiles['dSsep'],self.lp_profiles['te'],label=self.conf+'_exp',color=color1)
                    logger.debug('here te_ot')
                except:
                    logger.error('no te LP exp data for self')
            if self.plot_sim == "True":
                logger.debug('plot sim self true')
                try:
                    plt.plot(self.e2d_profiles_ot['dsrad_ot'],self.e2d_profiles_ot['te_ot'],'-',label=self.conf+'_sim',color=color1)
                    logger.debug('try plotting e2d te self')
                except:
                    plt.plot(self.e2d_profiles_ot['dsrad'],self.e2d_profiles_ot['teve'],'-',label=self.conf+'_sim',color=color1)
                    logger.debug('except plotting e2d te self')




            axes = plt.axes()
            axes.set_ylim(bottom=0)
            
            plt.legend(loc =0,prop={'size':18})
            #%%

            plt.savefig('./figures/'+fname+'_'+self.label, format='eps', dpi=300)
            plt.savefig('./figures/'+fname+'_'+self.label,  dpi=300) #
        except :
            logger.info("Could not plot te ot")
            # logger.error("Could not plot te ot")
        #     logger.info('plotting jsat_ot')
        try:
            logger.info('plotting jsat_ot')
            #%%
            fname = str(self.pulse) +'_'+str(self.label) + 'jsat_ot'
            ftitle='Saturation Current  OT'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$J_{sat,OT}\quad A m^{-2}$'
            plt.figure(num=fname + "_" + self.label)
            if self.plot_exp == "True":
                logger.debug('plot exp self true')
                try:
                    plt.scatter(self.lp_profiles['dSsep'],self.lp_profiles['jsat'],label=self.conf+'_exp',color=color1)
                    logger.debug('here jsat_ot')
                except:
                    logger.error('no jsat LP exp data for self')
            if self.plot_sim == "True":
                logger.debug('plot sim self true')
                try:
                    plt.plot(self.e2d_profiles_ot['dsrad_ot'],-self.e2d_profiles_ot['jtargi_ot'],'-',label=self.conf+'_sim',color=color1)
                    logger.debug('try plotting e2d jsat self')
                except:
                    plt.plot(self.e2d_profiles_ot['dsrad'],-self.e2d_profiles_ot['jtargi'],'-',label=self.conf+'_sim',color=color1)
                    logger.debug('except plotting e2d jsat self')




            axes = plt.axes()
            axes.set_ylim(bottom=0)
            plt.legend(loc =0,prop={'size':18})
            
            #%%
            # plt.tight_layout()
            plt.savefig('./figures/'+fname+'_'+self.label, format='eps', dpi=300)
            plt.savefig('./figures/'+fname+'_'+self.label,  dpi=300) #
        except :
            logger.error("Could not plot jsat")
                # logger.error("Could not plot jsat")
                         #%%
        try:
            logger.info('plotting dperp')
            fname = str(self.pulse) +'_'+str(self.label) +'dperp'
            fnorm=1
            ftitle='D perpendicular'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$D_{\perp}\quad   m^{2}/s})$'

            plt.figure(num=fname+"_"+self.label)
            if self.plot_sim == "True":
                try:
                    plt.scatter(self.e2d_profiles['dsrad_omp'],self.e2d_profiles['dperp_omp'],label=self.conf,color=color1)
                except:
                    plt.scatter(self.e2d_profiles['dsrad'],self.e2d_profiles['dperp'],label=self.conf,color=color1)
            axes = plt.axes()
            axes.set_ylim(bottom=0)
            plt.legend(loc =0,prop={'size':18})
            


        except :
            # logger.error("Could not plot dperp")
            logger.error("Could not plot dperp")
            #%%
        try:
            logger.info('plotting Xperp')
            fname = str(self.pulse) +'_'+str(self.label) + 'Xperp'
            fnorm=1
            ftitle='X perpendicular'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$X_{\perp}\quad   m^{2}/s})$'

            plt.figure(num=fname+"_"+self.label)
            # plt.suptitle(ftitle, fontsize=11)

            if self.plot_sim == "True":
                try:
                    plt.scatter(self.e2d_profiles['dsrad_omp'],self.e2d_profiles['chii_omp'],label=self.conf,color=color1)
                except:
                    plt.scatter(self.e2d_profiles['dsrad'],self.e2d_profiles['chii'],label=self.conf,color=color1)

            axes = plt.axes()
            axes.set_ylim(bottom=0)
            plt.legend(loc =0,prop={'size':18})
            

        except :
            # logger.error("Could not plot xperp")
            logger.error("Could not plot xperp")
            #logger.error("stop here")
            #%%

        try:
            logger.info('plotting HRTS NE/TE')
            # %%

            fname = str(self.pulse) + '_' + str(self.label) + '_ne_Te_omp'

            fnorm = 1
            ftitle = 'Electron Temperature OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$n_{e} and T_{e} normalized$'

            plt.figure(num=fname + "_" + self.label)

            # ax2 = ax1.twinx()
            # # ax1.yaxis.tick_right()
            # # ax1.yaxis.set_label_position('right')
            # ax2.set_ylabel('$T_{e,OMP}\quad keV$')
            # # ax2 = fig.add_subplot(111,sharex=ax1,frameon=False)



            if self.plot_sim == "True":
                try:
                    density = self.e2d_profiles['denel_omp'] / self.ne_omp_factor
                    temp = self.e2d_profiles['teve_omp'] / self.te_omp_factor
                    r_ped_mask = np.ma.masked_where((self.e2d_profiles['dsrad_omp'] > 0) , density)
                    index_ped = np.argmax(r_ped_mask)
                    density_ped = density[index_ped]

                    r_ped_mask = np.ma.masked_where(
                        (self.e2d_profiles['dsrad_omp'] > 0), temp)
                    index_ped = np.argmax(r_ped_mask)
                    temp_ped = temp[index_ped]

                    # data_masked = np.ma.masked_where((self.e2d_profiles['dsrad'] < -.15) | (self.e2d_profiles['dsrad'] > .1), density)
                    # index = np.argmax(data_masked)

                    # density = [2 * i / (density[index]) for i in
                    #            density]
                    # density_exp /= 2*np.max(np.abs(density_exp), axis=0)
                    # data_masked = np.ma.masked_where((self.e2d_profiles['dsrad'] < -.15) | (self.e2d_profiles['dsrad'] > .1), temp)
                    # index = np.argmax(data_masked)

                    # temp = [i / (temp[index]) for i in temp]
                    # density = [1*i /np.max(density) for i in density]
                    density = [i /density_ped for i in density]
                    # temp = [2*i /np.max(temp) for i in temp]
                    temp = [i /temp_ped for i in temp]

                    plt.scatter(self.e2d_profiles['dsrad_omp'],density,label=self.conf+'NE_sim', color='green')
                    plt.scatter(self.e2d_profiles['dsrad_omp'],temp,label=self.conf+'TE_sim', color='magenta',marker='^')




                    logger.debug('try plotting e2d ne/te pulse')

                except:
                    # pdb.set_trace()
                    density = self.e2d_profiles['denel'] / self.ne_omp_factor
                    temp = self.e2d_profiles['teve'] / self.te_omp_factor
                    r_ped_mask = np.ma.masked_where((self.e2d_profiles['dsrad'] > 0) , density)
                    index_ped = np.argmax(r_ped_mask)
                    density_ped = density[index_ped]

                    r_ped_mask = np.ma.masked_where(
                        (self.e2d_profiles['dsrad'] > 0), temp)
                    index_ped = np.argmax(r_ped_mask)
                    temp_ped = temp[index_ped]

                    # data_masked = np.ma.masked_where((self.e2d_profiles['dsrad'] < -.15) | (self.e2d_profiles['dsrad'] > .1), density)
                    # index = np.argmax(data_masked)

                    # density = [2 * i / (density[index]) for i in
                    #            density]
                    # density_exp /= 2*np.max(np.abs(density_exp), axis=0)
                    # data_masked = np.ma.masked_where((self.e2d_profiles['dsrad'] < -.15) | (self.e2d_profiles['dsrad'] > .1), temp)
                    # index = np.argmax(data_masked)

                    # temp = [i / (temp[index]) for i in temp]
                    # density = [1*i /np.max(density) for i in density]
                    density = [i /density_ped for i in density]
                    # temp = [2*i /np.max(temp) for i in temp]
                    temp = [i /temp_ped for i in temp]

                    plt.scatter(self.e2d_profiles['dsrad'],density,label=self.conf+'NE_sim', color='green')
                    plt.scatter(self.e2d_profiles['dsrad'],temp,label=self.conf+'TE_sim', color='magenta',marker='^')


                    logger.debug('except plotting e2d ne pulse')

            if self.plot_exp == "True":
                try:
                    # pdb.set_trace()
                    density_exp = self.hrts_profiles['NE']
                    temp_exp = self.hrts_profiles['TE']
                    # data_masked = np.ma.masked_where((self.hrts_profiles['RmRsep']+float(self.shift)<-.15) | (self.hrts_profiles['RmRsep']+float(self.shift)>0),density_exp)
                    # index = np.argmax(data_masked)
                    #
                    # density_exp = [ i / (density_exp[index]) for i in density_exp]
                    # # # density_exp /= 2*np.max(np.abs(density_exp), axis=0)
                    # data_masked1 = np.ma.masked_where((self.hrts_profiles['RmRsep']+float(self.shift)<-.15) | (self.hrts_profiles['RmRsep']+float(self.shift)>0),temp_exp)
                    # index1 = np.argmax(data_masked1)
                    # #
                    # temp_exp = [2*i / (temp_exp[index1]) for i in temp_exp]
                    ppfuid(str(self.hrts_uid), rw="R")
                    ihdata, iwdata, data, x, time, ier = ppfget(int(self.pulse[0:5]), str(self.hrts_ppf),'HN1')
                    ped_density=data[0]

                    ihdata, iwdata, data, x, time, ier = ppfget(
                        int(self.pulse[0:5]), str(self.hrts_ppf), 'HT1')
                    ped_temp=data[0]

                    density_exp /= ped_density
                    temp_exp /= ped_temp

                    plt.scatter(self.hrts_profiles['RmRsep']+float(self.shift),density_exp,label=None, color='green', s= 1)
                    plt.scatter(self.hrts_profiles['RmRsep']+float(self.shift),temp_exp,label=None, color='magenta',s = 1,marker='^')
                except:
                    logger.error('impossible to plot pulse NE TE from HRTS')
                try:
                    density_exp = self.hrts_fit['nef3']
                    temp_exp  = self.hrts_fit['tef5']
                    data_masked = np.ma.masked_where((self.hrts_profiles[
                                                          'RmRsep'] + float(
                        self.shift) < -.15) | (self.hrts_profiles[
                                                   'RmRsep'] + float(
                        self.shift) > .1), density_exp)
                    index = np.argmax(data_masked)

                    density_exp = [2 * i / (density_exp[index]) for i in
                                   density_exp]
                    # density_exp /= 2*np.max(np.abs(density_exp), axis=0)
                    data_masked = np.ma.masked_where((self.hrts_profiles[
                                                          'RmRsep'] + float(
                        self.shift) < -.15) | (self.hrts_profiles[
                                                   'RmRsep'] + float(
                        self.shift) > .1), temp_exp)
                    index = np.argmax(data_masked)

                    temp_exp = [i / (temp_exp[index]) for i in temp_exp]

                    # temp_exp /= np.max(np.abs(temp_exp), axis=0)
                    plt.scatter(self.hrts_fit['Rfit']+float(self.shift_fit),density_exp,label=None,color='green')
                    plt.scatter(self.hrts_fit['Rfit']+float(self.shift_fit),temp_exp,label=None,color=color1,marker='^')
                except:
                    logger.error('impossible to plot pulse NE TE HRTS fit')






            # ax1.set_ylim(bottom=0)

            plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
            # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color='k')
            axes = plt.axes()
            axes.set_xlim([-.15, .1])
            axes.set_ylim([0, 2.0])
            # axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            plt.legend(loc=0, prop={'size': 8})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs)))
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs)))

            plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
            plt.ylabel(fylabel, {'color': 'k', 'size': 16})
            plt.savefig('./figures/' + fname + '_' + self.label, format='eps',
                        dpi=300)
            plt.savefig('./figures/' + fname + '_' + self.label, dpi=300)  #

        except :
            logger.error("Could not plot HRTS ne/te data")
        # pdb.set_trace()



        #
        # try:
        #     logger.info('plotting OMP Te')
        #     #%%
        #     fname = str(self.pulse) +'_'+str(self.label) + 'OMP Te Core'
        #     plt.figure(num=fname+"_"+self.label)
        #     ftitle='OMP Te'
        #     fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
        #     fylabel='$T_{e} keV$'
        #     axes = plt.axes()
        #     if self.plot_exp == "True":
        #         try:
        #             plt.scatter(self.hrtstecore_profiles['Rmaj(m)']-3.8+float(self.shift),self.hrtstecore_profiles['Te(keV)'],label='te_omp_hrts',color='black')
        #         except:
        #             FileNotFoundError
        #         try:
        #             plt.scatter(self.lidrte_profiles['Rmaj(m)']-3.8+float(self.shift),self.lidrte_profiles['Te(keV)'],label='te_omp_lidr',color='red')
        #         except:
        #             FileNotFoundError
        #         try:
        #             plt.scatter(self.ecm1_profiles['Rmaj(m)'] - 3.8 + float(self.shift),self.ecm1_profiles['Te(keV)'], label='te_omp_ecm1', color='blue')
        #         except:
        #             FileNotFoundError
        #         try:
        #             plt.scatter(self.hrts_fit['Rfit']+float(self.shift),self.hrts_fit['tef5']/1e3,label='_nolegend_',color='red')
        #         except:
        #             logger.info('no HRTS fit data')
        #
        #     plt.savefig('./figures/'+fname+'_'+self.label, format='eps', dpi=300)
        #     plt.savefig('./figures/'+fname+'_'+self.label,  dpi=300) #
        #     # plt.tight_layout()
        # except :
        #         # logger.error("Could not plot te omp")
        #         logger.error("Could not plot te omp")
        # try:
        #     logger.info('plotting OMP pressure')
        #     #%%
        #     fname = str(self.pulse) +'_'+str(self.label) + 'OMP pressure'
        #     #fnorm=1e-6
        #     plt.figure(num=fname+"_"+self.label)
        #     ftitle='OMP pressure'
        #     fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
        #     fylabel='$pressure kPa$'
        #     axes = plt.axes()
        #
        #     if self.plot_exp == "True":
        #         try:
        #             plt.scatter(self.hrtspecore_profiles['Rmaj(m)']+float(self.shift),self.hrtspecore_profiles['Pe(kPa)'],label='Press_omp_hrts',color='black')
        #             plt.scatter(self.lidrpe_profiles['Rmaj(m)']+float(self.shift),self.lidrpe_profiles['Pe(kPa)'],label='Press_omp_lidr',color='red')
        #         except:
        #             logger.error("Could not plot OMP pressure")
        #     plt.savefig('./figures/'+fname+'_'+self.label, format='eps', dpi=300)
        #     plt.savefig('./figures/'+fname+'_'+self.label,  dpi=300) #
        #     # plt.tight_layout()
        #
        # except :
        #         # logger.error("Could not plot omp pressure")
        #         logger.error("Could not plot omp pressure")


        plt.show(block=True)

        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')



    def plot_bolo_hv(self,ms = None, lw = None,vert=True,color=None,bound=None):
        if bound is None:
            bound=1.6e6
        else:
            bound=bound
        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw
        if color is None:
            color = 'black'
        else:
            lw = color
        if vert:
            name='KB5V'
            channel = 'VERT'

            bolo_profiles_unseeded		=		self.bolov_profiles_unseeded
            bolo_profiles_medN			=	self.bolov_profiles_medN
            bolo_profiles_highN		=		self.bolov_profiles_highN
            bolo_profiles_unseeded_e2d	=			self.bolov_profiles_unseeded_e2d
            bolo_profiles_unseeded_e2d	=			self.bolov_profiles_unseeded_e2d
            bolo_profiles_lowN_e2d		=		self.bolov_profiles_lowN_e2d
            bolo_profiles_medN_e2d		=		self.bolov_profiles_medN_e2d
            bolo_profiles_highN_e2d	=			self.bolov_profiles_highN_e2d

        else:
            name='KB5H'
            channel='HORI'
            bolo_profiles_unseeded = self.boloh_profiles_unseeded
            bolo_profiles_medN = self.boloh_profiles_medN
            bolo_profiles_highN = self.boloh_profiles_highN
            bolo_profiles_unseeded_e2d = self.boloh_profiles_unseeded_e2d
            bolo_profiles_unseeded_e2d = self.boloh_profiles_unseeded_e2d
            bolo_profiles_lowN_e2d = self.boloh_profiles_lowN_e2d
            bolo_profiles_medN_e2d = self.boloh_profiles_medN_e2d
            bolo_profiles_highN_e2d = self.boloh_profiles_highN_e2d


        # %%
        fieldnames_h = list(bolo_profiles_unseeded.columns.values)
        fieldnames_h = [x.strip() for x in fieldnames_h]

        fieldnames_h_e2d = list(
            bolo_profiles_unseeded_e2d.columns.values)
        fieldnames_h_e2d = [x.strip() for x in fieldnames_h_e2d]
        #
        logger.info(fieldnames_h)
        logger.info(fieldnames_h_e2d)
        # %%
        # plt.close("all")
        fname = name+'_AVG_unseeded aug2017'
        fnorm = 1
        ftitle = name+'_AVG_unseeded aug2017'
        # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
        # fylabel='$I_{pump} (10^{22} s^{-1})$'
        fxlabel = '$deg$'
        fylabel = '$KB5H_{AVG} \quad (MW/m^2)$'

        plt.figure(num=fname)

        plt.scatter(bolo_profiles_unseeded[name+'_R'],
                    bolo_profiles_unseeded[name], label='', color=color,
                    s=ms, linewidth=lw)

        plt.plot(bolo_profiles_unseeded_e2d['PB5_'+channel+'_x'],
                 bolo_profiles_unseeded_e2d['PB5_'+channel+'_y'], marker='+',
                 label='_nolegend_', color=color, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(bolo_profiles_medN[name+'_R']) + min(
            bolo_profiles_medN[name+'_R'])) / 2, (
                     max(bolo_profiles_unseeded[name]) + min(
                         bolo_profiles_unseeded[name])) / 2, "unseeded",
                 {'fontsize': 30})
        axes = plt.axes()
        axes.set_xlim([min(bolo_profiles_unseeded[name+'_R']),
                       max(bolo_profiles_unseeded[name+'_R'])])
        axes.set_ylim([0, float(bound)])
        # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
        # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

        #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
        plt.legend(loc=2, prop={'size': 30})
        locs, labels = xticks()
        xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)), fontsize=20)
        # plt.tight_layout()
        plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
        plt.ylabel(fylabel, {'color': 'k', 'size': 28})
        #    plt.ioff()
        plt.tight_layout()
        # plt.savefig(fname,dpi=300) #
        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # plt.show(block=True)
        # %%
        # %%
        # plt.close("all")
        fname = name+'_AVG_medN aug2017'
        fnorm = 1
        ftitle = name+'_AVG_medN aug2017'
        # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
        # fylabel='$I_{pump} (10^{22} s^{-1})$'
        fxlabel = '$deg$'
        fylabel = '$KB5V_{AVG} \quad (MW/m^2)$'

        plt.figure(num=fname)

        # Now let's extract only the part of the data we're interested in...
        # x_filt = bolo_profiles_h_medN[name+'_R'][bolo_profiles_h_medN[name] > 0]
        # y_filt = bolo_profiles_medN[name][bolo_profiles_medN[name] > 0]
        plt.scatter(bolo_profiles_medN[name+'_R'],
                    bolo_profiles_medN[name], label='', color=color,
                    s=ms, linewidth=lw)

        plt.plot(bolo_profiles_lowN_e2d['PB5_'+channel+'_x'],
                 bolo_profiles_lowN_e2d['PB5_'+channel+'_y'], marker='+',
                 label='_nolegend_', color=color, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(bolo_profiles_medN[name+'_R']) + min(
            bolo_profiles_medN[name+'_R'])) / 2.1, (
                     max(bolo_profiles_medN[name]) + min(
                         bolo_profiles_medN[name])) / 2, "med seeding",
                 {'fontsize': 30})
        # plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
        # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
        axes = plt.axes()
        axes.set_xlim([min(bolo_profiles_medN[name+'_R']),
                       max(bolo_profiles_medN[name+'_R'])])
        axes.set_ylim([0, bound])
        # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
        # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

        #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
        plt.legend(loc=2, prop={'size': 30})
        locs, labels = xticks()
        xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)), fontsize=20)
        # plt.tight_layout()
        plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
        plt.ylabel(fylabel, {'color': 'k', 'size': 28})
        #    plt.ioff()
        plt.tight_layout()
        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

        # plt.show(block=True)
        # %%
        # %%
        # plt.close("all")
        fname = name+'_AVG_highN aug2017'
        fnorm = 1
        ftitle = name+'_AVG_highN aug2017'
        # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
        # fylabel='$I_{pump} (10^{22} s^{-1})$'
        fxlabel = '$deg$'
        fylabel = '$KB5V_{AVG} \quad (MW/m^2)$'

        plt.figure(num=fname)

        # plt.suptitle(ftitle, fontsize=11)
        # plt.scatter(self.e2d_profiles['DET_DEG'],self.e2d_profiles[name]/1e3,label='Te_omp_e2d',color='blue')

        plt.scatter(bolo_profiles_highN[name+'_R'],
                    bolo_profiles_highN[name], label='',
                    color=color, s=ms, linewidth=lw)

        plt.plot(bolo_profiles_highN_e2d['PB5_'+channel+'_x'],
                 bolo_profiles_highN_e2d['PB5_'+channel+'_y'], marker='+',
                 label='_nolegend_', color=color, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(bolo_profiles_medN[name+'_R']) + min(
            bolo_profiles_medN[name+'_R'])) / 2.1, (
                     max(bolo_profiles_highN[name]) + min(
                         bolo_profiles_highN[name])) / 2, "high seeding",
                 {'fontsize': 30})
        # plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
        # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
        axes = plt.axes()
        axes.set_xlim([min(bolo_profiles_highN[name+'_R']),
                       max(bolo_profiles_highN[name+'_R'])])
        axes.set_ylim([0, bound])
        # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
        # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

        #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
        plt.legend(loc=2, prop={'size': 30})
        locs, labels = xticks()
        xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)), fontsize=20)
        # plt.tight_layout()
        plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
        plt.ylabel(fylabel, {'color': 'k', 'size': 28})
        #    plt.ioff()
        plt.tight_layout()
        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  # #

        plt.show(block=True)
        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')

    def plot_spectr(self,ms = None, lw = None,color=None):
        logger.debug('inside')
        # if bound is None:
        #     bound=1.6e6
        # else:
        #     bound=bound
        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw
        if color is None:
            color = 'black'
        else:
            lw = color
        fname = 'spectro_'+str(self.pulse)
        fnorm = 1
        ftitle = 'spectro_'+str(self.pulse)
        fxlabel = '$R \quad [m[$'
        fylabel = '$Electron\	density\	from\	Stark\	broadening \quad	[m^{-3}]$'

        plt.figure(num=fname)


        plt.scatter(self.spectro_profiles_highN['R'],
                    self.spectro_profiles_highN['ne'], marker='+', label='LFE',
                    color='black', s=ms + 3, linewidth=lw)


        plt.plot(self.spectro_profiles_highN_e2d['R'],
                 self.spectro_profiles_highN_e2d['ne'], marker='1',
                 label='_nolegend_', color=color, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(self.spectro_profiles_highN['R']) + min(
            self.spectro_profiles_highN['R'])) / 1.9, (
                 max(self.spectro_profiles_highN['ne']) + min(
                     self.spectro_profiles_highN['ne'])) / 2, "highN",
                 {'fontsize': 30})
        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')


        axes = plt.axes()

        axes.set_xlim([2.485, 2.9])

        plt.legend(loc=0, prop={'size': 20})


        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

        # %%
        fname = 'spectro_'+str(self.pulse)+'$D_{\delta}\  radiance'
        fnorm = 1
        ftitle = 'spectro_'+str(self.pulse)+'  radiance'
        fxlabel = '$R \quad [m[$'
        fylabel = '$D_{\delta}\ I\ radiance  \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)


        plt.scatter(self.spectro_profiles_highN['R'],
                    self.spectro_profiles_highN['DI'], marker='+', label='LFE',
                    color='black', s=ms + 3, linewidth=lw)

        plt.plot(self.spectro_profiles_highN_e2d['R'],
                 self.spectro_profiles_highN_e2d['DI'], marker='1',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)


        plt.text((max(self.spectro_profiles_highN['R']) + min(
            self.spectro_profiles_highN['R'])) / 2, (
                 max(self.spectro_profiles_highN['DI']) + min(
                     self.spectro_profiles_highN['DI'])) / 2, "highN",
                 {'fontsize': 30})
        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')



        axes = plt.axes()
        axes.set_xlim([2.485, 2.9])
        plt.legend(loc=0, prop={'size': 20})

        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})
        #

        #
        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # %%

        fname = 'spectro_'+str(self.pulse)+'_N_lines radiance'
        fnorm = 1
        ftitle = 'spectro_'+str(self.pulse)+'_N_lines radiance'
        fxlabel = '$R \quad [m]$'
        fylabel = '$N\ lines\ radiance\ \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        nii = normalize(self.spectro_profiles_highN['NII'])
        niii = normalize(self.spectro_profiles_highN['NIII'])
        niv = normalize(self.spectro_profiles_highN['NIV'])

        nii_e2d = normalize(self.spectro_profiles_highN_e2d['NII'])
        niii_e2d = normalize(self.spectro_profiles_highN_e2d['NIII'])
        niv_e2d = normalize(self.spectro_profiles_highN_e2d['NIV'])

        plt.scatter(self.spectro_profiles_highN['R'], nii, marker='x',
                    label='N II', color='black', s=ms + 3, linewidth=lw)
        plt.scatter(self.spectro_profiles_highN['R'], niii, marker='_',
                    label='N III', color='black', s=ms + 3, linewidth=lw)
        plt.scatter(self.spectro_profiles_highN['R'], niv, marker='3',
                    label='N IV', color='black', s=ms + 3, linewidth=lw)



        plt.plot(self.spectro_profiles_highN_e2d['R'], nii_e2d, marker='x',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)
        plt.plot(self.spectro_profiles_highN_e2d['R'], niii_e2d, marker='_',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)
        plt.plot(self.spectro_profiles_highN_e2d['R'], niv_e2d, marker='3',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)


        plt.text((max(self.spectro_profiles_highN['R']) + min(
            self.spectro_profiles_highN['R'])) / 1.9,
                 (max(niii) + min(niii)) / 2, "highN", {'fontsize': 30})
        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')
        axes = plt.axes()
        axes.set_xlim([2.485, 2.9])
        #

        plt.legend(loc=0, prop={'size': 20})
        #
        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # # 92123 just exp nitrogen lines

        fname = 'exp spectro_'+str(self.pulse)+'_N_lines'
        fnorm = 1
        ftitle = 'exp spectro_'+str(self.pulse)+'_N_lines'
        fxlabel = '$R \quad [m]$'
        fylabel = '$N\ lines\ radiance\ \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        nii = normalize(self.spectro_profiles_highN['NII'])
        niii = normalize(self.spectro_profiles_highN['NIII'])
        niv = normalize(self.spectro_profiles_highN['NIV'])

        plt.plot(self.spectro_profiles_highN['R'], nii, '-', label='N II',
                 color='black', markersize=ms + 3, linewidth=lw)
        plt.plot(self.spectro_profiles_highN['R'], niii, '--',
                 label='N III', color='black', markersize=ms + 3, linewidth=lw)
        plt.plot(self.spectro_profiles_highN['R'], niv, '-.', label='N IV',
                 color='black', markersize=ms + 3, linewidth=lw)


        plt.text((max(self.spectro_profiles_highN['R']) + min(
            self.spectro_profiles_highN['R'])) / 1.9,
                 (max(niii) + min(niii)) / 2, "highN", {'fontsize': 30})

        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')



        axes = plt.axes()
        axes.set_xlim([2.485, 2.9])

        #
        # #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
        plt.legend(loc=0, prop={'size': 20})

        #
        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})

        # plt.tight_layout()

        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        #
        # #
        # #
        fname = 'spectro_'+str(self.pulse)+' low seeding'
        fnorm = 1
        ftitle = 'spectro_'+str(self.pulse)+' low seeding'
        fxlabel = '$R \quad [m[$'
        fylabel = '$Electron\	density\	from\	Stark\	broadening \quad	[m^{-3}]$'

        plt.figure(num=fname)


        plt.scatter(self.spectro_profiles_medN['R'],
                    self.spectro_profiles_medN['ne'], marker='+', label='LFE',
                    color='black', s=ms + 3, linewidth=lw)

        plt.plot(self.spectro_profiles_medN_e2d['R'],
                 self.spectro_profiles_medN_e2d['ne'], marker='1',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(self.spectro_profiles_medN['R']) + min(
            self.spectro_profiles_medN['R'])) / 2, (
                 max(self.spectro_profiles_medN['ne']) + min(
                     self.spectro_profiles_medN['ne'])) / 2, "highN",
                 {'fontsize': 30})

        axes = plt.axes()
        axes.set_xlim([min(self.spectro_profiles_medN['R']),
                       max(self.spectro_profiles_medN['R'])])

        plt.legend(loc=0, prop={'size': 30})


        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})

        # plt.tight_layout()

        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

        # %%
        # %%
        # plt.close("all")
        fname = 'spectro_'+str(self.pulse)+'_N_lines low seeding'
        fnorm = 1
        ftitle = 'spectro_'+str(self.pulse)+'_N_lines low seeding'

        fxlabel = '$R \quad [m]$'
        fylabel = '$N\ lines\ radiance\ \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        nii = normalize(self.spectro_profiles_medN['NII'])
        niii = normalize(self.spectro_profiles_medN['NIII'])
        niv = normalize(self.spectro_profiles_medN['NIV'])


        nii_e2d = normalize(self.spectro_profiles_medN_e2d['NII'])
        niii_e2d = normalize(self.spectro_profiles_medN_e2d['NIII'])
        niv_e2d = normalize(self.spectro_profiles_medN_e2d['NIV'])


        plt.scatter(self.spectro_profiles_medN['R'], nii, marker='x',
                    label='N II', color='black', s=ms + 3, linewidth=lw)
        plt.scatter(self.spectro_profiles_medN['R'], niii, marker='_',
                    label='N III', color='black', s=ms + 3, linewidth=lw)
        plt.scatter(self.spectro_profiles_medN['R'], niv, marker='3',
                    label='N IV', color='black', s=ms + 3, linewidth=lw)

        plt.plot(self.spectro_profiles_medN_e2d['R'], nii_e2d, marker='x',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)
        plt.plot(self.spectro_profiles_medN_e2d['R'], niii_e2d, marker='_',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)
        plt.plot(self.spectro_profiles_medN_e2d['R'], niv_e2d, marker='3',
                 label='_nolegend_', color='black', markersize=ms + 3,
                 linewidth=lw)


        plt.text((max(self.spectro_profiles_medN['R']) + min(
            self.spectro_profiles_medN['R'])) / 1.9,
                 (max(nii) + min(nii)) / 2, "medN", {'fontsize': 30})

        axes = plt.axes()


        plt.legend(loc=0, prop={'size': 20})

        #
        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # %%
        fname = 'spectro_'+str(self.pulse)+' radiance low seeding'
        fnorm = 1
        ftitle = 'spectro_'+str(self.pulse)+' radiance low seeding'
        # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
        # fylabel='$I_{pump} (10^{22} s^{-1})$'
        fxlabel = '$R \quad [m[$'
        fylabel = '$D_{\delta}\ I \  radiance \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        plt.scatter(self.spectro_profiles_medN['R'],
                    self.spectro_profiles_medN['DI'], marker='+', label='LFE',
                    color=color, s=ms + 3, linewidth=lw)

        plt.plot(self.spectro_profiles_medN_e2d['R'],
                 self.spectro_profiles_medN_e2d['DI'], marker='+',
                 label='_nolegend_', color=color, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(self.spectro_profiles_medN['R']) + min(
            self.spectro_profiles_medN['R'])) / 2, (
                 max(self.spectro_profiles_medN['DI']) + min(
                     self.spectro_profiles_medN['DI'])) / 2, "highN",
                 {'fontsize': 30})

        axes = plt.axes()
        axes.set_xlim([min(self.spectro_profiles_medN['R']),
                       max(self.spectro_profiles_medN['R'])])

        plt.legend(loc=0, prop={'size': 20})


        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        plt.show(block=True)
        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')

    @staticmethod
    def compare_spectr(pulse1,pulse2,ms = None, lw = None,color1=None,color2=None):
        logger.debug('inside')
        # if bound is None:
        #     bound=1.6e6
        # else:
        #     bound=bound
        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw
        if color1 is None:
            color1 = 'black'
        else:
            color1 = color1
        if color2 is None:
            color2 = 'red'
        else:
            color2 = color2
        fname = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)
        fnorm = 1
        ftitle = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)
        fxlabel = '$R \quad [m[$'
        fylabel = '$Electron\	density\	from\	Stark\	broadening \quad	[m^{-3}]$'

        plt.figure(num=fname)


        plt.scatter(pulse1.spectro_profiles_highN['R'],
                    pulse1.spectro_profiles_highN['ne'], marker='+', label='92121',
                    color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_highN['R'],
                    pulse2.spectro_profiles_highN['ne'], marker='+', label='92123',
                    color=color2, s=ms + 3, linewidth=lw)

        plt.plot(pulse1.spectro_profiles_highN_e2d['R'],
                 pulse1.spectro_profiles_highN_e2d['ne'], marker='1',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN_e2d['R'],
                 pulse2.spectro_profiles_highN_e2d['ne'], marker='1',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(pulse1.spectro_profiles_highN['R']) + min(
            pulse1.spectro_profiles_highN['R'])) / 1.9, (
                 max(pulse1.spectro_profiles_highN['ne']) + min(
                     pulse1.spectro_profiles_highN['ne'])) / 2, "highN",
                 {'fontsize': 30})
        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.490, ymin=0., ymax=500, linewidth=2, color='r',
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')
        plt.axvline(x=2.650, ymin=0., ymax=500, linewidth=2, color='r')

        axes = plt.axes()

        axes.set_xlim([2.485, 2.9])

        plt.legend(loc=0, prop={'size': 20})


        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})

        # plt.tight_layout()

        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

        # %%
        fname = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+'  radiance'
        fnorm = 1
        ftitle = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+'  radiance'
        fxlabel = '$R \quad [m[$'
        fylabel = '$D_{\delta}\ I\ radiance  \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)


        plt.scatter(pulse1.spectro_profiles_highN['R'],
                    pulse1.spectro_profiles_highN['DI'], marker='+', label='92121',
                    color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_highN['R'],
                    pulse2.spectro_profiles_highN['DI'], marker='+', label='92123',
                    color=color2, s=ms + 3, linewidth=lw)

        plt.plot(pulse1.spectro_profiles_highN_e2d['R'],
                 pulse1.spectro_profiles_highN_e2d['DI'], marker='1',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN_e2d['R'],
                 pulse2.spectro_profiles_highN_e2d['DI'], marker='1',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(pulse1.spectro_profiles_highN['R']) + min(
            pulse1.spectro_profiles_highN['R'])) / 2, (
                 max(pulse1.spectro_profiles_highN['DI']) + min(
                     pulse1.spectro_profiles_highN['DI'])) / 2, "highN",
                 {'fontsize': 30})
        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.490, ymin=0., ymax=500, linewidth=2, color=color2,
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')
        plt.axvline(x=2.650, ymin=0., ymax=500, linewidth=2, color=color2)


        axes = plt.axes()
        axes.set_xlim([2.485, 2.9])
        plt.legend(loc=0, prop={'size': 20})

        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})
        #

        #
        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # %%

        fname = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+'_N_lines'
        fnorm = 1
        ftitle = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+'_N_lines'
        fxlabel = '$R \quad [m]$'
        fylabel = '$N\ lines\ radiance\ \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        nii = normalize(pulse1.spectro_profiles_highN['NII'])
        niii = normalize(pulse1.spectro_profiles_highN['NIII'])
        niv = normalize(pulse1.spectro_profiles_highN['NIV'])
        nii_hfs = normalize(pulse2.spectro_profiles_highN['NII'])
        niii_hfs = normalize(pulse2.spectro_profiles_highN['NIII'])
        niv_hfs = normalize(pulse2.spectro_profiles_highN['NIV'])

        nii_e2d = normalize(pulse1.spectro_profiles_highN_e2d['NII'])
        niii_e2d = normalize(pulse1.spectro_profiles_highN_e2d['NIII'])
        niv_e2d = normalize(pulse1.spectro_profiles_highN_e2d['NIV'])
        nii_hfs_e2d = normalize(pulse2.spectro_profiles_highN_e2d['NII'])
        niii_hfs_e2d = normalize(pulse2.spectro_profiles_highN_e2d['NIII'])
        niv_hfs_e2d = normalize(pulse2.spectro_profiles_highN_e2d['NIV'])

        plt.scatter(pulse1.spectro_profiles_highN['R'], nii, marker='x',
                    label='N II', color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse1.spectro_profiles_highN['R'], niii, marker='_',
                    label='N III', color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse1.spectro_profiles_highN['R'], niv, marker='3',
                    label='N IV', color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_highN['R'], nii_hfs, marker='x',
                    label='_nolegend_', color=color2, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_highN['R'], niii_hfs, marker='_',
                    label='_nolegend_', color=color2, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_highN['R'], niv_hfs, marker='3',
                    label='_nolegend_', color=color2, s=ms + 3, linewidth=lw)



        plt.plot(pulse1.spectro_profiles_highN_e2d['R'], nii_e2d, marker='x',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse1.spectro_profiles_highN_e2d['R'], niii_e2d, marker='_',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse1.spectro_profiles_highN_e2d['R'], niv_e2d, marker='3',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN_e2d['R'], nii_hfs_e2d, marker='x',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN_e2d['R'], niii_hfs_e2d, marker='_',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN_e2d['R'], niv_hfs_e2d, marker='3',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(pulse1.spectro_profiles_highN['R']) + min(
            pulse1.spectro_profiles_highN['R'])) / 1.9,
                 (max(niii) + min(niii)) / 2, "highN", {'fontsize': 30})
        # #plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
        # #plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.490, ymin=0., ymax=500, linewidth=2, color=color2,
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')
        plt.axvline(x=2.650, ymin=0., ymax=500, linewidth=2, color=color2)

        # #plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
        axes = plt.axes()
        axes.set_xlim([2.485, 2.9])
        #

        plt.legend(loc=0, prop={'size': 20})
        #
        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # # 92123 just exp nitrogen lines
        fname = 'exp spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+'_N_lines'
        fnorm = 1
        ftitle = 'exp spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+'_N_lines'
        fxlabel = '$R \quad [m]$'
        fylabel = '$N\ lines\ radiance\ \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        nii = normalize(pulse1.spectro_profiles_highN['NII'])
        niii = normalize(pulse1.spectro_profiles_highN['NIII'])
        niv = normalize(pulse1.spectro_profiles_highN['NIV'])
        nii_hfs = normalize(pulse2.spectro_profiles_highN['NII'])
        niii_hfs = normalize(pulse2.spectro_profiles_highN['NIII'])
        niv_hfs = normalize(pulse2.spectro_profiles_highN['NIV'])

        # nii_e2d = normalize(pulse1.spectro_profiles_highN_e2d['NII'])
        # niii_e2d = normalize(pulse1.spectro_profiles_highN_e2d['NIII'])
        # niv_e2d = normalize(pulse1.spectro_profiles_highN_e2d['NIV'])
        # nii_hfs_e2d = normalize(pulse2.spectro_profiles_highN_e2d['NII'])
        # niii_hfs_e2d = normalize(pulse2.spectro_profiles_highN_e2d['NIII'])
        # niv_hfs_e2d = normalize(pulse2.spectro_profiles_highN_e2d['NIV'])

        plt.plot(pulse1.spectro_profiles_highN['R'], nii, '-', label='N II',
                 color=color1, markersize=ms + 3, linewidth=lw)
        plt.plot(pulse1.spectro_profiles_highN['R'], niii, '--',
                 label='N III', color=color1, markersize=ms + 3, linewidth=lw)
        plt.plot(pulse1.spectro_profiles_highN['R'], niv, '-.', label='N IV',
                 color=color1, markersize=ms + 3, linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN['R'], nii_hfs, '-',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN['R'], niii_hfs, '--',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_highN['R'], niv_hfs, '-.',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)



        plt.text((max(pulse1.spectro_profiles_highN['R']) + min(
            pulse1.spectro_profiles_highN['R'])) / 1.9,
                 (max(niii) + min(niii)) / 2, "highN", {'fontsize': 30})

        plt.axvline(x=2.560, ymin=0., ymax=500, linewidth=2, color='k',
                    linestyle='--')
        plt.axvline(x=2.490, ymin=0., ymax=500, linewidth=2, color=color2,
                    linestyle='--')
        plt.axvline(x=2.710, ymin=0., ymax=500, linewidth=2, color='k')
        plt.axvline(x=2.650, ymin=0., ymax=500, linewidth=2, color=color2)


        axes = plt.axes()
        axes.set_xlim([2.485, 2.9])

        #
        # #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
        plt.legend(loc=0, prop={'size': 20})

        #
        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})

        # plt.tight_layout()

        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        #
        # #
        # #
        fname = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+' low seeding'
        fnorm = 1
        ftitle = 'spectro_'+str(pulse1.pulse)+str(pulse2.pulse)+' low seeding'
        fxlabel = '$R \quad [m[$'
        fylabel = '$Electron\	density\	from\	Stark\	broadening \quad	[m^{-3}]$'

        plt.figure(num=fname)


        plt.scatter(pulse1.spectro_profiles_medN['R'],
                    pulse1.spectro_profiles_medN['ne'], marker='+', label='92121',
                    color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_medN['R'],
                    pulse2.spectro_profiles_medN['ne'], marker='+', label='92123',
                    color=color2, s=ms + 3, linewidth=lw)

        plt.plot(pulse1.spectro_profiles_medN_e2d['R'],
                 pulse1.spectro_profiles_medN_e2d['ne'], marker='1',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_medN_e2d['R'],
                 pulse2.spectro_profiles_medN_e2d['ne'], marker='1',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(pulse1.spectro_profiles_medN['R']) + min(
            pulse1.spectro_profiles_medN['R'])) / 2, (
                 max(pulse1.spectro_profiles_medN['ne']) + min(
                     pulse1.spectro_profiles_medN['ne'])) / 2, "highN",
                 {'fontsize': 30})

        axes = plt.axes()
        axes.set_xlim([min(pulse1.spectro_profiles_medN['R']),
                       max(pulse1.spectro_profiles_medN['R'])])

        plt.legend(loc=0, prop={'size': 30})


        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})

        # plt.tight_layout()

        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

        # %%
        # %%
        # plt.close("all")
        fname = 'spectro_'+str(pulse1.pulse)+'_'+str(pulse2.pulse)+'_N_lines low seeding'
        fnorm = 1
        ftitle = 'spectro_'+str(pulse1.pulse)+'_'+str(pulse2.pulse)+'_N_lines low seeding'
        fxlabel = '$R \quad [m]$'
        fylabel = '$N\ lines\ radiance\ \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        nii = normalize(pulse1.spectro_profiles_medN['NII'])
        niii = normalize(pulse1.spectro_profiles_medN['NIII'])
        niv = normalize(pulse1.spectro_profiles_medN['NIV'])
        nii_hfs = normalize(pulse2.spectro_profiles_medN['NII'])
        niii_hfs = normalize(pulse2.spectro_profiles_medN['NIII'])
        niv_hfs = normalize(pulse2.spectro_profiles_medN['NIV'])

        nii_e2d = normalize(pulse1.spectro_profiles_medN_e2d['NII'])
        niii_e2d = normalize(pulse1.spectro_profiles_medN_e2d['NIII'])
        niv_e2d = normalize(pulse1.spectro_profiles_medN_e2d['NIV'])
        nii_hfs_e2d = normalize(pulse2.spectro_profiles_medN_e2d['NII'])
        niii_hfs_e2d = normalize(pulse2.spectro_profiles_medN_e2d['NIII'])
        niv_hfs_e2d = normalize(pulse2.spectro_profiles_medN_e2d['NIV'])


        plt.scatter(pulse1.spectro_profiles_medN['R'], nii, marker='x',
                    label='N II', color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse1.spectro_profiles_medN['R'], niii, marker='_',
                    label='N III', color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse1.spectro_profiles_medN['R'], niv, marker='3',
                    label='N IV', color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_medN['R'], nii_hfs, marker='x',
                    label='_nolegend_', color=color2, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_medN['R'], niii_hfs, marker='_',
                    label='_nolegend_', color=color2, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_medN['R'], niv_hfs, marker='3',
                    label='_nolegend_', color=color2, s=ms + 3, linewidth=lw)

        plt.plot(pulse1.spectro_profiles_medN_e2d['R'], nii_e2d, marker='x',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse1.spectro_profiles_medN_e2d['R'], niii_e2d, marker='_',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse1.spectro_profiles_medN_e2d['R'], niv_e2d, marker='3',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_medN_e2d['R'], nii_hfs_e2d, marker='x',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_medN_e2d['R'], niii_hfs_e2d, marker='_',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_medN_e2d['R'], niv_hfs_e2d, marker='3',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(pulse1.spectro_profiles_medN['R']) + min(
            pulse1.spectro_profiles_medN['R'])) / 1.9,
                 (max(nii) + min(nii)) / 2, "medN", {'fontsize': 30})

        axes = plt.axes()


        plt.legend(loc=0, prop={'size': 20})

        #
        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        # %%
        fname = 'spectro_'+str(pulse1.pulse)+'_'+str(pulse2.pulse)+'_N_lines low seeding'
        fnorm = 1
        ftitle = 'spectro_'+str(pulse1.pulse)+'_'+str(pulse2.pulse)+'_N_lines low seeding'
        # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
        # fylabel='$I_{pump} (10^{22} s^{-1})$'
        fxlabel = '$R \quad [m[$'
        fylabel = '$D_{\delta}\ I \  radiance \quad [ph/s/m2/sr]$'

        plt.figure(num=fname)

        plt.scatter(pulse1.spectro_profiles_medN['R'],
                    pulse1.spectro_profiles_medN['DI'], marker='+', label='92121',
                    color=color1, s=ms + 3, linewidth=lw)
        plt.scatter(pulse2.spectro_profiles_medN['R'],
                    pulse2.spectro_profiles_medN['DI'], marker='+', label='92123',
                    color=color2, s=ms + 3, linewidth=lw)

        plt.plot(pulse1.spectro_profiles_medN_e2d['R'],
                 pulse1.spectro_profiles_medN_e2d['DI'], marker='+',
                 label='_nolegend_', color=color1, markersize=ms + 3,
                 linewidth=lw)
        plt.plot(pulse2.spectro_profiles_medN_e2d['R'],
                 pulse2.spectro_profiles_medN_e2d['DI'], marker='+',
                 label='_nolegend_', color=color2, markersize=ms + 3,
                 linewidth=lw)

        plt.text((max(pulse1.spectro_profiles_medN['R']) + min(
            pulse1.spectro_profiles_medN['R'])) / 2, (
                 max(pulse1.spectro_profiles_medN['DI']) + min(
                     pulse1.spectro_profiles_medN['DI'])) / 2, "highN",
                 {'fontsize': 30})

        axes = plt.axes()
        axes.set_xlim([min(pulse1.spectro_profiles_medN['R']),
                       max(pulse1.spectro_profiles_medN['R'])])

        plt.legend(loc=0, prop={'size': 20})


        plt.xlabel(fxlabel, {'color': 'k', 'size': 20})
        plt.ylabel(fylabel, {'color': 'k', 'size': 20})



        plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
        plt.show(block=True)
        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')


    @staticmethod
    def compare_bolo(pulse1,pulse2,ms = None, lw = None,vert=True,color1=None,color2=None,bound=None):
        if bound is None:
            bound=1.6e6
        else:
            bound=bound
        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw
        if color1 is None:
            color1 = 'black'
        else:
            color1 = color1
        if color2 is None:
            color2 = 'red'
        else:
            color2 = color2



        # %%
        fieldnames_h = list(pulse1.boloh_profiles_unseeded.columns.values)
        fieldnames_h = [x.strip() for x in fieldnames_h]

        fieldnames_h_e2d = list(
            pulse1.boloh_profiles_unseeded_e2d.columns.values)
        fieldnames_h_e2d = [x.strip() for x in fieldnames_h_e2d]
        #
        logger.info(fieldnames_h)
        logger.info(fieldnames_h_e2d)
        logger.info(pulse1.pulse)
        logger.info(pulse2.pulse)


        if vert:
            name='KB5V'
            channel = 'VERT'
            fname = name + '_AVG_unseeded aug2017'
            fnorm = 1
            ftitle = name + '_AVG_unseeded aug2017'
            # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
            # fylabel='$I_{pump} (10^{22} s^{-1})$'
            fxlabel = '$deg$'
            fylabel = name + '$_{AVG} \quad (MW/m^2)$'

            plt.figure(num=fname)

            plt.scatter(pulse1.bolov_profiles_unseeded[name + '_R'],
                        pulse1.bolov_profiles_unseeded[name], label=name,
                        color=color1,
                        s=ms, linewidth=lw)
            #
            plt.plot(pulse1.bolov_profiles_unseeded_e2d['PB5_' + channel + '_x'],
                     pulse1.bolov_profiles_unseeded_e2d['PB5_' + channel + '_y'],
                     marker='+',
                     label='_nolegend_', color=color1, markersize=ms + 3,
                     linewidth=lw)

            plt.scatter(pulse2.bolov_profiles_unseeded[name + '_R'],
                        pulse2.bolov_profiles_unseeded[name], label=name,
                        color=color2,
                        s=ms, linewidth=lw)

            plt.plot(pulse2.bolov_profiles_unseeded_e2d['PB5_' + channel + '_x'],
                     pulse2.bolov_profiles_unseeded_e2d['PB5_' + channel + '_y'],
                     marker='+',
                     label='_nolegend_', color=color2, markersize=ms + 3,
                     linewidth=lw)
            #
            plt.text((max(pulse2.bolov_profiles_medN[name + '_R']) + min(
                pulse2.bolov_profiles_medN[name + '_R'])) / 2, (
                         max(pulse2.bolov_profiles_unseeded[name]) + min(
                             pulse2.bolov_profiles_unseeded[name])) / 2,
                     "unseeded",
                     {'fontsize': 30})
            axes = plt.axes()
            axes.set_xlim([min(pulse2.bolov_profiles_unseeded[name + '_R']),
                           max(pulse2.bolov_profiles_unseeded[name + '_R'])])
            axes.set_ylim([0, float(bound)])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
            plt.legend(loc=2, prop={'size': 30})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)),
                   fontsize=20)
            # plt.tight_layout()
            plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
            plt.ylabel(fylabel, {'color': 'k', 'size': 28})
            #    plt.ioff()
            plt.tight_layout()
            # plt.savefig(fname,dpi=300) #
            plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
            #
            # # %%
            # # %%

            fname = name + '_AVG_medN aug2017'
            fnorm = 1
            ftitle = name + '_AVG_medN aug2017'
            # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
            # fylabel='$I_{pump} (10^{22} s^{-1})$'
            fxlabel = '$deg$'
            fylabel = name + '$_{AVG} \quad (MW/m^2)$'

            plt.figure(num=fname)

            # Now let's extract only the part of the data we're interested in...
            # x_filt = bolov_profiles_h_medN[name+'_R'][bolov_profiles_h_medN[name] > 0]
            # y_filt = bolov_profiles_medN[name][bolov_profiles_medN[name] > 0]
            plt.scatter(pulse1.bolov_profiles_medN[name + '_R'],
                        pulse1.bolov_profiles_medN[name], label=name,
                        color=color1,
                        s=ms, linewidth=lw)
            #
            plt.plot(pulse1.bolov_profiles_lowN_e2d['PB5_' + channel + '_x'],
                     pulse1.bolov_profiles_lowN_e2d['PB5_' + channel + '_y'],
                     marker='+',
                     label='_nolegend_', color=color1, markersize=ms + 3,
                     linewidth=lw)
            #
            plt.scatter(pulse2.bolov_profiles_medN[name + '_R'],
                        pulse2.bolov_profiles_medN[name], label=name,
                        color=color2,
                        s=ms, linewidth=lw)

            plt.plot(pulse2.bolov_profiles_lowN_e2d['PB5_' + channel + '_x'],
                     pulse2.bolov_profiles_lowN_e2d['PB5_' + channel + '_y'],
                     marker='x',
                     label='_nolegend_', color=color2, markersize=ms + 3,
                     linewidth=lw)
            #
            plt.text((max(pulse2.bolov_profiles_medN[name + '_R']) + min(
                pulse2.bolov_profiles_medN[name + '_R'])) / 2.1, (
                         max(pulse2.bolov_profiles_medN[name]) + min(
                             pulse2.bolov_profiles_medN[name])) / 2,
                     "med seeding",
                     {'fontsize': 30})
            # plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
            # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
            axes = plt.axes()
            axes.set_xlim([min(pulse2.bolov_profiles_medN[name + '_R']),
                           max(pulse2.bolov_profiles_medN[name + '_R'])])
            axes.set_ylim([0, bound])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
            plt.legend(loc=2, prop={'size': 30})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)),
                   fontsize=20)
            # plt.tight_layout()
            plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
            plt.ylabel(fylabel, {'color': 'k', 'size': 28})
            #    plt.ioff()
            plt.tight_layout()
            plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #
            #
            # # plt.show(block=True)
            # # %%
            # # %%

            fname = name + '_AVG_highN aug2017'
            fnorm = 1
            ftitle = name + '_AVG_highN aug2017'
            # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
            # fylabel='$I_{pump} (10^{22} s^{-1})$'
            fxlabel = '$deg$'
            fylabel = name + '$_{AVG} \quad (MW/m^2)$'

            plt.figure(num=fname)

            # plt.suptitle(ftitle, fontsize=11)
            # plt.scatter(self.e2d_profiles['DET_DEG'],self.e2d_profiles[name]/1e3,label='Te_omp_e2d',color='blue')

            plt.scatter(pulse1.bolov_profiles_highN[name + '_R'],
                        pulse1.bolov_profiles_highN[name], label=name,
                        color=color1, s=ms, linewidth=lw)

            plt.plot(pulse1.bolov_profiles_highN_e2d['PB5_' + channel + '_x'],
                     pulse1.bolov_profiles_highN_e2d['PB5_' + channel + '_y'],
                     marker='+',
                     label='_nolegend_', color=color1, markersize=ms + 3,
                     linewidth=lw)

            plt.scatter(pulse2.bolov_profiles_highN[name + '_R'],
                        pulse2.bolov_profiles_highN[name], label=name,
                        color=color2, s=ms, linewidth=lw)

            plt.plot(pulse2.bolov_profiles_highN_e2d['PB5_' + channel + '_x'],
                     pulse2.bolov_profiles_highN_e2d['PB5_' + channel + '_y'],
                     marker='+',
                     label='_nolegend_', color=color2, markersize=ms + 3,
                     linewidth=lw)
            #
            plt.text((max(pulse2.bolov_profiles_medN[name + '_R']) + min(
                pulse2.bolov_profiles_medN[name + '_R'])) / 2.1, (
                         max(pulse2.bolov_profiles_highN[name]) + min(
                             pulse2.bolov_profiles_highN[name])) / 2,
                     "high seeding",
                     {'fontsize': 30})
            # plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
            # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
            axes = plt.axes()
            axes.set_xlim([min(pulse2.bolov_profiles_highN[name + '_R']),
                           max(pulse2.bolov_profiles_highN[name + '_R'])])
            axes.set_ylim([0, bound])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
            plt.legend(loc=2, prop={'size': 30})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)),
                   fontsize=20)
            # plt.tight_layout()
            plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
            plt.ylabel(fylabel, {'color': 'k', 'size': 28})
            #    plt.ioff()
            plt.tight_layout()
            plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  # #
        else:
            name='KB5H'
            channel='HORI'
            fname = name+'_AVG_unseeded aug2017'
            fnorm = 1
            ftitle = name+'_AVG_unseeded aug2017'
            # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
            # fylabel='$I_{pump} (10^{22} s^{-1})$'
            fxlabel = '$deg$'
            fylabel = name+'$_{AVG} \quad (MW/m^2)$'

            plt.figure(num=fname)
            # logger.info(pulse1.boloh_profiles_unseeded)
            plt.scatter(pulse1.boloh_profiles_unseeded[name+'_R'],
                        pulse1.boloh_profiles_unseeded[name], label=name, color=color1,
                        s=ms, linewidth=lw)

            plt.plot(pulse1.boloh_profiles_unseeded_e2d['PB5_'+channel+'_x'],
                     pulse1.boloh_profiles_unseeded_e2d['PB5_'+channel+'_y'], marker='+',
                     label='_nolegend_', color=color1, markersize=ms + 3,
                     linewidth=lw)

            plt.scatter(pulse2.boloh_profiles_unseeded[name+'_R'],
                        pulse2.boloh_profiles_unseeded[name], label=name, color=color2,
                        s=ms, linewidth=lw)

            plt.plot(pulse2.boloh_profiles_unseeded_e2d['PB5_'+channel+'_x'],
                     pulse2.boloh_profiles_unseeded_e2d['PB5_'+channel+'_y'], marker='+',
                     label='_nolegend_', color=color2, markersize=ms + 3,
                     linewidth=lw)

            plt.text((max(pulse2.boloh_profiles_medN[name+'_R']) + min(
                pulse2.boloh_profiles_medN[name+'_R'])) / 2, (
                         max(pulse2.boloh_profiles_unseeded[name]) + min(
                             pulse2.boloh_profiles_unseeded[name])) / 2, "unseeded",
                     {'fontsize': 30})
            axes = plt.axes()
            axes.set_xlim([min(pulse2.boloh_profiles_unseeded[name+'_R']),
                           max(pulse2.boloh_profiles_unseeded[name+'_R'])])
            axes.set_ylim([0, float(bound)])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
            plt.legend(loc=2, prop={'size': 30})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)), fontsize=20)
            # plt.tight_layout()
            plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
            plt.ylabel(fylabel, {'color': 'k', 'size': 28})
            #    plt.ioff()
            plt.tight_layout()
            # plt.savefig(fname,dpi=300) #
            plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

            # %%
            # %%
            # plt.close("all")
            fname = name+'_AVG_medN aug2017'
            fnorm = 1
            ftitle = name+'_AVG_medN aug2017'
            # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
            # fylabel='$I_{pump} (10^{22} s^{-1})$'
            fxlabel = '$deg$'
            fylabel = name+'$_{AVG} \quad (MW/m^2)$'

            plt.figure(num=fname)

            # Now let's extract only the part of the data we're interested in...
            # x_filt = boloh_profiles_h_medN[name+'_R'][boloh_profiles_h_medN[name] > 0]
            # y_filt = boloh_profiles_medN[name][boloh_profiles_medN[name] > 0]
            plt.scatter(pulse1.boloh_profiles_medN[name+'_R'],
                        pulse1.boloh_profiles_medN[name], label=name, color=color1,
                        s=ms, linewidth=lw)

            plt.plot(pulse1.boloh_profiles_lowN_e2d['PB5_'+channel+'_x'],
                     pulse1.boloh_profiles_lowN_e2d['PB5_'+channel+'_y'], marker='+',
                     label='_nolegend_', color=color1, markersize=ms + 3,
                     linewidth=lw)

            plt.scatter(pulse2.boloh_profiles_medN[name+'_R'],
                        pulse2.boloh_profiles_medN[name], label=name, color=color2,
                        s=ms, linewidth=lw)

            plt.plot(pulse2.boloh_profiles_lowN_e2d['PB5_'+channel+'_x'],
                     pulse2.boloh_profiles_lowN_e2d['PB5_'+channel+'_y'], marker='x',
                     label='_nolegend_', color=color2, markersize=ms + 3,
                     linewidth=lw)

            plt.text((max(pulse2.boloh_profiles_medN[name+'_R']) + min(
                pulse2.boloh_profiles_medN[name+'_R'])) / 2.1, (
                         max(pulse2.boloh_profiles_medN[name]) + min(
                             pulse2.boloh_profiles_medN[name])) / 2, "med seeding",
                     {'fontsize': 30})
            # plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
            # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
            axes = plt.axes()
            axes.set_xlim([min(pulse2.boloh_profiles_medN[name+'_R']),
                           max(pulse2.boloh_profiles_medN[name+'_R'])])
            axes.set_ylim([0, bound])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
            plt.legend(loc=2, prop={'size': 30})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)), fontsize=20)
            # plt.tight_layout()
            plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
            plt.ylabel(fylabel, {'color': 'k', 'size': 28})
            #    plt.ioff()
            plt.tight_layout()
            plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  #

            # plt.show(block=True)
            # %%
            # %%
            # plt.close("all")
            fname = name+'_AVG_highN aug2017'
            fnorm = 1
            ftitle = name+'_AVG_highN aug2017'
            # fxlabel='$n_{e,sep,LFS-mp}  (10^{19} m^{-3})$'
            # fylabel='$I_{pump} (10^{22} s^{-1})$'
            fxlabel = '$deg$'
            fylabel = name+'$_{AVG} \quad (MW/m^2)$'

            plt.figure(num=fname)

            # plt.suptitle(ftitle, fontsize=11)
            # plt.scatter(self.e2d_profiles['DET_DEG'],self.e2d_profiles[name]/1e3,label='Te_omp_e2d',color='blue')

            plt.scatter(pulse1.boloh_profiles_highN[name+'_R'],
                        pulse1.boloh_profiles_highN[name], label=name,
                        color=color1, s=ms, linewidth=lw)

            plt.plot(pulse1.boloh_profiles_highN_e2d['PB5_'+channel+'_x'],
                     pulse1.boloh_profiles_highN_e2d['PB5_'+channel+'_y'], marker='+',
                     label='_nolegend_', color=color1, markersize=ms + 3,
                     linewidth=lw)

            plt.scatter(pulse2.boloh_profiles_highN[name+'_R'],
                        pulse2.boloh_profiles_highN[name], label=name,
                        color=color2, s=ms, linewidth=lw)

            plt.plot(pulse2.boloh_profiles_highN_e2d['PB5_'+channel+'_x'],
                     pulse2.boloh_profiles_highN_e2d['PB5_'+channel+'_y'], marker='+',
                     label='_nolegend_', color=color2, markersize=ms + 3,
                     linewidth=lw)

            plt.text((max(pulse2.boloh_profiles_medN[name+'_R']) + min(
                pulse2.boloh_profiles_medN[name+'_R'])) / 2.1, (
                         max(pulse2.boloh_profiles_highN[name]) + min(
                             pulse2.boloh_profiles_highN[name])) / 2, "high seeding",
                     {'fontsize': 30})
            # plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
            # plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color = 'k')
            axes = plt.axes()
            axes.set_xlim([min(pulse2.boloh_profiles_highN[name+'_R']),
                           max(pulse2.boloh_profiles_highN[name+'_R'])])
            axes.set_ylim([0, bound])
            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            #    plt.legend(loc="upper left",labelspacing=0.5,borderpad=0.5,fontsize=20)
            plt.legend(loc=2, prop={'size': 30})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs * 1)), fontsize=20)
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs * 1e-6)), fontsize=20)
            # plt.tight_layout()
            plt.xlabel(fxlabel, {'color': 'k', 'size': 28})
            plt.ylabel(fylabel, {'color': 'k', 'size': 28})
            #    plt.ioff()
            plt.tight_layout()
            plt.savefig('./figures/' + fname+'_'+pulse.label, format='eps', dpi=300)
            plt.savefig('./figures/' + fname+'_'+pulse.label, dpi=300)  # #

        plt.show(block=True)
        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')

    @staticmethod

    def compare_profiles(pulse1,pulse2,ms = None, lw = None,color1=None,color2=None):
        logger.debug('inside compare profiles')

        fieldnames = list(pulse1.e2d_profiles.columns.values)
        fieldnames = [x.strip() for x in fieldnames]
        logger.debug('pulse1 OMP fieldnames')
        logger.debug(fieldnames)
        #
        fieldnames = list(pulse2.e2d_profiles.columns.values)
        fieldnames = [x.strip() for x in fieldnames]
        logger.debug('pulse2 OMP fieldnames')
        logger.debug(fieldnames)
        #
        #
        #
        fieldnames_ot = list(pulse1.e2d_profiles_ot.columns.values)
        fieldnames_ot = [x.strip() for x in fieldnames_ot]
        print(pulse1.e2d_profiles_ot.columns.values)
        logger.debug('pulse1 ot fieldnames')
        logger.debug(fieldnames_ot)

        fieldnames_ot = list(pulse2.e2d_profiles_ot.columns.values)
        fieldnames_ot = [x.strip() for x in fieldnames_ot]
        logger.debug('pulse2 ot fieldnames')
        logger.debug(fieldnames_ot)

        logger.info('%s',str(pulse1.label))
        logger.info('%s',str(pulse2.label))
        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw
        if color1 is None:
            color1 = 'black'
        else:
            color1 = color1
        if color2 is None:
            color2 = 'red'
        else:
            color2 = color2


        # logger.info('plotting HRTS TE')
        try:
            
            logger.info('plotting HRTS TE \n')

            if str(pulse1.pulse) == str(pulse2.pulse):
                 fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'Te_omp'

            else:
                fname = str(pulse1.pulse) + '_' + str(pulse1.label) + '_' + str(
                    pulse2.pulse) + '_' + str(pulse2.label) + 'Te_omp'

            fnorm = 1
            ftitle = 'Electron Temperature OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$T_{e,OMP}\quad keV$'

            plt.figure(num=fname + "_" + pulse1.label)
            if pulse1.plot_exp == "True":
                try:
                    plt.errorbar(
                        pulse1.hrts_profiles['RmRsep'] + float(pulse1.shift),
                        pulse1.hrts_profiles['TE'], label='_nolegend_',
                        yerr=pulse1.hrts_profiles['DTE'], fmt=None, ecolor=color1)
                except:
                    logger.error('impossible to plot pulse1 TE from HRTS')
                try:
                    plt.scatter(pulse1.hrts_fit['Rfit'] + float(pulse1.shift_fit),
                                pulse1.hrts_fit['tef5'], label='_nolegend_',
                                color=color1)
                except:
                    logger.error('impossible to plot pulse1 TE HRTS fit')


            if pulse1.plot_sim == "True":
                try:
                    
                    plt.scatter(pulse1.e2d_profiles['dsrad'],
                            pulse1.e2d_profiles['teve'] / pulse1.te_omp_factor, label=pulse1.conf+'_sim',
                            color=color1)
                except:
                    
                    logger.debug('no te HRTS sim data found for pulse1')

            if pulse2.plot_exp == "True":
                try:
                    plt.errorbar(
                        pulse2.hrts_profiles['RmRsep'] + float(pulse2.shift),
                        pulse2.hrts_profiles['TE'], label='_nolegend_',
                        yerr=pulse2.hrts_profiles['DTE'], fmt=None, ecolor=color2)
                except:
                    logger.error('impossible to plot pulse2 TE from HRTS')
                try:
                    plt.scatter(pulse2.hrts_fit['Rfit'] + float(pulse2.shift_fit),
                                pulse2.hrts_fit['tef5'], label='_nolegend_',
                                color=color2)
                except:
                    logger.error('impossible to plot pulse2 TE HRTS fit')


            if pulse2.plot_sim == "True":
                try:
                    
                    plt.scatter(pulse2.e2d_profiles['dsrad'],
                                pulse2.e2d_profiles['teve'] / pulse2.te_omp_factor, label=pulse2.conf+'_sim',
                            color=color2)
                except:
                    
                    logger.debug('no te HRTS sim data found for pulse1')



            plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
            plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color='k')
            axes = plt.axes()
            axes.set_xlim([-.15, .1])
            axes.set_ylim([0, 1.0])
            # axes.set_ylim(bottom=0)
            # axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            plt.legend(loc=0, prop={'size': 18})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs)))
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
            
            plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
            plt.ylabel(fylabel, {'color': 'k', 'size': 16})
            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #
            
            # raise SystemExit
        except :

            logger.error("Could not plot HRTS te")
    # %%
        #    logger.info('plotting HRTS NE')
        try:
            logger.info('plotting HRTS NE')
            # %%
            

            if str(pulse1.pulse) == str(pulse2.pulse):
                            fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'ne_omp'
            else:
                            fname = str(pulse1.pulse) +'_'+str(pulse1.label) +'_'+str(pulse2.pulse) +'_'+str(pulse2.label) + 'ne_omp'

            fnorm = 1
            ftitle = 'Electron Density OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname + "_" + pulse1.label)
            if pulse1.plot_sim == "True":
                try:

                    plt.scatter(pulse1.e2d_profiles['dsrad_omp'],
                                pulse1.e2d_profiles['denel_omp'] / pulse1.ne_omp_factor,
                                label=pulse1.conf+'_sim', color=color1)
                    logger.debug('try plotting e2d ne pulse1')

                except:

                    plt.scatter(pulse1.e2d_profiles['dsrad'],
                                pulse1.e2d_profiles['denel'] / pulse1.ne_omp_factor,
                                label=pulse1.conf+'_sim', color=color1)
                    logger.debug('except plotting e2d ne pulse1')

            if pulse1.plot_exp == "True":
                try:
                    plt.errorbar(pulse1.hrts_profiles['RmRsep']+float(pulse1.shift),pulse1.hrts_profiles['NE'],label='_nolegend_', yerr=pulse1.hrts_profiles['DNE'], fmt=None, ecolor=color2)
                except:
                    logger.error('impossible to plot pulse1 NE from HRTS')
                try:
                    plt.scatter(pulse1.hrts_fit['Rfit']+float(pulse1.shift_fit),pulse1.hrts_fit['nef3'],label='_nolegend_',color=color1)
                except:
                    logger.error('impossible to plot pulse2 NE HRTS fit')

            if pulse2.plot_sim == "True":
                try:
                    logger.debug('here')
                    plt.scatter(pulse2.e2d_profiles['dsrad_omp'],
                                pulse2.e2d_profiles['denel_omp'] / pulse1.ne_omp_factor,
                                label=pulse2.conf+'_sim', color=color2)
                    logger.debug('try plotting e2d ne pulse2')

                except:
                    
                    plt.scatter(pulse2.e2d_profiles['dsrad'],
                                pulse2.e2d_profiles['denel'] / pulse2.ne_omp_factor,
                                label=pulse2.conf+'_sim', color=color2)
                    logger.debug('except plotting e2d ne pulse2')

            if pulse2.plot_exp == "True":
                try:
                    plt.errorbar(pulse2.hrts_profiles['RmRsep']+float(pulse2.shift),pulse2.hrts_profiles['NE'],label='_nolegend_', yerr=pulse2.hrts_profiles['DNE'], fmt=None, ecolor=color2)
                except:
                    logger.error('impossible to plot pulse2 NE HRTS')
                try:
                    plt.scatter(pulse2.hrts_fit['Rfit']+float(pulse2.shift_fit),pulse2.hrts_fit['nef3'],label='_nolegend_',color=color2)
                except:
                    logger.error('impossible to plot pulse2 NE HRTS fit')

            plt.axvline(x=0.0, ymin=0., ymax = 500, linewidth=2, color='k')
            plt.axhline(y=3.5, xmin=-.15, xmax=500, linewidth=2, color = 'k')

            axes = plt.axes()
            axes.set_xlim([-.15, .1])
            # axes.set_ylim([0, 10.0])
            axes.set_ylim(bottom=0)

            # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
            # axes.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])
            plt.legend(loc=0,prop={'size':18})



            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs)))
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
            plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
            plt.ylabel(fylabel, {'color': 'k', 'size': 16})
            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #
        except :
            logger.error("Could not plot HRTS ne")

        try:
            logger.info('plotting ne_ot')
            if str(pulse1.pulse) == str(pulse2.pulse):
                            fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'ne_ot'
            else:

                fname = str(pulse1.pulse) + '_' + str(pulse1.label) + '_' + str(
                    pulse2.pulse) + '_' + str(pulse2.label) + 'ne_ot'

            fnorm=1
            ftitle='Electron Density OT'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$n_{e,OT}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname)
            plt.suptitle(ftitle, fontsize=11)
            if pulse1.plot_exp == "True":
                logger.debug('plot exp pulse1 true')
                try:
                    plt.scatter(pulse1.lp_profiles['dSsep'],pulse1.lp_profiles['ne'],label=pulse1.conf+'_exp',color=color1)
                    logger.debug('here ne_ot')
                except:
                    logger.error('no ne LP exp data for pulse1')
            if pulse1.plot_sim == "True":
                logger.debug('plot sim pulse1 true')
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_ot'],pulse1.e2d_profiles_ot['denel_ot'],'-',label=pulse1.conf+'_sim',color=color1)
                    logger.debug('try plotting e2d ne pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],pulse1.e2d_profiles_ot['denel'],'-',label=pulse1.conf+'_sim',color=color1)
                    logger.debug('except plotting e2d ne pulse1')


            if pulse2.plot_exp == "True":
                logger.debug('plot exp pulse2 true')
                try:
                    plt.scatter(pulse2.lp_profiles['dSsep'],pulse2.lp_profiles['ne'],label=pulse2.conf+'_exp',color=color2)
                    logger.debug('here ne_ot')
                except:
                    logger.error('no ne LP exp data for pulse2')
            if pulse2.plot_sim == "True":
                logger.debug('plot sim pulse2 true')
                try:
                    plt.plot(pulse2.e2d_profiles_ot['dsrad_ot'],pulse2.e2d_profiles_ot['denel_ot'],'-',label=pulse2.conf+'_sim',color=color2)
                    logger.debug('try plotting e2d ne pulse2')
                except:
                    plt.plot(pulse2.e2d_profiles_ot['dsrad'],pulse2.e2d_profiles_ot['denel'],'-',label=pulse2.conf+'_sim',color=color2)
                    logger.debug('except plotting e2d ne pulse2')



            axes = plt.axes()
            axes.set_ylim(bottom=0)
            plt.legend(loc =0,prop={'size':18})

            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #
        except :
            logger.error("Could not plot ne ot")
            # logger.error("Could not plot ne ot")
        #     logger.info('plotting te_ot')
        try:
            logger.info('plotting te_ot')
            if str(pulse1.pulse) == str(pulse2.pulse):
                            fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'Te_ot'
            else:
                            fname = str(pulse1.pulse) +'_'+str(pulse1.label) +'_'+str(pulse2.pulse) + 'Te_ot'

            fnorm=1
            ftitle='Electron Temperature OT'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$T_{e,OT}\quad keV$'

            plt.figure(num=fname+"_"+pulse1.label)
            if pulse1.plot_exp == "True":
                logger.debug('plot exp pulse1 true')
                try:
                    plt.scatter(pulse1.lp_profiles['dSsep'],pulse1.lp_profiles['te'],label=pulse1.conf+'_exp',color=color1)
                    logger.debug('here te_ot')
                except:
                    logger.error('no te LP exp data for pulse1')
            if pulse1.plot_sim == "True":
                logger.debug('plot sim pulse1 true')
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_ot'],pulse1.e2d_profiles_ot['te_ot'],'-',label=pulse1.conf+'_sim',color=color1)
                    logger.debug('try plotting e2d te pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],pulse1.e2d_profiles_ot['teve'],'-',label=pulse1.conf+'_sim',color=color1)
                    logger.debug('except plotting e2d te pulse1')


            if pulse2.plot_exp == "True":
                logger.debug('plot exp pulse2 true')
                try:
                    plt.scatter(pulse2.lp_profiles['dSsep'],pulse2.lp_profiles['te'],label=pulse2.conf+'_exp',color=color2)
                    logger.debug('here ne_ot')
                except:
                    logger.error('no te LP exp data for pulse2')
            if pulse2.plot_sim == "True":
                logger.debug('plot sim pulse2 true')
                try:
                    plt.plot(pulse2.e2d_profiles_ot['dsrad_ot'],pulse2.e2d_profiles_ot['te_ot'],'-',label=pulse2.conf+'_sim',color=color2)
                    logger.debug('try plotting e2d te pulse2')
                except:
                    plt.plot(pulse2.e2d_profiles_ot['dsrad'],pulse2.e2d_profiles_ot['teve'],'-',label=pulse2.conf+'_sim',color=color2)
                    logger.debug('except plotting e2d te pulse2')


            axes = plt.axes()
            
            plt.legend(loc =0,prop={'size':18})
            #%%

            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #
        except :
            logger.error("Could not plot te ot")


        try:
            logger.info('plotting jsat_ot')
            #%%
            if str(pulse1.pulse) == str(pulse2.pulse):
                            fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'jsat_ot'
            else:
                fname = str(pulse1.pulse) + '_' + str(pulse1.label) + '_' + str(
                    pulse2.pulse) + '_' + str(pulse2.label) + 'jsat_ot'

            ftitle='Saturation Current  OT'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$J_{sat,OT}\quad A m^{-2}$'
            plt.figure(num=fname + "_" + pulse1.label)
            if pulse1.plot_exp == "True":
                logger.debug('plot exp pulse1 true')
                try:
                    plt.scatter(pulse1.lp_profiles['dSsep'],pulse1.lp_profiles['jsat'],label=pulse1.conf+'_exp',color=color1)
                    logger.debug('here jsat_ot')
                except:
                    logger.error('no jsat LP exp data for pulse1')
            if pulse1.plot_sim == "True":
                logger.debug('plot sim pulse1 true')
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_ot'],-pulse1.e2d_profiles_ot['jtargi_ot'],'-',label=pulse1.conf+'_sim',color=color1)
                    logger.debug('try plotting e2d jsat pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],-pulse1.e2d_profiles_ot['jtargi'],'-',label=pulse1.conf+'_sim',color=color1)
                    logger.debug('except plotting e2d jsat pulse1')


            if pulse2.plot_exp == "True":
                logger.debug('plot exp pulse2 true')
                try:
                    plt.scatter(pulse2.lp_profiles['dSsep'],pulse2.lp_profiles['jsat'],label=pulse2.conf+'_exp',color=color2)
                    logger.debug('here jsat_ot')
                except:
                    logger.error('no jsat LP exp data for pulse2')
            if pulse2.plot_sim == "True":
                logger.debug('plot sim pulse2 true')
                try:
                    plt.plot(pulse2.e2d_profiles_ot['dsrad_ot'],-pulse2.e2d_profiles_ot['jtargi_ot'],'-',label=pulse2.conf+'_sim',color=color2)
                    logger.debug('try plotting e2d jsat pulse2')
                except:
                    plt.plot(pulse2.e2d_profiles_ot['dsrad'],-pulse2.e2d_profiles_ot['jtargi'],'-',label=pulse2.conf+'_sim',color=color2)
                    logger.debug('except plotting e2d jsat pulse2')


            axes = plt.axes()
            plt.legend(loc =0,prop={'size':18})
            
            #%%
            # plt.tight_layout()
            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #
        except :

            logger.error("Could not plot jsat")


        try:
            logger.info('plotting Dperp')
            if str(pulse1.pulse) == str(pulse2.pulse):
                            fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'Dperp'
            else:
                fname = str(pulse1.pulse) + '_' + str(pulse1.label) + '_' + str(
                    pulse2.pulse) + '_' + str(pulse2.label) + 'Dperp'



            fnorm=1
            ftitle='D perpendicular'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$D_{\perp}\quad   m^{2}/s})$'
            plt.figure(num=fname + "_" + pulse1.label)

            if pulse1.plot_sim == "True":
                try:
                    logger.debug('try pulse1 Dperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad_omp'],pulse1.e2d_profiles['dperp_omp'],label=pulse1.conf,color=color1)
                except:
                    logger.debug('except pulse1 Dperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad'],pulse1.e2d_profiles['dperp'],label=pulse1.conf,color=color1)

            if pulse2.plot_sim == "True":
                try:
                    logger.debug('try pulse2 Dperp')
                    plt.scatter(pulse2.e2d_profiles['dsrad_omp'],pulse2.e2d_profiles['dperp_omp'],label=pulse2.conf,color=color2)
                except:
                    logger.debug('except pulse2 Dperp')
                    plt.scatter(pulse2.e2d_profiles['dsrad'],pulse2.e2d_profiles['dperp'],label=pulse2.conf,color=color2)

            axes = plt.axes()
            plt.legend(loc=0, prop={'size': 18})
            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #
        except :

            logger.error("Could not plot dperp")
            #%%
        try:
            logger.info('plotting Xperp')
            if str(pulse1.pulse) == str(pulse2.pulse):
                            fname = str(pulse1.pulse) +'_'+str(pulse2.label) + 'Xperp'
            else:
                fname = str(pulse1.pulse) + '_' + str(pulse1.label) + '_' + str(
                    pulse2.pulse) + '_' + str(pulse2.label) + 'Xperp'




            fnorm=1
            ftitle='X perpendicular'
            fxlabel='$R - R_{sep,LFS-mp}\quad  m$'
            fylabel='$X_{\perp}\quad   m^{2}/s})$'
            plt.figure(num=fname + "_" + pulse1.label)

            # plt.suptitle(ftitle, fontsize=11)

            if pulse1.plot_sim == "True":
                try:
                    logger.debug('try pulse1 Xperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad_omp'],pulse1.e2d_profiles['chii_omp'],label=pulse1.conf,color=color2)
                except:
                    logger.debug('except pulse1 Xperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad'],pulse1.e2d_profiles['chii'],label=pulse1.conf,color=color1)

            if pulse2.plot_sim == "True":
                try:
                    logger.debug('try pulse2 Xperp')
                    plt.scatter(pulse2.e2d_profiles['dsrad_omp'],pulse2.e2d_profiles['chii_omp'],label=pulse2.conf,color=color2)
                except:
                    logger.debug('except pulse2 Xperp')
                    plt.scatter(pulse2.e2d_profiles['dsrad'],pulse2.e2d_profiles['chii'],label=pulse2.conf,color=color2)
            axes = plt.axes()
            plt.legend(loc=0, prop={'size': 18})
            plt.savefig('./figures/' + fname, format='eps', dpi=300)
            plt.savefig('./figures/' + fname, dpi=300)  #


        except :
            logger.error("Could not plot xperp")
            #%%





        plt.show(block=True)
        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')

    @staticmethod
    def compare_multi_shots(dict1,*argv, ms=None, lw=None):
        if True:
            logger.debug('inside compare multi shots')

            if ms is None:
                ms = 40
            else:
                ms = ms
            if lw is None:
                lw = 2
            else:
                lw = lw



            input_dict = read_json(dict1)

            pulse1 = shot(input_dict)


            fieldnames = list(pulse1.e2d_profiles.columns.values)
            fieldnames = [x.strip() for x in fieldnames]
            logger.debug('pulse1 OMP fieldnames')
            logger.debug(fieldnames)

            fieldnames_ot = list(pulse1.e2d_profiles_ot.columns.values)
            fieldnames_ot = [x.strip() for x in fieldnames_ot]
            print(pulse1.e2d_profiles_ot.columns.values)
            logger.debug('pulse1 ot fieldnames')
            logger.debug(fieldnames_ot)

            
            logger.info('plotting HRTS TE')
            # logger.debug('%s',str(pulse1.pulse))
            # logger.debug('%s',str(vars()['pulse_'+arg].pulse))
            # print(pulse1)
            fname = 'Te_omp_comparison'
            
            fnorm = 1
            ftitle = 'Electron Temperature OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$T_{e,OMP}\quad keV$'

            plt.figure(num=fname)
            plt.suptitle(fname, fontsize=11)
            if pulse1.plot_exp == "True":
                try:
                    plt.errorbar(
                        pulse1.hrts_profiles['RmRsep'] + float(pulse1.shift),
                        pulse1.hrts_profiles['TE'], label='_nolegend_',
                        yerr=pulse1.hrts_profiles['DTE'], fmt=None,
                        ecolor=pulse1.color)
                except:
                    logger.error('impossible to plot pulse1 TE from HRTS')

                try:
                    plt.scatter(
                        pulse1.hrts_fit['Rfit'] + float(pulse1.shift_fit),
                        pulse1.hrts_fit['tef5'], label='_nolegend_',
                        color=pulse1.color)
                except:
                    logger.error('impossible to plot pulse1 TE HRTS fit')

            if pulse1.plot_sim == "True":
                try:
                    
                    plt.scatter(pulse1.e2d_profiles['dsrad'],
                                pulse1.e2d_profiles[
                                    'teve'] / pulse1.te_omp_factor,
                                label=pulse1.pulse,
                                color=pulse1.color)
                except:
                    
                    logger.debug('no te HRTS sim data found for pulse1')

            plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
            plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color='k')
            axes = plt.axes()
            axes.set_xlim([-.15, .1])
            axes.set_ylim([0, 1.0])
            # axes.set_ylim(bottom=0)
            # axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
            # axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

            plt.legend(loc=0, prop={'size': 8})
            locs, labels = xticks()
            xticks(locs, list(map(lambda x: "%g" % x, locs)))
            locs, labels = yticks()
            yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
            
            plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
            plt.ylabel(fylabel, {'color': 'k', 'size': 16})
            # plt.savefig('./figures/' + fname, format='eps', dpi=300)
            # plt.savefig('./figures/' + fname, dpi=300)  #
            
            # raise SystemExit

            logger.info('plotting HRTS NE')
            # %%
            
            fname = 'ne_omp_comparison'
            fnorm = 1
            ftitle = 'Electron Density OMP'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname)
            plt.suptitle(fname, fontsize=11)
            if pulse1.plot_sim == "True":
                try:

                    plt.scatter(pulse1.e2d_profiles['dsrad_omp'],
                                pulse1.e2d_profiles[
                                    'denel_omp'] / pulse1.ne_omp_factor,
                                label=pulse1.pulse, color=pulse.color)
                    logger.debug('try plotting e2d ne pulse1')

                except:

                    plt.scatter(pulse1.e2d_profiles['dsrad'],
                                pulse1.e2d_profiles[
                                    'denel'] / pulse1.ne_omp_factor,
                                label=pulse1.pulse, color=pulse1.color)
                    logger.debug('except plotting e2d ne pulse1')

            if pulse1.plot_exp == "True":
                try:
                    plt.errorbar(
                    pulse1.hrts_profiles['RmRsep'] + float(pulse1.shift),
                    pulse1.hrts_profiles['NE'], label='_nolegend_',
                    yerr=pulse1.hrts_profiles['DNE'], fmt=None, ecolor=pulse1.color)
                except:
                    logger.error('impossible to plot pulse1 NE HRTS')
                try:
                    plt.scatter(pulse1.hrts_fit['Rfit'] + float(pulse1.shift_fit),
                            pulse1.hrts_fit['nef3'], label='_nolegend_',
                            color=pulse1.color)
                except:
                    logger.error('impossible to plot pulse1 NE HRTS fit')



                plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')

                plt.axhline(y=3.5, xmin=-.15, xmax=500, linewidth=2, color='k')

                axes = plt.axes()
                axes.set_xlim([-.15, .1])
                # axes.set_ylim([0, 10.0])
                axes.set_ylim(bottom=0)

                # axes.set_xticks([-.15,-0.1, -0.05, -0.02, 0, 0.02, 0.05,0.1])
                # axes.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])
                plt.legend(loc=2, prop={'size': 8})

                locs, labels = xticks()
                xticks(locs, list(map(lambda x: "%g" % x, locs)))
                locs, labels = yticks()
                yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
                plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
                plt.ylabel(fylabel, {'color': 'k', 'size': 16})


                logger.info('plotting ne_ot')


            fname = 'ne_ot_comparison'
            fnorm = 1
            ftitle = 'Electron Density OT'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$n_{e,OT}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname)
            plt.suptitle(ftitle, fontsize=11)
            if pulse1.plot_exp == "True":
                logger.debug('plot exp pulse1 true')
                try:
                    plt.scatter(pulse1.lp_profiles['dSsep'],
                                pulse1.lp_profiles['ne'],
                                label=pulse1.pulse, color=pulse1.color)
                    logger.debug('here ne_ot')
                except:
                    logger.error('no ne LP exp data for pulse1')
            if pulse1.plot_sim == "True":
                logger.debug('plot sim pulse1 true')
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_ot'],
                             pulse1.e2d_profiles_ot['denel_ot'], '-',
                             label=pulse1.pulse , color=pulse1.color)
                    logger.debug('try plotting e2d ne pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],
                             pulse1.e2d_profiles_ot['denel'], '-',
                             label=pulse1.pulse , color=pulse1.color)
                    logger.debug('except plotting e2d ne pulse1')

            axes = plt.axes()
            axes.set_ylim(bottom=0)
            plt.legend(loc=0, prop={'size': 18})



            logger.info('plotting te_ot')
            fname = 'te_ot_comparison'
            fnorm = 1
            ftitle = 'Electron Temperature OT'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$T_{e,OT}\quad keV$'

            plt.figure(num=fname)
            plt.suptitle(fname, fontsize=11)
            if pulse1.plot_exp == "True":
                logger.debug('plot exp pulse1 true')
                try:
                    plt.scatter(pulse1.lp_profiles['dSsep'],
                                pulse1.lp_profiles['te'],
                                label=pulse1.pulse , color=pulse1.color)
                    logger.debug('here te_ot')
                except:
                    logger.error('no te LP exp data for pulse1')
            if pulse1.plot_sim == "True":
                logger.debug('plot sim pulse1 true')
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_ot'],
                             pulse1.e2d_profiles_ot['te_ot'], '-',
                             label=pulse1.pulse , color=pulse1.color)
                    logger.debug('try plotting e2d te pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],
                             pulse1.e2d_profiles_ot['teve'], '-',
                             label=pulse1.pulse , color=pulse1.color)
                    logger.debug('except plotting e2d te pulse1')

            axes = plt.axes()
            
            plt.legend(loc=0, prop={'size': 18})
            # %%



            logger.info('plotting jsat_ot')
            # %%
            fname = 'jsat_ot_comparison'
            ftitle = 'Saturation Current  OT'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$J_{sat,OT}\quad A m^{-2}$'

            plt.figure(num=fname)
            plt.suptitle(fname, fontsize=11)
            if pulse1.plot_exp == "True":
                logger.debug('plot exp pulse1 true')
                try:
                    plt.scatter(pulse1.lp_profiles['dSsep'],
                                pulse1.lp_profiles['jsat'],
                                label=pulse1.pulse , color=pulse1.color)
                    logger.debug('here jsat_ot')
                except:
                    logger.error('no jsat LP exp data for pulse1')
            if pulse1.plot_sim == "True":
                logger.debug('plot sim pulse1 true')
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_ot'],
                             -pulse1.e2d_profiles_ot['jtargi_ot'], '-',
                             label=pulse1.pulse , color=pulse1.color)
                    logger.debug('try plotting e2d jsat pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],
                             -pulse1.e2d_profiles_ot['jtargi'], '-',
                             label=pulse1.pulse , color=pulse1.color)
                    logger.debug('except plotting e2d jsat pulse1')

            axes = plt.axes()
            plt.legend(loc=0, prop={'size': 18})
            
            # %%
            # plt.tight_layout()

            logger.info('plotting Dperp')
            fname = 'Dperp_comparison'
            fnorm = 1
            ftitle = 'D perpendicular'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$D_{\perp}\quad   m^{2}/s})$'

            plt.figure(num=fname)
            plt.suptitle(fname, fontsize=11)

            if pulse1.plot_sim == "True":
                try:
                    logger.debug('try pulse1 Dperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad_omp'],
                                pulse1.e2d_profiles['dperp_omp'],
                                label=pulse1.pulse, color=pulse1.color)
                except:
                    logger.debug('except pulse1 Dperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad'],
                                pulse1.e2d_profiles['dperp'], label=pulse1.pulse,
                                color=pulse1.color)
            axes = plt.axes()
            plt.legend(loc=0, prop={'size': 18})

            logger.info('plotting Xperp')
            fname = 'Xperp_comparison'

            fnorm = 1
            ftitle = 'X perpendicular'
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            fylabel = '$X_{\perp}\quad   m^{2}/s})$'
            plt.figure(num=fname)

            plt.suptitle(ftitle, fontsize=11)

            if pulse1.plot_sim == "True":
                try:
                    logger.debug('try pulse1 Xperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad_omp'],
                                pulse1.e2d_profiles['chii_omp'],
                                label=pulse1.pulse, color=pulse1.color)
                except:
                    logger.debug('except pulse1 Xperp')
                    plt.scatter(pulse1.e2d_profiles['dsrad'],
                                pulse1.e2d_profiles['chii'], label=pulse1.pulse,
                                color=pulse1.color)
            axes = plt.axes()
            plt.legend(loc=0, prop={'size': 18})




        # print('HERE ')
        for i,arg in enumerate(argv):
            i=i+2
            json_dict = read_json(arg)
            pulse = shot(json_dict)

            
            logger.info('plotting HRTS TE')
            try:
                
                logger.info('plotting HRTS TE')
                fname = 'Te_omp_comparison'
                plt.figure(num=fname)
                plt.suptitle(fname, fontsize=11)
                if pulse.plot_exp == "True":
                    try:
                        plt.errorbar(
                            pulse.hrts_profiles['RmRsep'] + float(pulse.shift),
                            pulse.hrts_profiles['TE'], label='_nolegend_',
                            yerr=pulse.hrts_profiles['DTE'], fmt=None,ecolor=pulse.color)
                    except:
                        logger.error('impossible to plot TE from HRTS for pulse '+str(i))
                    try:
                        plt.scatter(
                            pulse.hrts_fit['Rfit'] + float(pulse.shift_fit),
                            pulse.hrts_fit['tef5'], label='_nolegend_',color=pulse.color)
                    except:
                        logger.error('impossible to plot '+ pulse + ' TE HRTS fit')

                if pulse.plot_sim == "True":
                    try:
                        
                        plt.scatter(pulse.e2d_profiles['dsrad'],
                                    pulse.e2d_profiles[
                                        'teve'] / pulse.te_omp_factor,
                                    label=pulse.pulse ,color=pulse.color)
                    except:
                        
                        logger.error(
                            'impossible to plot sim TE from HRTS for pulse ' + str(
                                i))
                plt.legend(loc=0, prop={'size': 18})
                
                # raise SystemExit
            except:

                logger.error("Could not plot HRTS te")
            # %%

            #    logger.info('plotting HRTS NE')
            try:
                logger.info('plotting HRTS NE')
                # %%
                
                fname = 'ne_omp_comparison'

                plt.figure(num=fname)
                plt.suptitle(fname, fontsize=11)

                if pulse.plot_sim == "True":
                    try:
                        logger.debug('here')
                        plt.scatter(pulse.e2d_profiles['dsrad_omp'],
                                    pulse.e2d_profiles[
                                        'denel_omp'] / pulse.ne_omp_factor,
                                    label=pulse.pulse,ecolor=pulse.color)


                    except:
                        
                        plt.scatter(pulse.e2d_profiles['dsrad'],
                                    pulse.e2d_profiles[
                                        'denel'] / pulse.ne_omp_factor,
                                    label=pulse.pulse,color=pulse.color)


                if pulse.plot_exp == "True":
                    try:
                        plt.errorbar(
                        pulse.hrts_profiles['RmRsep'] + float(pulse.shift),
                        pulse.hrts_profiles['NE'], label='_nolegend_',
                        yerr=pulse.hrts_profiles['DNE'], fmt=None,ecolor=pulse.color)
                    except:
                        logger.error(
                            'impossible to plot NE from HRTS for pulse ' + str(
                                i))
                    try:
                        plt.scatter(pulse.hrts_fit['Rfit'] + float(pulse.shift_fit),
                                pulse.hrts_fit['nef3'], label='_nolegend_',color=pulse.color)
                    except:
                        logger.error(
                            'impossible to plot NE fit from HRTS for pulse ' + str(
                                i))


                plt.legend(loc=0, prop={'size': 18})
            except:
                logger.error("Could not plot HRTS ne")

            try:
                logger.info('plotting ne_ot')
                fname = 'ne_ot_comparison'

                plt.figure(num=fname)
                plt.suptitle(ftitle, fontsize=11)

                if pulse.plot_exp == "True":
                    logger.debug('plot exp pulse '+str(i))
                    try:
                        plt.scatter(pulse.lp_profiles['dSsep'],
                                    pulse.lp_profiles['ne'],
                                    label=pulse.pulse,color=pulse.color)
                        logger.debug('here ne_ot')
                    except:
                        logger.error('no ne LP exp data for pulse '+str(i))
                if pulse.plot_sim == "True":
                    logger.debug('plot sim  pulse '+str(i) )
                    try:
                        plt.plot(pulse.e2d_profiles_ot['dsrad_ot'],
                                 pulse.e2d_profiles_ot['denel_ot'], '-',
                                 label=pulse.pulse,color=pulse.color)
                        logger.debug('try plotting e2d ne  pulse '+str(i))
                    except:
                        plt.plot(pulse.e2d_profiles_ot['dsrad'],
                                 pulse.e2d_profiles_ot['denel'], '-',
                                 label=pulse.pulse,color=pulse.color)
                        logger.debug('except plotting e2d ne pulse '+str(i))
                plt.legend(loc=0, prop={'size': 18})

            except:
                logger.error("Could not plot ne ot")
                # logger.error("Could not plot ne ot")
            #     logger.info('plotting te_ot')
            try:
                fname = 'te_ot_comparison'
                plt.figure(num=fname)
                plt.suptitle(fname, fontsize=11)
                if pulse.plot_exp == "True":
                    logger.debug('plot exp pulse '+str(i))
                    try:
                        plt.scatter(pulse.lp_profiles['dSsep'],
                                    pulse.lp_profiles['te'],
                                    label=pulse.pulse ,color=pulse.color)
                        logger.debug('here ne_ot')
                    except:
                        logger.error('no te LP exp data for pulse '+str(i))
                if pulse.plot_sim == "True":
                    logger.debug('plot sim pulse '+str(i))
                    try:
                        plt.plot(pulse.e2d_profiles_ot['dsrad_ot'],
                                 pulse.e2d_profiles_ot['te_ot'], '-',
                                 label=pulse.pulse ,color=pulse.color)
                        logger.debug('try plotting e2d te pulse '+str(i))
                    except:
                        plt.plot(pulse.e2d_profiles_ot['dsrad'],
                                 pulse.e2d_profiles_ot['teve'], '-',
                                 label=pulse.pulse ,color=pulse.color)
                        logger.debug('except plotting e2d te pulse '+str(i))

                plt.legend(loc=0, prop={'size': 18})
            except:
                logger.error("Could not plot te ot")

            try:
                fname = 'jsat_ot_comparison'
                plt.figure(num=fname)
                plt.suptitle(fname, fontsize=11)
                if pulse.plot_exp == "True":
                    logger.debug('plot exp pulse '+str(i))
                    try:
                        plt.scatter(pulse.lp_profiles['dSsep'],
                                    pulse.lp_profiles['jsat'],
                                    label=pulse.pulse ,color=pulse.color)
                        logger.debug('here jsat_ot')
                    except:
                        logger.error('no jsat LP exp data for pulse '+str(i))
                if pulse.plot_sim == "True":
                    logger.debug('plot sim pulse '+str(i))
                    try:
                        plt.plot(pulse.e2d_profiles_ot['dsrad_ot'],
                                 -pulse.e2d_profiles_ot['jtargi_ot'], '-',
                                 label=pulse.pulse ,color=pulse.color)
                        logger.debug('try plotting e2d jsat  pulse '+str(i))
                    except:
                        plt.plot(pulse.e2d_profiles_ot['dsrad'],
                                 -pulse.e2d_profiles_ot['jtargi'], '-',
                                 label=pulse.pulse ,color=pulse.color)
                        logger.debug('except plotting e2d jsat  pulse '+str(i))
                plt.legend(loc=0, prop={'size': 18})

            except:

                logger.error("Could not plot jsat")

            try:
                fname = 'Dperp_comparison'
                plt.figure(num=fname)
                plt.suptitle(fname, fontsize=11)
                # print(pulse)
                if pulse.plot_sim == "True":
                    try:
                        logger.debug('try pulse '+str(i) +' Dperp')
                        plt.scatter(pulse.e2d_profiles['dsrad_omp'],
                                    pulse.e2d_profiles['dperp_omp'],
                                    label=pulse.pulse,color=pulse.color)
                    except:
                        logger.debug('except pulse '+str(i)+' Dperp')
                        plt.scatter(pulse.e2d_profiles['dsrad'],
                                    pulse.e2d_profiles['dperp'], label=pulse.pulse,color=pulse.color)

                plt.legend(loc=0, prop={'size': 18})
            except:

                logger.error("Could not plot pulse "+str(i)+" dperp")
                # %%
            try:
                fname = 'Xperp_comparison'
                plt.figure(num=fname)
                plt.suptitle(fname, fontsize=11)
                if pulse.plot_sim == "True":
                    try:
                        logger.debug('try pulse '+str(i)+' Xperp')
                        plt.scatter(pulse.e2d_profiles['dsrad_omp'],
                                    pulse.e2d_profiles['chii_omp'],
                                    label=pulse.pulse,color=pulse.color)
                    except:
                        logger.debug('except  pulse '+str(i)+' Xperp')
                        plt.scatter(pulse.e2d_profiles['dsrad'],
                                    pulse.e2d_profiles['chii'], label=pulse.pulse,color=pulse.color)

                plt.legend(loc=0, prop={'size': 18})
            except:
                logger.error("Could not plot xperp")

                # %%
        # print('there')
        fname = 'Xperp_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

        fname = 'Dperp_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

        fname = 'jsat_ot_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

        fname = 'te_ot_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

        fname = 'ne_ot_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

        fname = 'ne_omp_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #

        fname = 'Te_omp_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname, format='eps', dpi=300)
        plt.savefig('./figures/' + fname, dpi=300)  #




        # plt.waitforbuttonpress(0)  # this will wait for indefinite time
        # plt.close('all')

    @staticmethod
    def compare_multi_shots_simdata(dict1,*argv, ms=None, lw=None,var, loc):
        logger.debug('inside compare multi shots sim')

        if ms is None:
            ms = 40
        else:
            ms = ms
        if lw is None:
            lw = 2
        else:
            lw = lw

        input_dict = read_json(dict1)

        pulse1 = shot(input_dict)

        var=var.lower()

        loc=loc
        fname = var+'_'+loc+'_comparison'
        fnorm = 1

        names = ep.getnames(pulse1.tranfile, 1)

        description = None
        for i in (range(names.nNames)):
            if names.names[i].decode('utf-8').strip().lower() == var:
                logger.info('collecting {} information for pulse 1'.format(names.description[i].decode('utf-8').strip()))
                description = names.description[i].decode(
                    'utf-8').strip()
        if description is None:
            logger.error('no information for {}'.format(var))
            raise SystemExit
        ftitle = description
        # if var == 'PREHYD':
        #     var1='prestat'
        # else:
        var1=var
        fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
        # fylabel = '$n_{e,OT}\quad 10 x 10^{19} m^{-3}})$'

        plt.figure(num=fname)
        plt.suptitle(ftitle, fontsize=11)

        if pulse1.plot_sim == "True":
            logger.debug('plot sim pulse1 true')
            if loc.lower() == 'ot' or loc.lower() == 'it' :
                try:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad_'+loc],
                             pulse1.e2d_profiles_ot[var1+'_'+loc], '-',
                             label=pulse1.pulse, color=pulse1.color)
                    logger.debug('try plotting e2d'+var1+'_'+loc+' pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles_ot['dsrad'],
                             pulse1.e2d_profiles_ot[var1], '-',
                             label=pulse1.pulse, color=pulse1.color)
                    logger.debug('except plotting e2d'+var1+'_'+loc+' pulse1')
            if loc.lower() == 'omp' or loc.lower() == 'imp' :
                try:
                    plt.plot(pulse1.e2d_profiles['dsrad_'+loc],
                             pulse1.e2d_profiles[var1+'_'+loc], '-',
                             label=pulse1.pulse, color=pulse1.color)
                    logger.debug('try plotting e2d'+var1+'_'+loc+' pulse1')
                except:
                    plt.plot(pulse1.e2d_profiles['dsrad'],
                             pulse1.e2d_profiles[var1], '-',
                             label=pulse1.pulse, color=pulse1.color)
                    logger.debug('except plotting e2d '+var1+'_'+loc+' pulse1')

        axes = plt.axes()
        plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
        # axes.set_ylim(bottom=0)
        plt.legend(loc=0, prop={'size': 18})


        # print('HERE ')
        for i,arg in enumerate(argv):
            i=i+2
            json_dict = read_json(arg)
            pulse = shot(json_dict)

            
            label = pulse.label
            fname = var + '_' + loc + '_comparison'
            fnorm = 1
            names = ep.getnames(pulse.tranfile, 1)

            for j in (range(names.nNames)):
                if names.names[i].decode(
                        'utf-8').strip().lower() == var:
                    logger.info(
                        'collecting {} information for pulse {}'.format(
                            names.description[j].decode('utf-8').strip(),str(j)))

                    description = names.description[j].decode('utf-8').strip()
            ftitle = description
            # if var == 'PREHYD':
            #     var1 = 'prestat'
            # else:
            var1 = var
            fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
            # fylabel = '$n_{e,OT}\quad 10 x 10^{19} m^{-3}})$'

            plt.figure(num=fname)
            plt.suptitle(ftitle, fontsize=11)

            if pulse.plot_sim == "True":
                logger.debug('plot sim pulse'+str(i) +' true')
                if loc.lower() == 'ot' or loc.lower() == 'it':
                    try:
                        plt.plot(pulse.e2d_profiles_ot['dsrad_' + loc],
                                 pulse.e2d_profiles_ot[
                                     var1 + '_' + loc], '-',
                                 label=pulse.pulse, color=pulse.color)
                        logger.debug(
                            'try plotting e2d' + var1 + '_' + loc + ' pulse '+str(i))
                    except:
                        plt.plot(pulse.e2d_profiles_ot['dsrad'],
                                 pulse.e2d_profiles_ot[var1], '-',
                                 label=pulse.pulse, color=pulse.color)
                        logger.debug(
                            'except plotting e2d' + var1 + '_' + loc + ' pulse '+str(i))
                if loc.lower() == 'omp' or loc.lower() == 'imp':
                    try:
                        plt.plot(pulse.e2d_profiles['dsrad_' + loc],
                                 pulse.e2d_profiles[var1 + '_' + loc],
                                 '-',
                                 label=pulse.pulse, color=pulse.color)
                        logger.debug(
                            'try plotting e2d' + var1 + '_' + loc + ' pulse '+str(i))
                    except:
                        plt.plot(pulse.e2d_profiles['dsrad'],
                                 pulse.e2d_profiles[var1], '-',
                                 label=pulse.pulse, color=pulse.color)
                        logger.debug(
                            'except plotting e2d ' + var1 + '_' + loc + ' pulse '+str(i))
            plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
            axes = plt.axes()
            # axes.set_ylim(bottom=0)
            plt.legend(loc=0, prop={'size': 18})
            label = pulse.label

        fname = var + '_' + loc + '_comparison'
        plt.figure(num=fname)
        plt.savefig('./figures/' + fname+'_'+pulse1.label, format='eps', dpi=300)
        plt.savefig('./figures/' + fname+'_'+pulse1.label, dpi=300)  #
