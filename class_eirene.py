import logging
logger = logging.getLogger(__name__)
from class_sim import sim

from types import SimpleNamespace

class Eirene():
    
    def __init__(self,folder):
        self.runfolder = folder
        self.NPLS = 27
        self.NMOL = 11
        self.NION = 7
        self.NMISC = 11


        self.ATM = SimpleNamespace()
        self.MOL = SimpleNamespace()
        self.ION = SimpleNamespace()
        self.MISC = SimpleNamespace()

        self.geom = SimpleNamespace()
        self.geom.xv = []
        self.geom.yx = []
        self.geom.trimap = []

        self.ATM.dataName = []
        self.ATM.unitName = []
        self.ATM.names = {}

        self.MOL.dataName = []
        self.MOL.unitName =  []
        self.ION.dataName = []
        self.ION.unitName= []
        self.MISC.dataName= []
        self.MISC.unitName= []

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


    def _read_eirene(self):

        TriPoints = load(folder+'eirene.npco_char', delimiter=' ')
        TriPoints = TriPoints[1:,1:2]/100

        self.geom.xv = TriPoints[:,0]
        self.geom.xv = TriPoints[:,1]

        self.geom.trimap = load(folder+'eirene.elemente', delimiter=' ')
        self.geom.trimap = self.geom.trimap[1:,1:3]

        with open(self.runfolder + 'eirene.input', 'rb') as f:
            lines = f.readlines()
            text_atoms_spec = '** 4a NEUTRAL ATOMS SPECIES CARDS:'
            text_mole_spec = '** 4b NEUTRAL MOLECULES SPECIES CARDS'

            for index, line in enumerate(lines):
                if text_atoms_spec in str(line):
                    index = index +1
                    dummy = lines[index].split()
                    self.natm = dummy[0]

                    for i in range(0,self.natm):
                        index = index + 1
                        dummy=lines(index).split()
                        self.ATM.names{i} = dummy[1]



                if text_mole_spec in str(line):
                    dummy = lines[index+1].split()
                    self.natm = dummy[0]


