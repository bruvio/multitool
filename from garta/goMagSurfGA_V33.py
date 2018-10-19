__author__ = 'garta'
# v.1 21.06.2018
# Boundary XLOC vs EFIT and linked with slider movement-release
# v.2 27.06.2018
# Implemented distinguish Diverter and limiter configuration
# Implemented Isopsi as stand alone button which work after the user
# press run and after release slider
# v.3 28.06.2018
# reset,default,exit buttons
# wrong XLOC interpolation, used cubic
#  v.3.1 29.06.2018
# Plot SOL (scrape off length) for single shot MagSurf tool (V3)
# plot core isopsi  3.07.2018
# plot WALLS 3.07.2018
# 05.07.2018:fixed XLOC interpolation points as continuos curve (used splines instead of cubic method)
# v.3.3 19.07.2018
# Plot equilibria not only when slider released but also when dragged as XLOC control room

import numpy as np
from PyQt4 import QtGui, QtCore
import magSurfGAV33
import sys
import matplotlib.gridspec as gridspec
from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from scipy import interpolate
from MAGTool import * # Magnetics Tool
import pyqtgraph as pg


class MagSurf(QtGui.QMainWindow, magSurfGAV33.Ui_MainWindow):
    """
    Class for running the GUI and handling events.

    """
    #----------------------------
    def __init__(self, parent=None):
        """
        Setup the GUI, and connect the buttons to functions.
        """
        super(MagSurf, self).__init__(parent)
        self.setupUi(self)
        toolBar = NavigationToolbar(self.canvas, self)
        self.addToolBar(toolBar)
        toolBarZoom = NavigationToolbar(self.canvasZoom, self)
        #optionToolBarZoom = QtGui.QStyleOptionToolBar.Middle
        self.addToolBar(toolBarZoom)
        #toolBarZoom.QStyleOptionToolBar.Middle




        #
        self.runPB.clicked.connect(self.goMagSurfGA)
        self.isopsiPB.clicked.connect(self.plotIsoPsi)
        self.isopsiFillPB.clicked.connect(self.plotIsoPsiFill)
        self.solPB.clicked.connect(self.plotSol)
        self.corePB.clicked.connect(self.plotCore)
        #
        self.JPNedit.setText('92504')
        self.timeEdit.setText('50') # s
        self.stepPsiEdit.setText('0.1') # V/s
        self.solEdit.setText('1') # cm
        self.NsolEdit.setText('5') # integer, nr of SOL lines
        self.coreEdit.setText('5') # integer, nr of CORE lines
        self.coreStepEdit.setText('0.1') # V/s
       #
        self.FW_CB.setChecked(True)
        self.GAP_CB.setChecked(True)
        self.GAP_CB.setStyleSheet("color:red")
        self.XLOC_CB.setChecked(True)
        self.XLOC_CB.setStyleSheet("color:magenta")
        self.WALLS_CB.setChecked(True)
        self.WALLS_CB.setStyleSheet("color:blue")
        self.EFIT_CB.setChecked(True)
        self.EFIT_CB.setStyleSheet("color:green")
        #
        self.minSlider.setText('40s')
        self.maxSlider.setText('70s')
        self.actualSlider.setText('  ')
        self.configPlasma.setText('   ')
        self.timeXLOC_LB.setText('   ')
        self.timeWALLS_LB.setText('   ')
        self.timeEFIT_LB.setText('   ')
        #
        self.resetPB.clicked.connect(self.resetGUI)
        self.defaultPB.clicked.connect(self.defaultGUI)
        self.exitPB.clicked.connect(self.exitGUI)
        #

        self.plotParam = {
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
            'checkXLOC' : None,
            'checkWALLS':None,
            'checkEFIT' : None,
            'flagDiverted' :  None,
            'rGrid': None,
            'zGrid': None,
            'psiGrid': None,
            'psiEFIT':None
        }


        self.horizontalSlider.valueChanged.connect(self.slider_moved)
        self.horizontalSlider.sliderReleased.connect(
           lambda: self.plotBoundaryFromSliderReleased(self.horizontalSlider))


    def defaultGUI(self):
        """
        Push this button to configure GUI with default values
        :return: GUI with default set
        """
        #
        self.JPNedit.setText('92504')
        self.timeEdit.setText('50')
        self.stepPsiEdit.setText('0.1')
        self.solEdit.setText('1') # cm
        self.NsolEdit.setText('5') # integer, nr of SOL lines
        self.coreEdit.setText('5') # integer, nr of CORE lines
        self.coreStepEdit.setText('0.1') # V/s
        #
        self.FW_CB.setChecked(True)
        self.GAP_CB.setChecked(True)
        self.XLOC_CB.setChecked(True)
        self.WALLS_CB.setChecked(True)
        self.EFIT_CB.setChecked(True)
        #
        self.minSlider.setText('40s')
        self.maxSlider.setText('70s')
        self.actualSlider.setText('  ')
        self.configPlasma.setText('   ')
        self.timeXLOC_LB.setText('   ')
        self.timeWALLS_LB.setText('   ')
        self.timeEFIT_LB.setText('   ')
        #
        self.canvas.figure.clear()
        self.canvas.draw()

    def resetGUI(self):
        """
        Push this button to configure GUI with reset values
        :return: reset GUI values
        """
        self.JPNedit.setText(' ')
        self.timeEdit.setText(' ')
        self.stepPsiEdit.setText(' ')
        self.solEdit.setText(' ') # cm
        self.NsolEdit.setText(' ') # integer, nr of SOL lines
        self.coreEdit.setText(' ') # integer, nr of CORE lines
        self.coreStepEdit.setText(' ') # V/s
        self.timeXLOC_LB.setText('   ')
        self.timeWALLS_LB.setText('   ')
        self.timeEFIT_LB.setText('   ')
        #
        self.FW_CB.setChecked(False)
        self.GAP_CB.setChecked(False)
        self.XLOC_CB.setChecked(False)
        self.WALLS_CB.setChecked(False)
        self.EFIT_CB.setChecked(False)
            #
        self.minSlider.setText(' ')
        self.maxSlider.setText(' ')
        self.actualSlider.setText('  ')
        self.configPlasma.setText('   ')
         #
        self.canvas.figure.clear()
        self.canvas.draw()

    def exitGUI(self):
        """
        close the GUI
        :return:
        """
        self.close()

    def plotBoundaryFromSliderReleased(self,button):
        """

        :param button: slider button, while dragging it shows new time equilibria
        and plasma shape configuration
        :return:  plot on main canvs once slider released
        """

        JPNobj = self.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.plotParam['expDataDictJPNobj_EFIT']
        nameListGap = self.plotParam['nameListGap']
        nameListStrikePoints = self.plotParam['nameListStrikePoints']
        expDataDictJPNobj_XLOC = self.plotParam['expDataDictJPNobj_XLOC']
        expDataDictJPNobj_WALLS = self.plotParam['expDataDictJPNobj_WALLS']
        nameListGapWALLS = self.plotParam['nameListGapWALLS']
        offR_XLOC = self.plotParam['offR_XLOC']
        offZ_XLOC = self.plotParam['offZ_XLOC']
        time = self.plotParam['time']
        gapDict = self.plotParam['gapDict']
        xFW= self.plotParam['xFW']
        yFW= self.plotParam['yFW']
        rC= self.plotParam['rEFIT']
        zC= self.plotParam['zEFIT']
        rXLOC= self.plotParam['rBND_XLOC_smooth']
        zXLOC= self.plotParam['rzBND_XLOC_smooth']
        rP_XLOC= self.plotParam['rBND_XLOC']
        zP_XLOC= self.plotParam['zBND_XLOC']
        rXp= self.plotParam['rXp']
        zXp= self.plotParam['zXp']
        rSP= self.plotParam['rSP']
        zSP= self.plotParam['zSP']
        rWALLS= self.plotParam['rBND_WALLS']
        zWALLS= self.plotParam['zBND_WALLS']
        checkFW= self.plotParam['checkFW']
        checkGAP= self.plotParam['checkGAP']
        checkXLOC= self.plotParam['checkXLOC']
        checkWALLS= self.plotParam['checkWALLS']
        checkEFIT= self.plotParam['checkEFIT']
        flagDiverted = self.plotParam['flagDiverted']


        if button.sliderReleased:
            print('PLOT @ time ---> ' + str(time[button.value()]))

            timeEquil = time[button.value()]

            rC,zC,\
            rXLOC,zXLOC,rP_XLOC,zP_XLOC, \
            rXp,zXp,rSP,zSP, flagDiverted, \
            rWALLS,zWALLS,iTWALLS    = MagSurf.shapeSnapShot(self,JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC,nameListGapWALLS,expDataDictJPNobj_WALLS)

            if flagDiverted:
                self.configPlasma.setText('diverted')
            else:
                self.configPlasma.setText('limiter')


            MagSurf.plotFWGapBoundary(self,gapDict,xFW, yFW, rC,zC,
                          rXLOC,zXLOC, rP_XLOC, zP_XLOC, \
                          rXp,zXp,rSP,zSP, rWALLS,zWALLS,iTWALLS,  \
                        checkFW,checkGAP,checkXLOC,checkWALLS,checkEFIT,\
                                      flagDiverted,nameListGapWALLS)


    def plotFWGapBoundary(self,gapDict,xFW, yFW, rC,zC,
                          rXLOC,zXLOC, rP_XLOC, zP_XLOC, \
                          rXp,zXp,rSP,zSP,rWALLS,zWALLS,iTWALLS, \
                        flagPlotFW,flagPlotGap,flagPlotXLOC,\
                          flagPlotWALLS,flagPlotEFIT,flagDiverted,nameListGapWALLS):
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
        :param flagPlotXLOC:
        :param flagPlotWALLS:
        :param flagPlotEFIT:
        :param flagDiverted:
        :param nameListGapWALLS:
        :return:
        """
        self.canvas.figure.clf() # clear canvas
        ax = self.canvas.figure.add_subplot(111)
        ax.plot()

        # Gaps
        if flagPlotGap:
            nameListGap = gapDict.keys()
            for jj in nameListGap:
                if ('RSOGB' in jj) or  ('RSIGB' in jj) or ('ZSIGB' in jj) \
                    or ('ZSOGB' in jj) or ('WLBSRP' in jj):

                    R1 = gapDict[jj]['R1']
                    Z1 = gapDict[jj]['Z1']
                    R2 = gapDict[jj]['R2']
                    Z2 = gapDict[jj]['Z2']
                    R3 = gapDict[jj]['R3']
                    Z3 = gapDict[jj]['Z3']
                    R4 = gapDict[jj]['R4']
                    Z4 = gapDict[jj]['Z4']
                    ax.plot([R1,R2,R3,R4],[Z1,Z2,Z3,Z4],'d-r')
                else:
                    R1 = gapDict[jj]['R1']
                    Z1 = gapDict[jj]['Z1']
                    R2 = gapDict[jj]['R2']
                    Z2 = gapDict[jj]['Z2']
                    ax.plot([R1,R2],[Z1,Z2],'d-r')
                if 'TOG5' in jj:
                    ax.text(R1,Z1+0.1,jj,color='red')
                else:
                   ax.text(R1,Z1,jj,color='red')

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

        if flagPlotGap or flagPlotFW or flagPlotXLOC or flagPlotEFIT:
            ax.axis('equal')
            self.canvas.draw()

    def slider_moved(self,position):
        time = self.plotParam['time']
        self.actualSlider.setText(str(time[position]))
        self.timeEdit.setText(str(time[position]))


        MagSurf.plotBoundaryFromSliderReleased(self,self.horizontalSlider)




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

        self.timeEFIT_LB.setText(str(timeEFIT[iTEFIT]) + ' s' ) # display timeEquil closest time XLOC


        # find if diverted or limiter configuration
        ctype_v = expDataDictJPNobj_XLOC['CTYPE']['v']
        ctype_t = expDataDictJPNobj_XLOC['CTYPE']['t']

        iTimeX = numpy.where(
            numpy.abs(float(timeEquil) - ctype_t) < 2 * min(numpy.diff(ctype_t)))  # twice of the min of EFIT delta time

        iTimeXLOC = iTimeX[0][0]
        self.timeXLOC_LB.setText(str(ctype_t[iTimeXLOC]) + ' s' ) # display timeEquil closest time XLOC

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
        self.timeWALLS_LB.setText(str(timeWALLS[iTWALLS]) + ' s')

        return  rC,zC,rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
                rXp,zXp,rSP,zSP,flagDiverted,rWALLS,zWALLS,iTWALLS


    def plotCore(self):
        core = int(self.coreEdit.text())
        coreStep = float(self.coreStepEdit.text())

        JPNobj = self.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.plotParam['expDataDictJPNobj_EFIT']

        time = self.plotParam['time']
        timeEquil = time[self.horizontalSlider.value()]
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

        coreStepPsi = float(self.coreStepEdit.text())
        psiMaxCore = psiAxisEquil+core*coreStepPsi
        psiCoreLevels = numpy.linspace(psiAxisEquil,psiMaxCore,core+1)

        #
        # pylab.figure()
        # pylab.plot(rMAGEquil,zMAGEquil,'*m')
        # pylab.contour(rGrid,zGrid,psiGrid,psiCoreLevels,colors = 'm')
        # pylab.axis('equal')
        # pylab.show()


        self.canvas.figure.clf() # clear canvas
        ax = self.canvas.figure.add_subplot(111)
        ax.plot()

        xFW = self.plotParam['xFW']
        yFW = self.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')

        #pylab.plot(rGrid,zGrid,'.b')
        ax.plot(rMAGEquil,zMAGEquil,'*m')
        CS = ax.contour(rGrid,zGrid,psiGrid,psiCoreLevels,colors = 'r')
        ax.clabel(CS,inline = 1,fontsize= 10)
        ax.axis('equal')
        self.canvas.draw()


    def plotSol(self):
        sol = float(self.solEdit.text())
        Nsol = int(self.NsolEdit.text())

        JPNobj = self.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.plotParam['expDataDictJPNobj_EFIT']

        time = self.plotParam['time']
        timeEquil = time[self.horizontalSlider.value()]

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

        self.canvas.figure.clf() # clear canvas
        ax = self.canvas.figure.add_subplot(111)
        ax.plot()

        xFW = self.plotParam['xFW']
        yFW = self.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')

        ax.plot(rC,zC)
        ax.plot(rC[iMax],zC[iMax],'*b')
        ax.plot(rMidPlaneSOL,zMidPlaneSOL,'or')
        #ax.plot(rGrid,zGrid,'.b')
        ax.contour(rGrid,zGrid,psiGrid,psiSOL,colors = 'm')
        ax.axis('equal')
        self.canvas.draw()


    def plotIsoPsi(self):

        JPNobj = self.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.plotParam['expDataDictJPNobj_EFIT']

        time = self.plotParam['time']
        timeEquil = time[self.horizontalSlider.value()]

        deltaPsi = float(self.stepPsiEdit.text())

        rC, zC, psiEFIT, rGrid, zGrid,iTEFIT,timeEFIT \
            = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT, float(timeEquil))

        # rGrid = self.plotParam['rGrid']
        # zGrid = self.plotParam['zGrid']
        # psiGrid = self.plotParam['psiGrid']
        # psiEFIT = self.plotParam['psiEFIT']

        psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))
        # deltaPsi = 0.1 # step of 0.1V/s
        psiLevels = numpy.arange(numpy.min(psiEFIT),numpy.max(psiEFIT),deltaPsi)

        self.canvas.figure.clf() # clear canvas
        ax = self.canvas.figure.add_subplot(111)
        ax.plot()

        xFW = self.plotParam['xFW']
        yFW = self.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')

        #pylab.plot(rGrid,zGrid,'.b')
        CS = ax.contour(rGrid,zGrid,psiGrid,psiLevels,colors = 'r')
        ax.clabel(CS,inline = 1,fontsize= 10)
        ax.axis('equal')
        self.canvas.draw()


    def plotIsoPsiFill(self):

        JPNobj = self.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.plotParam['expDataDictJPNobj_EFIT']

        time = self.plotParam['time']
        timeEquil = time[self.horizontalSlider.value()]

        deltaPsi = float(self.stepPsiEdit.text())

        rC, zC, psiEFIT, rGrid, zGrid ,iTEFIT,timeEFIT \
            = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT, float(timeEquil))

        # rGrid = self.plotParam['rGrid']
        # zGrid = self.plotParam['zGrid']
        # psiGrid = self.plotParam['psiGrid']
        # psiEFIT = self.plotParam['psiEFIT']

        psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))
        # deltaPsi = 0.1 # step of 0.1V/s
        psiLevels = numpy.arange(numpy.min(psiEFIT),numpy.max(psiEFIT),deltaPsi)

        self.canvas.figure.clf() # clear canvas
        ax = self.canvas.figure.add_subplot(111)
        plt.subplots_adjust(bottom=0.1,right= 0.9,top=0.9)
        cax = plt.axes([0.85,0.1,0.075,0.8])
        #cax = self.canvas.figure.add_subplot(144)

        ax.plot()

        xFW = self.plotParam['xFW']
        yFW = self.plotParam['yFW']
        ax.plot(xFW, yFW, 'k')


        CS = ax.contourf(rGrid,zGrid,psiGrid,psiLevels,cmap=cm.hot)
        cbar = plt.colorbar(CS,cax,ax,cmap=psiLevels)
        cbar.ax.tick_params(labelsize=5)
        ax.axis('equal')
        self.canvas.draw()



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
        JPN = self.JPNedit.text()
        timeEquil = self.timeEdit.text()

        checkFW   = self.FW_CB.isChecked()
        checkGAP  = self.GAP_CB.isChecked()
        checkXLOC = self.XLOC_CB.isChecked()
        checkWALLS = self.WALLS_CB.isChecked()
        checkEFIT = self.EFIT_CB.isChecked()

        JPNobj = MAGTool(JPN)

        print(JPN + '@' + timeEquil + 's')
        if self.XLOC_CB.isChecked():
            print('Plot XLOC')
        if self.EFIT_CB.isChecked():
            print('Plot EFIT')

        # READ JET GEOMETRY FW anf GAPS
        gapDict, xFW, yFW, nameListGap, nameListStrikePoints, nameListGapWALLS = \
            MagSurf.readJETgeom(self,JPNobj)

        # RETREIVE EXP DATA
            # treat with PICKLE
        expDataDictJPNobj_XLOC, expDataDictJPNobj_WALLS, \
        expDataDictJPNobj_EFIT, expDataDictJPNobj_SC = \
            MagSurf.downloadExpData(self,JPN,JPNobj)

        timeXLOC = expDataDictJPNobj_XLOC['ROG']['t']
        timeEFIT = expDataDictJPNobj_EFIT['PSI']['t']
        timeWALLS = expDataDictJPNobj_WALLS['IWLGR01']['t']


        self.plotParam['JPNobj'] = JPNobj
        self.plotParam['expDataDictJPNobj_EFIT'] = expDataDictJPNobj_EFIT
        self.plotParam['nameListGap'] = nameListGap
        self.plotParam['nameListStrikePoints'] = nameListStrikePoints
        self.plotParam['expDataDictJPNobj_XLOC'] = expDataDictJPNobj_XLOC
        self.plotParam['expDataDictJPNobj_WALLS'] = expDataDictJPNobj_WALLS
        self.plotParam['nameListGapWALLS'] = nameListGapWALLS
        self.plotParam['offR_XLOC'] = offR_XLOC
        self.plotParam['offZ_XLOC'] = offZ_XLOC


        rEFIT,zEFIT,\
        rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
        rXp,zXp,rSP,zSP, flagDiverted,\
        rWALLS,zWALLS,iTWALLS    = MagSurf.shapeSnapShot(self,JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC,nameListGapWALLS,expDataDictJPNobj_WALLS)

        self.plotParam['time'] = timeEFIT
        self.plotParam['gapDict'] = gapDict
        self.plotParam['xFW'] = xFW
        self.plotParam['yFW'] = yFW
        self.plotParam['rEFIT'] = rEFIT
        self.plotParam['zEFIT'] = zEFIT
        self.plotParam['rBND_XLOC_smooth'] = rBND_XLOC_smooth
        self.plotParam['rzBND_XLOC_smooth'] = zBND_XLOC_smooth
        self.plotParam['rBND_XLOC'] = rBND_XLOC
        self.plotParam['zBND_XLOC'] = zBND_XLOC
        self.plotParam['rXp'] = rXp
        self.plotParam['zXp'] = zXp
        self.plotParam['rSP'] = rSP
        self.plotParam['zSP'] = zSP
        self.plotParam['checkFW'] = checkFW
        self.plotParam['checkGAP'] = checkGAP
        self.plotParam['checkXLOC'] = checkXLOC
        self.plotParam['checkWALLS'] = checkWALLS
        self.plotParam['checkEFIT'] = checkEFIT
        self.plotParam['flagDiverted'] = flagDiverted

        #
        # rGrid = expDataDictJPNobj_EFIT['rGrid']
        # zGrid = expDataDictJPNobj_EFIT['zGrid']
        # psiGrid = expDataDictJPNobj_EFIT['psiGrid']
        # psiEFIT = expDataDictJPNobj_EFIT['psiEFIT']
        #
        # self.plotParam['rGrid'] = rGrid
        # self.plotParam['zGrid'] = zGrid
        # self.plotParam['psiGrid'] = psiGrid
        # self.plotParam['psiEFIT'] = psiEFIT



        MagSurf.plotFWGapBoundary(self,gapDict,xFW, yFW,rEFIT,zEFIT,\
                        rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
                        rXp,zXp,rSP,zSP,\
                        rWALLS,zWALLS,iTWALLS,\
                        checkFW,checkGAP,checkXLOC,checkWALLS,checkEFIT,\
                                  flagDiverted,nameListGapWALLS)


        iT_Start,timeStart,iT_End,timeEnd = \
            MagSurf.findIndexTime(self,tStartEFIT,tEndEFIT,timeEFIT)


        # #MagSurf.updateSlider(self,iT_Start,iT_End,timeEquil,timeEFIT)
        self.horizontalSlider.setMinimum(iT_Start)
        self.horizontalSlider.setMaximum(iT_End)
        self.minSlider.setText(str(tStartEFIT))
        self.maxSlider.setText(str(tEndEFIT))
        self.actualSlider.setText(str(timeEquil))
        iPosition = numpy.where(
            numpy.abs(float(timeEquil) - timeEFIT) < 2 * min(numpy.diff(timeEFIT)))  # twice of the min of EFIT delta time=
        self.horizontalSlider.setSliderPosition(iPosition[0][0])
        print('pos: ' + str(iPosition[0][0])  + \
              ' ---> time ' + str(timeEFIT[iPosition[0][0]]))
        lenSamples = numpy.round((self.horizontalSlider.maximum()\
                                  -self.horizontalSlider.minimum())/10)
        self.horizontalSlider.setTickPosition(2)
        self.horizontalSlider.setTickInterval(lenSamples)


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




app = QtGui.QApplication(sys.argv)
MainWindow = MagSurf()
MainWindow.show()
app.exec_()


#
# if 0:
#     # using contourf ( fill contour)
#     pylab.figure()
#     plotFWGapBoundEFIT(gapDict,xFW, yFW, rC,zC,0,1)
#     #pylab.plot(rGrid,zGrid,'.b')
#     CS = pylab.contourf(rGrid,zGrid,psiGrid,psiLevels,cmap=cm.jet)
#     #pylab.clabel(CS,inline = 1,fontsize= 10)
#     pylab.axis('equal')
#     pylab.title('EFIT flux map @ ' + str(timeEquil) + 's')
#     plt.colorbar(ticks=psiLevels)
#     pylab.show()
#