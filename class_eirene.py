import logging
logger = logging.getLogger(__name__)
from class_sim import sim


import pdb
import numpy as np
import gzip
from types import SimpleNamespace
from utility import *
class Eirene():
    
    def __init__(self,folder):
        self.runfolder = folder
        self.NPLSdataname = 27
        self.NMOLdataname = 11
        self.NATMdataName = 15
        self.NIONdataname = 7
        self.NMISCdataname = 11


        self.ATM = SimpleNamespace()
        self.MOL = SimpleNamespace()
        self.ION = SimpleNamespace()
        self.PLS = SimpleNamespace()
        self.MISC = SimpleNamespace()

        self.geom = SimpleNamespace()
        self.geom.xv = []
        self.geom.yv = []
        self.geom.trimap = []

        self.ATM.dataName = []
        self.ATM.unitName = []
        self.ATM.names = {}
        self.ATM.data = []

        self.MOL.dataName = []
        self.MOL.unitName =  []
        self.MOL.names ={}

        self.MOL.data = []


        self.ION.dataName = []
        self.ION.unitName= []
        self.ION.names ={}

        self.ION.data = []


        self.PLS.dataName = []
        self.PLS.unitName= []
        self.PLS.names ={}

        self.PLS.data = []



        self.MISC.dataName= []
        self.MISC.unitName= []
        self.MISC.names = {}

        self.MISC.data = []
   

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
	
        self._read_eirene()


    def _read_eirene(self):

        self.geom.xv, self.geom.yv= read_npco_file(self.runfolder+'eirene.npco_char')

        self.geom.trimap = read_elemente_file(self.runfolder+'eirene.elemente')


        # raise SystemExit



        with open(self.runfolder + 'eirene.input') as f:
            lines = f.readlines()
            text_atoms_spec = '** 4a NEUTRAL ATOMS SPECIES CARDS:'
            text_mole_spec = '** 4b NEUTRAL MOLECULES SPECIES CARDS'
            text_ion_spec = '**4c TEST ION SPECIES CARDS:'
            text_bulk_spec = '*** 5. DATA FOR PLASMA-BACKGROUND'
            info1 = False
            info2 = False
            info3 = False
            info4 = False
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
                if info1 & info2 & info3 & info4 is True:
                    break
            f.close()

                
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
        pdb.set_trace()
        self.PLS.data = np.zeros((self.npls,self.NPLSdataname,self.geom.trimap.shape[0]))
                # 5          27        6086
        for i in range(0,self.npls):
            dummy=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0]-1,delim_whitespace=True, header=None)
            self.PLS.data[i, :, :] = dummy.T
        row_to_skip = row_to_skip + size(self.geom.trimap, axis=0) + 1

        self.ATM.data = np.zeros((self.natm,self.NATMdataName,self.geom.trimap.shape[0]))
                # 5          27        6086
        for i in range(0,self.natm):
            dummy = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0]-1,delim_whitespace=True, header=None)
            self.ATM.data[i, :, :] = dummy.T
        row_to_skip = row_to_skip + size(self.geom.trimap, axis=0) + 1

        self.MOL.data = np.zeros((self.nmol,self.NMOLdataname,self.geom.trimap.shape[0]))
                # 5          27        6086
        for i in range(0,self.nmol):
            dummy = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip', skiprows=row_to_skip, nrows=self.geom.trimap.shape[0]-1,delim_whitespace=True, header=None)
            self.MOL.data[i, :, :] = dummy.T
        row_to_skip = row_to_skip + size(self.geom.trimap, axis=0) + 1

        self.ION.data = np.zeros((self.nion,self.NIONdataname,self.geom.trimap.shape[0]))
                # 5          27        6086
        for i in range(0,self.nion):
            dummy = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0]-1,delim_whitespace=True, header=None)
            self.ION.data[i, :, :] = dummy.T
        row_to_skip = row_to_skip + size(self.geom.trimap, axis=0) + 1

        self.MISC.data = np.zeros((self.NMISCdataname,self.geom.trimap.shape[0]))
                # 5          27        6086
        for i in range(0,self.npls):
            dummy = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=12, nrows=self.geom.trimap.shape[0]-1,delim_whitespace=True, header=None)
            self.MISC.data[i, :, :] = dummy.T
                        

