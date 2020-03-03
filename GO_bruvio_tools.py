#!/usr/bin/env python


# ----------------------------
__author__ = "Bruno Viola"
__Name__ = "bruvio tool GUI"
__version__ = "1"
__release__ = "2"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
# __status__ = "Testing"
__status__ = "Production"
__credits__ = ["gioart"]


import argparse
from pathlib import Path
import logging
from logging import handlers
import pathlib
import numpy as np
import sys
import os
from importlib import import_module
libnames = ['ppf','eproc']

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

        lib = import_module(libr)
        # lib = import_module(libr,package=package)
    except:
        exc_type, exc, tb = sys.exc_info()
        print(os.path.realpath(__file__))
        print(exc)
    else:
        globals()[libr] = lib
import bruvio_tools
from MAGTool import *  # Magnetics Tool

# from PyQt4 import Qt, QtCore,QtGui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from magSurfGA_SL import Ui_magsurf_window
from edge2d_window import Ui_edge2d_window
from eqdsk_window import Ui_eqdsk_window

from matplotlib import cm
from plotdata import Ui_plotdata_window
from scipy import interpolate
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import subprocess
# sys.path.append('../')

from class_sim import sim
from EDGE2DAnalyze import shot
from utility import *
import matplotlib.pyplot as plt
plt.rcParams["savefig.directory"] = os.chdir(os.getcwd())






try:
    ep = eproc
except:
    logger.error('failed to load EPROC')
    # raise Systexit

if 'ppf' not in sys.modules:
    logging.warning('failed to load ppf')
    logging.warning('you are offline!')

myself = lambda: inspect.stack()[1][3]
logger = logging.getLogger(__name__)


class bruvio_tool(QMainWindow, bruvio_tools.Ui_MainWindow):
    """
    Class for running the GUI and handling events.

    This GUI allows the user to:


    """

    # ----------------------------


    def __init__(self,parent=None):
        """
        Setup the GUI, and connect the buttons to functions.
        """
        try:

            super(bruvio_tool, self).__init__(parent)
            self.setupUi(self)
            logger.debug('start')
            cwd = os.getcwd()
            self.workfold = cwd
            self.home = cwd
            parent= Path(self.home)



            with open("./user_installation_data.json", mode="r", encoding="utf-8") as f:
                # Remove comments from input json
                with open("temp.json", "w") as wf:
                    for line in f.readlines():
                        if line[0:2] == "//" or line[0:1] == "#":
                            continue
                        wf.write(line)

            with open("temp.json", "r") as f:
                self.input_dict = json.load(f, object_pairs_hook=OrderedDict)
                os.remove("temp.json")

            self.installationfolder =self.input_dict['install_folder']
            self.basefolder = self.input_dict['base_folder']






            if "USR" in os.environ:
                logger.debug('USR in env')
                #self.owner = os.getenv('USR')
                self.owner = os.getlogin()
            else:
                logger.debug('using getuser to authenticate')
                import getpass
                self.owner = getpass.getuser()

            logger.info('this is your username {}'.format(self.owner))
            self.homefold = os.path.join(os.sep, 'u', self.owner)
            logger.info('this is your homefold {}'.format(self.homefold))
            # logger.info('this is edge2d fold {}'.format(self.edge2dfold))
            home = str(Path.home())


            logger.info('we are in %s', cwd)


            pathlib.Path(cwd + os.sep + 'figures').mkdir(parents=True,exist_ok=True)
            pathlib.Path(cwd + os.sep + 'e2d_data').mkdir(parents=True,exist_ok=True)
            pathlib.Path(cwd + os.sep + 'exp_data').mkdir(parents=True,exist_ok=True)

            pathlib.Path(cwd + os.sep + 'standard_set').mkdir(parents=True,exist_ok=True)

            self.readdata_button.clicked.connect(self.handle_readdata_button)
            self.edge2d_button.clicked.connect(self.handle_edge2d_button)
            self.eqdsk_button.clicked.connect(self.handle_eqdsk_button)
            self.magsurf_button.clicked.connect(self.handle_magsurf_button)
            self.readdata_button.setToolTip(
                'opens windows to read standard set to plot time traces')


            self.exit_button.clicked.connect(self.handle_exit_button)
            self.PathTranfile = None
            logger.info('init DONE!\n')
            self.value = 1
        except:
            logger.error('init FAILED!\n')
            self.value = 0

    def __int__(self):
        return int(self.value)

    def handle_readdata_button(self):
        """
        opens a new windows where the user can input a list of pulses he/she wants to plot

        than the user can select a standard sets (a list of signal)
        and then plot them


        :return:
        """
        try:
            logger.info('\n')
            logger.info('plotting tool')

            self.window_plotdata = QMainWindow()
            self.ui_plotdata = Ui_plotdata_window()
            self.ui_plotdata.setupUi(self.window_plotdata)
            self.window_plotdata.show()

            initpulse = ppf.pdmsht()
            initpulse2 = initpulse -1

            self.ui_plotdata.textEdit_pulselist.setText(str(initpulse))
            # self.ui_plotdata.textEdit_colorlist.setText('black')

            self.ui_plotdata.selectfile.clicked.connect(self.selectstandardset)

            self.ui_plotdata.plotbutton.clicked.connect(self.plotdata)
            self.ui_plotdata.savefigure_checkBox.setChecked(False)
            self.ui_plotdata.smooth_checkBox.setChecked(False)
            self.ui_plotdata.calcmean_checkBox.setChecked(False)
            self.ui_plotdata.checkBox.setChecked(False)
            self.ui_plotdata.checkBox.toggled.connect(
                lambda: self.checkstateJSON(self.ui_plotdata.checkBox))

            self.JSONSS = "PLASMA_main_parameters_new.json"

            logger.debug('default set is {}'.format(self.JSONSS))
            logger.info('select a standard set')
            logger.info('\n')
            logger.info('type in a list of pulses')
            return 1
        except:
            logger.error('failed to run Plot Data GUI')
            return 0
    def handle_eqdsk_button(self):
        try:
            logger.info('\n')
            logger.info('eqdsk tool')

            self.window_eqdsk = QMainWindow()
            self.ui_eqdsk = Ui_eqdsk_window()
            self.ui_eqdsk.setupUi(self.window_eqdsk)
            self.window_eqdsk.show()

            self.ui_eqdsk.checkBox_invert.setChecked(True)
            self.ui_eqdsk.checkBox_normalize.setChecked(True)

            self.ui_eqdsk.eqdsk_exit.clicked.connect(self.exitGUI_eqdsk)


            self.ui_eqdsk.lineEdit_eqdskname.setText('g_p92121_t49.445_mod.eqdsk')

            self.eqdsk = "/u/"+ self.owner+ "/"+ self.basefolder+ "/" + self.installationfolder+'/exp_data/g_p92121_t49.445_mod.eqdsk'

            self.ui_eqdsk.radioButton_efit.setChecked(True)
            self.ui_eqdsk.radioButton_other.setChecked(False)
            self.ui_eqdsk.lineEdit_psioffset.setText('7.4032')
            self.ui_eqdsk.lineEdit_labelIN.setText('LFE_81472')
            self.ui_eqdsk.lineEdit_labelOUT.setText('LFEexp_JET_python')




            self.ui_eqdsk.select_eqdsk.clicked.connect(self.handle_select_eqdsk)
            self.ui_eqdsk.pushButton_read.clicked.connect(self.handle_readeqdsk)
            self.ui_eqdsk.pushButton_lcmsmap.clicked.connect(self.handle_lcmsmap)
            self.ui_eqdsk.pushButton_lcmsmapX.clicked.connect(self.handle_lcmsmapX)
            self.ui_eqdsk.pushButton_solmap.clicked.connect(self.handle_solmap)
            self.ui_eqdsk.pushButton_getmagneticdata.clicked.connect(self.handle_getmagneticdata)
            self.ui_eqdsk.pushButton_writemagneticdata.clicked.connect(self.handle_writemagneticdata)
            self.ui_eqdsk.pushButton_writematrix.clicked.connect(self.handle_writematrix)
            self.ui_eqdsk.pushButton_openinputfile.clicked.connect(self.handle_openinputfile)



            self.vesselfile =             "/u/"+ self.owner+ "/"+ self.basefolder+ "/"+ self.installationfolder+'/exp_data/vessel_JET_csv.txt'
            return 1
        except:
            logger.error('failed to launch EQDSK GUI ')
            return 0

    def handle_edge2d_button(self):
        try:
            logger.info('\n')
            logger.info('edge2d tool')
            self.Inputcode = 0
            self.ExtraInput = 0
            self.PathCatalog = '/home'

            self.edge2d_window = QMainWindow()
            self.ui_edge2d = Ui_edge2d_window()
            self.ui_edge2d.setupUi(self.edge2d_window)
            self.edge2d_window.show()

            self.ui_edge2d.edge2d_exit.clicked.connect(self.exitGUI_edge2d)
            self.ui_edge2d.rungetnames_button.clicked.connect(self.getsimnames)

            self.ui_edge2d.pushButton_pumpcurrents.clicked.connect(self.handle_pumpcurrents)
            self.ui_edge2d.pushButton_contour.clicked.connect(self.handle_contour)
            self.ui_edge2d.pushButton_powerbalance.clicked.connect(self.handle_powerbalance)
            self.ui_edge2d.pushButton_print.clicked.connect(self.handle_print)
            self.ui_edge2d.pushButton_profiles.clicked.connect(self.handle_profiles)
            # self.ui_edge2d.pushButton_profiles.clicked.connect(self.handle_profiles)
            self.ui_edge2d.pushButton_radiation.clicked.connect(self.handle_radiation)

            # self.ui_edge2d.pushButton_pumpcurrents.setEnabled(False);


            self.ui_edge2d.lineEdit_1st.setText('compare_dict_84600.json')
            self.JSONSS1 = 'compare_dict_84600.json'
            self.ui_edge2d.lineEdit_2nd.setText('compare_dict_84600_tuningVassili.json')
            self.JSONSS2 = 'compare_dict_84600_tuningVassili.json'

            fsm = QFileSystemModel()
            index = fsm.setRootPath(self.PathCatalog)
            # self.comboBox = Qt.QComboBox()
            self.ui_edge2d.comboBox_Name.setModel(fsm)
            self.ui_edge2d.comboBox_Name.setRootModelIndex(index)
            self.ui_edge2d.comboBox_Name.currentIndexChanged.connect(self.ScanName)

            self.simlist = []
            self.namelist = []

            # self.ui_edge2d.comboBoxProgramE2d.currentIndexChanged.connect(self.ProgramE2dFunc)

            self.ui_edge2d.comboBox_Machine.currentIndexChanged.connect(self.MachineFunc)

            self.ui_edge2d.comboBox_Shot.currentIndexChanged.connect(self.ShotFunc)

            self.ui_edge2d.comboBox_Date.currentIndexChanged.connect(self.DatagFunc)

            self.ui_edge2d.comboBox_Seq.currentIndexChanged.connect(self.SeqFunc)


            self.ui_edge2d.add_sim.clicked.connect(self.handle_add_sim)
            self.ui_edge2d.lineEdit_var.setText('denel')
            self.ui_edge2d.lineEdit_var_5.setText(self.ui_edge2d.lineEdit_var.text())


            self.ui_edge2d.lineEdit_var.textChanged.connect(lambda: self.updateLineedit(self.ui_edge2d.lineEdit_var))
            self.ui_edge2d.lineEdit_var_5.textChanged.connect(lambda: self.updateLineedit(self.ui_edge2d.lineEdit_var_5))


            self.ui_edge2d.lineEdit_var_2.setText('ot')
            self.ui_edge2d.lineEdit_var_3.setText('test')
            self.ui_edge2d.lineEdit_var_4.setText('targetfilename')
            self.targetfilename = self.ui_edge2d.lineEdit_var_4.text()






            self.ui_edge2d.checkBox_profile.setChecked(False)
            self.ui_edge2d.checkBox_time.setChecked(False)
            self.ui_edge2d.checkBox_flux.setChecked(False)
            self.ui_edge2d.checkBox_geom.setChecked(False)

            self.ui_edge2d.select_json1.clicked.connect(self.handle_selectjson1)
            self.ui_edge2d.select_json2.setEnabled(False);
            self.ui_edge2d.lineEdit_2nd.setEnabled(False);
            self.ui_edge2d.enablecompare_check.setChecked(False)

            self.ui_edge2d.enablecompare_check.toggled.connect(
                lambda: self.checkprintstate(self.ui_edge2d.enablecompare_check))

            self.ui_edge2d.select_json2.clicked.connect(self.handle_selectjson2)

            self.ui_edge2d.runanalyze_button.clicked.connect(self.handle_runanalyze_button)

            self.ui_edge2d.edit_JSON2.setChecked(False)
            self.ui_edge2d.edit_JSON1.setChecked(False)

            self.ui_edge2d.edit_JSON1.toggled.connect(
                lambda: self.checkstateJSON(self.ui_edge2d.edit_JSON1))
            self.ui_edge2d.edit_JSON2.toggled.connect(
                lambda: self.checkstateJSON(self.ui_edge2d.edit_JSON2))
            self.ui_edge2d.textEdit_message2.setText('input_dict_84600.json')
            self.ui_edge2d.runcpmparesims_button.clicked.connect(self.handle_run)

            return 1
        except:
            logger.error('failed to open EDGE2D GUI')
            return 0


    def handle_magsurf_button(self):
        try:
            self.magsurf_window = QMainWindow()
            self.ui_magsurf = Ui_magsurf_window()
            self.ui_magsurf.setupUi(self.magsurf_window)
            plt.close()
            self.magsurf_window.show()
            #
            toolBar = NavigationToolbar(self.ui_magsurf.canvas, self.magsurf_window)
            self.magsurf_window.addToolBar(toolBar)

            #
            initpulse = ppf.pdmsht()
            self.ui_magsurf.JPNedit.setText(str(initpulse))
            self.ui_magsurf.timeEdit.setText('50')  # s
            self.ui_magsurf.stepPsiEdit.setText('0.1') # V/s
            self.ui_magsurf.solEdit.setText('1') # cm
            self.ui_magsurf.NsolEdit.setText('5') # integer, nr of SOL lines
            self.ui_magsurf.coreEdit.setText('5') # integer, nr of CORE lines
            self.ui_magsurf.coreStepEdit.setText('0.1') # V/s



            #
            # #



            self.ui_magsurf.FW_CB.setChecked(True)
            self.ui_magsurf.GAP_CB.setChecked(True)
            self.ui_magsurf.GAP_CB.setStyleSheet("color:red")
            self.ui_magsurf.SP_CB.setChecked(True)
            self.ui_magsurf.SP_CB.setStyleSheet("color:cyan")
            self.ui_magsurf.XLOC_CB.setChecked(True)
            self.ui_magsurf.XLOC_CB.setStyleSheet("color:magenta")
            self.ui_magsurf.WALLS_CB.setChecked(True)
            self.ui_magsurf.WALLS_CB.setStyleSheet("color:blue")
            self.ui_magsurf.EFIT_CB.setChecked(True)
            self.ui_magsurf.EFIT_CB.setStyleSheet("color:green")
            #
            self.ui_magsurf.minSlider.setText('40s')
            self.ui_magsurf.maxSlider.setText('70s')
            self.ui_magsurf.actualSlider.setText('  ')
            self.ui_magsurf.configPlasma.setText('   ')
            self.ui_magsurf.timeXLOC_LB.setText('   ')
            self.ui_magsurf.timeWALLS_LB.setText('   ')
            self.ui_magsurf.timeEFIT_LB.setText('   ')
            #
            self.ui_magsurf.resetPB.clicked.connect(self.resetGUI)
            self.ui_magsurf.defaultPB.clicked.connect(self.defaultGUI)
            self.ui_magsurf.exitPB.clicked.connect(self.exitGUI)
            #

            self.ui_magsurf.plotParam = {
                'JPNobj': None,
                'expDataDictJPNobj_EFIT': None,
                'nameListGap': None,
                'nameListStrikePoints': None,
                'expDataDictJPNobj_XLOC': None,
                'expDataDictJPNobj_WALLS': None,
                'offR_XLOC': None,
                'offZ_XLOC': None,
                'time' : None,
                'gapDict' : None,
                'xFW' : None,
                'yFW' : None,
                'rEFIT' : None,
                'zEFIT' : None,
                'rBND_XLOC_smooth' : None,
                'zBND_XLOC_smooth' : None,
                'rBND_XLOC' : None,
                'zBND_XLOC' : None,
                'rXp' : None,
                'zXp' : None,
                'rSP' : None,
                'zSP' : None,
                'rBND_WALLS': None,
                'zBND_WALLS': None,
                'checkFW' : None,
                'checkGAP' : None,
                'checkSP'  : None,
                'checkXLOC' : None,
                'checkWALLS':None,
                'checkEFIT' : None,
                'flagDiverted' :  None,
                'rGrid': None,
                'zGrid': None,
                'psiGrid': None,
                'psiEFIT':None
            }


            #
            self.ui_magsurf.runPB.clicked.connect(self.goMagSurfGA)
            self.ui_magsurf.isopsiPB.clicked.connect(self.plotIsoPsi)
            self.ui_magsurf.isopsiFillPB.clicked.connect(self.plotIsoPsiFill)
            self.ui_magsurf.solPB.clicked.connect(self.plotSol)
            self.ui_magsurf.corePB.clicked.connect(self.plotCore)

            self.ui_magsurf.runPB.released.connect(self.button_released)
            self.ui_magsurf.isopsiPB.released.connect(self.button_released)
            self.ui_magsurf.isopsiFillPB.released.connect(self.button_released)
            self.ui_magsurf.solPB.released.connect(self.button_released)
            self.ui_magsurf.corePB.released.connect(self.button_released)


            self.SenderActual=[]

            self.ui_magsurf.horizontalSlider.valueChanged.connect(self.slider_moved)
            # self.ui_magsurf.horizontalSlider.sliderReleased.connect(
            #    lambda: self.ui_magsurf.plotBoundaryFromSliderReleased(self.horizontalSlider))

            return 1
        except:
            logger.error('failed to start MAGSurf GUI')
            return 0



    def handle_select_eqdsk(self):
        folder = os.path.join(self.homefold,os.sep, self.basefolder,os.sep,self.installationfolder,os.sep,"exp_data")
        self.eqdsk, _filter = QtGui.QFileDialog.getOpenFileName(None,'Select EQDSK',folder,'EQDSK Files(*.eqdsk)')
        if not self.eqdsk=='':
            # self.eqdsk = os.path(self.eqdsk)
            self.ui_eqdsk.lineEdit_eqdskname.setText(os.path.basename(self.eqdsk))

            logger.debug('you have chosen {}'.format(os.path.basename(self.eqdsk)))
            os.chdir(self.home)
            return self.eqdsk
    #
    # def handle_readeqdsk(self):
    #     if not self.eqdsk:
    #         logger.error('select eqdsk first')
    #     else:
    #         if self.ui_eqdsk.radioButton_efit.isChecked() == True:
    #             input_dict = {'fixfree': False, 'efit': True}
    #         if self.ui_eqdsk.radioButton_other.isChecked() == True:
    #             input_dict = {'fixfree': True, 'efit': False}
    #         rdim, rleft, zmid, zdim, bcentr, current, rcentr, sibry, simag, fpol, rlim, zlim, fpol, rbbbs, zbbbs, psirzm, psinorm, nrgr, nzgr, rmax, rmin, zmax, zmin, Smoothpsirz, r_rect, z_rect, rmaxis, zmaxis = read_eqdsk(
    #             self.eqdsk, input_dict)


    def handle_openinputfile(self):
        if self.owner == 'bviola':
            inputfilefortran =  "/u/"+ self.owner+ "/work/Fortran/tokmagnmap_mac/tokinfo.txt"
            logger.info('opening input file to Fortran code')
            # os.system('kate {}'.format(inputfilefortran))
            subprocess.Popen('atom {}'.format(inputfilefortran), shell=True)



    def handle_lcmsmap(self):
        if self.owner == 'bviola':
            os.chdir("/u/"+ self.owner+ "/work/Fortran/tokmagnmap_mac")
            logger.info('running LCMS map')

            # os.system('toksepmap')
            subprocess.Popen('toksepmap', shell=True)
            os.chdir(self.home)
            logger.info('done')

    def handle_lcmsmapX(self):
        if self.owner == 'bviola':
            os.chdir("/u/"+ self.owner+ "/work/Fortran/tokmagnmap_mac")
            logger.info('running LCMS X map')

            # os.system('toksepmapx')
            subprocess.Popen('toksepmapx', shell=True)
            os.chdir(self.home)
            logger.info('done')




    def handle_solmap(self):
        if self.owner == 'bviola':
            os.chdir("/u/" + self.owner + "/work/Fortran/tokmagnmap_mac")
            logger.info('running SOL map')

            # os.system('toksolmap')
            subprocess.Popen('toksolmap', shell=True)
            os.chdir(self.home)
            logger.info('done')




    def handle_getmagneticdata(self):

        if not self.eqdsk:
            logger.error('select eqdsk first')
        else:
            if self.ui_eqdsk.radioButton_efit.isChecked() == True:
                input_dict = {'fixfree': False, 'efit': True}
            if self.ui_eqdsk.radioButton_other.isChecked() == True:
                input_dict = {'fixfree': True, 'efit': False}
            name = self.ui_eqdsk.lineEdit_labelIN.text()
            # if self.owner == 'bviola':
            #     os.chdir(self.edge2dfold)
            # os.chdir(self.edge2dfold)
            B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2D, z2D, r_rect, z_rect, rmaxis, zmaxis = get_magnetic_data_from_eqdsk(
                self.eqdsk, input_dict, name)
            os.chdir(self.home)
            logger.info('magnetic data computed!')
            self.ui_eqdsk.pushButton_writemagneticdata.setEnabled(True);

    def handle_readeqdsk(self):
        if not self.eqdsk:
            logger.error('select eqdsk first')
        else:
            psioffset = float(self.ui_eqdsk.lineEdit_psioffset.text())

            if self.ui_eqdsk.radioButton_efit.isChecked() == True:
                input_dict = {'fixfree': False, 'efit': True}
            if self.ui_eqdsk.radioButton_other.isChecked() == True:
                input_dict = {'fixfree': True, 'efit': False}
            rdim, rleft, zmid, zdim, bcentr, current, rcentr, sibry, simag, fpol, rlim, zlim, fpol, rbbbs, zbbbs, psirzm, psinorm, nrgr, nzgr, rmax, rmin, zmax, zmin, Smoothpsirz, r_rect, z_rect, rmaxis, zmaxis = read_eqdsk(
                self.eqdsk, input_dict)
            r_ves, z_ves = read_vessel(self.vesselfile)
            from math import pi
            fig, ax = plt.subplots()
            CS = ax.contour(r_rect, z_rect, -(psirzm + sibry) + psioffset,180)
            plt.clabel(CS, inline=1, fontsize=10)
            ax.contour(r_rect,z_rect,psirzm,100)
            ax.plot(r_ves, z_ves, "k")
            ax.plot(rbbbs, zbbbs, "ro")
            ax.plot(rlim, zlim, "bo")
            plt.show(block=True)
            logger.info('EQDSK read done')

    def handle_writemagneticdata(self):
        """
        write magnetic data to file
        :return:
        """
        import os
        if not self.eqdsk:
            logger.error('select eqdsk first')
        else:
            psioffset = float(self.ui_eqdsk.lineEdit_psioffset.text())
            nameIN = self.ui_eqdsk.lineEdit_labelIN.text()
            nameOUT = self.ui_eqdsk.lineEdit_labelOUT.text()
            if self.ui_eqdsk.checkBox_normalize.isChecked():
                normalize = True
            else:
                normalize = False
            if self.ui_eqdsk.checkBox_invert.isChecked():
                invert = True
            else:
                invert = False
            os.chdir(self.home)
            if [file for file in os.listdir(self.home) if nameIN in file]:
            # if os.path.isfile(nameIN):
                B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2, z2D, \
                r_rect, z_rect, rmaxis, zmaxis = write_magnetic_data(nameIN,
                                                                 nameOUT,
                                                                 psioffset,
                                                                 invert=invert,
                                                                 normalize=normalize)
                os.chdir(self.home)
                logger.info('magnetic data written')
            else:
                logger.error('generate magnetic data first!')
                self.ui_eqdsk.pushButton_writemagneticdata.setEnabled(False);

            self.ui_eqdsk.pushButton_writematrix.setEnabled(True);
            logger.info('copy output files in correct folder before running Mapping tools')



    def handle_writematrix(self):
        if not self.eqdsk:
            logger.error('select eqdsk first')
        else:
            nameIN = self.ui_eqdsk.lineEdit_labelIN.text()
            nameOUT = self.ui_eqdsk.lineEdit_labelOUT.text()
            os.chdir(self.home)
            if [file for file in os.listdir(self.home) if nameIN in file]:
            # if os.path.isfile(nameIN) :
                R, Z, PSI, BR, Bz, dPSIdR, dPSIdz, dBRdR, dBRdz, dBzdR, dBzdz = define_input_matrix_for_mesh(
                    nameOUT)

                os.chdir(self.home)
                logger.info('matrix written to file')
            else:
                logger.error('generate input files first!')
                self.ui_eqdsk.pushButton_writematrix.setEnabled(False);


    def handle_pumpcurrents(self):

        if not self.simlist:
            logger.error('choose a simulation first')
        else:

            self.targetfilename = self.ui_edge2d.lineEdit_var_4.text()

            for index1 in range(0, len(self.simlist)):
                logger.info('analyzing sim {}'.format(self.namelist[index1]))
                simdata = self.namelist[index1].split('/')
                owner = simdata[0]
                pulse = simdata[1]
                date = simdata[2]
                seq = simdata[3]

                folder = "/u/"+owner+os.sep+'cmg/catalog/edge2d/jet/'+pulse+os.sep+date+os.sep+'seq#'+seq
                eirenesurfaces= 'eirene_nondefaultsur'
                if not [file for file in os.listdir(folder) if eirenesurfaces in file]:
                    logger.error('simulation {} does not contain EIRENE non default surfaces files\n skipping'.format(self.namelist[index1]))
                    self.simlist.pop(index1)
                    self.ui_edge2d.textEdit_message.clear()

                    self.namelist.pop(index1)
                    for simname in self.namelist:
                        self.ui_edge2d.textEdit_message.append(str(simname))



            folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder
            sim.write_eirene_cur2file(self.simlist, folder + '/e2d_data', self.targetfilename)




    def handle_contour(self):
        if not self.simlist:
            logger.error('choose a simulation first')
        else:
            folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder

            os.chdir(folder)

            self.variable = self.ui_edge2d.lineEdit_var.text().split(',')
            for index1 in range(0, len(self.simlist)):
                logger.info('analyzing sim {}'.format(self.namelist[index1]))
                for j, vari in enumerate(self.variable):
                    logger.info(
                        'collection {} data'.format(vari))
                    simu = self.simlist[index1][0]
                    label = self.simlist[index1][1]
                    var = ep.data(simu.fullpath, vari).data
                    var = np.trim_zeros(var, 'b')
                    simu.contour(var, vari.lower()+'_' + label)
                    # variable = ep.data(simu.fullpath, vari ).data
                    # variable = -np.trim_zeros(variable, 'b')
                    # simu.contour(vari, vari.lower()+'_' + label)
                    plt.show(block=True)
            os.chdir(self.home)


    def handle_powerbalance(self):
        if not self.simlist:
            logger.error('choose a simulation first')
        else:
            logger.info('computing power balance')
            for index1 in range(0, len(self.simlist)):
                logger.info('analyzing sim {}'.format(self.namelist[index1]))
                simu = self.simlist[index1][0]
                label = self.simlist[index1][1]
                simu_pb = simu.read_print_file_edge2d()

                if simu_pb:
                    sim.bar_power_balance(simu_pb, label)
                    plt.show(block=True)

    def handle_print(self):
        if not self.simlist:
            logger.error('choose a simulation first')
        else:
            self.targetfilename = self.ui_edge2d.lineEdit_var_4.text()
            # for index1 in range(0, len(self.simlist)):
                # print(simlist[i][0].fullpath)
            logger.info('writing print-file data to csv file')
            # logger.info('analyzing sim {}'.format(self.namelist[index1]))
            folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder


            sim.write_print2file(self.simlist, folder+'/e2d_data', self.targetfilename)

            logger.info('done')

    def handle_profiles(self):
        if not self.simlist:
            logger.error('choose a simulation first')
        else:
            logger.info('writing simulation profiles to file')
            sim.write_edge2d_profiles1(self.simlist, 'e2dprofiles_python')
            logger.info('done')


    def handle_radiation(self):
        if not self.simlist :
            logger.error('choose a simulation first')
        else:
            # for index1 in range(0, len(self.simlist)):
            #     simu = self.simlist[index1][0]
                folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder

                os.chdir(folder)

                upper = input('enter upper bound in exp notation \n')
                sim.contour_rad_power(self.simlist, float(upper))
                plt.show(block=True)
                os.chdir(self.home)


    def updateLineedit(self,lineedit):
        if lineedit.objectName() == "lineEdit_var":
            self.ui_edge2d.lineEdit_var_5.setText(self.ui_edge2d.lineEdit_var.text())
        if lineedit.objectName() == "lineEdit_var_5":
            self.ui_edge2d.lineEdit_var.setText(self.ui_edge2d.lineEdit_var_5.text())

    def exitGUI(self):
        """
        close the GUI
        :return:
        """
        self.magsurf_window.close()
    def exitGUI_edge2d(self):
        """
        close the GUI
        :return:
        """
        self.edge2d_window.close()

    def exitGUI_eqdsk(self):
        """
        close the GUI
        :return:
        """
        self.window_eqdsk.close()



############################################
    def button_released(self):
        sending_button = self.sender()
        print('%s Clicked!' % str(sending_button.objectName()))
        self.SenderActual= sending_button.objectName()
        return sending_button


    def defaultGUI(self):
        """
        Push this button to configure GUI with default values
        :return: GUI with default set
        """
        #
        self.ui_magsurf.JPNedit.setText('92504')
        self.ui_magsurf.timeEdit.setText('50')
        self.ui_magsurf.stepPsiEdit.setText('0.1')
        self.ui_magsurf.solEdit.setText('1') # cm
        self.ui_magsurf.NsolEdit.setText('5') # integer, nr of SOL lines
        self.ui_magsurf.coreEdit.setText('5') # integer, nr of CORE lines
        self.ui_magsurf.coreStepEdit.setText('0.1') # V/s
        #
        self.ui_magsurf.FW_CB.setChecked(True)
        self.ui_magsurf.GAP_CB.setChecked(True)
        self.ui_magsurf.SP_CB.setChecked(True)
        self.ui_magsurf.XLOC_CB.setChecked(True)
        self.ui_magsurf.WALLS_CB.setChecked(True)
        self.ui_magsurf.EFIT_CB.setChecked(True)
        #
        self.ui_magsurf.minSlider.setText('40s')
        self.ui_magsurf.maxSlider.setText('70s')
        self.ui_magsurf.actualSlider.setText('  ')
        self.ui_magsurf.configPlasma.setText('   ')
        self.ui_magsurf.timeXLOC_LB.setText('   ')
        self.ui_magsurf.timeWALLS_LB.setText('   ')
        self.ui_magsurf.timeEFIT_LB.setText('   ')
        #
        self.ui_magsurf.canvas.figure.clear()
        self.ui_magsurf.canvas.draw()

    def resetGUI(self):
        """
        Push this button to configure GUI with reset values
        :return: reset GUI values
        """
        self.ui_magsurf.JPNedit.setText(' ')
        self.ui_magsurf.timeEdit.setText(' ')
        self.ui_magsurf.stepPsiEdit.setText(' ')
        self.ui_magsurf.solEdit.setText(' ') # cm
        self.ui_magsurf.NsolEdit.setText(' ') # integer, nr of SOL lines
        self.ui_magsurf.coreEdit.setText(' ') # integer, nr of CORE lines
        self.ui_magsurf.coreStepEdit.setText(' ') # V/s
        self.ui_magsurf.timeXLOC_LB.setText('   ')
        self.ui_magsurf.timeWALLS_LB.setText('   ')
        self.ui_magsurf.timeEFIT_LB.setText('   ')
        #
        self.ui_magsurf.FW_CB.setChecked(False)
        self.ui_magsurf.GAP_CB.setChecked(False)
        self.ui_magsurf.SP_CB.setChecked(False)
        self.ui_magsurf.XLOC_CB.setChecked(False)
        self.ui_magsurf.WALLS_CB.setChecked(False)
        self.ui_magsurf.EFIT_CB.setChecked(False)
            #
        self.ui_magsurf.minSlider.setText(' ')
        self.ui_magsurf.maxSlider.setText(' ')
        self.ui_magsurf.actualSlider.setText('  ')
        self.ui_magsurf.configPlasma.setText('   ')
         #
        self.ui_magsurf.canvas.figure.clear()
        self.ui_magsurf.canvas.draw()



    def plotBoundaryFromSliderReleased(self,button):
        """

        :param button: slider button, while dragging it shows new time equilibria
        and plasma shape configuration
        :return:  plot on main canvs once slider released
        """

        JPNobj = self.ui_magsurf.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.ui_magsurf.plotParam['expDataDictJPNobj_EFIT']
        nameListGap = self.ui_magsurf.plotParam['nameListGap']
        nameListStrikePoints = self.ui_magsurf.plotParam['nameListStrikePoints']
        expDataDictJPNobj_XLOC = self.ui_magsurf.plotParam['expDataDictJPNobj_XLOC']
        expDataDictJPNobj_WALLS = self.ui_magsurf.plotParam['expDataDictJPNobj_WALLS']
        nameListGapWALLS = self.ui_magsurf.plotParam['nameListGapWALLS']
        offR_XLOC = self.ui_magsurf.plotParam['offR_XLOC']
        offZ_XLOC = self.ui_magsurf.plotParam['offZ_XLOC']
        time = self.ui_magsurf.plotParam['time']
        gapDict = self.ui_magsurf.plotParam['gapDict']
        xFW= self.ui_magsurf.plotParam['xFW']
        yFW= self.ui_magsurf.plotParam['yFW']
        rC= self.ui_magsurf.plotParam['rEFIT']
        zC= self.ui_magsurf.plotParam['zEFIT']
        rXLOC= self.ui_magsurf.plotParam['rBND_XLOC_smooth']
        zXLOC= self.ui_magsurf.plotParam['rzBND_XLOC_smooth']
        rP_XLOC= self.ui_magsurf.plotParam['rBND_XLOC']
        zP_XLOC= self.ui_magsurf.plotParam['zBND_XLOC']
        rXp = self.ui_magsurf.plotParam['rXp']
        zXp = self.ui_magsurf.plotParam['zXp']
        rSP = self.ui_magsurf.plotParam['rSP']
        zSP = self.ui_magsurf.plotParam['zSP']
        rWALLS   = self.ui_magsurf.plotParam['rBND_WALLS']
        zWALLS   = self.ui_magsurf.plotParam['zBND_WALLS']
        checkFW  = self.ui_magsurf.plotParam['checkFW']
        checkGAP = self.ui_magsurf.plotParam['checkGAP']
        checkSP  = self.ui_magsurf.plotParam['checkSP']
        checkXLOC = self.ui_magsurf.plotParam['checkXLOC']
        checkWALLS = self.ui_magsurf.plotParam['checkWALLS']
        checkEFIT = self.ui_magsurf.plotParam['checkEFIT']
        flagDiverted = self.ui_magsurf.plotParam['flagDiverted']


        if button.sliderReleased:
            print('PLOT @ time ---> ' + str(time[button.value()]))

            timeEquil = time[button.value()]

            rC,zC,\
            rXLOC,zXLOC,rP_XLOC,zP_XLOC, \
            rXp,zXp,rSP,zSP, flagDiverted, \
            rWALLS,zWALLS,iTWALLS,gapXLOC,spXLOC    = self.shapeSnapShot(JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC,nameListGapWALLS,expDataDictJPNobj_WALLS)

            if flagDiverted:
                self.ui_magsurf.configPlasma.setText('diverted')
            else:
                self.ui_magsurf.configPlasma.setText('limiter')


            self.plotFWGapBoundary(gapDict,xFW, yFW, rC,zC,
                          rXLOC,zXLOC, rP_XLOC, zP_XLOC, \
                          rXp,zXp,rSP,zSP, rWALLS,zWALLS,iTWALLS,  \
                        checkFW,checkGAP,checkSP,checkXLOC,checkWALLS,checkEFIT,\
                                      flagDiverted,nameListGapWALLS,gapXLOC,spXLOC)


    def plotFWGapBoundary(self,gapDict,xFW, yFW, rC,zC,
                          rXLOC,zXLOC, rP_XLOC, zP_XLOC, \
                          rXp,zXp,rSP,zSP,rWALLS,zWALLS,iTWALLS, \
                        flagPlotFW,flagPlotGap,flagPlotSP,flagPlotXLOC,\
                          flagPlotWALLS,flagPlotEFIT,flagDiverted,nameListGapWALLS,gapXLOC,spXLOC):
        """
        Plot: FW, XLOC gap and strike points geometry, XLOC boundary, EFIT boundary,
        WALLS gap (Inner,Outer and Upper)
        :param gapDict:
        :param xFW:
        :param yFW:
        :param rC:
        :param zC:
        :param rXLOC:
        :param zXLOC:
        :param rP_XLOC:
        :param zP_XLOC:
        :param rXp:
        :param zXp:
        :param rSP:
        :param zSP:
        :param rWALLS:
        :param zWALLS:
        :param iTWALLS:
        :param flagPlotFW:
        :param flagPlotGap:
        :param flagPlotSP:
        :param flagPlotXLOC:
        :param flagPlotWALLS:
        :param flagPlotEFIT:
        :param flagDiverted:
        :param nameListGapWALLS:
        :param gapXLOC:
        :param spXLOC:
        :return:
        """
        self.ui_magsurf.canvas.figure.clf() # clear canvas
        ax = self.ui_magsurf.canvas.figure.add_subplot(111)
        ax.plot()

        gapItems = gapXLOC.items() # return tupla
        minGAP = min(gapItems,key=lambda x:x[1])

        iTimeStart = numpy.where(min(gapXLOC.values()))


        nameListGap = []
        nameListSP  = []
        nameListGapSP = gapDict.keys()
        for jj in nameListGapSP:
                #print(jj)
                if ('RSOGB' in jj) or  ('RSIGB' in jj) or ('ZSIGB' in jj) \
                    or ('ZSOGB' in jj) or ('WLBSRP' in jj):
                    nameListSP.append(jj) # its a strike point      \zxdasdasasdas
                else:
                    nameListGap.append(jj) # its a gap


        #axPLT = plt.gca().axes
        # plot Gaps
        if flagPlotGap:
            for jj in nameListGap:
                R1 = gapDict[jj]['R1']
                Z1 = gapDict[jj]['Z1']
                R2 = gapDict[jj]['R2']
                Z2 = gapDict[jj]['Z2']
                ax.plot([R1,R2],[Z1,Z2],'d-r')
                ax.plot(R1,Z1,'o-b')


                # m = (y1-y2)/(x1-x2)
                # P2(x2,y2) starting point (from inside VACUUM), opposite to gap definition which start from FW
                # P1(x1,y1) ending point

                # angular coefficient
                if R2==R1:
                    mm= numpy.pi/2
                else:
                    mm = numpy.arctan((Z1-Z2)/(R1-R2))

                pt = np.array([R1,Z1]).reshape((1,2))
                gapAngle = numpy.degrees(mm)
                gapAngleCorr=ax.transData.transform_angles(np.array((gapAngle,)),pt)[0]

                    #numpy.arctan(mm*180/numpy.pi) # deg
                #print(gapDict[jj])
                #print([jj + ' : ' + str(gapAngle) + ' deg' + '---> corrected in : ' + str(gapAngleCorr) ])

                #gapAngle=gapAngleCorr

                sizeLabel = 7
                if jj in gapXLOC.keys():
                     if jj == minGAP[0]:
                        ax.text(R1,Z1,jj + ' (' + str(round(gapXLOC[jj],2)) + ')',color='g',\
                                fontsize=sizeLabel,weight='bold',rotation=gapAngle,rotation_mode='anchor')
                     elif gapXLOC[jj]<4.5e-2:
                         ax.text(R1,Z1,jj + ' (' + str(round(gapXLOC[jj],2)) + ')',\
                                 color='r',fontsize=sizeLabel,rotation=gapAngle,rotation_mode='anchor')
                     else:
                         ax.text(R1,Z1,jj + ' (' + str(round(gapXLOC[jj],2)) + ')',color='k',\
                                 fontsize=sizeLabel,rotation=gapAngle,rotation_mode='anchor')
                     # if 'TOG5' in jj:
                     #     if gapXLOC[jj]<4.5e-2:
                     #        ax.text(R1,Z1+0.1,jj + '(' + str(round(gapXLOC[jj],2)) + ')',color='r',\
                     #                fontsize=sizeLabel,rotation=gapAngle,rotation_mode='anchor')
                     #     else:
                     #        ax.text(R1,Z1+0.1,jj + ' (' + str(round(gapXLOC[jj],2)) + ')',color='k',\
                     #                fontsize=sizeLabel,rotation=gapAngle,rotation_mode='anchor')


        # plot strike points
        if flagPlotSP:
            for jj in nameListSP:
                R1 = gapDict[jj]['R1']
                Z1 = gapDict[jj]['Z1']
                R2 = gapDict[jj]['R2']
                Z2 = gapDict[jj]['Z2']
                R3 = gapDict[jj]['R3']
                Z3 = gapDict[jj]['Z3']
                R4 = gapDict[jj]['R4']
                Z4 = gapDict[jj]['Z4']

                ax.plot([R1,R2,R3,R4],[Z1,Z2,Z3,Z4],'-c')
                if jj in spXLOC.keys():
                    ax.text(R1,Z1,jj + ' (' + str(round(spXLOC[jj],2)) + ')',color='c',fontsize=sizeLabel)


        if flagPlotFW:
            # FW
            ax.plot(xFW,yFW,'k')

        if flagPlotEFIT:
             ax.plot(rC,zC,'-g',label='EFIT')

        if flagPlotXLOC:
            ax.plot(rXLOC,zXLOC,'-m',label='XLOC')
            ax.plot(rP_XLOC,zP_XLOC,'*m')
            if flagDiverted:
                ax.plot(rXp,zXp,'*c',markersize=16)
                ax.plot([rSP[0],rXp,rSP[2]],\
                                [zSP[0],zXp,zSP[2]],'*-m')

        if flagPlotWALLS:
            #ax.plot(rWALLS,zWALLS,'-b',label='WALLS')
            ax.plot(rWALLS,zWALLS,'*b')
            # for jj,vv in enumerate(nameListGapWALLS):
            #     ax.text(rWALLS[jj],zWALLS[jj],vv,color='b')

        if flagPlotGap or flagPlotSP or flagPlotFW or flagPlotXLOC or flagPlotEFIT:
            ax.axis('equal')
            self.ui_magsurf.canvas.draw()

    def slider_moved(self,position):
        time = self.ui_magsurf.plotParam['time']
        self.ui_magsurf.actualSlider.setText(str(time[position]))
        self.ui_magsurf.timeEdit.setText(str(time[position]))


        #position = self.ui_magsurf.horizontalSlider.value()

        if self.SenderActual=='runPB':
           print('clicked inside slider moved RUNPB')

           self.plotBoundaryFromSliderReleased(self.ui_magsurf.horizontalSlider)

        elif self.SenderActual=='isopsiPB':
            print('clicked inside slider moved RUNisopsi')

            self.plotIsoPsi(position)


        elif self.SenderActual=='isopsiFillPB':
            print('clicked inside slider moved RUNisopsiFill')

            self.plotIsoPsiFill(position)


        elif self.SenderActual=='solPB':
            print('clicked inside slider moved RUNSOLPSI')

            self.plotSol(position)

        elif self.SenderActual=='corePB':
            print('clicked inside slider moved RUNcorePSI')

            self.plotCore(position)

        #    self.ui_magsurf.runPB.released.connect(self.button_released)
        # self.ui_magsurf.isopsiPB.released.connect(self.button_released)
        # self.ui_magsurf.isopsiFillPB.released.connect(self.button_released)
        # self.ui_magsurf.solPB.released.connect(self.button_released)
        # self.ui_magsurf.corePB.released.connect(self.button_released)


    def downloadExpData(self,JPN,JPNobj):
        """
        download experimental data
        :param JPN:
        :param JPNobj:
        :return:
        """
          # #~~~~~~~~~~~~~~~EXP. DAT from XLOC, EFIT, SC ~~~~~~~~~~~~~~~~~~~~
        nameSignalsTable_XLOC = 'signalsTable_XLOC' #
        nameSignals_XLOC = STJET.signalsTableJET(nameSignalsTable_XLOC)
        expDataDictJPNobj_XLOC = JPNobj.download(JPN,nameSignalsTable_XLOC,nameSignals_XLOC,0)
        nameSignalsTable_WALLS = 'signalsTable_WALLS' #
        nameSignals_WALLS = STJET.signalsTableJET(nameSignalsTable_WALLS)
        expDataDictJPNobj_WALLS= JPNobj.download(JPN,nameSignalsTable_WALLS,\
                                                 nameSignals_WALLS,0)
        nameSignalsTable_EFIT = 'signalsTable_EFIT' #
        nameSignals_EFIT = STJET.signalsTableJET(nameSignalsTable_EFIT)
        expDataDictJPNobj_EFIT = JPNobj.download(JPN,nameSignalsTable_EFIT,nameSignals_EFIT,0)
        nameSignalsTable_SC   = 'signalsTable_SC' #
        nameSignals_SC = STJET.signalsTableJET(nameSignalsTable_SC)
        expDataDictJPNobj_SC = JPNobj.download(JPN,nameSignalsTable_SC,nameSignals_SC,0)
        # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        return expDataDictJPNobj_XLOC, expDataDictJPNobj_WALLS, \
               expDataDictJPNobj_EFIT, expDataDictJPNobj_SC



    def findIndexTime(self,tStart,tEnd,timeVector):

        iTimeStart = numpy.where(
            numpy.abs(tStart - timeVector) < 2 * min(numpy.diff(timeVector)))  # twice of the min of EFIT delta time
        timeStart = timeVector[iTimeStart[0][0]]
        iT_Start =  iTimeStart[0][0]

        if max(timeVector)<tEnd: # default 70s is too much, means darta acquired less than 70s
           tEnd = max(timeVector)
        iTimeEnd = numpy.where(
            numpy.abs(tEnd - timeVector) < 2 * min(numpy.diff(timeVector)))  # twice of the min of EFIT delta time
        timeEnd = timeVector[iTimeEnd[0][0]]
        iT_End = iTimeEnd[0][0]


        return iT_Start,timeStart,iT_End,timeEnd


    def readJETgeom(self,JPNobj):
        """

        :param JPNobj:
        :return:
        """
        gapFileName       = 'gapILW.csv'
        firstWallFileName = 'FWILW.csv'

        # no ZUP to avoid strange XLOC plot
        nameListGap = ['GAP32','GAP6','GAP31','GAP30','RIG','GAP29','GAP28','GAP7','GAP27','GAP26',\
                       'TOG1','GAP25','TOG2','TOG3','TOG4','GAP24','TOG5',\
                       'GAP2','GAP23','GAP3','GAP22','GAP21','GAP20','ROG','GAP19','GAP4','GAP18','LOG','GAP17']

        nameListStrikePoints = ['RSOGB','ZSOGB','RSIGB','ZSIGB']#,'WLBSRP']
        #nameListStrikePoints = ['ZSOGB','ZSIGB']#,'WLBSRP']

        nameListGapWALLS = ['IWLG01','IWLG02','IWLG03','IWLG04','IWLG05',\
                            'IWLG06','IWLG07','IWLG08','IWLG09','IWLG10',\
                            'IWLG11','IWLG12','IWLG13','IWLG14','IWLG15',\
                            'IWLG16','IWLG17','IWLG18','IWLG19',\
                            'UDPG01','UDPG02','UDPG03','UDPG04','UDPG05',\
                            'UDPG06','UDPG07','UDPG08',\
                            'WPLG01','WPLG02','WPLG03','WPLG04','WPLG05',\
                            'WPLG06','WPLG07','WPLG08','WPLG09','WPLG10',\
                            'WPLG11','WPLG12','WPLG13','WPLG14','WPLG15',\
                            'WPLG16','WPLG17','WPLG18','WPLG19','WPLG20',\
                            'WPLG21','WPLG22','WPLG23','WPLG24','WPLG25',\
                            'UDPG01','UDPG02','UDPG03','UDPG04','UDPG05',\
                            'UDPG06','UDPG07','UDPG08']

        # nameListGapWALLS = ['IWLGR01','IWLGR02','IWLGR03','IWLGR04','IWLGR05',\
        #                     'IWLGR06','IWLGR07','IWLGR08','IWLGR09','IWLGR10',\
        #                     'IWLGR11','IWLGR12','IWLGR13','IWLGR14','IWLGR15',\
        #                     'IWLGR16','IWLGR17','IWLGR18','IWLGR19',\
        #                     'IWLGZ01','IWLGZ02','IWLGZ03','IWLGZ04','IWLGZ05',\
        #                     'IWLGZ06','IWLGZ07','IWLGZ08','IWLGZ09','IWLGZ10',\
        #                     'IWLGZ11','IWLGZ12','IWLGZ13','IWLGZ14','IWLGZ15',\
        #                     'IWLGZ16','IWLGZ17','IWLGZ18','IWLGZ19',\
        #                     'WPLGR01','WPLGR02','WPLGR03','WPLGR04','WPLGR05',\
        #                     'WPLGR06','WPLGR07','WPLGR08','WPLGR09','WPLGR10',\
        #                     'WPLGR11','WPLGR12','WPLGR13','WPLGR14','WPLGR15',\
        #                     'WPLGR16','WPLGR17','WPLGR18','WPLGR19','WPLGR20',\
        #                     'WPLGR21','WPLGR22','WPLGR23','WPLGR24','WPLGR25',\
        #                     'WPLGZ01','WPLGZ02','WPLGZ03','WPLGZ04','WPLGZ05',\
        #                     'WPLGZ06','WPLGZ07','WPLGZ08','WPLGZ09','WPLGZ10',\
        #                     'WPLGZ11','WPLGZ12','WPLGZ13','WPLGZ14','WPLGZ15',\
        #                     'WPLGZ16','WPLGZ17','WPLGZ18','WPLGZ19','WPLGZ20',\
        #                     'WPLGZ21','WPLGZ22','WPLGZ23','WPLGZ24','WPLGZ25',\
        #                     'UDPGR01','UDPGR02','UDPGR03','UDPGR04','UDPGR05',\
        #                     'UDPGR06','UDPGR07','UDPGR08',\
        #                     'UDPGZ01','UDPGZ02','UDPGZ03','UDPGZ04','UDPGZ05',\
        #                     'UDPGZ06','UDPGZ07','UDPGZ08']

                            # First Wall
        xFW, yFW,= JPNobj.readFWFile(firstWallFileName)

        # Gap % Strike Points
        gapDict = JPNobj.readGapFile(gapFileName)

        return gapDict, xFW, yFW, nameListGap, nameListStrikePoints, nameListGapWALLS


    def shapeSnapShot(self,JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC,nameListGapWALLS,expDataDictJPNobj_WALLS):

         # EFIT
        rC,zC,psiEFIT,rGrid,zGrid,iTEFIT,timeEFIT = \
            JPNobj.readEFITFlux(expDataDictJPNobj_EFIT,float(timeEquil))

        self.ui_magsurf.timeEFIT_LB.setText(str(timeEFIT[iTEFIT]) + ' s' ) # display timeEquil closest time XLOC


        # find if diverted or limiter configuration
        ctype_v = expDataDictJPNobj_XLOC['CTYPE']['v']
        ctype_t = expDataDictJPNobj_XLOC['CTYPE']['t']

        iTimeX = numpy.where(
            numpy.abs(float(timeEquil) - ctype_t) < 2 * min(numpy.diff(ctype_t)))  # twice of the min of EFIT delta time

        iTimeXLOC = iTimeX[0][0]
        self.ui_magsurf.timeXLOC_LB.setText(str(ctype_t[iTimeXLOC]) + ' s' ) # display timeEquil closest time XLOC

        if ctype_v[iTimeXLOC]==-1: # diverted
            flagDiverted  = 1
        else:
            flagDiverted = 0


        # XLOC
        gapXLOC,rG,zG,iTXLOC  = JPNobj.gapXLOC(nameListGap,expDataDictJPNobj_XLOC,\
                                               gapDict,float(timeEquil))
        spXLOC,rSP,zSP,iTXLOC = JPNobj.strikePointsXLOC(nameListStrikePoints,\
                                expDataDictJPNobj_XLOC,gapDict,float(timeEquil))

        rX_XLOC = expDataDictJPNobj_XLOC['RX']['v']
        zX_XLOC = expDataDictJPNobj_XLOC['ZX']['v']

        rXp = rX_XLOC[iTXLOC]+offR_XLOC
        zXp = zX_XLOC[iTXLOC]+offZ_XLOC

        rBND_XLOC = []
        if flagDiverted:
            rBND_XLOC.append(rXp)
        for jj,vv in enumerate(rG):
            rBND_XLOC.append(rG[jj])
        if flagDiverted:
             rBND_XLOC.append(rXp)
        else:
            rBND_XLOC.append(rBND_XLOC[0])

        zBND_XLOC = []
        if flagDiverted:
            zBND_XLOC.append(zXp)
        for jj,vv in enumerate(zG):
            zBND_XLOC.append(zG[jj])
        if flagDiverted:
             zBND_XLOC.append(zXp)
        else:
            zBND_XLOC.append(zBND_XLOC[0])

        # connect  XLOC boundary points with a cubic
        # n = 10
        # i = numpy.arange(len(rBND_XLOC))
        # # Nx the original number of points
        # interp_i = numpy.linspace(0, i.max(), n  * i.max())
        # rBND_XLOC_smooth = interpolate.interp1d(i, rBND_XLOC, kind='cubic')(interp_i)
        # zBND_XLOC_smooth = interpolate.interp1d(i, zBND_XLOC, kind='cubic')(interp_i)

         # interpolate with splines
        tck,u = interpolate.splprep([rBND_XLOC,zBND_XLOC], s = 0)
        rBND_XLOC_smooth, zBND_XLOC_smooth \
            = interpolate.splev(np.linspace(0,1,1000),tck,der=0)

        # pylab.figure()
        # pylab.plot(rBND_XLOC,zBND_XLOC,'*m')
        # pylab.plot(rBND_XLOC_smooth, zBND_XLOC_smooth,'-b')
        # pylab.axis('equal')
        # pylab.show()

        rWALLS,zWALLS,iTWALLS  = JPNobj.gapWALLS(nameListGapWALLS,\
                                                 expDataDictJPNobj_WALLS,float(timeEquil))

        timeWALLS = expDataDictJPNobj_WALLS['IWLGR01']['t']
        self.ui_magsurf.timeWALLS_LB.setText(str(timeWALLS[iTWALLS]) + ' s')

        return  rC,zC,rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
                rXp,zXp,rSP,zSP,flagDiverted,rWALLS,zWALLS,iTWALLS,gapXLOC,spXLOC


    def plotCore(self,*args):
        position = self.ui_magsurf.horizontalSlider.value()


        core = int(self.ui_magsurf.coreEdit.text())
        coreStep = float(self.ui_magsurf.coreStepEdit.text())

        JPNobj = self.ui_magsurf.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.ui_magsurf.plotParam['expDataDictJPNobj_EFIT']

        time = self.ui_magsurf.plotParam['time']
        timeEquil = time[position]
        iCurrentTime = numpy.where(numpy.abs(timeEquil-time)<2*min(numpy.diff(time)))# twice of the min of EFIT delta time


        rC, zC, psiEFIT, rGrid, zGrid,iTEFIT,timeEFIT \
            = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT, float(timeEquil))
        psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))

        psiAxis = expDataDictJPNobj_EFIT['FAXS']['v']
        psiAxisEquil = psiAxis[iCurrentTime[0][0]]
        rMAG = expDataDictJPNobj_EFIT['RMAG']['v']
        rMAGEquil = rMAG[iCurrentTime[0][0]]
        zMAG = expDataDictJPNobj_EFIT['ZMAG']['v']
        zMAGEquil = zMAG[iCurrentTime[0][0]]

        coreStepPsi = float(self.ui_magsurf.coreStepEdit.text())
        psiMaxCore = psiAxisEquil+core*coreStepPsi
        psiCoreLevels = numpy.linspace(psiAxisEquil,psiMaxCore,core+1)

        #
        # pylab.figure()
        # pylab.plot(rMAGEquil,zMAGEquil,'*m')
        # pylab.contour(rGrid,zGrid,psiGrid,psiCoreLevels,colors = 'm')
        # pylab.axis('equal')
        # pylab.show()


        self.ui_magsurf.canvas.figure.clf() # clear canvas
        ax = self.ui_magsurf.canvas.figure.add_subplot(111)
        ax.plot()

        xFW = self.ui_magsurf.plotParam['xFW']
        yFW = self.ui_magsurf.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')

        #pylab.plot(rGrid,zGrid,'.b')
        ax.plot(rMAGEquil,zMAGEquil,'*m')
        CS = ax.contour(rGrid,zGrid,psiGrid,psiCoreLevels,colors = 'r')
        ax.clabel(CS,inline = 1,fontsize= 10)
        ax.axis('equal')
        self.ui_magsurf.canvas.draw()


    def plotSol(self,*args):
        position = self.ui_magsurf.horizontalSlider.value()

        sol = float(self.ui_magsurf.solEdit.text())
        Nsol = int(self.ui_magsurf.NsolEdit.text())

        JPNobj = self.ui_magsurf.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.ui_magsurf.plotParam['expDataDictJPNobj_EFIT']

        time = self.ui_magsurf.plotParam['time']
        timeEquil = time[position]

        rC, zC, psiEFIT, rGrid, zGrid,iTEFIT,timeEFIT \
            = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT, float(timeEquil))
        psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))

        FBND_v = expDataDictJPNobj_EFIT['FBND']['v']
        FBND_t = expDataDictJPNobj_EFIT['FBND']['t']

        iCurrentTime = numpy.where(numpy.abs(timeEquil-time)<2*min(numpy.diff(time)))# twice of the min of EFIT delta time

        FBND_exp = FBND_v[iCurrentTime[0][0]]

        iMax = np.argmax(rC)

        rMidPlaneSOL = []
        rMidPlaneSOL.append(rC[iMax])
        zMidPlaneSOL = []
        zMidPlaneSOL.append(zC[iMax])

        X0 = rMidPlaneSOL[0]
        Z0 = zMidPlaneSOL[0]
        points = np.array( (rGrid.flatten(),zGrid.flatten()) ).T
        values = psiEFIT
        psiB = interpolate.griddata(points,values,(X0,Z0))


        print('PSI @ boundary EXP:' + str(FBND_exp) + '   REC: ' +  str(psiB) )
        psiSOL = []
        for jj in np.arange(0,Nsol+1):
            X0tmp = rC[iMax]+sol*jj/1e2
            Z0tmp = zC[iMax]
            rMidPlaneSOL.append(X0tmp)
            zMidPlaneSOL.append(Z0tmp)
            psiSOL.append(interpolate.griddata(points,values,(X0tmp,Z0tmp)))
        #
        # pylab.figure()
        # pylab.plot(rC,zC)
        # pylab.plot(rC[iMax],zC[iMax],'*b')
        # pylab.plot(rMidPlaneSOL,zMidPlaneSOL,'or')
        # pylab.contour(rGrid,zGrid,psiGrid,psiSOL,colors = 'm')
        # pylab.axis('equal')
        # pylab.show()

        self.ui_magsurf.canvas.figure.clf() # clear canvas
        ax = self.ui_magsurf.canvas.figure.add_subplot(111)
        ax.plot()

        xFW = self.ui_magsurf.plotParam['xFW']
        yFW = self.ui_magsurf.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')

        ax.plot(rC,zC)
        ax.plot(rC[iMax],zC[iMax],'*b')
        ax.plot(rMidPlaneSOL,zMidPlaneSOL,'or')
        #ax.plot(rGrid,zGrid,'.b')
        ax.contour(rGrid,zGrid,psiGrid,psiSOL,colors = 'm')
        ax.axis('equal')
        self.ui_magsurf.canvas.draw()


    def plotIsoPsi(self,*args):

        position = self.ui_magsurf.horizontalSlider.value()
        JPNobj = self.ui_magsurf.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.ui_magsurf.plotParam['expDataDictJPNobj_EFIT']

        time = self.ui_magsurf.plotParam['time']
        timeEquil = time[position]

        deltaPsi = float(self.ui_magsurf.stepPsiEdit.text())

        rC, zC, psiEFIT, rGrid, zGrid,iTEFIT,timeEFIT \
            = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT, float(timeEquil))

        # rGrid = self.ui_magsurf.plotParam['rGrid']
        # zGrid = self.ui_magsurf.plotParam['zGrid']
        # psiGrid = self.ui_magsurf.plotParam['psiGrid']
        # psiEFIT = self.ui_magsurf.plotParam['psiEFIT']

        psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))
        # deltaPsi = 0.1 # step of 0.1V/s
        psiLevels = numpy.arange(numpy.min(psiEFIT),numpy.max(psiEFIT),deltaPsi)

        self.ui_magsurf.canvas.figure.clf() # clear canvas
        ax = self.ui_magsurf.canvas.figure.add_subplot(111)
        ax.plot()

        xFW = self.ui_magsurf.plotParam['xFW']
        yFW = self.ui_magsurf.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')

        #pylab.plot(rGrid,zGrid,'.b')
        CS = ax.contour(rGrid,zGrid,psiGrid,psiLevels,colors = 'r')
        ax.clabel(CS,inline = 1,fontsize= 10)
        ax.axis('equal')
        self.ui_magsurf.canvas.draw()


    def plotIsoPsiFill(self,*args):

        position = self.ui_magsurf.horizontalSlider.value()


        JPNobj = self.ui_magsurf.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.ui_magsurf.plotParam['expDataDictJPNobj_EFIT']

        time = self.ui_magsurf.plotParam['time']
        timeEquil = time[position]

        deltaPsi = float(self.ui_magsurf.stepPsiEdit.text())

        rC, zC, psiEFIT, rGrid, zGrid ,iTEFIT,timeEFIT \
            = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT, float(timeEquil))

        # rGrid = self.ui_magsurf.plotParam['rGrid']
        # zGrid = self.ui_magsurf.plotParam['zGrid']
        # psiGrid = self.ui_magsurf.plotParam['psiGrid']
        # psiEFIT = self.ui_magsurf.plotParam['psiEFIT']

        psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))
        # deltaPsi = 0.1 # step of 0.1V/s
        psiLevels = numpy.arange(numpy.min(psiEFIT),numpy.max(psiEFIT),deltaPsi)

        self.ui_magsurf.canvas.figure.clf() # clear canvas
        ax = self.ui_magsurf.canvas.figure.add_subplot(111)
        plt.subplots_adjust(bottom=0.1,right= 0.9,top=0.9)
        cax = plt.axes([0.85,0.1,0.075,0.8])
        #cax = self.ui_magsurf.canvas.figure.add_subplot(144)

        ax.plot()

        xFW = self.ui_magsurf.plotParam['xFW']
        yFW = self.ui_magsurf.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')


        CS = ax.contourf(rGrid,zGrid,psiGrid,psiLevels,cmap=cm.hot)
        cbar = plt.colorbar(CS,cax,ax,cmap=psiLevels)
        cbar.ax.tick_params(labelsize=5)
        ax.axis('equal')
        self.ui_magsurf.canvas.draw()



    def goMagSurfGA(self):

        # center of divertor
        offR_XLOC = 2.6780
        offZ_XLOC = -1.7120

        # XLOC
        tStartXLOC = 39.7
        tEndXLOC = 70

        # EFIT
        tStartEFIT = 40.25
        tEndEFIT = 70

        # READ from INTERFACE ~~~~~~~~~~~~~~~~~~~~~~~~
        JPN = self.ui_magsurf.JPNedit.text()
        timeEquil = self.ui_magsurf.timeEdit.text()

        checkFW   = self.ui_magsurf.FW_CB.isChecked()
        checkGAP  = self.ui_magsurf.GAP_CB.isChecked()
        checkSP = self.ui_magsurf.SP_CB.isChecked()
        checkXLOC = self.ui_magsurf.XLOC_CB.isChecked()
        checkWALLS = self.ui_magsurf.WALLS_CB.isChecked()
        checkEFIT = self.ui_magsurf.EFIT_CB.isChecked()

        JPNobj = MAGTool(JPN)

        print(JPN + '@' + timeEquil + 's')
        if self.ui_magsurf.XLOC_CB.isChecked():
            print('Plot XLOC')
        if self.ui_magsurf.EFIT_CB.isChecked():
            print('Plot EFIT')

        # READ JET GEOMETRY FW anf GAPS
        gapDict, xFW, yFW, nameListGap, nameListStrikePoints, nameListGapWALLS = \
            self.readJETgeom(JPNobj)

        # RETREIVE EXP DATA
            # treat with PICKLE
        expDataDictJPNobj_XLOC, expDataDictJPNobj_WALLS, \
        expDataDictJPNobj_EFIT, expDataDictJPNobj_SC = \
            self.downloadExpData(JPN,JPNobj)

        timeXLOC = expDataDictJPNobj_XLOC['ROG']['t']
        timeEFIT = expDataDictJPNobj_EFIT['PSI']['t']
        timeWALLS = expDataDictJPNobj_WALLS['IWLGR01']['t']


        self.ui_magsurf.plotParam['JPNobj'] = JPNobj
        self.ui_magsurf.plotParam['expDataDictJPNobj_EFIT'] = expDataDictJPNobj_EFIT
        self.ui_magsurf.plotParam['nameListGap'] = nameListGap
        self.ui_magsurf.plotParam['nameListStrikePoints'] = nameListStrikePoints
        self.ui_magsurf.plotParam['expDataDictJPNobj_XLOC'] = expDataDictJPNobj_XLOC
        self.ui_magsurf.plotParam['expDataDictJPNobj_WALLS'] = expDataDictJPNobj_WALLS
        self.ui_magsurf.plotParam['nameListGapWALLS'] = nameListGapWALLS
        self.ui_magsurf.plotParam['offR_XLOC'] = offR_XLOC
        self.ui_magsurf.plotParam['offZ_XLOC'] = offZ_XLOC


        rEFIT,zEFIT,\
        rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
        rXp,zXp,rSP,zSP, flagDiverted,\
        rWALLS,zWALLS,iTWALLS,gapXLOC,spXLOC    = self.shapeSnapShot(JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC,nameListGapWALLS,expDataDictJPNobj_WALLS)

        self.ui_magsurf.plotParam['time'] = timeEFIT
        self.ui_magsurf.plotParam['gapDict'] = gapDict
        self.ui_magsurf.plotParam['xFW'] = xFW
        self.ui_magsurf.plotParam['yFW'] = yFW
        self.ui_magsurf.plotParam['rEFIT'] = rEFIT
        self.ui_magsurf.plotParam['zEFIT'] = zEFIT
        self.ui_magsurf.plotParam['rBND_XLOC_smooth'] = rBND_XLOC_smooth
        self.ui_magsurf.plotParam['rzBND_XLOC_smooth'] = zBND_XLOC_smooth
        self.ui_magsurf.plotParam['rBND_XLOC'] = rBND_XLOC
        self.ui_magsurf.plotParam['zBND_XLOC'] = zBND_XLOC
        self.ui_magsurf.plotParam['rXp'] = rXp
        self.ui_magsurf.plotParam['zXp'] = zXp
        self.ui_magsurf.plotParam['rSP'] = rSP
        self.ui_magsurf.plotParam['zSP'] = zSP
        self.ui_magsurf.plotParam['checkFW'] = checkFW
        self.ui_magsurf.plotParam['checkGAP'] = checkGAP
        self.ui_magsurf.plotParam['checkSP']  = checkSP
        self.ui_magsurf.plotParam['checkXLOC'] = checkXLOC
        self.ui_magsurf.plotParam['checkWALLS'] = checkWALLS
        self.ui_magsurf.plotParam['checkEFIT'] = checkEFIT
        self.ui_magsurf.plotParam['flagDiverted'] = flagDiverted

        #
        # rGrid = expDataDictJPNobj_EFIT['rGrid']
        # zGrid = expDataDictJPNobj_EFIT['zGrid']
        # psiGrid = expDataDictJPNobj_EFIT['psiGrid']
        # psiEFIT = expDataDictJPNobj_EFIT['psiEFIT']
        #
        # self.ui_magsurf.plotParam['rGrid'] = rGrid
        # self.ui_magsurf.plotParam['zGrid'] = zGrid
        # self.ui_magsurf.plotParam['psiGrid'] = psiGrid
        # self.ui_magsurf.plotParam['psiEFIT'] = psiEFIT



        self.plotFWGapBoundary(gapDict,xFW, yFW,rEFIT,zEFIT,\
                        rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
                        rXp,zXp,rSP,zSP,\
                        rWALLS,zWALLS,iTWALLS,\
                        checkFW,checkGAP,checkSP,checkXLOC,checkWALLS,checkEFIT,\
                                  flagDiverted,nameListGapWALLS,gapXLOC,spXLOC)


        iT_Start,timeStart,iT_End,timeEnd = \
            self.findIndexTime(tStartEFIT,tEndEFIT,timeEFIT)


        # #self.updateSlider(iT_Start,iT_End,timeEquil,timeEFIT)
        self.ui_magsurf.horizontalSlider.setMinimum(iT_Start)
        self.ui_magsurf.horizontalSlider.setMaximum(iT_End)
        self.ui_magsurf.minSlider.setText(str(timeStart)) # from PSI EFIT time
        self.ui_magsurf.maxSlider.setText(str(timeEnd))  # from PSI EFIT time
        self.ui_magsurf.actualSlider.setText(str(timeEquil))
        iPosition = numpy.where(
            numpy.abs(float(timeEquil) - timeEFIT) < 2 * min(numpy.diff(timeEFIT)))  # twice of the min of EFIT delta time=
        self.ui_magsurf.horizontalSlider.setSliderPosition(iPosition[0][0])
        print('pos: ' + str(iPosition[0][0])  + \
              ' ---> time ' + str(timeEFIT[iPosition[0][0]]))
        lenSamples = numpy.round((self.ui_magsurf.horizontalSlider.maximum()\
                                  -self.ui_magsurf.horizontalSlider.minimum())/10)
        self.ui_magsurf.horizontalSlider.setTickPosition(2)
        self.ui_magsurf.horizontalSlider.setTickInterval(lenSamples)


        # freqXLOC = int(numpy.max(1/numpy.diff(timeXLOC)))
        # freqEFIT = int(numpy.max(1/numpy.diff(timeEFIT)))






        # sampling frequency
        # pylab.figure()
        # pylab.plot(timeXLOC[0:-1],1/numpy.diff(timeXLOC),label='XLOC')
        # pylab.plot(timeEFIT[0:-1],1/numpy.diff(timeEFIT),label='EFIT')
        # pylab.legend(loc='best',prop={'size':12})
        # pylab.show()

        # plot CTYPE
        # pylab.figure()
        # pylab.plot(expDataDictJPNobj_XLOC['CTYPE']['t'],expDataDictJPNobj_XLOC['CTYPE']['v'],label='XLOC CTYPE')
        # pylab.show()
        #







############################################


    # ---------------------------
    def selectstandardset(self):


        self.JSONSS, ddd = QFileDialog.getOpenFileName(
            None, "Select Standard set", "./standard_set", "JSON Files(*.json)"
        )

        self.JSONSS = os.path.basename(self.JSONSS)

        os.chdir(self.home)
        return self.JSONSS



    # ---------------------------
    def plotdata(self):
        pulselist = self.ui_plotdata.textEdit_pulselist.toPlainText()
        pulselist = pulselist.split(',')

        search_window = self.ui_plotdata.search_window.toPlainText()
        search_window = search_window.split(",")


        if isBlank(search_window[0]):
            start_value = None
            stop_value = None
        else:

            start_value = float(search_window[0])

        if len(search_window) > 1:
            try:
                stop_value = float(search_window[1])
            except:
                stop_value = None


        if self.ui_plotdata.savefigure_checkBox.isChecked():
            save = True
        else:
            save = False

        if self.ui_plotdata.smooth_checkBox.isChecked():
            smooth = True
        else:
            smooth = False
        if self.ui_plotdata.calcmean_checkBox.isChecked():
            calc_mean = True
        else:
            calc_mean = False
        # pulselist = pulselist.rstrip()

        pulselist = [int(i) for i in pulselist]
        # pulselist = list(map(int, pulselist))
        # colorlist = self.ui_plotdata.textEdit_colorlist.toPlainText()
        # colorlist = colorlist.split(',')
        # colorlist = colorlist.rstrip()

        inputlist = []
        for i,j in enumerate(pulselist):
            # print(i,j)
            # inputlist.append([pulselist[i],colorlist[i].strip()])
            inputlist.append([pulselist[i]])
        #
        #
        # if self.owner =='bviola':
        #     os.chdir("/u/"
        #     + self.owner
        #     + "/"
        #     + self.basefolder
        #     + "/"
        #     + self.installationfolder
        #     +"/Python/kg1_tools/kg1_tools_gui')

        plot_time_traces(self.JSONSS, inputlist, save=save, smooth=smooth,
                         calc_mean=calc_mean, start_value=start_value,
                         stop_value=stop_value)

        #plt.show(block=True)
        if self.owner == 'bviola':
            os.chdir(self.home)




    # ----------------------------
    def handle_exit_button(self):
        """
        Exit the application
        """
        logger.info('\n')
        logger.info('Exit now')
        sys.exit()



    def handle_add_sim(self):

        folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder
        # print(self.seq)
        simul = sim(self.shot,self.date,(self.seq.split('#')[1]),folder,self.user)
        name='/'.join([self.owner,self.shot, self.date,self.seq.split('#')[1]])
        label = self.ui_edge2d.lineEdit_var_3.text()
        if name in self.namelist:
            pass
        else:


            self.ui_edge2d.textEdit_message.append(
                str(name))

            self.namelist.append(name)
            self.simlist.append([simul,label])


            # self.ui_edge2d.textEdit_message.setText(name)


    def handle_run(self):
        if not self.ui_edge2d.textEdit_message2.toPlainText():
            logger.error('Attempt to run without selecting an input dictionary')
        self.inputJson = self.ui_edge2d.textEdit_message2.toPlainText()
        # jsonlist=[]
        # jsonlist.append(self.inputJson)
        # for i,j in enumerate(jsonlist):
        dictionary = self.inputJson.split(',')
        # dictionary =   self.inputJson
        self.variable = self.ui_edge2d.lineEdit_var.text().split(',')

        self.location = self.ui_edge2d.lineEdit_var_2.text().split(',')



        # print(dictionary[0],var, loc)
        # for i,j in enumerate(dictionary):
        #     print(i,j)
        folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder
        os.chdir(folder)
        # print(os.curdir)
        # print(dictionary[0])
        # if len(dictionary) ==1:
        #     shot.compare_multi_shots_simdata(dictionary[0], ms=None,lw=None, var=var, loc=loc)
        # else:
        for i,dicti in enumerate(dictionary):
            for j,vari in enumerate(self.variable):
                for t, loca in enumerate(self.location):
                    logger.info(
                        'plotting {} profiles at {}'.format(str(vari), str(loca)))
                    shot.compare_multi_shots_simdata(dicti, ms=None, lw=None,
                                             var=vari, loc=loca)

        # shot.compare_multi_shots_simdata('input_dict_84600.json', ms=None,lw=None, var='denel', loc='ot')
        plt.show(block=True)
        os.chdir(self.workfold)


    def handle_runanalyze_button(self):
        folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder
        if self.ui_edge2d.enablecompare_check.isChecked() == False:
            logger.debug('running edge2d_analyze on {}'.format(self.JSONSS1))

            os.chdir(folder)
            # os.system(
            #     'run_edge2danalysis.py  {} -d 0'.format(self.JSONSS1))
            subprocess.Popen('run_edge2danalysis.py  {} -d 0'.format(self.JSONSS1), shell=True)
            os.chdir(self.home)
        if self.ui_edge2d.enablecompare_check.isChecked() ==  True:
            logger.debug('running edge2d_analyze on {} and {}'.format(self.JSONSS1, self.JSONSS2))

            os.chdir(folder)
            # os.system(
                # 'run_edge2danalysis.py  {} --input_dict2 {} -d 0'.format(self.JSONSS1,self.JSONSS2))
            subprocess.Popen(
                'run_edge2danalysis.py  {} --input_dict2 {} -d 0'.format(self.JSONSS1,self.JSONSS2), shell=True)
            os.chdir(self.home)



    # ----------------------------
    def checkprintstate(self, button):
        """
        option to compare pulse reading a second JSON

        """
        if button.isChecked() == True:
            self.ui_edge2d.select_json2.setEnabled(True)
            self.ui_edge2d.lineEdit_2nd.setEnabled(True);
        else:
            self.ui_edge2d.select_json2.setEnabled(False)
            self.ui_edge2d.lineEdit_2nd.setEnabled(False);


    def checkstateJSON(self, button):
        folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder
        if button.isChecked() == True:
            if button.text() == "edit JSON1":

                # os.system('kate {}'.format(self.edge2dfold+'/'+self.JSONSS1))
                subprocess.Popen('atom {}'.format(folder+'/'+self.JSONSS1), shell=True)

                self.ui_edge2d.edit_JSON1.setChecked(False)
            if button.text() == "edit JSON2":
                # os.system('kate {}'.format(self.edge2dfold+'/'+self.JSONSS2))
                subprocess.Popen('atom {}'.format(folder+'/'+self.JSONSS2), shell=True)
                self.ui_edge2d.edit_JSON2.setChecked(False)

            if button.isChecked() == True:
                if button.text() == "edit_JSON":
                    # os.system(
                    #     'kate {}'.format('/work/bviola/Python/kg1_tools/kg1_tools_gui/standard_set/'+ self.JSONSS))

                    subprocess.Popen('atom {}'.format(folder+ self.JSONSS), shell=True)
                    self.ui_plotdata.checkBox.setChecked(False)



    def handle_selectjson1(self):
        folder = self.homefold + os.sep+ self.basefolder+os.sep+ self.installationfolder
        self.JSONSS1, _filter = QFileDialog.getOpenFileName(None,'Select PULSE JSON',folder,'JSON Files(*.json)')
        if not self.JSONSS1=='':
            self.JSONSS1 = os.path.basename(self.JSONSS1)
            self.ui_edge2d.lineEdit_1st.setText(self.JSONSS1)

            logger.debug('you have chosen {}'.format(self.JSONSS1))
            os.chdir(self.home)
            return self.JSONSS1

    def handle_selectjson2(self):
        folder = self.homefold + os.sep + self.basefolder + os.sep + self.installationfolder
        self.JSONSS2, _filter = QFileDialog.getOpenFileName(None,'Select PULSE JSON',folder,'JSON Files(*.json)')
        if not self.JSONSS2=='':
            self.JSONSS2 = os.path.basename(self.JSONSS2)
            self.ui_edge2d.lineEdit_2nd.setText(self.JSONSS2)
            logger.debug('you have chosen {}'.format(self.JSONSS2))
            os.chdir(self.home)
            return self.JSONSS2

    def getsimnames(self):
        import eproc as ep


        logger.info('here are the variables stored in the tran file of the selected simulation')
        if self.ui_edge2d.checkBox_profile.isChecked() == True:
            if self.PathTranfile is None:
                logger.error('choose a simulation first')
            else:

                names = ep.names(self.PathTranfile, 1, 0, 0, 0)
        if self.ui_edge2d.checkBox_time.isChecked() == True:
            if self.PathTranfile is None:
                logger.error('choose a simulation first')
            else:
                names = ep.names(self.PathTranfile, 0, 1, 0, 0)
        if self.ui_edge2d.checkBox_flux.isChecked() == True:
            if self.PathTranfile is None:
                logger.error('choose a simulation first')
            else:
                names = ep.names(self.PathTranfile, 0, 0, 1, 0)
        if self.ui_edge2d.checkBox_geom.isChecked() == True:
            if self.PathTranfile is None:
                logger.error('choose a simulation first')
            else:
                names = ep.names(self.PathTranfile, 0, 0, 0, 1)

        if (self.ui_edge2d.checkBox_profile.isChecked() == False &
            self.ui_edge2d.checkBox_time.isChecked() == False &
            self.ui_edge2d.checkBox_flux.isChecked() == False &
            self.ui_edge2d.checkBox_geom.isChecked() == False ):
            if self.PathTranfile is None:
                logging.error('choose a simulation first')
            else:
                names = ep.names(self.PathTranfile, 1, 1, 1, 1)








    def ScanName(self,i):
            self.user = self.ui_edge2d.comboBox_Name.itemText(i)
            self.Name =  self.PathCatalog +"/"+self.ui_edge2d.comboBox_Name.itemText(i)+"/cmg/catalog/edge2d"
            fsm = QFileSystemModel()
            index = fsm.setRootPath(self.Name)
            self.ui_edge2d.comboBox_Machine.setModel(fsm)
            self.ui_edge2d.comboBox_Machine.setRootModelIndex(index)
    # def ProgramE2dFunc(self,i):
    #         self.Name4 =  self.Name +"/"+self.ProgramE2d.itemText(i)
    #         fsm = QFileSystemModel()()()()
    #         index = fsm.setRootPath(self.Name4)
    #         self.Machine.setModel(fsm)
    #         self.Machine.setRootModelIndex(index)
    def MachineFunc(self,i):
            self.machine = self.ui_edge2d.comboBox_Machine.itemText(i)
            self.Name5 =  self.Name +"/"+self.ui_edge2d.comboBox_Machine.itemText(i)
            fsm = QFileSystemModel()
            index = fsm.setRootPath(self.Name5)
            self.ui_edge2d.comboBox_Shot.setModel(fsm)
            self.ui_edge2d.comboBox_Shot.setRootModelIndex(index)
    def ShotFunc(self,i):
            self.shot = self.ui_edge2d.comboBox_Shot.itemText(i)
            self.Name6 =  self.Name5 +"/"+self.ui_edge2d.comboBox_Shot.itemText(i)
            fsm = QFileSystemModel()
            index = fsm.setRootPath(self.Name6)
            self.ui_edge2d.comboBox_Date.setModel(fsm)
            self.ui_edge2d.comboBox_Date.setRootModelIndex(index)
    def DatagFunc(self,i):
            self.date = self.ui_edge2d.comboBox_Date.itemText(i)
            self.Name7 =  self.Name6 +"/"+self.ui_edge2d.comboBox_Date.itemText(i)
            fsm = QFileSystemModel()
            index = fsm.setRootPath(self.Name7)
            self.ui_edge2d.comboBox_Seq.setModel(fsm)
            self.ui_edge2d.comboBox_Seq.setRootModelIndex(index)
    def SeqFunc(self,i):
            self.seq = self.ui_edge2d.comboBox_Seq.itemText(i)
            # if self.seq != '/':
            #     self.seq =self.seq.split('#')[1]
            self.Name8 =  self.Name7 +"/"+self.seq
            if self.ui_edge2d.comboBox_Seq.itemText(i) != "/":
                self.PathTranfile = self.Name8+'/tran'
            # print(self.seq)


# ----------------------------
# Custom formatter
class MyFormatter(logging.Formatter):
    """
    class to handle the logging formatting
    """
    err_fmt = "%(levelname)-8s %(message)s"
    dbg_fmt = "%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    info_fmt = "%(levelname)-8s %(message)s"

    # def __init__(self):
    #     super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = MyFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result



def main():
    """
    Main function

    the only input to the GUI is the debug

    by default is set to INFO
    """
    logger.info("Running bruvio tool.")
    import sys
    app = QApplication(sys.argv)
    MainWindow = bruvio_tool()
    MainWindow.show()
    app.exec_()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run GO_bruvio_tools')
    parser.add_argument("-d", "--debug", type=int,
                        help="Debug level. 0: Info, 1: Warning, 2: Debug,"
                             " 3: Error, 4: Debug Plus; \n default level is INFO",
                        default=0)
    # parser.add_argument("-d", "--debug", type=int,
    #                     help="Debug level. 0: Info, 1: Warning, 2: Debug,"
    #                         " 3: Error; \n default level is INFO", default=2)
    parser.add_argument("-doc", "--documentation", type=str,
                        help="Make documentation. yes/no", default='no')



    args = parser.parse_args(sys.argv[1:])
    # debug_map = {0: logging.INFO,
    #             1: logging.WARNING,
    #             2: logging.DEBUG,
    #             3: logging.ERROR}
    #
    # logger = logging.getLogger(__name__)
    # fmt = MyFormatter()
    # hdlr = logging.StreamHandler(sys.stdout)
    #
    # hdlr.setFormatter(fmt)
    # logging.root.addHandler(hdlr)
    #
    # logging.root.setLevel(level=debug_map[args.debug])
    # main()

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
    main()
