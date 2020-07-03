import logging
logger = logging.getLogger(__name__)
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import pdb;
import numpy as np
import gzip
import pandas as pd
import xarray as xr
from types import SimpleNamespace
from utility import *
from class_geom import geom

import sys
import os
import warnings

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
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

try:
    ep = eproc
except:
    logger.error('failed to load EPROC')
    # raise SystemExit

# ----------------------------
__author__ = "Bruno Viola"
__Name__ = "class EIRENE"
__version__ = "0.1"
__release__ = "0"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
__status__ = "Testing"
# __status__ = "Production"
# __credits__ = [""]


class Eirene():
    """
    class to store information from EIRENE
    """
    
    def __init__(self,folder):


        #defyning a few colors

        self.BLUE = '#6699cc'
        self.GRAY = '#999999'
        self.DARKGRAY = '#333333'
        self.YELLOW = '#ffcc33'
        self.GREEN = '#339933'
        self.RED = '#ff3333'
        self.BLACK = '#000000'
        #default setting for EIRENE outputs (may change in the future)

        #folder containing eirene files (can be the catalog folder or run folder)
        self.runfolder = folder

        # Set         necessary        version         number
        self.chemFluxDepFileVersion_withSAREA = 1.2

        self.transferFileVersion_withSurfaceResolution = 1.1

        # following are not used (yet)
        # #########

        self.NPLS_vol_dataname = 27 # number of columns of PLS data
        self.NMOL_vol_dataname = 11 # number of columns of MOL data
        self.NATM_vol_VoldataName = 15# number of columns of ATM data
        self.NION_vol_dataname = 7# number of columns of ION data
        self.NMISCdataname = 11 # number of columns of MISC data

        self.NPLS_surf_dataname = 4
        self.NATM_surf_dataname = 4
        self.NMOL_surf_dataname = 14
        self.NION_surf_dataname = 14
        # #########

        #puff information
        self.npuff = 0
        self.nz1puff = 0
        self.nz2puff = 0


        self.nD2puff = 0
        self.nDpuff = 0
        self.nImp1Puff = 0
        self.nImp2Puff = 0



        #defining storage classes and initialising them
        self.ATM = SimpleNamespace()
        self.MOL = SimpleNamespace()
        self.ION = SimpleNamespace()
        self.PLS = SimpleNamespace()
        self.MISC = SimpleNamespace()
        self.PHOT = SimpleNamespace()

        self.geom = SimpleNamespace()
        self.geom.xv = []
        self.geom.yv = []
        self.geom.Elements = []
        self.geom.verts = []
        self.geom.pump = []
        self.geom.pump = []
        self.geom.puff = []

        self.ESRF_TYPE_NAMES = []


        self.ATM.VoldataName = []
        self.ATM.VolunitName = []
        self.ATM.SurfdataName = []
        self.ATM.SurfunitName = []
        self.ATM.names = {}
        self.ATM.vol_avg_data = []
        self.ATM.surf_avg_data = []

        self.MOL.VoldataName = []
        self.MOL.VolunitName =  []
        self.MOL.SurfdataName = []
        self.MOL.SurfunitName = []
        self.MOL.names ={}
        self.MOL.vol_avg_data = []
        self.MOL.surf_avg_data = []

        self.ION.VoldataName = []
        self.ION.VolunitName= []
        self.ION.SurfdataName = []
        self.ION.SurfunitName = []
        self.ION.names ={}
        self.ION.vol_avg_data = []
        self.ION.surf_avg_data = []

        self.PHOT.VoldataName = []
        self.PHOT.VolunitName= []
        self.PHOT.SurfdataName = []
        self.PHOT.SurfunitName = []
        self.PHOT.names ={}
        self.PHOT.vol_avg_data = []
        self.PHOT.surf_avg_data = []

        self.PLS.VoldataName = []
        self.PLS.VolunitName= []
        self.PLS.SurfdataName = []
        self.PLS.SurfunitName = []
        self.PLS.names ={}
        self.PLS.vol_avg_data = []
        self.PLS.surf_avg_data = []


        self.MISC.VoldataName= []
        self.MISC.VolunitName= []
        self.MISC.SurfunitName = []
        self.MISC.SurfunitName = []
        self.MISC.names = {}
        self.MISC.vol_avg_data = []
        self.MISC.surf_avg_data = []

        #
        #initialising names for volumetric data- check with Gerard/Derek
        #
        self.PLS.VoldataName.append('papl - part.source atm coll.')
        self.PLS.VoldataName.append('pmpl - part.source mol coll.')
        self.PLS.VoldataName.append('pipl - part.source ion coll.')
        self.PLS.VoldataName.append('pphpl - part.source phot coll.')
        self.PLS.VoldataName.append('papl+pmpl+pipl - part.source')
        self.PLS.VoldataName.append('mapl - mom.source atm coll.')
        self.PLS.VoldataName.append('mmpl - mom.source mol coll.')
        self.PLS.VoldataName.append('mipl - mom.source ion coll.')
        self.PLS.VoldataName.append('mphpl - mom.source phot coll.')
        self.PLS.VoldataName.append('mapl+mmpl+mipl - mom.source')
        self.PLS.VoldataName.append('diin - plasma density bulk plasma')
        self.PLS.VoldataName.append('vxin - plasma drift velocity (x)')
        self.PLS.VoldataName.append('vyin - plasma drift velocity (y)')
        self.PLS.VoldataName.append('vzin - plasma drift velocity (z)')
        self.PLS.VoldataName.append('bvin - ')
        self.PLS.VoldataName.append('tiin - plasma temperature bulk plasma')
        self.PLS.VoldataName.append('edrift - kinetic energy in drift motion bulk plasma')
        self.PLS.VoldataName.append('eapl - eng.source atm coll.')
        self.PLS.VoldataName.append('empl - eng.source mol coll.')
        self.PLS.VoldataName.append('eipl - eng.source ion coll.')
        self.PLS.VoldataName.append('ephpl - eng.source phot coll.')
        self.PLS.VoldataName.append('eapl+empl+eipl - eng.source')
        self.PLS.VoldataName.append('eael - eng.source electrons atm coll.')
        self.PLS.VoldataName.append('emel - eng.source electrons mol coll.')
        self.PLS.VoldataName.append('eiel - eng.source electrons ion coll.')
        self.PLS.VoldataName.append('ephel - eng.source electrons phot coll.')
        self.PLS.VoldataName.append('eael+emel+eiel - eng.source electrons')


        # set unit names for bulk plasma ions
        self.PLS.VolunitName.append('amp/cm^3')
        self.PLS.VolunitName.append('amp/cm^3')
        self.PLS.VolunitName.append('amp/cm^3')
        self.PLS.VolunitName.append('amp/cm^3')
        self.PLS.VolunitName.append('amp/cm^3')
        self.PLS.VolunitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.VolunitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.VolunitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.VolunitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.VolunitName.append( 'amp*g*cm/(s*cm^3)')
        self.PLS.VolunitName.append( '1/cm^3')
        self.PLS.VolunitName.append( 'cm/s')
        self.PLS.VolunitName.append( 'cm/s')
        self.PLS.VolunitName.append( 'cm/s')
        self.PLS.VolunitName.append( '?')
        self.PLS.VolunitName.append( 'eV')
        self.PLS.VolunitName.append( 'eV')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')
        self.PLS.VolunitName.append( 'watt/cm^3')

        self.ATM.VoldataName.append('pdena - atom density')
        self.ATM.VoldataName.append('vxdena - atom momentum density (x)')
        self.ATM.VoldataName.append('vydena - atom momentum density (y)')
        self.ATM.VoldataName.append('vzdena - atom momentum density (z)')
        self.ATM.VoldataName.append('vdenpara - atom momentum density (B)')
        self.ATM.VoldataName.append('edena - atom energy density')
        self.ATM.VoldataName.append('edena/pdena - ')
        self.ATM.VoldataName.append('not used - ')
        self.ATM.VoldataName.append('sigma - ')
        self.ATM.VoldataName.append('not used - ')
        self.ATM.VoldataName.append('not used - ')
        self.ATM.VoldataName.append('paat - part.source atm coll.')
        self.ATM.VoldataName.append('pmat - part.source mol coll.')
        self.ATM.VoldataName.append('piat - part.source ion coll.')
        self.ATM.VoldataName.append('paat+pmat+piat - part.source')

        # set unit names for neutral atoms

        self.ATM.VolunitName.append('1/cm^3')
        self.ATM.VolunitName.append('g*cm/(s*cm^3)')
        self.ATM.VolunitName.append('g*cm/(s*cm^3)')
        self.ATM.VolunitName.append('g*cm/(s*cm^3)')
        self.ATM.VolunitName.append('g*cm/(s*cm^3)')
        self.ATM.VolunitName.append('eV/cm^3')
        self.ATM.VolunitName.append('eV*s/(g*cm)')
        self.ATM.VolunitName.append(' ')
        self.ATM.VolunitName.append('?')
        self.ATM.VolunitName.append(' ')
        self.ATM.VolunitName.append(' ')
        self.ATM.VolunitName.append('amp/cm^3')
        self.ATM.VolunitName.append('amp/cm^3')
        self.ATM.VolunitName.append('amp/cm^3')
        self.ATM.VolunitName.append('amp/cm^3')

        # set data names for neutral molecules

        self.MOL.VoldataName.append('pdenm - molecule density')
        self.MOL.VoldataName.append('vxdenm - molecule momentum density (x)')
        self.MOL.VoldataName.append('vydenm - molecule momentum density (y)')
        self.MOL.VoldataName.append('vzdenm - molecule momentum density (z)')
        self.MOL.VoldataName.append('vdenpara - molecule momentum density (B)')
        self.MOL.VoldataName.append('edenm - molecule energy density')
        self.MOL.VoldataName.append('edenm/pdenm - ')

        # set unit names for neutral molecules
        self.MOL.VolunitName.append('1/cm^3')
        self.MOL.VolunitName.append('g*cm/(s*cm^3)')
        self.MOL.VolunitName.append('g*cm/(s*cm^3)')
        self.MOL.VolunitName.append('g*cm/(s*cm^3)')
        self.MOL.VolunitName.append('g*cm/(s*cm^3)')
        self.MOL.VolunitName.append('eV/cm^3')
        self.MOL.VolunitName.append('eV*s/(g*cm)')

        # set data names for test ions

        self.ION.VoldataName.append('pdeni - test ion density')
        self.ION.VoldataName.append('vxdeni - test ion momentum density (x)')
        self.ION.VoldataName.append('vydeni - test ion momentum density (y)')
        self.ION.VoldataName.append('vzdeni - test ion momentum density (z)')
        self.ION.VoldataName.append('vdenpara - test ion momentum density (B)')
        self.ION.VoldataName.append('edeni - test ion energy density')
        self.ION.VoldataName.append('edeni/pdeni - ')

        # set unit names for test ions
        self.ION.VolunitName.append('1/cm^3')
        self.ION.VolunitName.append('g*cm/(s*cm^3)')
        self.ION.VolunitName.append('g*cm/(s*cm^3)')
        self.ION.VolunitName.append('g*cm/(s*cm^3)')
        self.ION.VolunitName.append('g*cm/(s*cm^3)')
        self.ION.VolunitName.append('eV/cm^3')
        self.ION.VolunitName.append('eV*s/(g*cm)')
        #
        # set data names for misc data

        self.MISC.VoldataName.append('ncltal - ')
        self.MISC.VoldataName.append('not used - 1')
        self.MISC.VoldataName.append('not used - 2')
        self.MISC.VoldataName.append('vol - zone volume')
        self.MISC.VoldataName.append('voltal - ')
        self.MISC.VoldataName.append('dein - plasma density electrons')
        self.MISC.VoldataName.append('tein - plasma temperature electrons')
        self.MISC.VoldataName.append('bxin - B unit vector (x)')
        self.MISC.VoldataName.append('byin - B unit vector (y)')
        self.MISC.VoldataName.append('bzin - B unit vector (z)')
        self.MISC.VoldataName.append('bfin - B strength')
        #
        # set unit names for misc data
        self.MISC.VolunitName.append('?')
        self.MISC.VolunitName.append(' ')
        self.MISC.VolunitName.append(' ')
        self.MISC.VolunitName.append('cm^3')
        self.MISC.VolunitName.append('?')
        self.MISC.VolunitName.append('1/cm^3')
        self.MISC.VolunitName.append('eV')
        self.MISC.VolunitName.append(' ')
        self.MISC.VolunitName.append(' ')
        self.MISC.VolunitName.append(' ')
        self.MISC.VolunitName.append('tesla')


        #
        #initialising names for surface data- check with Gerard/Derek
        #

        # ; set data names for bulk plasma ions

        self.PLS.SurfdataName.append("potpl - Incident part. flux bulk ions")
        self.PLS.SurfdataName.append("eotpl - Incident enrg. flux bulk ions")
        self.PLS.SurfdataName.append(
            "sptpl - Sputtered flux by incident bulk ions")
        self.PLS.SurfdataName.append("spump - Pumped flux by bulk ions")

        # ; set unit names for bulk plasma ions

        self.PLS.SurfunitName.append("amp")
        self.PLS.SurfunitName.append("watt")
        self.PLS.SurfunitName.append("amp")
        self.PLS.SurfunitName.append("amp")

        # ; set data names for neutral atoms

        self.ATM.SurfdataName.append("potat - Incident part. flux atoms")
        self.ATM.SurfdataName.append("prfaat - Emitted part. flux atm => atm")
        self.ATM.SurfdataName.append("prfmat - Emitted part. flux mol => atm")
        self.ATM.SurfdataName.append(
            "prfiat - Emitted part. flux test ion => atm")
        self.ATM.SurfdataName.append(
            "prfphat - Emitted part. flux photon => atm")
        self.ATM.SurfdataName.append(
            "prfpat - Emitted part. flux bulk ion => atm")
        self.ATM.SurfdataName.append("eotat - Incident enrg. flux atoms")
        self.ATM.SurfdataName.append("erfaat - Emitted enrg. flux atm => atm")
        self.ATM.SurfdataName.append("erfmat - Emitted enrg. flux mol => atm")
        self.ATM.SurfdataName.append(
            "erfiat - Emitted enrg. flux test ion => atm")
        self.ATM.SurfdataName.append(
            "erfphat - Emitted enrg. flux photon => atm")
        self.ATM.SurfdataName.append(
            "erfpat - Emitted enrg. flux bulk ion => atm")
        self.ATM.SurfdataName.append("sptat - Sputtered flux by incident atoms")
        self.ATM.SurfdataName.append("spump - Pumped flux by atoms")

        # ; set unit names for neutral atoms

        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('watt')
        self.ATM.SurfunitName.append('watt')
        self.ATM.SurfunitName.append('watt')
        self.ATM.SurfunitName.append('watt')
        self.ATM.SurfunitName.append('watt')
        self.ATM.SurfunitName.append('watt')
        self.ATM.SurfunitName.append('amp')
        self.ATM.SurfunitName.append('amp')

        # ; set data names for neutral molecules

        self.MOL.SurfdataName.append("potml - Incident part. flux molecules")
        self.MOL.SurfdataName.append("prfaml - Emitted part. flux atm => mol")
        self.MOL.SurfdataName.append("prfmml - Emitted part. flux mol => mol")
        self.MOL.SurfdataName.append(
            "prfiml - Emitted part. flux test ion => mol")
        self.MOL.SurfdataName.append(
            "prfphml - Emitted part. flux photon => mol")
        self.MOL.SurfdataName.append(
            "prfpml - Emitted part. flux bulk ion => mol")
        self.MOL.SurfdataName.append("eotml - Incident enrg. flux molecules")
        self.MOL.SurfdataName.append("erfaml - Emitted enrg. flux atm => mol")
        self.MOL.SurfdataName.append("erfmml - Emitted enrg. flux mol => mol")
        self.MOL.SurfdataName.append(
            "erfiml - Emitted enrg. flux test ion => mol")
        self.MOL.SurfdataName.append(
            "erfphml - Emitted enrg. flux photon => mol")
        self.MOL.SurfdataName.append(
            "erfpml - Emitted enrg. flux bulk ion => mol")
        self.MOL.SurfdataName.append(
            "sptml - Sputtered flux by incident molecules")
        self.MOL.SurfdataName.append("spump - Pumped flux by molecules")

        # ; set unit names for neutral molecules

        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('watt')
        self.MOL.SurfunitName.append('watt')
        self.MOL.SurfunitName.append('watt')
        self.MOL.SurfunitName.append('watt')
        self.MOL.SurfunitName.append('watt')
        self.MOL.SurfunitName.append('watt')
        self.MOL.SurfunitName.append('amp')
        self.MOL.SurfunitName.append('amp')

        # ; set data names for test ions

        self.ION.SurfdataName.append("potio - Incident part. flux test ions")
        self.ION.SurfdataName.append("prfaio - Emitted part. flux atm => t.i.")
        self.ION.SurfdataName.append("prfmio - Emitted part. flux mol => t.i.")
        self.ION.SurfdataName.append(
            "prfiio - Emitted part. flux test ion => t.i.")
        self.ION.SurfdataName.append(
            "prfphio - Emitted part. flux photon => t.i.")
        self.ION.SurfdataName.append(
            "prfpio - Emitted part. flux bulk ion => t.i.")
        self.ION.SurfdataName.append("eotio - Incident enrg. flux test ions")
        self.ION.SurfdataName.append("erfaio - Emitted enrg. flux atm => t.i.")
        self.ION.SurfdataName.append("erfmio - Emitted enrg. flux mol => t.i.")
        self.ION.SurfdataName.append(
            "erfiio - Emitted enrg. flux test ion => t.i.")
        self.ION.SurfdataName.append(
            "erfphio - Emitted enrg. flux photon => t.i.")
        self.ION.SurfdataName.append(
            "erfpio - Emitted enrg. flux bulk ion => t.i.")
        self.ION.SurfdataName.append(
            "sptio - Sputtered flux by incident test ions")
        self.ION.SurfdataName.append("spump - Pumped flux by test ions")

        # ; set unit names for test ions

        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('watt')
        self.ION.SurfunitName.append('watt')
        self.ION.SurfunitName.append('watt')
        self.ION.SurfunitName.append('watt')
        self.ION.SurfunitName.append('watt')
        self.ION.SurfunitName.append('watt')
        self.ION.SurfunitName.append('amp')
        self.ION.SurfunitName.append('amp')



        # ; init eirene surface type names

        self.ESRF_TYPE_NAMES.append("time surface")
        self.ESRF_TYPE_NAMES.append("puffing surface")
        self.ESRF_TYPE_NAMES.append("pumping surface")
        self.ESRF_TYPE_NAMES.append("inner core boundary")
        self.ESRF_TYPE_NAMES.append("target")
        self.ESRF_TYPE_NAMES.append("radial SOL/private boundary")
        self.ESRF_TYPE_NAMES.append("vessel surface")
        self.ESRF_TYPE_NAMES.append("diagnostic surfaces")
        self.ESRF_TYPE_NAMES.append("semi transparent surfaces")

        self.npump = 0
        self.npuff = 0
        self.npuf2 = 0
        self.nzpuff = 0
        self.poly = []

        self.nImp1puff = 0
        self.nImp2puff = 0



        self.D2puff_sfnum = []
        self.Dpuff_sfnum = []
        self.Imp1puff_sfnum = []
        self.Imp2puff_sfnum = []






        super(Eirene, self).__init__()

        self._read_eirene()


    def _read_eirene(self):
        """
        function that reads EIRENE files (automatically when initialising objects)
        :return:
        """
        #read triangles coordinates
        logger.info(' reading eirene.npco_char file \n')
        self.geom.xv, self.geom.yv,z= read_npco_file(self.runfolder+'eirene.npco_char')
        #reads triangles map and vertices
        logger.info( 'reading eirene.elemente file \n')
        self.geom.Elements,self.geom.verts = read_elemente_file(self.runfolder+'eirene.elemente')
        logger.info( 'reading eirene.trimap file \n')
        self.geom.trimap,self.geom.trimap_1,self.geom.trimap_2 = read_trimap_file(self.runfolder+'eirene.trimap')

        logger.info('reading e2deir.dat file \n')
        self.npo, self.ne2ddata, self.KORPG, self.RVERTP, self.ZVERTP, self.IKOR, self.JKOR = load_eiri_geo_data(
            self.runfolder + 'e2deir.dat')

        #reads pump (only for standard EIRENE files)
        logger.info( 'reading eirene pump file \n')
        self.geom.pump = read_pump_file(self.runfolder + 'pump')
        #read puff location
        logger.info( 'reading puff file \n')
        self.geom.puff = read_puff_file(self.runfolder + 'puff.dat')

###################################

        with open("../exp_data/vessel_JET_csv.txt", "rt") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            # col = list(zip(*reader))[1]
            csv_dic = []

            for row in reader:
                csv_dic.append(row)
            # print(csv_dic)
            col1 = []
            col2 = []

            for row in csv_dic:
                col1.append(row[0])
                col2.append(row[1])
            dummy = np.array(col1)
            # print(dummy)
            dummy2 = np.array(col2)
            dummy2 = [float(i) for i in dummy2]
            self.z_ves = -np.asarray(dummy2)
            dummy = [float(i) for i in dummy]
            self.r_ves = np.asarray(dummy)

        BoundCoordTuple = list(zip(self.r_ves, self.z_ves))
        self.VesselpolygonBound = Polygon(BoundCoordTuple)

        #start reading informations
        logger.info( 'collecting information from eirene.input file \n')
        with open(self.runfolder + 'eirene.input') as f:
            lines = f.readlines()

            text_block3 = '** 3b'

            text_atoms_spec = '** 4a NEUTRAL ATOMS SPECIES CARDS:'
            text_mole_spec = '** 4b NEUTRAL MOLECULES SPECIES CARDS'
            text_ion_spec = '**4c TEST ION SPECIES CARDS:'
            text_bulk_spec = '*** 5. DATA FOR PLASMA-BACKGROUND'
            text_phot      = '** 4d photons'
            text_block7 = '*** 7.'

            text_molecular = "*       D2 molecular puff"
            text_molecular_bis = "molecular fuel puff (wall puff)"
            text_atomic = "*        D atom puff (CX "
            text_atomic_bis="atom fuel puff (CX"
            text_imp1="*   IMP 01 atom puff"
            text_imp1_bis= "IMP. 1 puff "
            text_imp2 = "*   IMP 02 atom puff"
            text_imp2_bis = "IMP. 2 puff "
            info_text_phot = False
            info_text_molecular = False
            info_text_mole_spec = False
            info_text_phot = False
            info_text_block7 = False
            info_text_atoms_spec = False
            info_text_atomic = False
            info_text_imp1 = False
            info_text_imp2 = False
            info_text_bulk_spec = False
            info_text_ion_spec = False

            for index, line in enumerate(lines):

                if text_block3 in str(line):
                    index =index+1
                    dummy = lines[index].split()
                    self.ntot = int(dummy[0])
                    index = index + 1
                    for i in range(0,self.ntot):
                        if lines[index].startswith('* puff (wall)'):
                            self.npuff=self.npuff+1
                            poly=1.0
                        if lines[index].startswith('* core puff (atomic)'):
                            self.npuf2 = self.npuf2+1
                            poly=2.0
                        if lines[index].startswith('* pump'):
                            self.npump= self.npump +1
                            poly=3.0
                        if lines[index].startswith('* semi'):
                            self.npump= self.npump+1
                            poly=3.0
                        if lines[index].startswith('* zpuff'):
                            self.nzpuff = self.nzpuff
                            poly=4.0
                        index = index + 3
                        dummy = lines[index].split()
                        r1 = float(dummy[0])
                        z1 = float(dummy[1])
                        phi1 = float(dummy[2])
                        r2 = float(dummy[3])
                        z2 = float(dummy[4])
                        phi2 = float(dummy[5])
                        self.poly.append([poly,r1,z1,r2,z2])
                        logger.log(5,"{}".format([poly,r1,z1,r2,z2]))
                        index = index + 1
                        if not lines[index].startswith('SURFMOD'):
                            index = index + 3
                        else:
                            break




                if text_atoms_spec in str(line):
                    if info_text_atoms_spec:
                        pass
                    else:
                        index = index +1
                        dummy = lines[index].split()
                        self.natm = int(dummy[0])

                        for i in range(0,self.natm):
                            index = index + 1
                            dummy=lines[index].split()
                            self.ATM.names[i] = dummy[1]
                            nreac = int(dummy[9])
                            index = index + 2*nreac
                        info_text_atoms_spec=True


                if text_mole_spec in str(line):
                    if info_text_mole_spec:
                        pass
                    else:
                        index = index +1
                        dummy = lines[index].split()
                        self.nmol = int(dummy[0])

                        for i in range(0,self.nmol):
                            index = index + 1
                            dummy=lines[index].split()
                            self.MOL.names[i] = dummy[1]
                            nreac = int(dummy[9])
                            index = index + 2 * nreac
                        info_text_mole_spec = True

                if text_ion_spec in str(line):
                    if info_text_ion_spec:
                        pass
                    else:
                        index = index +1
                        dummy = lines[index].split()
                        self.nion = int(dummy[0])

                        for i in range(0,self.nion):
                            index = index + 1
                            dummy=lines[index].split()
                            self.ION.names[i] = dummy[1]
                            nreac = int(dummy[9])
                            index = index + 2 * nreac
                            info_text_ion_spec=True

                if text_phot in str(line):
                    if info_text_phot:
                        pass
                    else:

                        index = index +1
                        dummy = lines[index].split()
                        self.nphot = int(dummy[0])

                        for i in range(0,self.nphot):
                            index = index + 1
                            dummy=lines[index].split()
                            self.PHOT.names[i] = dummy[1]
                            nreac = int(dummy[9])
                            index = index + 2 * nreac
                        info_text_phot=True

                if text_bulk_spec in str(line):
                    if info_text_bulk_spec:
                        pass
                    else:
                        index = index +2
                        dummy = lines[index].split()
                        self.npls = int(dummy[0])

                        for i in range(0,self.npls):
                            index = index + 1
                            dummy=lines[index].split()
                            self.PLS.names[i] = dummy[1]
                            nreac = int(dummy[9])
                            index = index + 2 * nreac
                            info_text_bulk_spec=True


                if text_block7 in str(line):
                    if info_text_block7:
                        pass
                    else:
                        index =index +1
                        dummy = lines[index].split()
                        self.nstrata = int(dummy[0])
                        info_text_block7 = True



                if text_molecular in str(line):
                    if info_text_molecular:
                        pass
                    else:

                        index =index + 7

                        dummy = lines[index].split()

                        self.nD2puff = int(dummy[0])
                        logger.log(5,
                                   "Found D molecular puff with{} segments in EIRENE input block 7".format(
                                       self.nD2puff))
                        index =index +1
                        for i in range(0, self.nD2puff):
                            dummy = lines[index].split()
                            self.D2puff_sfnum.append(int(dummy[2]))
                            index = index + 2
                        info_text_molecular = True

                if text_molecular_bis in str(line):
                    if info_text_molecular:
                        pass
                    else:
                        index =index + 7

                        dummy = lines[index].split()

                        self.nD2puff = int(dummy[0])
                        logger.log(5,
                                   "Found D molecular puff with {} segments in EIRENE input block 7".format(
                                       self.nD2puff))

                        for i in range(0, self.nD2puff):
                            index = index + 1
                            dummy = lines[index].split()
                            self.D2puff_sfnum.append(int(dummy[2]))
                            index = index + 3
                        info_text_molecular = True

                if text_atomic in str(line):
                    if info_text_atomic:
                        pass
                    else:
                        index = index + 7

                        dummy = lines[index].split()

                        self.nDpuff = int(dummy[0])
                        logger.log(5,
                                   "Found D atomic puff with {} segments in EIRENE input block 7".format(
                                       self.nDpuff))
                        index = index + 1
                        for i in range(0, self.nDpuff):
                            dummy = lines[index].split()
                            self.Dpuff_sfnum.append(int(dummy[2]))
                            index = index + 2
                        info_text_atomic = True

                if text_imp1 in str(line):
                    if info_text_imp1:
                        pass
                    else:
                        index = index + 7

                        dummy = lines[index].split()

                        self.nImp1puff = int(dummy[0])
                        logger.log(5,
                                   "Found IMP 01 atomic puff with {} segments in EIRENE input block 7".format(
                                       self.nImp1puff))
                        index = index + 1
                        for i in range(0, self.nImp1puff):
                            dummy = lines[index].split()
                            self.Imp1puff_sfnum.append(int(dummy[2]))
                            index = index + 4
                            info_text_imp1 = True

                if text_imp2 in str(line):
                    if info_text_imp2:
                        pass
                    else:
                        index = index + 7

                        dummy = lines[index].split()

                        self.nImp2puff = int(dummy[0])
                        logger.log(5,
                                   "Found IMP 02 atomic puff with {} segments in EIRENE input block 7".format(
                                       self.nImp2puff))
                        index = index + 1
                        for i in range(0, self.nImp2puff):
                            dummy = lines[index].split()
                            self.Imp2puff_sfnum.append(int(dummy[2]))
                            index = index + 4
                        info_text_imp2 = True

                if text_atomic_bis in str(line):
                    if info_text_atomic:
                        pass
                    else:
                        index = index + 7

                        dummy = lines[index].split()

                        self.nDpuff = int(dummy[0])
                        logger.log(5,
                                   "Found D atomic puff with {} segments in EIRENE input block 7".format(
                                       self.nDpuff))
                        index = index + 1
                        for i in range(0, self.nDpuff):
                            dummy = lines[index].split()
                            self.Dpuff_sfnum.append(int(dummy[2]))
                            index = index + 4
                        info_text_atomic= True

                if text_imp1_bis in str(line):
                    if info_text_imp1:
                        pass
                    else:
                        index = index + 7

                        dummy = lines[index].split()

                        self.nImp1puff = int(dummy[0])
                        logger.log(5,
                                   "Found IMP 01 atomic puff with {} segments in EIRENE input block 7".format(
                                       self.nImp1puff))
                        index = index + 1
                        for i in range(0, self.nImp1puff):
                            dummy = lines[index].split()
                            self.Imp1puff_sfnum.append(int(dummy[2]))
                            index = index + 4
                        info_text_imp1 = True

                if text_imp2_bis in str(line):
                    if info_text_imp2:
                        pass
                    else:
                        index = index + 7

                        dummy = lines[index].split()

                        self.nImp2puff = int(dummy[0])
                        logger.log(5,
                                   "Found IMP 02 atomic puff with {} segments in EIRENE input block 7".format(
                                       self.nImp2puff))
                        index = index + 1
                        for i in range(0, self.nImp2puff):
                            dummy = lines[index].split()
                            self.Imp2puff_sfnum.append(int(dummy[2]))
                            index = index + 4
                        info_text_imp2 = True

                # if info_text_imp2 & info_text_imp1 & info_text_atomic & info_text_phot & info_text_atoms_spec & info_text_block7 & info_text_mole_spec  & info_text_molecular  is True:
                #     break
            f.close()

        logger.info("Found {} D2 wall puffs".format(self.npuff))
        logger.info("Found {} D core puffs".format(self.nDpuff))
        logger.info("Found {} impurity 01 puffs".format(self.nImp1puff))
        logger.info("Found {} impurity 02 puffs".format(self.nImp2puff))
        logger.info("Found {} pumps".format(self.npump))

        self.puff_polygon  = []
        self.puf2_polygon  = []
        self.pump_polygon  = []
        self.zpuff2_polygon  = []
        self.zpuff1_polygon  = []


        for i in range(0, self.npuff):
            if (self.poly[i][0] == 3.0):
                newlist=self.poly[i][1:4]
                newlist = [x / 100 for x in newlist]
                # self.pump_polygon.append(self.poly[i][1:4] )
                self.pump_polygon.append(newlist )
        # self.pump_polygon = [x / 100 for x in self.pump_polygon]

        for i in range(0,self.nD2puff):
            newlist = self.poly[self.D2puff_sfnum[i]][1:4]
            newlist = [x / 100 for x in newlist]
            # self.puff_polygon.append(self.D2puff_sfnum[i][1:4])
            # self.puff_polygon.append(self.poly[self.D2puff_sfnum[i]][1:4])
            self.puff_polygon.append(newlist)
        # self.puff_polygon = [x / 100 for x in self.puff_polygon]

        for i in range(0,self.nDpuff):
            newlist = self.poly[self.Dpuff_sfnum[i]][1:4]
            newlist = [x / 100 for x in newlist]
            # self.puf2_polygon.append(self.Dpuff_sfnum[i][1:4])
            self.puf2_polygon.append(newlist)
            # self.puf2_polygon.append(self.poly[self.Dpuff_sfnum[i]][1:4])
        # self.puf2_polygon = [x / 100 for x in self.puf2_polygon]

        for i in range(0,self.nImp1puff):
            newlist = self.poly[self.Imp1puff_sfnum[i]][1:4]
            newlist = [x / 100 for x in newlist]
            # self.zpuff2_polygon.append(self.Imp1puff_sfnum[i][1:4])
            self.zpuff2_polygon.append(newlist)
            # self.zpuff2_polygon.append(self.poly[self.Imp1puff_sfnum[i]][1:4])
        # self.zpuff2_polygon = [x / 100 for x in self.zpuff2_polygon]

        for i in range(0,self.nImp2puff):
            newlist = self.poly[self.Imp2puff_sfnum[i]][1:4]
            newlist = [x / 100 for x in newlist]
            # self.zpuff1_polygon.append(self.Imp2puff_sfnum[i][1:4])
            self.zpuff1_polygon.append(newlist)
            # self.zpuff1_polygon.append(self.poly[self.Imp2puff_sfnum[i]][1:4])
        # self.zpuff1_polygon = [x / 100 for x in self.zpuff1_polygon]

###################################

        # read transfer file and store data as pandas dataframe (first column is always a pandas index!)
        logger.info( 'reading eirene.transfer file \n')
        exists = os.path.isfile(self.runfolder + 'eirene.transfer.gz')

        if exists:

            f = gzip.open(self.runfolder + 'eirene.transfer.gz', 'rb')            

        else:
            f = open(self.runfolder + 'eirene.transfer', 'rb')              

        
        lines = f.readlines()
        text_version = '* Neutral transfer file version:'
        row_to_skip = 0
        for index, line in enumerate(lines):
            if text_version in str(line):
                dummy = lines[index].split()
                transfer_version = float(dummy[-1])

                if transfer_version < self.transferFileVersion_withSurfaceResolution:
                    logger.warning(
                'Need at least eirene.transfer file version {} to allow surface plotting of EIRENE data'.format(
                    self.transferFileVersion_withSurfaceResolution))
                break
            else:
                transfer_version = None


        text = '* nlimps'
        for index, line in enumerate(lines):
            if text in str(line):
                index=index+1
                dummy=lines[index].split()
                self.nlimps = int(dummy[0])
                self.nlim = int(dummy[1])
                self.nsts = int(dummy[2])
                if transfer_version is None:
                    surface_points=self.nlimps
                    row_to_skip = index + 3
                    break
                else:
                    if transfer_version>= self.transferFileVersion_withSurfaceResolution:
                        self.nlmps= int(dummy[3])
                        row_to_skip = index + 3
                        surface_points = self.nlmps
                        break
                    else:
                        surface_points=self.nlimps
                        row_to_skip = index + 2
                        break



        logger.log(5, row_to_skip)
                # 5          27        6086
        logger.info(' reading bulk plasma data')
        for i in range(0, self.npls):
            #READING DATA AS A BLOCK
            try:
                dummy1=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.Elements.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            except:
                dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                     nrows=self.geom.Elements.shape[0],
                                     delim_whitespace=True, header=None,
                                     index_col=False, error_bad_lines=False,
                                     warn_bad_lines=False)
            #dummy1 contains all volumetric average data for a species (has NPLSdataname column +1, the index)
            # dummy1[dummy1.columns[11]]
            dummy1.fillna(0, inplace=True)#converts nan into 0
            row_to_skip = row_to_skip +self.geom.Elements.shape[0]+1#
            logger.log(5, row_to_skip)
            # if transfer_version is not None:
            #dummy2 contains surface average data for the same specie
            try:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)


            except:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip +surface_points+ 3
            logger.log(5, row_to_skip)

            #as I loop through species I append this block, creating a big block matrix


            self.PLS.vol_avg_data.append(dummy1)
            # if transfer_version is not None:
            self.PLS.surf_avg_data.append(dummy2)
        # concatenate all data as a big dataframe (the first column is just the index)
        self.PLS.vol_avg_data = pd.concat(self.PLS.vol_avg_data, axis=0)#concatenates as row
        self.PLS.vol_avg_data.reset_index(drop=True, inplace=True)
        # if transfer_version is not None:
        self.PLS.surf_avg_data = pd.concat(self.PLS.surf_avg_data, axis=0)#concatenates as row
        self.PLS.surf_avg_data.reset_index(drop=True, inplace=True)





        # row_to_skip = 30648
        #row to skip should be 30647
        logger.info(' reading neutral atom data')
        for i in range(0,self.natm):
            try:
                dummy1=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.Elements.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            except:
                dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                     nrows=self.geom.Elements.shape[0],
                                     delim_whitespace=True, header=None,
                                     index_col=False, error_bad_lines=False,
                                     warn_bad_lines=False)
                # 36730
            dummy1.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip + self.geom.Elements.shape[0] + 1
            logger.log(5, row_to_skip)
            # if transfer_version is not None:
            try:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)

            except:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip +surface_points+ 1
            logger.log(5, row_to_skip)
            self.ATM.vol_avg_data.append(dummy1)
            # if transfer_version is not None:
            self.ATM.surf_avg_data.append(dummy2)

        self.ATM.vol_avg_data = pd.concat(self.ATM.vol_avg_data,
                                          axis=0)  # concatenates as row
        self.ATM.vol_avg_data.reset_index(drop=True, inplace=True)
        # if transfer_version is not None:
        self.ATM.surf_avg_data = pd.concat(self.ATM.surf_avg_data,
                                               axis=0)  # concatenates as row
        self.ATM.surf_avg_data.reset_index(drop=True, inplace=True)

        row_to_skip = row_to_skip + 1
        logger.log(5,row_to_skip)
        logger.info(' reading neutral molecules data')
        for i in range(0,self.nmol):
            try:
                dummy1=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.Elements.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            except:
                dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                     nrows=self.geom.Elements.shape[0],
                                     delim_whitespace=True, header=None,
                                     index_col=False, error_bad_lines=False,
                                     warn_bad_lines=False)
            dummy1.fillna(0, inplace=True)#converts nan into 0
            row_to_skip = row_to_skip + self.geom.Elements.shape[0] + 1
            logger.log(5, row_to_skip)
            # if transfer_version is not None:
            try:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            except:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip + surface_points + 2
            logger.log(5, row_to_skip)
            self.MOL.vol_avg_data.append(dummy1)
            # if transfer_version is not None:
            self.MOL.surf_avg_data.append(dummy2)

        self.MOL.vol_avg_data = pd.concat(self.MOL.vol_avg_data,
                                          axis=0)  # concatenates as row
        self.MOL.vol_avg_data.reset_index(drop=True, inplace=True)
        # if transfer_version is not None:
        self.MOL.surf_avg_data = pd.concat(self.MOL.surf_avg_data,
                                               axis=0)  # concatenates as row
        self.MOL.surf_avg_data.reset_index(drop=True, inplace=True)

        # row_to_skip = row_to_skip + 1
        # logger.log(5, row_to_skip)

        logger.info('  reading test ions data')
        for i in range(0,self.nion):
            try:
                dummy1=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.Elements.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            except:
                dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                     nrows=self.geom.Elements.shape[0],
                                     delim_whitespace=True, header=None,
                                     index_col=False, error_bad_lines=False,
                                     warn_bad_lines=False)
            dummy1.fillna(0, inplace=True) #converts nan into 0
            row_to_skip = row_to_skip + self.geom.Elements.shape[0] + 1
            logger.log(5, row_to_skip)
            # if transfer_version is not None:
            try:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            except:
                dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer', skiprows=row_to_skip,
                                 nrows=surface_points,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip + surface_points + 2
            logger.log(5, row_to_skip)
            self.ION.vol_avg_data.append(dummy1)
            # if transfer_version is not None:
            self.ION.surf_avg_data.append(dummy2)

        self.ION.vol_avg_data = pd.concat(self.ION.vol_avg_data,
                                          axis=0)  # concatenates as row
        self.ION.vol_avg_data.reset_index(drop=True, inplace=True)
        # if transfer_version is not None:
        self.ION.surf_avg_data = pd.concat(self.ION.surf_avg_data,
                                               axis=0)  # concatenates as row
        self.ION.surf_avg_data.reset_index(drop=True, inplace=True)

        logger.info('  reading miscellaneous data')
        try:
            self.MISC.vol_avg_data = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.Elements.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
        except:
            self.MISC.vol_avg_data = pd.read_csv(
                self.runfolder + 'eirene.transfer',
                skiprows=row_to_skip, nrows=self.geom.Elements.shape[0],
                delim_whitespace=True, header=None, index_col=False,
                error_bad_lines=False, warn_bad_lines=False)
        self.MISC.vol_avg_data.reset_index(drop=True, inplace=True)

        logger.debug(" stratum data is not read YET!")

###################################
        logger.info(' reading EIRENE ChemFluxDep \n')

        exists = os.path.isfile(self.runfolder + 'eirene.chemFluxDep')

        if exists:

            f = open(self.runfolder + 'eirene.chemFluxDep', 'rb')
            lines = f.readlines()
            text='*  NLIM'
            text_version = '* Neutral flux file version:'
            # if
            row_to_skip =0
            for index, line in enumerate(lines):
                if text_version in str(line):
                    dummy = lines[index].split()
                    version= float(dummy[-1])
                    break
            if version < self.chemFluxDepFileVersion_withSAREA:
                logger.warning(
                    'Need at least eirene.chemFluxDep file version {} to allow surface plotting of EIRENE data'.format(
                        self.chemFluxDepFileVersion_withSAREA))
                return
            else:
                for index, line in enumerate(lines):

                        if text in str(line):
                            index = index + 1
                            dummy = lines[index].split()
                            self.NLIM_tmp = int(dummy[0])
                            self.NSTS_tmp = int(dummy[1])
                            self.NGITT = int(dummy[2])
                            self.NGSTAL = int(dummy[3])
                            # self.NATM = int(dummy[4])
                            # self.NMOL = int(dummy[5])
                            self.NLMPGS  = int(dummy[6])
                            self.NTRII = int(dummy[7])


                            if self.nlim != self.NLIM_tmp:
                                logger.error('NLIM from eirene.chemFluxDep not equal to eirene.transfer! STOPPING')
                            # return
                            else:
                                row_to_skip = index + 3
                                logger.log(5, row_to_skip)
                                # 5          27        6086
                                logger.info('  reading bulk plasma data')
                                # for i in range(0, self.NLIM_tmp):
                                    # READING DATA AS A BLOCK
                                dummy1 = pd.read_csv(self.runfolder + 'eirene.chemFluxDep',
                                                         skiprows=row_to_skip,
                                                         nrows=self.NLMPGS,
                                                         delim_whitespace=True, header=None,
                                                         index_col=False, error_bad_lines=False,
                                                         warn_bad_lines=False)

                                    # readf,1,idum1,rdum1,rdum2,idum2,idum3,idum4
                                self.ESRF_SAREA_atom = np.asarray(dummy1[dummy1.columns[2]])
                                self.ESRF_ITRIA_atom = np.asarray(dummy1[dummy1.columns[3]])
                                self.ESRF_ISIDE_atom = np.asarray(dummy1[dummy1.columns[4]])
                                self.ESRF_ISURF_atom = np.asarray(dummy1[dummy1.columns[5]])

                                row_to_skip = row_to_skip + self.NLMPGS +2

                                dummy1 = pd.read_csv(
                                    self.runfolder + 'eirene.chemFluxDep',
                                    skiprows=row_to_skip,
                                    nrows=self.NLMPGS,
                                    delim_whitespace=True, header=None,
                                    index_col=False, error_bad_lines=False,
                                    warn_bad_lines=False)

                                # readf,1,idum1,rdum1,rdum2,idum2,idum3,idum4
                                self.ESRF_SAREA_mol = np.asarray(
                                    dummy1[dummy1.columns[2]])
                                self.ESRF_ITRIA_mol = np.asarray(
                                    dummy1[dummy1.columns[3]])
                                self.ESRF_ISIDE_mol = np.asarray(
                                    dummy1[dummy1.columns[4]])
                                self.ESRF_ISURF_mol = np.asarray(
                                    dummy1[dummy1.columns[5]])




        else:
            logger.warning('eirene.ChemFluxDep file was NOT found')
###################################
        logger.info(' reading EIRENE surfaces \n')

        exists = os.path.isfile(self.runfolder + 'eirene.surfaces')

        if exists:
            data = read_surfaces_file(self.runfolder + 'eirene.surfaces')

            self.ESRF_TYPES = np.asarray(data[data.columns[1]])
            self.ESRF_NAMES = np.asarray(data[data.columns[3]])

        else:
            logger.warning('eirene.surfaces file was NOT found')



###################################
        logger.info(' reading EIRENE geometrical info \n')
        # self.sh = ep.data(self.runfolder + 'tran', ' SH ').data
        # # self.sh = np.trim_zeros(sh, 'b')
        # self.hrho = ep.data(self.runfolder + 'tran', ' HRHO ' ).data
        # # self.hrho = np.trim_zeros(hrho, 'b')
        # self.rmesh = ep.data(self.runfolder + 'tran', ' RMESH ').data
        # self.rmesh = np.trim_zeros(ls
        # , 'b')

        self.sh,self.sh_title = load_eiri_signal(self.npo, self.runfolder+'e2deir.dat', ' SH ')
        self.hrho,self.hrho_title = load_eiri_signal(self.npo, self.runfolder+'e2deir.dat', ' HRHO ')
        self.rmesh,self.rmesh_title = load_eiri_signal(self.npo, self.runfolder+'e2deir.dat', ' RMESH ')

        self.EIR_TRI_SH = transform_eiri_data(self.sh,self.geom)
        self.EIR_TRI_HRHO = transform_eiri_data(self.hrho,self.geom)
        self.EIR_TRI_RMESH = transform_eiri_data(self.rmesh,self.geom)


            ###################################

        logger.info( 'reading eirene data done! \n')




    def get_surface_name(self,iselect,atmmol=None):
        if iselect >9:
            logger.error('Surface number must be <9')
            return

        if atmmol =='atm':
            self.ESRF_SAREA = self.ESRF_SAREA_atom
            self.ESRF_ITRIA = self.ESRF_ITRIA_atom
            self.ESRF_ISIDE = self.ESRF_ISIDE_atom
            self.ESRF_ISURF = self.ESRF_ISURF_atom
        elif atmmol =='mol':
            self.ESRF_SAREA = self.ESRF_SAREA_mol
            self.ESRF_ITRIA = self.ESRF_ITRIA_mol
            self.ESRF_ISIDE = self.ESRF_ISIDE_mol
            self.ESRF_ISURF = self.ESRF_ISURF_mol
        else:
            self.ESRF_SAREA = self.ESRF_SAREA_mol
            self.ESRF_ITRIA = self.ESRF_ITRIA_mol
            self.ESRF_ISIDE = self.ESRF_ISIDE_mol
            self.ESRF_ISURF = self.ESRF_ISURF_mol


        isrf = self.nlim + iselect
        surface_number = isrf + 1

        surface_name = self.ESRF_NAMES[isrf]

        logger.info(
                   "surface {}, EIRENE surface number= {} - index = {}".format(
                       surface_name, surface_number,iselect))

        return isrf,surface_name,surface_number


    def create_connected_eirene_surface(self, iselect,atmmol=None):

        isrf, surface_name, surface_number = self.get_surface_name(iselect,atmmol)
        logger.log(5,
                   "creating connected polygon groups for surface {}, EIRENE surface number= {}".format(
                       surface_name, surface_number))
        # poly = lonarr(NLMPGS,2)
        poly = np.zeros((2,self.NLMPGS),dtype=int)
        poly_sfidx = np.zeros(self.NLMPGS,dtype=int)
        npoly = 0
        x = []
        y = []
        for i in range(0, self.NLMPGS):
            if self.ESRF_ISURF[i] == isrf+1:
                itria = self.ESRF_ITRIA[i] - 1
                iside = self.ESRF_ISIDE[i] - 1
                ip1 = iside
                ip2 = ip1 + 1
                if ip2 > 2:
                    ip2=ip2-3
                poly[0,npoly] = self.geom.Elements[itria, ip1]
                poly[1,npoly] = self.geom.Elements[itria, ip2]

                # x.append(self.geom.Elements[itria, ip1])
                # y.append(self.geom.Elements[itria, ip2])

                poly_sfidx[npoly] = i
                npoly = npoly+1

        # poly=np.stack([x,y])
        npoly_size = poly.shape[1]

        logger.log(5, "Found {} polygons for this surface".format(npoly))
        #
        # # Check connectivity
        poly_added = np.zeros(npoly,dtype=bool)

        poly_idx = np.zeros(npoly,dtype=int)

        #
        npoly_group = 0
        poly_group = np.zeros((2, npoly), dtype=int)
        # poly_group_x = np.zeros(npoly,dtype=int)
        # poly_group_y = np.zeros(npoly,dtype=int)
        #
        tip = 0
        tail = 0

        poly_idx[tail] =0
        poly_added[0]=True
        #
        piece_left = True  # true
        piece_added = False  # false
        #
        # self.plot_eirene_grid()
        # plt.plot(poly[0],poly[1],'b')
        # plt.show()


        while piece_left:
            # logger.log(5,"Current tip: {} {} {} {}".format(tip,poly_idx[tip], poly[0][poly_idx[tip]], poly[1][poly_idx[tip]]))
            # logger.log(5,"Current tail: {} {} {} {}".format(tail,poly_idx[tail], poly[0][poly_idx[tail]], poly[1][poly_idx[tail]]))

            piece_added = False  # false
            for i in range(0, npoly):
                logger.log(5," i= {}".format(i))
                logger.log(5," poly_added[i]= {}".format(poly_added[i]))
                if not poly_added[i]:
                    # ;          found poly piece which is not yet added
                    logger.log(5,"Checking poly {} {} {} {}: ".format(i,poly[0][i],poly[1][i],tail))
                    if (poly[1][poly_idx[tail]] == poly[0][i]):
        #

                        # poly_idx = np.append(poly_idx, 1)
                        tail = tail + 1
                        poly_idx[tail] = i

                        poly_added[i]=True  # mark poly piece to be already added

                        piece_added = True  # remember that a piece was added
                    elif poly[1][poly_idx[tail]] == poly[1][i]:
        # #             switch order of points in poly
                        idummy = poly[0][i]
                        # print(idummy)
                        poly[0][i] = poly[1][i]
                        poly[1][i] = idummy

        # #             add poly piece to tail
                        tail = tail + 1
                        poly_idx[tail] = i

                        poly_added[i] = True  # mark poly piece to be already added

                        piece_added = True  # remember that a piece was added
                    elif poly[0][poly_idx[tip]] == poly[1][i]:
        # #             shift polygon upwards
                        e1 = poly_idx[-1]
                        # for ii, e2 in enumerate(poly_idx):
                        #     poly_idx[ii], e1 = e1, e2
                        for j in range(tail, tip-1,-1):
                            poly_idx[j + 1] = poly_idx[j]

        # #             add poly piece to tip
                        tail = tail + 1

                        poly_idx[tip] = i

                        poly_added[i] = True   # mark poly piece to be already added
                        piece_added = True  # remember that a piece was added
                    elif poly[0][poly_idx[tip]] == poly[0][i]:
        # #             switch order of points in poly
                        idummy = poly[0][i]
                        poly[0][i] = poly[1][i]
                        poly[1][i] = idummy
                    #             shift polygon upwards

                        e1 = poly_idx[-1]
                        # for ii, e2 in enumerate(poly_idx):
                        #     poly_idx[ii], e1 = e1, e2
                        for j in range(tail, tip-1,-1):
                            poly_idx[j + 1] = poly_idx[j]

            # #             add poly piece to tip
                        tail = tail + 1

                        poly_idx[tip] = i
                        poly_added[i] = True   # mark poly piece to be already added
                        piece_added = True  # remember that a piece was added

                # logger.log(5,"i {}".format(i))
                # logger.log(5,"tail {} \n".format(tail))
                # logger.log(5,"poly_idx {} \n".format(poly_idx))

            if not piece_added:
        # #       No piece was added so the poly group is finished
        # #       add new poly group
                poly_group[0,npoly_group] = tip
                poly_group[1,npoly_group] = tail
                npoly_group = npoly_group + 1
                logger.log(5,"Polygon indices in group {}".format(npoly_group))

            # #       get next group start piece
                piece_left = False  # false
                for j in range(0,npoly):
                    # logger.log(5, " j= {}".format(j))
                    if not poly_added[j]:
                        piece_left = True
                        tip = tail + 1
                        tail = tail + 1
                        poly_idx[tail] = j

                        poly_added[j] = True   # mark poly piece to be already added
                        break
            # print('end while')
        # poly_group = np.stack([poly_group_x, poly_group_y])
        self.surface_npoly_group = npoly_group
        # surface_poly_group = lonarr(npoly_group, 2)
        self.surface_poly_group = [poly_group[0][0:npoly_group],poly_group[1][0:npoly_group]]
        self.surface_npoly = npoly
        # surface_poly = lonarr(npoly, 2)
        self.surface_poly = [poly[0][0:npoly],poly[1][0:npoly]]
        # surface_poly_idx = lonarr(npoly)
        self.surface_poly_idx = poly_idx[0:npoly]
        # surface_poly_sfidx = lonarr(npoly)
        self.surface_poly_sfidx = poly_sfidx[0:npoly]

        logger.log(5, "Found {} polygon groups in this surface".format(self.surface_npoly_group))
        for i in range(0,self.surface_npoly_group):
            n = self.surface_poly_group[1][i] - self.surface_poly_group[0][i] + 1
            logger.log(5,"Group {} has {} polygons".format(i+1,n))
            # for j in range(self.surface_poly_group[0][i] ,  self.surface_poly_group[1][i] ):
            #     logger.log(5,"{} {} {} {}".format( j, self.surface_poly_idx[j], poly[0][poly_idx[j]], poly[1][poly_idx[j]]))

        logger.log(5,'surface_npoly_group {}'.format(self.surface_npoly_group))
        logger.log(5,'surface_poly_group {}'.format(self.surface_poly_group))
        logger.log(5,'surface_npoly {}'.format(self.surface_npoly))
        logger.log(5,'surface_poly {}'.format(self.surface_poly))
        logger.log(5,'surface_poly_idx {}'.format(self.surface_poly_idx))
        logger.log(5,'surface_poly_sfidx {}'.format(self.surface_poly_sfidx))





    def assemble_eirene_surfaces(self,group,iselect):

        isrf = self.nlim + iselect
        surface_number = isrf + 1

        logger.info("assembling surface group {} for surface '{}'".format((group+1),self.ESRF_NAMES[isrf]))

        npolygon = self.surface_poly_group[1][group] - self.surface_poly_group[0][group] + 1
        logger.log(5, "Surface group has {} polygons".format(npolygon))

        self.surface_polygon_sfidx = np.zeros(npolygon,dtype=int)
        surface_polygon_x1 = []
        surface_polygon_y1 = []
        surface_polygon_x2 = []
        surface_polygon_y2 = []
        for i in range(0,npolygon):
            idx = self.surface_poly_group[0][group]+i
            surface_polygon_x1.append(self.geom.xv[self.surface_poly[0][self.surface_poly_idx[idx]]])
            surface_polygon_y1.append(self.geom.yv[self.surface_poly[0][self.surface_poly_idx[idx]]])
            surface_polygon_x2.append(self.geom.xv[self.surface_poly[1][self.surface_poly_idx[idx]]])
            surface_polygon_y2.append(self.geom.yv[self.surface_poly[1][self.surface_poly_idx[idx]]])

            self.surface_polygon_sfidx[i]=int(self.surface_poly_sfidx[self.surface_poly_idx[idx]])

        self.surface_polygon= np.stack([surface_polygon_x1,surface_polygon_y1,surface_polygon_x2,surface_polygon_y2])

        logger.log(5, "surface_polygon {}".format(self.surface_polygon))
        logger.log(5, "surface_polygon_sfidx {}".format(self.surface_polygon_sfidx))


    def create_surface_start_end_poly(self):
# Get max min coordinates of all surfaces
        Rmax = -1e30
        Rmin = +1e30
        Zmax = -1e30
        Zmin = +1e30
        for i in range(0, self.NLMPGS):
            if self.ESRF_ISURF[i] > 0:
                itria = self.ESRF_ITRIA[i] - 1
                iside = self.ESRF_ISIDE[i] - 1
                ip1 = iside
                ip2 = ip1 + 1
                if ip2 > 2:
                    ip2=ip2-3
                if itria > 0:
                    Rmax = max([Rmax, self.geom.xv[self.geom.Elements[itria, ip1]]])
                    Rmin = min([Rmin, self.geom.xv[self.geom.Elements[itria, ip1]]])
                    Zmax = max([Zmax, self.geom.yv[self.geom.Elements[itria, ip1]]])
                    Zmin = min([Zmin, self.geom.yv[self.geom.Elements[itria, ip1]]])


        sizeR = Rmin - Rmax
        sizeZ = Zmin - Zmax

        marker_size = np.sqrt(sizeR ** 2 + sizeZ ** 2) * 0.01

        # ; start marker


        self.surface_polygon_start = np.zeros(([2,4]))
        dRpoly = self.surface_polygon[2][0] - self.surface_polygon[0][0]
        dZpoly = self.surface_polygon[3][0] - self.surface_polygon[1][0]
        leng = np.sqrt(dRpoly ** 2 + dZpoly ** 2)
        dRpoly = dRpoly / leng
        dZpoly = dZpoly / leng
        dRperp = -dZpoly
        dZperp = dRpoly


        self.surface_polygon_start[0, 0] = self.surface_polygon[0][0]
        self.surface_polygon_start[0, 1] = self.surface_polygon[1][0]
        self.surface_polygon_start[0, 2] = self.surface_polygon[0][0] + marker_size * dRperp
        self.surface_polygon_start[0, 3] = self.surface_polygon[1][0] + marker_size * dZperp
        self.surface_polygon_start[1, 0] = self.surface_polygon[0][0] + 0.5 * marker_size * dRperp
        self.surface_polygon_start[1, 1] = self.surface_polygon[1][0] + 0.5 * marker_size * dZperp
        self.surface_polygon_start[1, 2] = self.surface_polygon[0][0] + 0.5 * marker_size * dRperp + marker_size * dRpoly
        self.surface_polygon_start[1, 3] = self.surface_polygon[1][0] + 0.5 * marker_size * dZperp + marker_size * dZpoly

        # ; end  marker
        self.surface_polygon_end = np.zeros(([2,4]))
        # a = size(self.surface_polygon)
        idx = self.surface_polygon.shape[1] - 1
        dRpoly = self.surface_polygon[2][idx] - self.surface_polygon[0][idx]
        dZpoly = self.surface_polygon[3][idx]  - self.surface_polygon[1][idx]
        leng = np.sqrt(dRpoly ** 2 + dZpoly ** 2)
        dRpoly = dRpoly / leng
        dZpoly = dZpoly / leng
        dRperp = dZpoly
        dZperp = -dRpoly

        self.surface_polygon_end[0, 0] = self.surface_polygon[2][idx]
        self.surface_polygon_end[0, 1] = self.surface_polygon[3][idx]
        self.surface_polygon_end[0, 2] = self.surface_polygon[2][idx] + marker_size * dRperp
        self.surface_polygon_end[0, 3] = self.surface_polygon[3][idx] + marker_size * dZperp
        self.surface_polygon_end[1, 0] = self.surface_polygon[2][idx] + 0.5 * marker_size * dRperp
        self.surface_polygon_end[1, 1] = self.surface_polygon[3][idx] + 0.5 * marker_size * dZperp
        self.surface_polygon_end[1, 2] = self.surface_polygon[2][idx] + 0.5 * marker_size * dRperp - marker_size * dRpoly
        self.surface_polygon_end[1, 3] = self.surface_polygon[3][idx] + 0.5 * marker_size * dZperp - marker_size * dZpoly


    def get_eirene_surface_data(self,data=None,species=None,var=None):
        if species is None:
            species = 0
        else:
            species = species

        if var is None:
            var = 0
        else:
            var = var
        # number of triangles in the mesh, i.e. number of data points
        triangnum = self.NLMPGS
        if data is None:
            # accessing data inside the block matrix
            data = self.MOL.surf_avg_data[
                   triangnum * (species):(species + 1) * triangnum]
            data = data[data.columns[1]]
            label = self.MOL.names[species] + ' - ' + self.MOL.SurfunitName[var]
            title = self.MOL.SurfdataName[var]
        elif data.lower() == 'pls':
            data = self.PLS.surf_avg_data[
                   triangnum * (species):(species + 1) * triangnum]
            data = data[data.columns[1]]
            label = self.PLS.names[species] + ' - ' + self.PLS.SurfunitName[var]
            title = self.PLS.SurfdataName[var]
            logger.info('loading surface BULK IONS data')
            logger.info('loading {} data - {}'.format(self.PLS.names[species],title))
        elif data.lower() == "mol":
            data = self.MOL.surf_avg_data[
                   triangnum * (species):(species + 1) * triangnum]
            data = data[data.columns[1]]
            label = self.MOL.names[species] + ' - ' + self.MOL.SurfunitName[var]
            title = self.MOL.SurfdataName[var]
            logger.info('loading surface MOLECULES data')
            logger.info('loading {} data - {}'.format(self.MOL.names[species],title))
        elif data.lower() == "atm":
            data = self.ATM.surf_avg_data[
                   triangnum * (species):(species + 1) * triangnum]
            data = data[data.columns[1]]
            label = self.ATM.names[species] + ' - ' + self.ATM.SurfunitName[var]
            title = self.ATM.SurfdataName[var]
            logger.info('loading surface ATOM data ')
            logger.info('loading {} data - {}'.format(self.ATM.names[species],title))
        elif isinstance(data, np.ndarray):
            data = data[triangnum * (species):(species + 1) * triangnum]
            label = label
        # elif isinstance(data,pd.Series):
        #     var = data[triangnum*(species):(species+1)*triangnum-1]
        #     label = label
        elif isinstance(data, pd.DataFrame):
            # if input data is the whole dataframe use species and var to determine which block of the matrix to use for plotting

            data = data[triangnum * (species):(species + 1) * triangnum]
            data = data[data.columns[var + 1]]
            label = label
        else:
            logger.error('choose between MOL/ATM \n')
            return


        surface_ndata = self.surface_polygon.shape[1]


        surface_data_x = np.zeros(surface_ndata)
        surface_data_y = np.zeros(surface_ndata)
        surface_data_dx = np.zeros(surface_ndata)
        surface_data_p = np.zeros((surface_ndata, 2))
        surface_data_area = np.zeros(surface_ndata)
        surface_data_itria = np.zeros(surface_ndata,dtype=int)
        surface_data_iside = np.zeros(surface_ndata,dtype=int)
        #
        for i in range(0, surface_ndata):
            surface_data_dx[i] = np.sqrt(
                (self.surface_polygon[2][i] - self.surface_polygon[0][i]) ** 2 +
            ((self.surface_polygon[3][i] - self.surface_polygon[1][i]) ** 2) )
            surface_data_p[i][0] = 0.5 * (
                    self.surface_polygon[0][i] + self.surface_polygon[2][i])
            surface_data_p[i][1] = 0.5 * (
                    self.surface_polygon[1][i] + self.surface_polygon[3][i])
            surface_data_y[i] = data[self.surface_polygon_sfidx[i]]
            surface_data_area[i] = self.ESRF_SAREA[self.surface_polygon_sfidx[i]]
            surface_data_itria[i] = self.ESRF_ITRIA[self.surface_polygon_sfidx[i]]
            surface_data_iside[i] = self.ESRF_ISIDE[self.surface_polygon_sfidx[i]]

        #
        #
        # # ; create surface   with segment edges acording to EDGE2D grid
        surface_polygon_e2d = np.zeros((4,surface_ndata))
        surface_polygon_e2d[0][0] = self.surface_polygon[0][0]
        surface_polygon_e2d[1][0] = self.surface_polygon[1][0]
        surface_polygon_e2d[2][surface_ndata - 1] = self.surface_polygon[2][
            surface_ndata - 1]
        surface_polygon_e2d[3][surface_ndata - 1] = self.surface_polygon[3][
            surface_ndata - 1]
        for i in range(0, surface_ndata-1):
            px = 0.5 * (surface_data_p[i][0] + surface_data_p[i+1][0])
            py = 0.5 * (surface_data_p[i][1] + surface_data_p[i+1][1])
            surface_polygon_e2d[2][i] = px
            surface_polygon_e2d[3][i] = py
            surface_polygon_e2d[0][i + 1] = px
            surface_polygon_e2d[1][i + 1] = py

        surface_data_e2d_p = np.zeros((surface_ndata, 2))
        surface_data_e2d_dx = np.zeros(surface_ndata)
        surface_data_e2d_area = np.zeros(surface_ndata)
        for i in range(0, surface_ndata):
            surface_data_e2d_dx[i] = np.sqrt(
                (surface_polygon_e2d[2][i] - surface_polygon_e2d[0][i]) ** 2 +
            ((surface_polygon_e2d[3][i] - surface_polygon_e2d[1][i]) ** 2) )
            surface_data_e2d_p[0] = 0.5 * (
                        surface_polygon_e2d[0][i] + surface_polygon_e2d[2][i])
            surface_data_e2d_p[i][1] = 0.5 * (
                        surface_polygon_e2d[1][i] + surface_polygon_e2d[3][i])
            # ;     surface_data_e2d_area[i] = 1.0e4 * 2.0 *!PI * surface_data_e2d_p[i, 0] *
            #                                                surface_data_e2d_dx[i]$
            # ; / EIR_TRI_SH[surface_data_itria[i]]
            surface_data_e2d_area[i] = 1.0e4 * 2.0 *np.pi * self.EIR_TRI_RMESH[surface_data_itria[i]]*self.EIR_TRI_HRHO[surface_data_itria[i]]*self.EIR_TRI_SH[surface_data_itria[i]]


        surface_data_x[0] = 0.
        for i in range (1, surface_ndata):
            surface_data_x[i] = surface_data_x[i - 1] + 0.5* surface_data_dx[i - 1] + 0.5* surface_data_dx[i]

        self.surface_data_e2d_area = surface_data_e2d_area
        self.surface_data_area = surface_data_area

        self.surface_data_x = surface_data_x
        self.surface_data_y = surface_data_y
        self.surface_flux_data_e2d_y = surface_data_y / surface_data_e2d_area
        self.surface_flux_data_y = surface_data_y / surface_data_area



    def get_data_names(self,data=None):
        if data.lower()=='pls':
            logger.info('BULK IONS list {} \n'.format(self.PLS.names))
        if data.lower()=='mol':
            logger.info('MOLECULES list {} \n'.format(self.MOL.names))
        if data.lower()=='atm':
            logger.info('ATOMS list {} \n'.format(self.ATM.names))
        if data.lower()=='ion':
            logger.info('IONS list {} \n'.format(self.ION.names))
        # print(simu.data.eirene.PLS.names)
        # # Out[12]: {0: 'D+', 1: 'Be1+', 2: 'Be2+', 3: 'Be3+', 4: 'Be4+'}
        # print(simu.data.eirene.MOL.names)
        # # Out[13]: {0: 'D2'}
        # print(simu.data.eirene.ATM.names)
        # # Out[14]: {0: 'D', 1: 'Be'}
        # print(simu.data.eirene.ION.names)
        # # Out[15]: {0: 'D2+'}

    def plot_eirere_surf_data(self,data = None, species = None, var = None):
        if species is None:
            species = 0
        else:
            species = species

        if var is None:
            var = 0
        else:
            var = var
        # number of triangles in the mesh, i.e. number of data points
        triangnum = self.NLMPGS
        if data is None:
            # accessing data inside the block matrix
            label = self.MOL.names[species] + ' - ' + self.MOL.SurfunitName[var]
            title = self.MOL.SurfdataName[var]
            logger.info(
                'plotting {} data - {}'.format(self.MOL.names[species], title))
        elif data.lower() == 'pls':
            label = self.PLS.names[species] + ' - ' + self.PLS.SurfunitName[var]
            title = self.PLS.SurfdataName[var]
            logger.info(
                'plotting {} data - {}'.format(self.PLS.names[species], title))
        elif data.lower() == "mol":
            label = self.MOL.names[species] + ' - ' + self.MOL.SurfunitName[var]
            title = self.MOL.SurfdataName[var]
            logger.info(
                'plotting {} data - {}'.format(self.MOL.names[species], title))
        elif data.lower() == "atm":
            label = self.ATM.names[species] + ' - ' + self.ATM.SurfunitName[var]
            title = self.ATM.SurfdataName[var]
            logger.info(
                'plotting {} data - {}'.format(self.ATM.names[species], title))
        # elif isinstance(data, np.ndarray):
        #     data = data[triangnum * (species):(species + 1) * triangnum]
        #     label = label
        # elif isinstance(data,pd.Series):
        #     var = data[triangnum*(species):(species+1)*triangnum-1]
        #     label = label
        # elif isinstance(data, pd.DataFrame):
        # # if input data is the whole dataframe use species and var to determine which block of the matrix to use for plotting
        #
        # data = data[triangnum * (species):(species + 1) * triangnum]
        # data = data[data.columns[var + 1]]
        # label = label
        else:
            logger.error('choose between PLS/MOL/ATM \n')

        figtitle = label.split()[0] + label.split()[1] + title
        plt.figure(figtitle)
        logger.info('plotting {}'.format(figtitle))
        plt.plot(self.surface_data_x,self.surface_data_y)
        xlabel('Distance along the surface [m]')
        ylabel(label.split()[-1])
        plt.title(figtitle)

        figtitle = label.split()[0] + label.split()[1] + title
        plt.figure('flux density ' + figtitle + ' based on eirene')
        logger.info('flux density selected {} (based on eirene triangle segments)'.format(figtitle))
        plt.plot(self.surface_data_x,self.surface_flux_data_y)
        xlabel('Distance along the surface [m]')
        ylabel(label.split()[-1] + '/cm^2')

        plt.title(figtitle)

        figtitle = label.split()[0] + label.split()[1] + title
        plt.figure('flux density ' + figtitle + ' based on  reconstructed edge2d')
        logger.info('flux density selected {} (based on reconstructed edge2d grid segments)'.format(figtitle))
        plt.plot(self.surface_data_x,self.surface_flux_data_e2d_y)
        xlabel('Distance along the surface [m]')
        ylabel(label.split()[-1] + '/cm^2')
        plt.title(figtitle)

        plt.show()


    def plot_eirene_surface(self):
        GM = (math.sqrt(5) - 1) / 2
        W = 8
        H = GM * W
        SIZE = (W, H)

        from shapely.geometry.polygon import LinearRing
        logging.disable(logging.CRITICAL)
        ring1 = LinearRing(
            [(self.surface_polygon_start[0][0],
              self.surface_polygon_start[0][1]),
             (self.surface_polygon_start[0][2],
              self.surface_polygon_start[0][3]),
             (self.surface_polygon_start[1][0],
              self.surface_polygon_start[1][1]),
             (self.surface_polygon_start[1][2],
              self.surface_polygon_start[1][3])])
        ring2 = LinearRing(
            [(self.surface_polygon_end[0][0],
              self.surface_polygon_end[0][1]),
             (self.surface_polygon_end[0][2],
              self.surface_polygon_end[0][3]),
             (self.surface_polygon_end[1][0],
              self.surface_polygon_end[1][1]),
             (self.surface_polygon_end[1][2],
              self.surface_polygon_end[1][3])])
        x, y = ring1.xy
        plt.plot(x, y, 'o', color=self.YELLOW, zorder=1, alpha=1)
        x, y = ring2.xy
        plt.plot(x, y, 'o', color=self.GREEN, zorder=1, alpha=1)

        plt.plot(self.surface_polygon[0],
                 self.surface_polygon[1], 'rx-')
        # plt.plot(self.surface_polygon[1], self.surface_polygon[3], 'bo') #axial symmetric surface
        plt.plot(self.r_ves, self.z_ves, 'x',
                 color=self.BLACK, zorder=1, alpha=1)

        logging.disable(logging.NOTSET)

    def plot_eirene_vol_data(self,data=None,species=None,var=None, lowerbound=None,upperbound=None,label=None):
        """
        function that allow contour plots of EIRENE data
        :param data input data (dataframe, string or empty)
        as data is stored by read_eirene as a dataframe species and var determine for which species user want the data (row index) and which variable (column index)
        :param species: simu.data.eirene.PLS.names
        {0: 'D+', 1: 'Be1+', 2: 'Be2+', 3: 'Be3+', 4: 'Be4+'}
        :param var:
        column number indentifying variables
        :param label: simu.data.eirene.ATM.names[species] + \
            simu.data.eirene.ATM.VoldataName[species]
        :param lowerbound minimum value to be used to normalise data
        :param upperbound minimum value to be used to normalise data


        :return: contour plot of data
        usage

            # I want Be1+
            species =1
            data = simu.data.eirene.PLS.vol_avg_data
            label = simu.data.eirene.PLS.names[species-1] + simu.data.eirene.PLS.VoldataName[26]

            # I want D
            species = 0
            species_name = simu.data.eirene.ATM.names[species]
            data = simu.data.eirene.ATM.vol_avg_data
            label = simu.data.eirene.ATM.names[species] + \
            simu.data.eirene.ATM.VoldataName[species]

            simu.data.eirene.plot_eirene(data=data,species=species,label=label)

        """
        if species is None:
            species =0
        else:
            species=species

        if var is None:
            var =0
        else:
            var=var
#number of triangles in the mesh, i.e. number of data points
        triangnum = self.geom.Elements.shape[0]
        if data is None:
            #accessing data inside the block matrix
            data = self.MOL.vol_avg_data[triangnum*(species):(species+1)*triangnum]
            data = data[data.columns[1]]
            label = self.MOL.names[species] +' - '+ self.MOL.VolunitName[var]
        elif data == "PLS":
            data = self.PLS.vol_avg_data[triangnum*(species):(species+1)*triangnum]
            data = data[data.columns[1]]
            label = self.PLS.names[species] +' - '+ self.PLS.VolunitName[var]
        elif data == "MOL":
            data = self.MOL.vol_avg_data[triangnum*(species):(species+1)*triangnum]
            data = data[data.columns[1]]
            label = self.MOL.names[species] +' - '+ self.MOL.VolunitName[var]
        elif data == "ATM":
            data = self.ATM.vol_avg_data[triangnum*(species):(species+1)*triangnum]
            data = data[data.columns[1]]
            label = self.ATM.names[species] +' - '+ self.ATM.VolunitName[var]
        elif isinstance(data,np.ndarray):
            data = data[triangnum*(species):(species+1)*triangnum]
            label = label
        # elif isinstance(data,pd.Series):
        #     var = data[triangnum*(species):(species+1)*triangnum-1]
        #     label = label
        elif isinstance(data,pd.DataFrame):
            #if input data is the whole dataframe use species and var to determine which block of the matrix to use for plotting

            data = data[triangnum*(species):(species+1)*triangnum]
            data=data[data.columns[var+1]]
            label = label
        else:
            logger.error('choose between MOL/ATM \n')
            return

        logger.log(5,'plotting {} data volume avg data \n'.format(label))
        # plt.figure()
        # x = [self.geom.xv[i] for i in self.geom.Elements]
        # y = [self.geom.yv[i] for i in self.geom.Elements]
        #
        # plt.tricontourf(x,y,self.MOL.vol_avg_data)
        # plt.show()


        #getting coordinates of the triangles and creating arrays that describe polygons
        logger.log(5,"collecting coordinates of triangles \n")
        x = [self.geom.xv[i] for i in
             self.geom.Elements]
        y = [self.geom.yv[i] for i in
             self.geom.Elements]

        # matplotlib.pyplot.tricontourf(x, y, sim_hfe_Nrad0.vol_avg_data.eirene.MOL.vol_avg_data)

        # plt.tricontourf(sim_hfe_Nrad0.vol_avg_data.eirene.geom.xv,sim_hfe_Nrad0.vol_avg_data.eirene.geom.yv,sim_hfe_Nrad0.vol_avg_data.eirene.geom.Elements,sim_hfe_Nrad0.vol_avg_data.eirene.MOL.vol_avg_data[1])


        if lowerbound is None:
            lower = min(data)
        else:
          lower=lowerbound
        if upperbound is None:
            upper = max(data)
        else:
          upper=upperbound
        x1 = []
        x2 = []
        x3 = []
        for i, value in enumerate(x):
            x1.append(x[i][0])
            x2.append(x[i][1])
            x3.append(x[i][2])
        y1 = []
        y2 = []
        y3 = []
        for i, value in enumerate(y):
            y1.append(y[i][0])
            y2.append(y[i][1])
            y3.append(y[i][2])


        #now starting to create the polygon using triangles coordinates
        logger.log(5, "now starting to create the polygon using triangles coordinates \n")
        patches = []
        for i in list(range(0, len(x1))):
            # print(i)
            polygon = Polygon([[x1[i], y1[i]], [x2[i], y2[i]], [x3[i], y3[i]]],
                              edgecolor='none', alpha=0.1, linewidth=0,
                              closed=True)
            patches.append(polygon)

        #normalisation of the variable
        logger.log(5, " normalisation of the variable \n ")
        norm = mpl.colors.Normalize(vmin=lower, vmax=upper)
        collection = PatchCollection(patches, match_original=True)
        collection.set(array=data, cmap='jet', norm=norm)

        #plotting patches
        logger.log(5, " plotting patches \n ")
        fig, ax = plt.subplots()
        ax.add_collection(collection)

        ax.autoscale_view()

        #setting up colorbar and normalising it accordint to variable to plot
        sfmt = ScalarFormatter(useMathText=True)
        sfmt.set_powerlimits((0, 0))
        sm = plt.cm.ScalarMappable(cmap="jet",
                                   norm=plt.Normalize(vmin=lower, vmax=upper))
        sm.set_array([])
        plt.xlabel('R [m]')
        plt.ylabel('Z [m]')

        cbar = plt.colorbar(sm, format=sfmt)
        cbar.set_label(label)
        logger.log(5,'done \n')
        # plt.show(block=True)

    def plot_subdivertor(self,path,subdivertor_file):
        """
        function that reads and plots subdivertor structure
        :param path: location of tranfile
        :param subdivertor_file: location of subdivertor structure file
        :return:
        """
        logger.info(' plotting subdivertor structure \n')
        #reading edge2d mesh
        rvert = ep.data(path, 'RVERTP').data
        rvert = np.trim_zeros(rvert, 'b')
        zvert = ep.data(path, 'ZVERTP').data
        zvert = -np.trim_zeros(zvert, 'b')


        #from line 465 to line 493
        #finding vertices of polygons

        rvert_size = len(rvert) + 5
        dummy = list(range(1, int(rvert_size / 5)))
        dummy1 = list(map(lambda x: 5 * x, dummy))
        dummy2 = list(map(lambda x: x - 1, dummy1))
        rvert_cent = rvert[dummy2[:]]
        zvert_cent = zvert[dummy2[:]]

        leng = len(rvert)
        dummy = list(range(0, int(leng / 5)))

        dummy1 = list(map(lambda x: 5 * x + 1, dummy))
        dummy2 = list(map(lambda x: 5 * x + 2, dummy))
        dummy3 = list(map(lambda x: 5 * x + 3, dummy))
        dummy4 = list(map(lambda x: 5 * x + 4, dummy))

        dummy1 = list(map(lambda x: x - 1, dummy1))
        dummy2 = list(map(lambda x: x - 1, dummy2))
        dummy3 = list(map(lambda x: x - 1, dummy3))
        dummy4 = list(map(lambda x: x - 1, dummy4))

        A = rvert[dummy1]
        B = rvert[dummy2]
        C = rvert[dummy3]
        D = rvert[dummy4]

        A1 = zvert[dummy1]
        B1 = zvert[dummy2]
        C1 = zvert[dummy3]
        D1 = zvert[dummy4]


        #creating polygon to plot variable
        #variable is defined inside the polygon
        patches = []
        for i in list(range(0, len(A))):
            # print(i)
            polygon = Polygon(
                [[A[i], A1[i]], [B[i], B1[i]], [C[i], C1[i]], [D[i], D1[i]]],
                edgecolor='black', alpha=0.5, linewidth=0.5, closed=True)
            patches.append(polygon)

        collection = PatchCollection(patches, match_original=True)

        fig, ax = plt.subplots()
        ax.add_collection(collection)
        ax.autoscale_view()


        plt.xlabel('R [m]')
        plt.ylabel('Z [m]')

        rpoint = []
        zpoint = []
        color = ['red', 'white', 'green', 'blue']
        rvertex = []
        zvertex = []

        logger.log(5,"reading subdivertor file and extracting coordinates \n")
        #reading subdivertor file and extracting coordinates
        with open(subdivertor_file) as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                if '# VACUUM VESSEL.' in str(line):

                    index = index + 2
                    dummy = lines[index].split(',')
                    no_vertices = int(dummy[0])
                    surf_type = int(dummy[1])
                    nread = 0
                    index = index + 3

                    while nread < no_vertices:
                        if lines[index].startswith('#'):
                            index = index + 1
                        else:
                            dummy = lines[index].split(',')
                            nread = nread + 1

                            rvertex.append(float(dummy[0]))
                            zvertex.append(float(dummy[1]))
                            index = index + 1

            plt.plot(rvertex, zvertex, 'x-', color=color[surf_type - 1],
                     linewidth=0.5)

            #now it is time to read following regions
            logger.log(5, "reading following regions \n")
            for index, line in enumerate(lines):
                if '# (TOT. NO OF REMAINING STRUCTURES), (MAX. NO. OF VERTICES IN ANY ONE OF THEM)' in str(
                        line):
                    index = index + 1
                    dummy = lines[index].split(',')
                    no_holes = int(dummy[0])
                    index = index + 1

                    nholesread = 0
                    while nholesread < no_holes:
                        rpoint = []
                        zpoint = []
                        if lines[index].startswith('#'):
                            index = index + 1
                        else:
                            dummy = lines[index].split(',')

                            nread = 0
                            npts = int(dummy[0])
                            stype = int(dummy[1])
                            index = index + 1
                            while nread < npts + 1:
                                if lines[index].startswith('#'):
                                    index = index + 1
                                else:
                                    nread = nread + 1
                                    dummy = lines[index].split(',')
                                    rpoint.append(float(dummy[0]))
                                    zpoint.append(float(dummy[1]))
                                    index = index + 1

                            rinternal = rpoint[0]
                            zinternal = zpoint[0]
                            plt.plot(rinternal, zinternal, '*',
                                     color=color[stype - 1])
                            plt.plot(rpoint[1:], zpoint[1:], '.-',
                                     color=color[stype - 1], linewidth=0.5)
                            nholesread = nholesread + 1
                            index = index + 1


            # plt.show()
            plt.axis('equal')
            logger.log(5,"done \n")

    def plot_eirene_grid(self,pufffile=None):
        """
        function to read and plot EIRENE grids
        :param pufffile: if using a catalogued puff file is not saved, so user can provide it
        :return:
        """
        logger.info(' plotting eirene grid \n')

        logger.log(5," reading puff file")
        if pufffile is None:#
            pass
        else:
            self.geom.puff = read_puff_file(self.runfolder + 'puff.dat', alternativefile=pufffile)
        x = [self.geom.xv[i] for i in
             self.geom.Elements]
        y = [self.geom.yv[i] for i in
             self.geom.Elements]

        x1 = []
        x2 = []
        x3 = []
        for i, value in enumerate(x):
            x1.append(x[i][0])
            x2.append(x[i][1])
            x3.append(x[i][2])
        y1 = []
        y2 = []
        y3 = []
        for i, value in enumerate(y):
            y1.append(y[i][0])
            y2.append(y[i][1])
            y3.append(y[i][2])

        patches = []
        for i in list(range(0, len(x1))):

            polygon = Polygon([[x1[i], y1[i]], [x2[i], y2[i]], [x3[i], y3[i]]],
                              edgecolor='black', alpha=0.5, linewidth=0.5,
                              closed=True)
            patches.append(polygon)


        collection = PatchCollection(patches, match_original=True)


        fig, ax = plt.subplots()
        ax.add_collection(collection)

        ax.autoscale_view()

        try:
            for i in range(0,len(self.geom.pump[0]),2):
                plt.plot(self.geom.pump[0][i:i+2],self.geom.pump[1][i:i+2],color='magenta',marker='x')
        except:
            logging.error('this simulation has not a standard pump file')

        npuff = len(self.geom.puff)
        xp=np.zeros(2)
        yp=np.zeros(2)
        for i in range(0,npuff):
            izs = self.geom.puff[i, 0]
            xp[0] = self.geom.puff[i, 5]/100
            yp[0] = self.geom.puff[i, 6]/100
            xp[1] = self.geom.puff[i, 7]/100
            yp[1] = self.geom.puff[i, 8]/100
            # sqrt((xp(1) - xp(2)) ^ 2 + (yp(1) - yp(2)) ^ 2);
            if (izs == 0):

                plt.plot(xp, yp, color='red', marker='o');

            if (izs == 1):

                plt.plot(xp, yp, color='green', marker='o');

            if (izs == 2):

                plt.plot(xp, yp, color='blue', marker='o');


    def get_pressure(self):
        triangnum = self.geom.Elements.shape[0]
        mD2 = 2 * 2.01410178 * 1.660538921E-27;  # kg


        vxD2 = np.asarray(self.MOL.vol_avg_data[2] / 1000 / mD2 /
                          self.MOL.vol_avg_data[1] / 100);  # m/s
        vyD2 = np.asarray(self.MOL.vol_avg_data[3] / 1000 / mD2 /
                          self.MOL.vol_avg_data[1] / 100);  # m/s
        vzD2 = np.asarray(self.MOL.vol_avg_data[4] / 1000 / mD2 /
                          self.MOL.vol_avg_data[1] / 100);  # m/s
        vxD2[np.isnan(vxD2)] = 0;
        vyD2[np.isnan(vyD2)] = 0;
        vzD2[np.isnan(vzD2)] = 0;

        # static pressure
        pD2 = np.asarray(
            2 / 3 * (self.MOL.vol_avg_data[6] * 1.6022E-19 * 1E6 -
                     0.5 * mD2 * self.MOL.vol_avg_data[1] * 1E6 * (
                                 vxD2 ** 2 + vyD2 ** 2 + vzD2 ** 2)));


        mD =  2.01410178 * 1.660538921E-27;  # kg


        vxD = np.asarray(self.ATM.vol_avg_data[2] / 1000 / mD /
                          self.ATM.vol_avg_data[1] / 100);  # m/s
        vyD = np.asarray(self.ATM.vol_avg_data[3] / 1000 / mD /
                          self.ATM.vol_avg_data[1] / 100);  # m/s
        vzD = np.asarray(self.ATM.vol_avg_data[4] / 1000 / mD /
                          self.ATM.vol_avg_data[1] / 100);  # m/s
        vxD[np.isnan(vxD)] = 0;
        vyD[np.isnan(vyD)] = 0;
        vzD[np.isnan(vzD)] = 0;

        pD = np.asarray(
            2 / 3 * (self.ATM.vol_avg_data[6] * 1.6022E-19 * 1E6 -
                     0.5 * mD * self.ATM.vol_avg_data[1] * 1E6 * (
                                 vxD ** 2 + vyD ** 2 + vzD ** 2)));

        # total pressure using energy
        pD2_total = np.asarray(self.MOL.vol_avg_data[6] * 1.6022E-19 * 1E6)
        pD_total = np.asarray(self.ATM.vol_avg_data[6] * 1.6022E-19 * 1E6)

        #deriving temperature
        TD2 = np.asarray(
            pD2 / self.MOL.vol_avg_data[1] / 1E6 / 1.3806488E-23);

        TD = np.asarray(
            pD / self.ATM.vol_avg_data[1] / 1E6 / 1.3806488E-23);

        TD[np.isnan(TD)] = 0;
        TD2[np.isnan(TD2)] = 0;
        pD2[np.isnan(pD2)] = 0;
        pD[np.isnan(pD)] = 0;

        return pD2,pD,TD2,TD,pD2_total,pD_total

