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
# from class_sim import sim

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
import eproc as ep

class Eirene():
    """
    class to store information from EIRENE
    """
    
    def __init__(self,folder):
        #default setting for EIRENE outputs (may change in the future)

        #folder containing eirene files (can be the catalog folder or run folder)
        self.runfolder = folder

        self.NPLSdataname = 27
        self.NMOLdataname = 11
        self.NATMdataName = 15
        self.NIONdataname = 7
        self.NMISCdataname = 11

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
        self.geom.trimap = []
        self.geom.verts = []
        self.geom.pump = []
        self.geom.pump = []
        self.geom.puff = []


        self.ATM.dataName = []
        self.ATM.unitName = []
        self.ATM.names = {}
        self.ATM.vol_avg_data = []
        self.ATM.surf_avg_data = []

        self.MOL.dataName = []
        self.MOL.unitName =  []
        self.MOL.names ={}
        self.MOL.vol_avg_data = []
        self.MOL.surf_avg_data = []

        self.ION.dataName = []
        self.ION.unitName= []
        self.ION.names ={}
        self.ION.vol_avg_data = []
        self.ION.surf_avg_data = []

        self.PHOT.dataName = []
        self.PHOT.unitName= []
        self.PHOT.names ={}
        self.PHOT.vol_avg_data = []
        self.PHOT.surf_avg_data = []

        self.PLS.dataName = []
        self.PLS.unitName= []
        self.PLS.names ={}
        self.PLS.vol_avg_data = []
        self.PLS.surf_avg_data = []


        self.MISC.dataName= []
        self.MISC.unitName= []
        self.MISC.names = {}
        self.MISC.vol_avg_data = []
        self.MISC.surf_avg_data = []


        #initialising names - check with Gerard/Derek

        self.PLS.dataName.append('papl - part.source atm coll.')
        self.PLS.dataName.append('pmpl - part.source mol coll.')
        self.PLS.dataName.append('pipl - part.source ion coll.')
        self.PLS.dataName.append('pphpl - part.source phot coll.')
        self.PLS.dataName.append('papl+pmpl+pipl - part.source')
        self.PLS.dataName.append('mapl - mom.source atm coll.')
        self.PLS.dataName.append('mmpl - mom.source mol coll.')
        self.PLS.dataName.append('mipl - mom.source ion coll.')
        self.PLS.dataName.append('mphpl - mom.source phot coll.')
        self.PLS.dataName.append('mapl+mmpl+mipl - mom.source')
        self.PLS.dataName.append('diin - plasma density bulk plasma')
        self.PLS.dataName.append('vxin - plasma drift velocity (x)')
        self.PLS.dataName.append('vyin - plasma drift velocity (y)')
        self.PLS.dataName.append('vzin - plasma drift velocity (z)')
        self.PLS.dataName.append('bvin - ')
        self.PLS.dataName.append('tiin - plasma temperature bulk plasma')
        self.PLS.dataName.append('edrift - kinetic energy in drift motion bulk plasma')
        self.PLS.dataName.append('eapl - eng.source atm coll.')
        self.PLS.dataName.append('empl - eng.source mol coll.')
        self.PLS.dataName.append('eipl - eng.source ion coll.')
        self.PLS.dataName.append('ephpl - eng.source phot coll.')
        self.PLS.dataName.append('eapl+empl+eipl - eng.source')
        self.PLS.dataName.append('eael - eng.source electrons atm coll.')
        self.PLS.dataName.append('emel - eng.source electrons mol coll.')
        self.PLS.dataName.append('eiel - eng.source electrons ion coll.')
        self.PLS.dataName.append('ephel - eng.source electrons phot coll.')
        self.PLS.dataName.append('eael+emel+eiel - eng.source electrons')


        # set unit names for bulk plasma ions
        self.PLS.unitName.append('amp/cm^3')
        self.PLS.unitName.append('amp/cm^3')
        self.PLS.unitName.append('amp/cm^3')
        self.PLS.unitName.append('amp/cm^3')
        self.PLS.unitName.append('amp/cm^3')
        self.PLS.unitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.unitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.unitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.unitName.append('amp*g*cm/(s*cm^3)')
        self.PLS.unitName.append( 'amp*g*cm/(s*cm^3)')
        self.PLS.unitName.append( '1/cm^3')
        self.PLS.unitName.append( 'cm/s')
        self.PLS.unitName.append( 'cm/s')
        self.PLS.unitName.append( 'cm/s')
        self.PLS.unitName.append( '?')
        self.PLS.unitName.append( 'eV')
        self.PLS.unitName.append( 'eV')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')
        self.PLS.unitName.append( 'watt/cm^3')





        self.ATM.dataName.append('pdena - atom density')
        self.ATM.dataName.append('vxdena - atom momentum density (x)')
        self.ATM.dataName.append('vydena - atom momentum density (y)')
        self.ATM.dataName.append('vzdena - atom momentum density (z)')
        self.ATM.dataName.append('vdenpara - atom momentum density (B)')
        self.ATM.dataName.append('edena - atom energy density')
        self.ATM.dataName.append('edena/pdena - ')
        self.ATM.dataName.append('not used - ')
        self.ATM.dataName.append('sigma - ')
        self.ATM.dataName.append('not used - ')
        self.ATM.dataName.append('not used - ')
        self.ATM.dataName.append('paat - part.source atm coll.')
        self.ATM.dataName.append('pmat - part.source mol coll.')
        self.ATM.dataName.append('piat - part.source ion coll.')
        self.ATM.dataName.append('paat+pmat+piat - part.source')

        # set unit names for neutral atoms

        self.ATM.unitName.append('1/cm^3')
        self.ATM.unitName.append('g*cm/(s*cm^3)')
        self.ATM.unitName.append('g*cm/(s*cm^3)')
        self.ATM.unitName.append('g*cm/(s*cm^3)')
        self.ATM.unitName.append('g*cm/(s*cm^3)')
        self.ATM.unitName.append('eV/cm^3')
        self.ATM.unitName.append('eV*s/(g*cm)')
        self.ATM.unitName.append(' ')
        self.ATM.unitName.append('?')
        self.ATM.unitName.append(' ')
        self.ATM.unitName.append(' ')
        self.ATM.unitName.append('amp/cm^3')
        self.ATM.unitName.append('amp/cm^3')
        self.ATM.unitName.append('amp/cm^3')
        self.ATM.unitName.append('amp/cm^3')

        # set data names for neutral molecules

        self.MOL.dataName.append('pdenm - molecule density')
        self.MOL.dataName.append('vxdenm - molecule momentum density (x)')
        self.MOL.dataName.append('vydenm - molecule momentum density (y)')
        self.MOL.dataName.append('vzdenm - molecule momentum density (z)')
        self.MOL.dataName.append('vdenpara - molecule momentum density (B)')
        self.MOL.dataName.append('edenm - molecule energy density')
        self.MOL.dataName.append('edenm/pdenm - ')

        # set unit names for neutral molecules
        self.MOL.unitName.append('1/cm^3')
        self.MOL.unitName.append('g*cm/(s*cm^3)')
        self.MOL.unitName.append('g*cm/(s*cm^3)')
        self.MOL.unitName.append('g*cm/(s*cm^3)')
        self.MOL.unitName.append('g*cm/(s*cm^3)')
        self.MOL.unitName.append('eV/cm^3')
        self.MOL.unitName.append('eV*s/(g*cm)')

        # set data names for test ions

        self.ION.dataName.append('pdeni - test ion density')
        self.ION.dataName.append('vxdeni - test ion momentum density (x)')
        self.ION.dataName.append('vydeni - test ion momentum density (y)')
        self.ION.dataName.append('vzdeni - test ion momentum density (z)')
        self.ION.dataName.append('vdenpara - test ion momentum density (B)')
        self.ION.dataName.append('edeni - test ion energy density')
        self.ION.dataName.append('edeni/pdeni - ')

        # set unit names for test ions
        self.ION.unitName.append('1/cm^3')
        self.ION.unitName.append('g*cm/(s*cm^3)')
        self.ION.unitName.append('g*cm/(s*cm^3)')
        self.ION.unitName.append('g*cm/(s*cm^3)')
        self.ION.unitName.append('g*cm/(s*cm^3)')
        self.ION.unitName.append('eV/cm^3')
        self.ION.unitName.append('eV*s/(g*cm)')
        #
        # set data names for misc data

        self.MISC.dataName.append('ncltal - ')
        self.MISC.dataName.append('not used - 1')
        self.MISC.dataName.append('not used - 2')
        self.MISC.dataName.append('vol - zone volume')
        self.MISC.dataName.append('voltal - ')
        self.MISC.dataName.append('dein - plasma density electrons')
        self.MISC.dataName.append('tein - plasma temperature electrons')
        self.MISC.dataName.append('bxin - B unit vector (x)')
        self.MISC.dataName.append('byin - B unit vector (y)')
        self.MISC.dataName.append('bzin - B unit vector (z)')
        self.MISC.dataName.append('bfin - B strength')
        #
        # set unit names for misc data
        self.MISC.unitName.append('?')
        self.MISC.unitName.append(' ')
        self.MISC.unitName.append(' ')
        self.MISC.unitName.append('cm^3')
        self.MISC.unitName.append('?')
        self.MISC.unitName.append('1/cm^3')
        self.MISC.unitName.append('eV')
        self.MISC.unitName.append(' ')
        self.MISC.unitName.append(' ')
        self.MISC.unitName.append(' ')
        self.MISC.unitName.append('tesla')

        super(Eirene, self).__init__()

        self._read_eirene()


    def _read_eirene(self):
        """
        function that reads EIRENE files (automatically when initialising objects)
        :return:
        """
        #read triangles coordinates
        logger.info('reading eirene.npco_char file \n')
        self.geom.xv, self.geom.yv,z= read_npco_file(self.runfolder+'eirene.npco_char')
        #reads triangles map and vertices
        logger.info( 'reading eirene.elemente file \n')
        self.geom.trimap,self.geom.verts = read_elemente_file(self.runfolder+'eirene.elemente')

        #reads pump (only for standard EIRENE files)
        logger.info( 'reading eirene pump file \n')
        self.geom.pump = read_pump_file(self.runfolder + 'pump')
        #read puff location
        logger.info( 'reading puff file \n')
        self.geom.puff = read_puff_file(self.runfolder + 'puff.dat')

        #start reading informations
        logger.info( 'collecting information from eirene.input file \n')
        with open(self.runfolder + 'eirene.input') as f:
            lines = f.readlines()
            text_atoms_spec = '** 4a NEUTRAL ATOMS SPECIES CARDS:'
            text_mole_spec = '** 4b NEUTRAL MOLECULES SPECIES CARDS'
            text_ion_spec = '**4c TEST ION SPECIES CARDS:'
            text_bulk_spec = '*** 5. DATA FOR PLASMA-BACKGROUND'
            text_phot      = '** 4d photons'
            info1 = False
            info2 = False
            info3 = False
            info4 = False
            info_phot = False

            for index, line in enumerate(lines):

                if text_atoms_spec in str(line):
                    index = index +1
                    dummy = lines[index].split()
                    self.natm = int(dummy[0])

                    for i in range(0,self.natm):
                        index = index + 1
                        dummy=lines[index].split()
                        self.ATM.names[i] = dummy[1]
                        nreac = int(dummy[9])
                        index = index + 2*nreac
                    info1=True


                if text_mole_spec in str(line):
                    index = index +1
                    dummy = lines[index].split()
                    self.nmol = int(dummy[0])

                    for i in range(0,self.nmol):
                        index = index + 1
                        dummy=lines[index].split()
                        self.MOL.names[i] = dummy[1]
                        nreac = int(dummy[9])
                        index = index + 2 * nreac
                    info2 = True

                if text_ion_spec in str(line):
                    index = index +1
                    dummy = lines[index].split()
                    self.nion = int(dummy[0])

                    for i in range(0,self.nion):
                        index = index + 1
                        dummy=lines[index].split()
                        self.ION.names[i] = dummy[1]
                        nreac = int(dummy[9])
                        index = index + 2 * nreac
                    info3=True

                if text_phot in str(line):
                    index = index +1
                    dummy = lines[index].split()
                    self.nphot = int(dummy[0])

                    for i in range(0,self.nphot):
                        index = index + 1
                        dummy=lines[index].split()
                        self.PHOT.names[i] = dummy[1]
                        nreac = int(dummy[9])
                        index = index + 2 * nreac
                    info_phot=True

                if text_bulk_spec in str(line):
                    index = index +2
                    dummy = lines[index].split()
                    self.npls = int(dummy[0])

                    for i in range(0,self.npls):
                        index = index + 1
                        dummy=lines[index].split()
                        self.PLS.names[i] = dummy[1]
                        nreac = int(dummy[9])
                        index = index + 2 * nreac
                    info4=True
                if info1 & info2 & info3 & info4 & info_phot is True:
                    break
            f.close()



        # read transfer file and store data as pandas dataframe (first column is always a pandas index!)
        logger.info( 'reading eirene.transfer file \n')
        exists = os.path.isfile(self.runfolder + 'eirene.transfer.gz')

        if exists:

            f = gzip.open(self.runfolder + 'eirene.transfer.gz', 'rb')            

        else:
            f = open(self.runfolder + 'eirene.transfer', 'rb')              

        
        lines = f.readlines()
        text = '* nlimps'
        for index, line in enumerate(lines):
            if text in str(line):
                index=index+1
                dummy=lines[index].split()
                self.nlimps = int(dummy[0])
                self.nlim = int(dummy[1])
                self.nsts = int(dummy[2])
                break
        row_to_skip=index+3
        logger.log(5, row_to_skip)
                # 5          27        6086
        logger.log(5,' reading bulk plasma data')
        for i in range(0, self.npls):
            dummy1=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            # dummy1[dummy1.columns[11]]
            dummy1.fillna(0, inplace=True)#converts nan into 0
            row_to_skip = row_to_skip +self.geom.trimap.shape[0]+1
            logger.log(5, row_to_skip)
            dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=self.nlimps,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip +self.nlimps+ 2
            logger.log(5, row_to_skip)
            self.PLS.vol_avg_data.append(dummy1)
            self.PLS.surf_avg_data.append(dummy2)

        self.PLS.vol_avg_data = pd.concat(self.PLS.vol_avg_data, axis=0)#concatenates as row
        self.PLS.vol_avg_data.reset_index(drop=True, inplace=True)
        self.PLS.surf_avg_data = pd.concat(self.PLS.surf_avg_data, axis=0)#concatenates as row
        self.PLS.surf_avg_data.reset_index(drop=True, inplace=True)


        row_to_skip = row_to_skip +1
        logger.log(5, row_to_skip)

        # row_to_skip = 30648
        #row to skip should be 30647
        logger.log(5, ' reading neutral atom data')
        for i in range(0,self.natm):
            dummy1= pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            # 36730
            dummy1.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip + self.geom.trimap.shape[0] + 1
            logger.log(5, row_to_skip)
            dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=self.nlimps,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip +self.nlimps+ 1
            logger.log(5, row_to_skip)
            self.ATM.vol_avg_data.append(dummy1)
            self.ATM.surf_avg_data.append(dummy2)

        self.ATM.vol_avg_data = pd.concat(self.ATM.vol_avg_data,
                                          axis=0)  # concatenates as row
        self.ATM.vol_avg_data.reset_index(drop=True, inplace=True)
        self.ATM.surf_avg_data = pd.concat(self.ATM.surf_avg_data,
                                           axis=0)  # concatenates as row
        self.ATM.surf_avg_data.reset_index(drop=True, inplace=True)

        row_to_skip = row_to_skip + 1
        logger.log(5,row_to_skip)
        logger.log(5, ' reading neutral molecules data')
        for i in range(0,self.nmol):
            dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip', skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            dummy1.fillna(0, inplace=True)#converts nan into 0
            row_to_skip = row_to_skip + self.geom.trimap.shape[0] + 1
            logger.log(5, row_to_skip)
            dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=self.nlimps,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip + self.nlimps + 2
            logger.log(5, row_to_skip)
            self.MOL.vol_avg_data.append(dummy1)
            self.MOL.surf_avg_data.append(dummy2)

        self.MOL.vol_avg_data = pd.concat(self.MOL.vol_avg_data,
                                          axis=0)  # concatenates as row
        self.MOL.vol_avg_data.reset_index(drop=True, inplace=True)
        self.MOL.surf_avg_data = pd.concat(self.MOL.surf_avg_data,
                                           axis=0)  # concatenates as row
        self.MOL.surf_avg_data.reset_index(drop=True, inplace=True)

        # row_to_skip = row_to_skip + 1
        # logger.log(5, row_to_skip)



        logger.log(5, ' reading test ions data')
        for i in range(0,self.nion):
            dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            dummy1.fillna(0, inplace=True) #converts nan into 0
            row_to_skip = row_to_skip + self.geom.trimap.shape[0] + 1
            logger.log(5, row_to_skip)
            dummy2 = pd.read_csv(self.runfolder + 'eirene.transfer.gz',
                                 compression='gzip', skiprows=row_to_skip,
                                 nrows=self.nlimps,
                                 delim_whitespace=True, header=None,
                                 index_col=False, error_bad_lines=False,
                                 warn_bad_lines=False)
            dummy2.fillna(0, inplace=True)  # converts nan into 0
            row_to_skip = row_to_skip + self.nlimps + 2
            logger.log(5, row_to_skip)
            self.ION.vol_avg_data.append(dummy1)
            self.ION.surf_avg_data.append(dummy2)

        self.ION.vol_avg_data = pd.concat(self.ION.vol_avg_data,
                                          axis=0)  # concatenates as row
        self.ION.vol_avg_data.reset_index(drop=True, inplace=True)
        self.ION.surf_avg_data = pd.concat(self.ION.surf_avg_data,
                                           axis=0)  # concatenates as row
        self.ION.surf_avg_data.reset_index(drop=True, inplace=True)


        logger.log(5, ' reading miscellaneous data')
        self.MISC.vol_avg_data = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
        self.MISC.vol_avg_data.reset_index(drop=True, inplace=True)


        logger.log(5, "stratum data is not read YET!")

        logger.log(5, 'done \n')
        logger.info( 'reading eirene data done! \n')
                        


    def plot_eirene(self,data=None,species=None,var=None, lowerbound=None,upperbound=None,label=None):
        """
        function that allow contour plots of EIRENE data
        :param data input data (dataframe, string or empty)
        as data is stored by read_eirene as a dataframe species and var determine for which species user want the data (row index) and which variable (column index)
        :param species: simu.data.eirene.PLS.names
        {0: 'D+', 1: 'Be1+', 2: 'Be2+', 3: 'Be3+', 4: 'Be4+'}
        :param var:
        column number indentifying variables
        :param label: simu.data.eirene.ATM.names[species] + \
            simu.data.eirene.ATM.dataName[species]
        :param lowerbound minimum value to be used to normalise data
        :param upperbound minimum value to be used to normalise data


        :return: contour plot of data
        usage

            # I want Be1+
            species =1
            data = simu.data.eirene.PLS.vol_avg_data
            label = simu.data.eirene.PLS.names[species-1] + simu.data.eirene.PLS.dataName[26]

            # I want D
            species = 0
            species_name = simu.data.eirene.ATM.names[species]
            data = simu.data.eirene.ATM.vol_avg_data
            label = simu.data.eirene.ATM.names[species] + \
            simu.data.eirene.ATM.dataName[species]

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

        triangnum = self.geom.trimap.shape[0]
        if data is None:
            data = self.MOL.vol_avg_data[triangnum*(species):(species+1)*triangnum]
            data = data[data.columns[1]]
            label = self.MOL.names[0] +' - '+ self.MOL.unitName[0]
        elif data is "MOL":
            data = self.MOL.vol_avg_data[triangnum*(species):(species)*triangnum]
            data = data[data.columns[1]]
            label = self.MOL.names[0] +' - '+ self.MOL.unitName[0]
        elif data is "ATM":
            data = self.ATM.vol_avg_data[triangnum*(species):(species+1)*triangnum]
            data = data[data.columns[1]]
            label = self.ATM.names[0] +' - '+ self.ATM.unitName[0]
        elif isinstance(data,np.ndarray):
            data = data[triangnum*(species):(species+1)*triangnum]
            label = label
        # elif isinstance(data,pd.Series):
        #     var = data[triangnum*(species):(species+1)*triangnum-1]
        #     label = label
        elif isinstance(data,pd.DataFrame):

            data = data[triangnum*(species):(species+1)*triangnum]
            data=data[data.columns[var+1]]
            label = label
        else:
            logger.error('choose between MOL/ATM \n')
            return

        logger.log(5,'plotting {} data volume avg data \n'.format(label))
        # plt.figure()
        # x = [self.geom.xv[i] for i in self.geom.trimap]
        # y = [self.geom.yv[i] for i in self.geom.trimap]
        #
        # plt.tricontourf(x,y,self.MOL.vol_avg_data)
        # plt.show()


        #getting coordinates of the triangles and creating arrays that describe polygons
        logger.log(5,"collecting coordinates of triangles \n")
        x = [self.geom.xv[i] for i in
             self.geom.trimap]
        y = [self.geom.yv[i] for i in
             self.geom.trimap]

        # matplotlib.pyplot.tricontourf(x, y, sim_hfe_Nrad0.vol_avg_data.eirene.MOL.vol_avg_data)

        # plt.tricontourf(sim_hfe_Nrad0.vol_avg_data.eirene.geom.xv,sim_hfe_Nrad0.vol_avg_data.eirene.geom.yv,sim_hfe_Nrad0.vol_avg_data.eirene.geom.trimap,sim_hfe_Nrad0.vol_avg_data.eirene.MOL.vol_avg_data[1])


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
        logger.info('plotting subdivertor structure \n')
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
        :param pufffile:
        :return:
        """
        logger.info('plotting eirene grid \n')

        logger.log(5," reading puff file")
        if pufffile is None:#
            pass
        else:
            self.geom.puff = read_puff_file(self.runfolder + 'puff.dat', alternativefile=pufffile)
        x = [self.geom.xv[i] for i in
             self.geom.trimap]
        y = [self.geom.yv[i] for i in
             self.geom.trimap]

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



