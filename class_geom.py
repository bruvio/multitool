# -*- coding: utf-8 -*-
# ----------------------------

# Created on July 2017
"""
__author__ = "Bruno Viola"
__Name__ = "class geom"
__version__ = "0.1"
__release__ = "0"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
__status__ = "Testing"
# __status__ = "Production"
# __credits__ = [""]
"""



import pdb
import numpy as np
import pathlib
import logging
import sys
import os
from importlib import import_module
libnames = ['eproc']

relative_imports = []

logger = logging.getLogger(__name__)
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




def set_folder(folder, owner=None):
    if owner is None:
        owner=os.getenv('USR')
    else:
        owner=owner
        homefold = os.path.join(os.sep, 'u', owner)
        # print(owner)
        # print(homefold)
        # print(homefold + folder)
        pathlib.Path(homefold + os.sep + folder).mkdir(parents=True,
                                                       exist_ok=True)
class geom:
  """"
  class geom
  given a catalogues edge2d simulation it provides geometric info, like:
  owner
  date
  sequence
  machine
  shot number
  xpoint location
  separatrix coordinates
  mesh coordinates
  plus useful info about the poloidal mesh (nr of rings, rows..)


  """

  #def __init__(self,fileArg):

  def __init__(self,shotIDArg,dateIDArg,seqNumArg, ownerArg=None, codeArg=None, macArg=None, fileArg=None ):

      if ownerArg is None:
          self.owner = os.getenv('USR')
      else:
          self.owner = ownerArg


      if codeArg is None:
          self.code = "edge2d"
      else:
          self.code = codeArg
      if macArg is None:
          self.machine = "jet"
      else:
          self.machine =  macArg
      if fileArg is None:
          self.tfile= "tran"
      else:
          self.tfile = fileArg




      self.shot           = shotIDArg
      self.date           = dateIDArg
      self.seq          =  seqNumArg
      self.fullpath     = "/u/"+self.owner+"/cmg/catalog/"+self.code+"/"+self.machine+"/"+self.shot+"/"+self.date+"/seq#"+self.seq+"/"+self.tfile
      folder_sim = self.date + '/seq#' + self.seq
      destination_folder = os.getcwd() + os.sep + 'e2d_data' + os.sep + str(
          self.shot) + os.sep + folder_sim + os.sep + 'tran'

      if os.path.isfile(self.fullpath):
          try:
              rxpoint = eproc.data(self.fullpath, 'RPX', ALL_TRANFILES=0)
              zxpoint = eproc.data(self.fullpath, 'ZPX', ALL_TRANFILES=0)
              rsp = eproc.data(self.fullpath, 'RSEPX', ALL_TRANFILES=0)
              zsp = eproc.data(self.fullpath, 'ZSEPX', ALL_TRANFILES=0)
              rmesh = eproc.data(self.fullpath, 'RMESH', ALL_TRANFILES=0)
              zmesh = eproc.data(self.fullpath, 'ZMESH', ALL_TRANFILES=0)

              self.rxp=rxpoint.data[0]
              self.zxp=zxpoint.data[0]
              self.npts_s=rsp.nPts
              # self.rsep=rsp.data[0:self.npts_s]
              # self.zsep=zsp.data[0:self.npts_s]
              self.rsep = np.around(rsp.data[0:self.npts_s], 4)
              self.zsep = np.around(zsp.data[0:self.npts_s], 4)
              self.RHS_row=0
              self.non_div_row=0
              self.LHS_row=0
              locr=np.equal(self.rsep , self.rxp).nonzero()[0]
              locz=np.equal(self.zsep , self.zxp).nonzero()[0]
              # locr=self.rsep[self.rsep == self.rxp]
              # locz=self.zsep[self.zsep == self.zxp]
              #print(locr,locz)
              if ((locr[0] == locz[0]) and locr[1] == locz[1]):
                  loc=locr
                  self.RHS_row=int(loc[0]-1)
                  self.non_div_row=int(loc[1]-loc[0]-1)
                  self.LHS_row=int(self.npts_s-loc[1]-2)

              #print(self.RHS_row,self.non_div_row,self.LHS_row)
              self.npts_m=int(rmesh.nPts)
              #print(self.npts_m)

              self.rme=rmesh.data[0:self.npts_m]
              self.zme=zmesh.data[0:self.npts_m]
              #print(self.rme,self.zme)
              #locc=self.zme[self.zme > self.zxp]
              locc=np.greater(self.zme, self.zxp).nonzero()[0]
              #print(locc)
              self.core_ring=int(locc[0]/(self.non_div_row + 2)-1)
              ind=locc[0]
              ver=0
              while ver==0:
                  ind=ind+self.RHS_row+1+self.non_div_row+1+self.LHS_row+1
                  sep_t=self.rsep[0]+(self.zme[ind]-self.zsep[0])/(self.zsep[1]-self.zsep[0])*(self.rsep[1]-self.rsep[0])
                  if (self.rme[ind] > sep_t):
                      ver=0
                  else:
                      ver=1
              self.sol_ring=int((ind-locc[0])/(self.RHS_row+1+self.non_div_row+1+self.LHS_row+1)-1)
              self.pr_ring=int((self.npts_m-ind)/(self.RHS_row+1+self.LHS_row+1)-1)
          except:
              raise SystemExit('Unable to read %s file ' % self.fullpath )
      elif os.path.isfile(destination_folder):
          try:
              rxpoint = eproc.data(destination_folder, 'RPX', ALL_TRANFILES=0)
              zxpoint = eproc.data(destination_folder, 'ZPX', ALL_TRANFILES=0)
              rsp = eproc.data(destination_folder, 'RSEPX', ALL_TRANFILES=0)
              zsp = eproc.data(destination_folder, 'ZSEPX', ALL_TRANFILES=0)
              rmesh = eproc.data(destination_folder, 'RMESH', ALL_TRANFILES=0)
              zmesh = eproc.data(destination_folder, 'ZMESH', ALL_TRANFILES=0)

              self.rxp=rxpoint.data[0]
              self.zxp=zxpoint.data[0]
              self.npts_s=rsp.nPts
              # self.rsep=rsp.data[0:self.npts_s]
              # self.zsep=zsp.data[0:self.npts_s]
              self.rsep = np.around(rsp.data[0:self.npts_s], 4)
              self.zsep = np.around(zsp.data[0:self.npts_s], 4)
              self.RHS_row=0
              self.non_div_row=0
              self.LHS_row=0
              locr=np.equal(self.rsep , self.rxp).nonzero()[0]
              locz=np.equal(self.zsep , self.zxp).nonzero()[0]
              # locr=self.rsep[self.rsep == self.rxp]
              # locz=self.zsep[self.zsep == self.zxp]
              #print(locr,locz)
              if ((locr[0] == locz[0]) and locr[1] == locz[1]):
                  loc=locr
                  self.RHS_row=int(loc[0]-1)
                  self.non_div_row=int(loc[1]-loc[0]-1)
                  self.LHS_row=int(self.npts_s-loc[1]-2)

              #print(self.RHS_row,self.non_div_row,self.LHS_row)
              self.npts_m=int(rmesh.nPts)
              #print(self.npts_m)

              self.rme=rmesh.data[0:self.npts_m]
              self.zme=zmesh.data[0:self.npts_m]
              #print(self.rme,self.zme)
              #locc=self.zme[self.zme > self.zxp]
              locc=np.greater(self.zme, self.zxp).nonzero()[0]
              #print(locc)
              self.core_ring=int(locc[0]/(self.non_div_row + 2)-1)
              ind=locc[0]
              ver=0
              while ver==0:
                  ind=ind+self.RHS_row+1+self.non_div_row+1+self.LHS_row+1
                  sep_t=self.rsep[0]+(self.zme[ind]-self.zsep[0])/(self.zsep[1]-self.zsep[0])*(self.rsep[1]-self.rsep[0])
                  if (self.rme[ind] > sep_t):
                      ver=0
                  else:
                      ver=1
              self.sol_ring=int((ind-locc[0])/(self.RHS_row+1+self.non_div_row+1+self.LHS_row+1)-1)
              self.pr_ring=int((self.npts_m-ind)/(self.RHS_row+1+self.LHS_row+1)-1)
          except:
              raise SystemExit('Unable to read %s file ' % self.fullpath)

      else:
          raise SystemExit('Unable to open %s file does not exist' % self.fullpath )




  def __str__(self):
      ret = "Structure Struct contains:\n"
      ret = ret+ "  .shot\n"
      ret = ret+ "  .date\n"
      ret = ret+ "  .seq\n"
      ret = ret+ "  .owner\n"
      ret = ret+ "  .code\n"
      ret = ret+ "  .machine\n"
      ret = ret+ "  .fullpath\n"
      ret + ret+ "  .core_ring\n"
      ret + ret+ "  .sol_ring\n"
      ret + ret+ "  .pr_ring\n"
      ret + ret+ "  .RHS_row\n"
      ret + ret+ "  .non_div_row\n"
      ret + ret+ "  .LHS_row\n"
      ret + ret+ "  .rxp\n"
      ret + ret+ "  .zxp\n"
      ret + ret+ "  .npts_s\n"
      ret + ret+ "  .rsep\n"
      ret + ret+ "  .zsep\n"
      ret + ret+ "  .npts_m\n"
      ret + ret+ "  .rme\n"
      ret + ret+ "  .zme\n"

      return ret

  def write_geometry_e2d(self,path,mesh_filename, separatrix_filename):
      import csv
      # with open(path+'/'+mesh_filename+'.csv', 'wb') as outcsv:
      # 	writer = csv.DictWriter(outcsv, fieldnames = ["RMESH", "ZMESH"])
      # 	writer.writeheader()
      # 	writer.writerow([enumerate(self.rme),enumerate(self.zme)])
      with open(path+'/'+mesh_filename+'.csv', 'wt') as outcsv:
          writer = csv.writer(outcsv, delimiter=' ')
          writer.writerow(["RMESH", "ZMESH"])
          writer.writerows(zip(self.rme, self.zme))
      with open(path+'/'+separatrix_filename+'.csv', 'wt') as outcsv2:
          writer = csv.writer(outcsv2, delimiter=' ')
          writer.writerow(["RSPX", "ZSPX"])
          writer.writerows(zip(self.rsep, self.zsep))
      outcsv.close()
      outcsv2.close()

  def plot_mesh_e2d(self):
      import matplotlib.pyplot as plt
      fname='mesh'+self.shot+'_'+self.date+'_'+self.seq
      plt.plot(self.rme,-self.zme,'+')
      plt.plot(self.rsep, -self.zsep,'o',color='red',markersize=3, linewidth=4)

      plt.tight_layout()
      # plt.show()
      set_folder('figures')
      plt.savefig('./figures/'+fname, format='eps', dpi=300) #
      plt.savefig('./figures/'+fname,  dpi=300)


# import cat as ct
# caselog=ct.cat('92123','jul1717','2','bviola','edge2d')

# a=geom('92123','jul1717','2','bviola','edge2d')
# print(a)
