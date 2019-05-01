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

import eproc as ep

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

        super(Eirene, self).__init__()
	
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
                # 5          27        6086
        for i in range(0, self.npls):
            dummy1=pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            # dummy1[dummy1.columns[11]]
            dummy1.fillna(0, inplace=True)
            row_to_skip = row_to_skip + self.geom.trimap.shape[0]+ self.nlimps+3
            self.PLS.data.append(dummy1)

        self.PLS.data = pd.concat(self.PLS.data, axis=0)
        self.PLS.data.reset_index(drop=True, inplace=True)


        row_to_skip = row_to_skip +1
        # row_to_skip = 30648
        #row to skip should be 30647
        for i in range(0,self.natm):
            dummy1= pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            # 36730
            dummy1.fillna(0, inplace=True)
            # a = dummy2[dummy2.columns[0:3]][-1:]
            row_to_skip = row_to_skip + self.geom.trimap.shape[0] + self.nlimps +2
            self.ATM.data.append(dummy1)
        #
        self.ATM.data = pd.concat(self.ATM.data, axis=0)
        self.ATM.data.reset_index(drop=True, inplace=True)
        row_to_skip = row_to_skip + 1


        for i in range(0,self.nmol):
            dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip', skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            dummy1.fillna(0, inplace=True)
            row_to_skip = row_to_skip + self.geom.trimap.shape[0] + self.nlimps+ 2
            self.MOL.data.append(dummy1)
        self.MOL.data = pd.concat(self.MOL.data, axis=0)
        self.MOL.data.reset_index(drop=True, inplace=True)
        row_to_skip = row_to_skip + 1

        for i in range(0,self.nion):
            dummy1 = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
            dummy1.fillna(0, inplace=True)
            row_to_skip = row_to_skip + self.geom.trimap.shape[0] + self.nlimps+ 2
            self.ION.data.append(dummy1)

        self.ION.data = pd.concat(self.ION.data, axis=0)
        self.ION.data.reset_index(drop=True, inplace=True)
        row_to_skip = row_to_skip + 1

        self.MISC.data = pd.read_csv(self.runfolder + 'eirene.transfer.gz', compression='gzip' , skiprows=row_to_skip, nrows=self.geom.trimap.shape[0],delim_whitespace=True, header=None,index_col=False, error_bad_lines=False, warn_bad_lines=False)
        self.MISC.data.reset_index(drop=True, inplace=True)
                        


    def plot_eirene(self,species=None):

        if species is None:
            var = self.MOL.data[1]
            label = self.MOL.names[0] +' - '+ self.MOL.unitName[0]
        elif species is "MOL":
            var = self.MOL.data[1]
            label = self.MOL.names[0] +' - '+ self.MOL.unitName[0]
        elif species is "ATM":
            var = self.ATM.data[1]
            label = self.ATM.names[0] +' - '+ self.ATM.unitName[0]
        else:
            logger.error('choose between MOL/ATM')
            return


        # plt.figure()
        # x = [self.geom.xv[i] for i in self.geom.trimap]
        # y = [self.geom.yv[i] for i in self.geom.trimap]
        #
        # plt.tricontourf(x,y,self.MOL.data)
        # plt.show()

        x = [self.geom.xv[i] for i in
             self.geom.trimap]
        y = [self.geom.yv[i] for i in
             self.geom.trimap]

        # matplotlib.pyplot.tricontourf(x, y, sim_hfe_Nrad0.data.eirene.MOL.data)

        # plt.tricontourf(sim_hfe_Nrad0.data.eirene.geom.xv,sim_hfe_Nrad0.data.eirene.geom.yv,sim_hfe_Nrad0.data.eirene.geom.trimap,sim_hfe_Nrad0.data.eirene.MOL.data[1])


        # if lowerbound is None:
        lower = min(var)
        # else:
        #   lower=lowerbound
        # if upperbound is None:
        upper = max(var)
        # else:
        #   upper=upperbound
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
            # print(i)
            polygon = Polygon([[x1[i], y1[i]], [x2[i], y2[i]], [x3[i], y3[i]]],
                              edgecolor='none', alpha=0.1, linewidth=0,
                              closed=True)
            patches.append(polygon)

        norm = mpl.colors.Normalize(vmin=lower, vmax=upper)
        collection = PatchCollection(patches, match_original=True)
        collection.set(array=var, cmap='jet', norm=norm)

        fig, ax = plt.subplots()
        ax.add_collection(collection)

        ax.autoscale_view()

        sfmt = ScalarFormatter(useMathText=True)
        sfmt.set_powerlimits((0, 0))
        sm = plt.cm.ScalarMappable(cmap="jet",
                                   norm=plt.Normalize(vmin=lower, vmax=upper))
        sm.set_array([])
        plt.xlabel('R [m]')
        plt.ylabel('Z [m]')

        cbar = plt.colorbar(sm, format=sfmt)
        cbar.set_label(label)
        # plt.show(block=True)

    def plot_subdivertor(self,path,subdivertor_file):

        rvert = ep.data(path, 'RVERTP').data
        rvert = np.trim_zeros(rvert, 'b')
        zvert = ep.data(path, 'ZVERTP').data
        zvert = -np.trim_zeros(zvert, 'b')

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

        patches = []
        for i in list(range(0, len(A))):
            # print(i)
            polygon = Polygon(
                [[A[i], A1[i]], [B[i], B1[i]], [C[i], C1[i]], [D[i], D1[i]]],
                edgecolor='black', alpha=0.5, linewidth=0.5, closed=True)
            patches.append(polygon)
            #
            # polygon = Polygon(
            #     [[rv[0,i], zv[0,i]], [rv[0,i], zv[1,i]], [rv[2,i], zv[2,i]], [rv[3,i], zv[3,i]]],
            #     edgecolor='black', alpha=0.5, linewidth=0.5, closed=True)
            # patches.append(polygon)

        collection = PatchCollection(patches, match_original=True)

        fig, ax = plt.subplots()
        ax.add_collection(collection)
        ax.autoscale_view()

        # sm.set_array([])
        plt.xlabel('R [m]')
        plt.ylabel('Z [m]')

        rpoint = []
        zpoint = []
        color = ['red', 'white', 'green', 'blue']
        rvertex = []
        zvertex = []
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
                            # rvertex.append([float(dummy[0]),float(dummy[1])])
                            rvertex.append(float(dummy[0]))
                            zvertex.append(float(dummy[1]))
                            index = index + 1

            plt.plot(rvertex, zvertex, 'x-', color=color[surf_type - 1],
                     linewidth=0.5)

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
                            # nread = nread +1
                            rinternal = rpoint[0]
                            zinternal = zpoint[0]
                            plt.plot(rinternal, zinternal, '*',
                                     color=color[stype - 1])
                            plt.plot(rpoint[1:], zpoint[1:], '.-',
                                     color=color[stype - 1], linewidth=0.5)
                            nholesread = nholesread + 1
                            index = index + 1
                            # print(stype-1,color[stype-1])
                            # plt.show()
                            # plt.axis('equal')

            plt.show()
            plt.axis('equal')
