__author__ = 'garta'
# v.1 21.06.2018
# Boundary XLOC vs EFIT and linked with slider movement-release


import numpy as np
from PyQt4 import QtGui, QtCore
import magSurfGA
import sys
import matplotlib.gridspec as gridspec
from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from scipy import interpolate
from MAGTool import * # Magnetics Tool
import pyqtgraph as pg


class MagSurf(QtGui.QMainWindow, magSurfGA.Ui_MainWindow):
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
        self.addToolBar(NavigationToolbar(self.canvas, self))

        #
        self.runPB.clicked.connect(self.goMagSurfGA)
        self.runPB.clicked.connect(self.goMagSurfGA)
        #
        self.JPNedit.setText('92504')
        self.timeEdit.setText('50')
        #
        self.FW_CB.setChecked(True)
        self.GAP_CB.setChecked(True)
        self.XLOC_CB.setChecked(True)
        self.EFIT_CB.setChecked(True)
        #
        self.minSlider.setText('  ')
        self.maxSlider.setText('  ')
        self.actualSlider.setText('  ')


        self.plotParam = {
            'JPNobj': None,
            'expDataDictJPNobj_EFIT': None,
            'nameListGap': None,
            'nameListStrikePoints': None,
            'expDataDictJPNobj_XLOC': None,
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
            'checkFE' : None,
            'checkGAP' : None,
            'checkXLOC' : None,
            'checkEFIT' : None
        }


        self.horizontalSlider.valueChanged.connect(self.slider_moved)
        self.horizontalSlider.sliderReleased.connect(
           lambda: self.plotBoundaryFromSliderReleased(self.horizontalSlider))



    def plotBoundaryFromSliderReleased(self,button):
        JPNobj = self.plotParam['JPNobj']
        expDataDictJPNobj_EFIT = self.plotParam['expDataDictJPNobj_EFIT']
        nameListGap = self.plotParam['nameListGap']
        nameListStrikePoints = self.plotParam['nameListStrikePoints']
        expDataDictJPNobj_XLOC = self.plotParam['expDataDictJPNobj_XLOC']
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
        checkFW= self.plotParam['checkFW']
        checkGAP= self.plotParam['checkGAP']
        checkXLOC= self.plotParam['checkXLOC']
        checkEFIT= self.plotParam['checkEFIT']


        if button.sliderReleased:
            print('PLOT @ time ---> ' + str(time[button.value()]))

            timeEquil = time[button.value()]

            rC,zC,\
            rXLOC,zXLOC,rP_XLOC,zP_XLOC, \
            rXp,zXp,rSP,zSP = MagSurf.shapeSnapShot(self,JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC)


            MagSurf.plotFWGapBoundary(self,gapDict,xFW, yFW, rC,zC,
                          rXLOC,zXLOC, rP_XLOC, zP_XLOC, \
                          rXp,zXp,rSP,zSP,  \
                        checkFW,checkGAP,checkXLOC,checkEFIT)


    def plotFWGapBoundary(self,gapDict,xFW, yFW, rC,zC,
                          rXLOC,zXLOC, rP_XLOC, zP_XLOC, \
                          rXp,zXp,rSP,zSP,  \
                        flagPlotFW,flagPlotGap,flagPlotXLOC,flagPlotEFIT):

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
            #pylab.plot(rGrid,zGrid,'.r')
            ax.plot(rC,zC,'-c',label='EFIT')

        if flagPlotXLOC:
            ax.plot(rXLOC,zXLOC,'-m',label='XLOC')
            ax.plot(rP_XLOC,zP_XLOC,'*m')
            ax.plot(rXp,zXp,'*c',markersize=16)
            ax.plot([rSP[0],rXp,rSP[2]],\
                            [zSP[0],zXp,zSP[2]],'*-g')

        if flagPlotGap or flagPlotFW or flagPlotXLOC or flagPlotEFIT:
            ax.axis('equal')
            self.canvas.draw()

    def slider_moved(self,position):
        time = self.plotParam['time']
        self.actualSlider.setText(str(time[position]))
        self.timeEdit.setText(str(time[position]))




    def downloadExpData(self,JPN,JPNobj):
          # #~~~~~~~~~~~~~~~EXP. DAT from XLOC, EFIT, SC ~~~~~~~~~~~~~~~~~~~~
        nameSignalsTable_XLOC = 'signalsTable_XLOC' #
        nameSignals_XLOC = STJET.signalsTableJET(nameSignalsTable_XLOC)
        expDataDictJPNobj_XLOC = JPNobj.download(JPN,nameSignalsTable_XLOC,nameSignals_XLOC,0)
        nameSignalsTable_EFIT = 'signalsTable_EFIT' #
        nameSignals_EFIT = STJET.signalsTableJET(nameSignalsTable_EFIT)
        expDataDictJPNobj_EFIT = JPNobj.download(JPN,nameSignalsTable_EFIT,nameSignals_EFIT,0)
        nameSignalsTable_SC   = 'signalsTable_SC' #
        nameSignals_SC = STJET.signalsTableJET(nameSignalsTable_SC)
        expDataDictJPNobj_SC = JPNobj.download(JPN,nameSignalsTable_SC,nameSignals_SC,0)
        # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        return expDataDictJPNobj_XLOC, expDataDictJPNobj_EFIT, expDataDictJPNobj_SC



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

        gapFileName       = 'gapILW.csv'
        firstWallFileName = 'FWILW.csv'


        nameListGap = ['GAP32','GAP6','GAP31','GAP30','RIG','GAP29','GAP28','GAP7','GAP27','GAP26',\
                       'TOG1','GAP25','TOG2','TOG3','TOG4','GAP24','TOG5',\
                       'GAP2','GAP23','GAP3','GAP22','GAP21','GAP20','ROG','GAP19','GAP4','GAP18','LOG','GAP17']

        nameListStrikePoints = ['RSOGB','ZSOGB','RSIGB','ZSIGB']#,'WLBSRP']
        #nameListStrikePoints = ['ZSOGB','ZSIGB']#,'WLBSRP']

        # First Wall
        xFW, yFW,= JPNobj.readFWFile(firstWallFileName)

        # Gap % Strike Points
        gapDict = JPNobj.readGapFile(gapFileName)

        return gapDict, xFW, yFW, nameListGap, nameListStrikePoints


    def shapeSnapShot(self,JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC):

         # EFIT
        rC,zC,psiEFIT,rGrid,zGrid = JPNobj.readEFITFlux(expDataDictJPNobj_EFIT,float(timeEquil))

        gapXLOC,rG,zG,iTXLOC  = JPNobj.gapXLOC(nameListGap,expDataDictJPNobj_XLOC,\
                                               gapDict,float(timeEquil))
        spXLOC,rSP,zSP,iTXLOC = JPNobj.strikePointsXLOC(nameListStrikePoints,\
                                expDataDictJPNobj_XLOC,gapDict,float(timeEquil))

        rX_XLOC = expDataDictJPNobj_XLOC['RX']['v']
        zX_XLOC = expDataDictJPNobj_XLOC['ZX']['v']

        rXp = rX_XLOC[iTXLOC]+offR_XLOC
        zXp = zX_XLOC[iTXLOC]+offZ_XLOC

        rBND_XLOC = []
        rBND_XLOC.append(rXp)
        for jj,vv in enumerate(rG):
            rBND_XLOC.append(rG[jj])
        rBND_XLOC.append(rXp)

        zBND_XLOC = []
        zBND_XLOC.append(zXp)
        for jj,vv in enumerate(zG):
            zBND_XLOC.append(zG[jj])
        zBND_XLOC.append(zXp)

        # connect  XLOC boundary points with a cubic
        n = 10
        i = numpy.arange(len(rBND_XLOC))
        # Nx the original number of points
        interp_i = numpy.linspace(0, i.max(), n  * i.max())
        rBND_XLOC_smooth = interpolate.interp1d(i, rBND_XLOC, kind='cubic')(interp_i)
        zBND_XLOC_smooth = interpolate.interp1d(i, zBND_XLOC, kind='cubic')(interp_i)

        return  rC,zC,rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
                rXp,zXp,rSP,zSP

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
        checkEFIT = self.EFIT_CB.isChecked()

        JPNobj = MAGTool(JPN)

        print(JPN + '@' + timeEquil + 's')
        if self.XLOC_CB.isChecked():
            print('Plot XLOC')
        if self.EFIT_CB.isChecked():
            print('Plot EFIT')

        # READ JET GEOMETRY FW anf GAPS
        gapDict, xFW, yFW, nameListGap, nameListStrikePoints = \
            MagSurf.readJETgeom(self,JPNobj)

        # RETREIVE EXP DATA
            # treat with PICKLE
        expDataDictJPNobj_XLOC, expDataDictJPNobj_EFIT, expDataDictJPNobj_SC = \
            MagSurf.downloadExpData(self,JPN,JPNobj)

        timeXLOC = expDataDictJPNobj_XLOC['ROG']['t']
        timeEFIT = expDataDictJPNobj_EFIT['PSI']['t']

        self.plotParam['JPNobj'] = JPNobj
        self.plotParam['expDataDictJPNobj_EFIT'] = expDataDictJPNobj_EFIT
        self.plotParam['nameListGap'] = nameListGap
        self.plotParam['nameListStrikePoints'] = nameListStrikePoints
        self.plotParam['expDataDictJPNobj_XLOC'] = expDataDictJPNobj_XLOC
        self.plotParam['offR_XLOC'] = offR_XLOC
        self.plotParam['offZ_XLOC'] = offZ_XLOC


        rEFIT,zEFIT,\
        rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
        rXp,zXp,rSP,zSP = MagSurf.shapeSnapShot(self,JPNobj,timeEquil,expDataDictJPNobj_EFIT,\
                        nameListGap,nameListStrikePoints,expDataDictJPNobj_XLOC,gapDict,\
                        offR_XLOC,offZ_XLOC)

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
        self.plotParam['checkEFIT'] = checkEFIT


        MagSurf.plotFWGapBoundary(self,gapDict,xFW, yFW,rEFIT,zEFIT,\
                        rBND_XLOC_smooth,zBND_XLOC_smooth,rBND_XLOC,zBND_XLOC, \
                        rXp,zXp,rSP,zSP,\
                        checkFW,checkGAP,checkXLOC,checkEFIT)


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



        #hS.sliderReleased.connect(self.plotFWGapBoundary)

        #hS.setTickInterval(10*int(len(timeXLOC)/freqXLOC))
        #hS.setTickInterval(freqXLOC)

        #hS.valueChanged.connect(self.actualSliderXLOC.setText('a'))
        #hS.sliderPressed.connect(self.actualSliderXLOC.setText)
        #hS.sliderReleased.connect(self.actualSliderXLOC.setText)



app = QtGui.QApplication(sys.argv)
MainWindow = MagSurf()
MainWindow.show()
app.exec_()

#
#
#
# # ZSIGB: [-0.33062926]
# # ZSOGB: [ 0.10380276]
# # CTYPE: [ 54.]
# # ZX: [ 0.3553504]
# # RSIGB: [ 0.31418687]
# # RX: [-0.01753851]
# # RSOGB: [ 0.09116709]
# # ZSIGB: [-0.33062926]
#
#

#
#
# if 0:
#     pylab.figure()
#     gs = gridspec.GridSpec(3,6)
#
#     ax1 = pylab.subplot(gs[:,:-4])
#     plotFWGapBoundEFIT(gapDict,xFW, yFW, rC,zC,1,1)
#     pylab.axis('equal')
#     ax2 = pylab.subplot(gs[:,2:])
#     plotFWGapBoundEFIT(gapDict,xFW, yFW, rC,zC,1,1)
#     ax2.axis('equal')
#     ax2.set_xlim([2,3.4])
#     ax2.set_ylim([-1.3,-1.1])
#     pylab.show()
#
#
# psiGrid = numpy.reshape(psiEFIT,(len(rGrid),len(rGrid)))
# deltaPsi = 0.1 # step of 0.1V/s
# psiLevels = numpy.arange(numpy.min(psiEFIT),numpy.max(psiEFIT),deltaPsi)
#
# if 0:
#     # using countour
#     pylab.figure()
#     plotFWGapBoundEFIT(gapDict,xFW, yFW, rC,zC,0,1)
#     #pylab.plot(rGrid,zGrid,'.b')
#     CS = pylab.contour(rGrid,zGrid,psiGrid,psiLevels,colors = 'r')
#     pylab.clabel(CS,inline = 1,fontsize= 10)
#     pylab.axis('equal')
#     pylab.title('EFIT flux map @ ' + str(timeEquil) + 's')
#     pylab.show()
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
#

#
#
# if 1:
#     pylab.figure()
#     plotFWGapBoundEFIT(gapDict,xFW, yFW, rC,zC,1,1)
#     #pylab.plot(rBND_XLOC,zBND_XLOC,'*-g',label='XLOC',markersize=12) # spezzata I DONT LIKE IT
#     pylab.plot(rBND_XLOC,zBND_XLOC,'*g',label='XLOC',markersize=12)
#     pylab.plot(rBND_XLOC_smooth,zBND_XLOC_smooth,'-g',label='XLOC',markersize=12) # kind of spline
#     pylab.plot(rSP,zSP,'*c',label='XLOC',markersize=12)
#     pylab.plot(rXp,zXp,'*c',markersize=16)
#     pylab.plot([rSP[0],rXp,rSP[2]],\
#                 [zSP[0],zXp,zSP[2]],'*-g')
#     pylab.axis('equal')
#     pylab.title('#' + str(JPN) + ':XLOC vs EFIT ' + str(timeEquil) + 's')
#     pylab.legend(loc='best',prop={'size':10})
#     pylab.show()