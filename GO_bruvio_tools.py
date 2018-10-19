#!/usr/bin/env python


# ----------------------------
__author__ = "Bruno Viola"
__Name__ = "KG1 RO tool GUI" 
__version__ = "0"
__release__ = "2"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
# __status__ = "Testing"
__status__ = "Production"
__credits__ = ["gioart"]


import argparse
import logging
import sys
import numpy as np
import pathlib
import stat
import os
import subprocess
import time
from shutil import copyfile
from PyQt4 import QtGui
import bruvio_tools



from pathlib import Path

from ppf import *

sys.path.append('../')
from status_flags.status_flag import GetSF
from utility import *
from reqco.test_reqco_ver01 import *
from smtpexample_fork import mail

from numpy import arange,asscalar
import matplotlib.pyplot as plt
plt.rcParams["savefig.directory"] = os.chdir(os.getcwd())

class bruvio_tool(QtGui.QMainWindow, main_window_gui.Ui_MainWindow):
    """
    Class for running the GUI and handling events.

    This GUI allows the user to:


    """

    # ----------------------------
    def __init__(self, parent=None):
        """
        Setup the GUI, and connect the buttons to functions.
        """
        import os
        super(KG1RO_tool, self).__init__(parent)
        self.setupUi(self)
        logging.debug('start')

        self.pulse_to_reprocess=[]
        self.pulse_not_to_reprocess=[]
        self.days=[]



        self.Cormat_button.clicked.connect(self.handle_Cormat_button)
        self.reqco_button.clicked.connect(self.handle_reqco_button)
        self.Kg1_py_button.clicked.connect(self.handle_Kg1_py_button)
        self.exit_button.clicked.connect(self.handle_exit_button)
        self.kg1lh_button.clicked.connect(self.handle_kg1lh_button)
        self.lidchoose_button.clicked.connect(self.handle_lidchoose_button)
        self.send_email_button.clicked.connect(self.handle_sendemail_button)
        self.database_button.clicked.connect(self.handle_database_button)
        self.status_flag_button.clicked.connect(self.handle_statusflag_button)
        self.readdata_button.clicked.connect(self.handle_readdata_button)
        self.actionHelp.triggered.connect(self.handle_help_menu)
        self.actionOpen_PDF_guide.triggered.connect(self.handle_pdf_open)



        self.Cormat_button.setToolTip('connects to JAC-12 and runs Cormat')
        self.reqco_button.setToolTip('opens Reqco GUI ')
        self.Kg1_py_button.setToolTip('opens GUI to run KG1_py code')
        self.exit_button.setToolTip('Exit application')
        self.kg1lh_button.setToolTip('opens GUI to run KG1L/H codes')
        self.lidchoose_button.setToolTip('opens lid choose dialog that helps writing the input file to be used by kg1 code')
        self.send_email_button.setToolTip('opens GUI to send email to Chain1 Manager')
        self.database_button.setToolTip('opens new windows to run database tools')
        self.readdata_button.setToolTip('opens windows to read standard set to plot time traces')
        self.status_flag_button.setToolTip('check status flag of a pulse')





        self.initfolder='kg1_tools_logbook'
        self.chain1 = '/common/chain1/kg1/'
        cwd = os.getcwd()
        self.home = cwd
        if "USR" in os.environ:
            logging.debug('USR in env')
            #self.owner = os.getenv('USR')
            self.owner = os.getlogin()
        else:
            logging.debug('using getuser to authenticate')
            import getpass
            self.owner = getpass.getuser()

        logging.debug('this is your username {}'.format(self.owner))
        homefold = os.path.join(os.sep, 'u', self.owner)
        logging.debug('this is your homefold {}'.format(homefold))
        home = str(Path.home())

        cwd = os.getcwd()
        self.home = cwd
        # print(owner)
        logging.debug('we are in %s', cwd)
        # psrint(homefold + os.sep+ folder)
        pathlib.Path(cwd + os.sep + self.initfolder).mkdir(parents=True,exist_ok=True)
        pathlib.Path(cwd + os.sep + 'figures').mkdir(parents=True,exist_ok=True)
        pathlib.Path(cwd + os.sep + 'standard_set').mkdir(parents=True,exist_ok=True)

        self.logbookdir = cwd + os.sep + self.initfolder
        logging.info('Logbook folder will be')
        logging.info('%s', cwd + os.sep + self.initfolder)



        #disabled until further checks with Aboboc
        self.run_local_database()

        # reading date of last reprocessing
        if os.path.isfile(self.logbookdir+os.sep+'reprocessed_pulses.txt'):
            with open(self.logbookdir+os.sep+'reprocessed_pulses.txt', 'r') as f_in:
                lines = f_in.readlines()
                for index, line in enumerate(lines):
                    if "reprocessed pulses from" in str(line):
                        dummy = lines[index].split()
                        logging.info('last reprocessing done on {}'.format(str(dummy[-1])))



        #making documentation
        if (args.documentation).lower() =='yes' :

            logging.info('creating documentation')

            os.chdir('docs')
            import subprocess
            subprocess.check_output('make html',shell=True)
            subprocess.check_output('make latex',shell=True)

            os.chdir(self.home)
        logging.info('\n')
        logging.info('INIT DONE')

    # ---------------------------
    def handle_readdata_button(self):
        """
        opens a new windows where the user can input a list of pulses he/she wants to plot

        than the user can select a standard sets (a list of signal)
        and then plot them


        :return:
        """

        logging.info('\n')
        logging.info('plotting tool')

        self.window_plotdata = QtGui.QMainWindow()
        self.ui_plotdata = Ui_plotdata_window()
        self.ui_plotdata.setupUi(self.window_plotdata)
        self.window_plotdata.show()

        initpulse = pdmsht()
        initpulse2 = initpulse -1

        self.ui_plotdata.textEdit_pulselist.setText(str(initpulse))
        # self.ui_plotdata.textEdit_colorlist.setText('black')

        self.ui_plotdata.selectfile.clicked.connect(self.selectstandardset)

        self.ui_plotdata.plotbutton.clicked.connect(self.plotdata)
        self.ui_plotdata.savefigure_checkBox.setChecked(False)

        self.JSONSS = 'main_parameters_new.json'

        logging.info('select a standard set')
        logging.info('\n')
        logging.info('type in a list of pulses')


    # ---------------------------
    def selectstandardset(self):
        # qfd = QtGui.QFileDialog()
        # path = "/"
        # filter = "JSON(*.json)"
        # f = QFileDialog.getOpenFileName(qfd, title, path, filter)
        self.JSONSS = QtGui.QFileDialog.getOpenFileName(None,'Select Standard set',"./standard_set",'JSON Files(*.json)')

        self.JSONSS = os.path.basename(self.JSONSS)
        os.chdir(self.home)
        return self.JSONSS



    # ---------------------------
    def plotdata(self):
        pulselist = self.ui_plotdata.textEdit_pulselist.toPlainText()
        pulselist = pulselist.split(',')
        if self.ui_plotdata.savefigure_checkBox.isChecked():
            save = True
        else:
            save = False

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
        plot_time_traces(self.JSONSS, inputlist,save=save)
        plt.show()



    # ---------------------------
    def handle_database_button(self):
        """
        opens a window that allows to check if there is a
        KG1V (or KG1L or KG1H) ppf written for a pulse (or list o pulses)
        """
        logging.info('\n')
        logging.info('KG1 DATABASE tool')
        # logging.info('use just pulse1 to check just that')

        self.window_database = QtGui.QMainWindow()
        self.ui_database = Ui_database_window()
        self.ui_database.setupUi(self.window_database)
        self.window_database.show()

        initpulse = pdmsht()


        self.ui_database.lineEdit_pulse.setText(str(initpulse))
        self.ui_database.lineEdit_jpn.setText(str(initpulse))

        # self.ui_database.lineEdit_pulse_2.setText('')
        self.ui_database.radioButton_kg1v.setChecked(True)
        self.ui_database.radioButton_kg1l.setChecked(False)
        self.ui_database.radioButton_kg1h.setChecked(False)
        self.ui_database.run_button_database.clicked.connect(
            self.run_button_database)
        #self.ui_database.run_local_database_button.clicked.connect(
            #self.run_local_database)
        self.ui_database.run_button_checkifdatabase.clicked.connect(self.run_checkifindatabase)
        self.ui_database.run_button_reprocess.clicked.connect(self.run_button_reprocess)
        self.ui_database.run_button_reprocess_2.clicked.connect(self.run_local_database)


        self.ui_database.run_button_database.setToolTip('checks if selected pulse (or interval of pulse if pulse2 is a valid JPN) if there are ppf for the selected dda in the JET database')
        #self.ui_database.run_local_database_button.setToolTip('creates a local logbook for the user')
        self.ui_database.run_button_checkifdatabase.setToolTip('checks if selected pulse is in the local user database')

    # ---------------------------
    def run_local_database(self):
        """
            each KG1 code (Cormat, kg1py,kg1l & kg1h create a local log in the user running folder

            this tool reads from Cormat running folder in /home/aboboc/
            the diary (from 2016 onwards) crated after each pulse is validated

            and then reads the local logs and creates database

        :return: pandas Dataframes of the created databases
        """
        logging.info('\n')
        logging.info('creating database')
        logging.info('data from 2016 onwards!')
        extract_cormat_history("/home/aboboc/LIB.OUTPUT/diary.2016",
                               self.chain1 + 'cormat_out.txt')

        extract_cormat_history("/home/aboboc/LIB.OUTPUT/diary.2017",
                               self.chain1 + 'cormat_out.txt')

        extract_cormat_history("/home/aboboc/LIB.OUTPUT/cormat.diary",
                               self.chain1 + 'cormat_out.txt')

        extract_kg1lh_history(
           '/u/'+self.owner+ '/work/intershot/run/kg1l/logbook.txt',
            self.chain1 + 'kg1l_out.txt')
        extract_kg1lh_history(
            '/u/' + self.owner + '/work/intershot/run/kg1h/logbook.txt',
            self.chain1 + 'kg1h_out.txt')
        extract_kg1py_history(
            '/u/'+self.owner+'/work/Python/KG1_code/python/run_out.txt',
            self.chain1 + 'kg1py_out.txt')
        logging.info('copying to local user profile')

        copyfile(self.chain1 + 'cormat_out.txt',
                 self.logbookdir + os.sep + 'cormat_out.txt')
        copyfile(self.chain1 + 'kg1l_out.txt',
                 self.logbookdir + os.sep + 'kg1l_out.txt', )
        copyfile(self.chain1 + 'kg1h_out.txt',
                 self.logbookdir + os.sep + 'kg1h_out.txt', )
        copyfile(self.chain1 + 'kg1py_out.txt',
                 self.logbookdir + os.sep + 'kg1py_out.txt', )

        # raise SystemExit
        logging.info('done')
        cormat_DF = create_database(self.chain1 + 'cormat_out.txt')
        kg1l_DF = create_database(self.chain1 + 'kg1l_out.txt')
        kg1h_DF = create_database(self.chain1 + 'kg1h_out.txt')
        kg1py_DF = create_database(self.chain1 + 'kg1py_out.txt')
        return cormat_DF,kg1l_DF,kg1h_DF,kg1py_DF

    # ---------------------------
    def run_checkifindatabase(self):
        """
        checks if the input pulse is in any database

        Databases are stored in /common/chan1/kg1
        """
        logging.info('\n')
        pulse = int(self.ui_database.lineEdit_jpn.text())

        # check_pulse_in_database(pulse,cormat_DF)
        # check_pulse_in_database(pulse,kg1l_DF)
        # check_pulse_in_database(pulse,kg1h_DF)
        # check_pulse_in_database(pulse,kg1py_DF)

        database_list = []
        database_list.append(self.chain1 + 'cormat_out.txt')
        database_list.append(self.chain1 + 'kg1l_out.txt')
        database_list.append(self.chain1 + 'kg1h_out.txt')
        database_list.append(self.chain1 + 'kg1py_out.txt')

        check_pulse_in_database_list(pulse, database_list)
        logging.info('done')

    # ---------------------------
    def run_button_database(self):
        """
        for the selected DDA
        checks if there are PPF for the pulse (or interval of pulses)
        written by any user (private ppf) or public ppfs



        """
        logging.info('\n')
        if self.ui_database.radioButton_kg1v.isChecked() == True:
            dda = 'KG1V'
        if self.ui_database.radioButton_kg1l.isChecked() == True:
            dda = 'KG1L'
        if self.ui_database.radioButton_kg1h.isChecked() == True:
            dda = 'KG1H'

        pulse1 = int(self.ui_database.lineEdit_pulse.text())
        logging.debug('%s', self.ui_database.lineEdit_pulse_2.text())
        # if not self.ui_database.lineEdit_pulse_2.text().isnumeric():

        if self.ui_database.lineEdit_pulse_2.text() == 'pulse2':
            logging.info('\n')
            logging.info('scan for ppf for pulse {} dda {} '.format(
                str(pulse1),dda))
            logging.info('\n')
            pulseSpec, userlist, numofseqlist, seqlist, datelist = create_database_4_dda(
                dda, pulse1, pulse2=None)

            show_database_4_dda(pulseSpec, userlist, numofseqlist, seqlist,
                                datelist)

        else:

            logging.debug('pulse 2 is {}'.format(
                str(self.ui_database.lineEdit_pulse_2.text())))
            pulse2 = int(self.ui_database.lineEdit_pulse_2.text())
            logging.info('\n')
            logging.info('scan for ppf between pulse1 {} and pulse2 {} dda {}'.format(
                str(pulse1), str(pulse2),dda))
            logging.info('\n')
            pulseSpec, userlist, numofseqlist, seqlist, datelist = create_database_4_dda(
                dda, pulse1, pulse2)

            show_database_4_dda(pulseSpec, userlist, numofseqlist, seqlist,
                                datelist)

    # else:
    #     logging.error('pulse2 MUST BE a valid JPN')
    #     self.window_database.hide()

    def run_button_reprocess(self):
        """

        :return:
        """
        logging.info('\n')
        days = int(self.ui_database.lineEdit_days.text())
        database_list = []
        database_list.append(self.chain1 + 'cormat_out.txt')
        # database_list.append(self.chain1 + 'kg1l_out.txt')
        # database_list.append(self.chain1 + 'kg1h_out.txt')
        database_list.append(self.chain1 + 'kg1py_out.txt')

        self.pulse_to_reprocess, self.pulse_not_to_reprocess, self.days,self.num_pulse_to_reprocess = validated_pulses(days, database_list)


        # self.ui_sendemail.textEdit_pulselist.setText(str(self.pulse_to_reprocess))

        # BODY = "Dear Chain1 Manager,\n \n" \
        #        "this is a list of pulses that have been validated in the last "+ str(self.days) +" \n" \
        #        " \n" + str(self.pulse_to_reprocess) + "\n \n" \
        #                            "Regards \n" \
        #                            "bruvio \n \n \n" \
        #                            "ATTENTION this is an Automated message \n" \
        #                            "please contact KG1 data RO " \
        #                            "if you need further information"

        # self.ui_sendemail.textEdit_message.setText(BODY)
        logging.info('the list has been copied')
        logging.info('you can now send this list to Chain1 Manager')
        logging.info('done')





    # ---------------------------
    def handle_sendemail_button(self):
        """

        opens GUI
        that allows to send an email (by default to chain1 manager)
        to notify change in kg1v data so other ppfs can be reprocessed
        at the moment (june 2018) the pulse list has to be set manually.

        during the installation process of the tool (/u/bviola/work/install_kg1_tools.sh) \
        the account name will be changed
        """
        logging.info('\n')
        logging.info('preparing  email')
        logging.info('write list of pulses that have been validated')
        logging.info('please WAIT')

        self.window_sendemail = QtGui.QMainWindow()
        self.ui_sendemail = Ui_sendemail_window()
        self.ui_sendemail.setupUi(self.window_sendemail)
        self.window_sendemail.show()

        self.ui_sendemail.lineEdit_toaddr.setText('chain1@jet.uk')

        self.ui_sendemail.pushButton_send.setEnabled(False)

        BODY = "Dear Chain1 Manager,\n \n" \
               "this is a list of pulses that have been recently validated \n" \
               " \n"

        self.ui_sendemail.textEdit_message.setText(BODY)

        self.ui_sendemail.textEdit_pulselist.setText(
            str(self.pulse_to_reprocess))

        self.ui_sendemail.create_message_button.clicked.connect(
            self.create_message)

        self.ui_sendemail.pushButton_send.clicked.connect(self.sendemail)

    def create_message(self):
        """

        create message before sending it
        :return: pulse list that is asked to reprocess
        """

        pulselist = self.ui_sendemail.textEdit_pulselist.toPlainText()

        if not self.days:
            BODY = "Dear Chain1 Manager,\n \n" \
               "this is a list of pulses that have been recently validated \n" \
               " \n" + pulselist + "\n \n" \
               "I kindly ask you to reprocess them \n" \
                                   "Regards \n" \
                                   "bruvio \n \n \n" \
                                   "ATTENTION this is an Automated message \n" \
                                   "please contact KG1 data RO " \
                                   "if you need further information"
        else:
            BODY = "Dear Chain1 Manager,\n \n" \
               "this is a list of pulses that have been validated in the last "+str(self.days) +" days \n" \
               " \n" + pulselist + "\n \n" \
                                   "I kindly ask you to reprocess them \n" \
                                   "Regards \n" \
                                   "bruvio \n \n \n" \
                                   "ATTENTION this is an Automated message \n" \
                                   "please contact KG1 data RO " \
                                   "if you need further information"


        self.ui_sendemail.textEdit_message.setText(BODY)
        self.ui_sendemail.pushButton_send.setEnabled(True)



    def save_pulselist_of_reprocessedpulses(self,pulselist):
        """

        :param pulselist:
        :return: save to file the pulse list  that is asked to reprocess \
        the file will be stored in the logbook folder

        """
        from datetime import date, timedelta

        fileout = open(self.logbookdir + os.sep +'reprocessed_pulses.txt', 'a+')
        endtime = date.today()
        starttime = endtime - timedelta(days=self.days)
        fileout.write('{} reprocessed pulses from {} to {} \n'.format(self.num_pulse_to_reprocess,str(starttime),str(endtime)))

        for pulse in pulselist:
            fileout.write("%s\n" % pulse)
        fileout.write("\n" )
        fileout.close()



    def sendemail(self):
        """
        retrieves input from gui then send


        """
        logging.info('\n')
        toaddr = str(self.ui_sendemail.lineEdit_toaddr.text())
        logging.info('Sending email to %s', toaddr)
        pulselist = self.ui_sendemail.textEdit_pulselist.toPlainText()
        logging.info('asking Chain1 Manager to reprocess \n %s', str(pulselist))
        body = self.ui_sendemail.textEdit_message.toPlainText()
        logging.debug('email message \n %s', body)
        reply_to = 'bruno.viola@ukaea.uk'
        bcc = reply_to
        subject = 'KG1V data have been modified'

        mail(toaddr, subject, body, cc=None, bcc=bcc, reply_to=reply_to,
             attach=None,
             html=None, pre=False, custom_headers=None)
        self.ui_sendemail.pushButton_send.setEnabled(False)


        logging.info('saving pulse list')
        self.save_pulselist_of_reprocessedpulses(pulselist.split())
        logging.info('email sent!')

    # ----------------------------
    def handle_Cormat_button(self):
        """
        runs Cormat:
        for now it just opens a shell and connects to jac-12
        here the ~/.bashrc file runs automatically launching Cormat2012




        """
        logging.info('\n')
        logging.info('running Cormat')
        logging.info('a new terminal window will be now open')
        logging.info('please WAIT')

        #user = os.getenv('USR')
        # import os
        #import subprocess
        
        x = os.system("xterm -hold -e ssh -X {}@jac-12".format(self.owner))
        #x = subprocess.Popen("xterm -hold -e ssh -X {}@jac-12".format(self.owner))
        # logging.debug('Cormat exit code is %s', x)
        #result = Popen(["ssh", "jac-12"], creationflags=CREATE_NEW_CONSOLE)

    # ----------------------------
    def handle_lidchoose_button(self):
        """
        opens lid choose dialog that helps writing the input file to be used by kg1 code

        """
        logging.info('\n')
        logging.info('running lid chooser GUI')
        self.window_lidchoose = QtGui.QMainWindow()
        self.ui_lidchoose = Ui_filegenerator()
        self.ui_lidchoose.setupUi(self.window_lidchoose)
        self.window_lidchoose.show()
        self.ui_lidchoose.generate_button.clicked.connect(
            self.handle_generate_button)
        self.ui_lidchoose.kg1r_py_button.toggled.connect(self.changeCode)

    # ----------------------------
    def handle_kg1lh_button(self):
        """
        opens runKG1LHcodes dialog and sets defaults
        """
        logging.info('\n')
        logging.info('running KG1L/H codes GUI')
        self.window_runKG1LHcodes = QtGui.QMainWindow()
        self.Ui_runKG1LHcodes = Ui_runKG1LHcodes()
        self.Ui_runKG1LHcodes.setupUi(self.window_runKG1LHcodes)
        self.window_runKG1LHcodes.show()
        self.Ui_runKG1LHcodes.run_KG1LH_button.clicked.connect(self.run_KG1LH)
        self.Ui_runKG1LHcodes.run_KG1LH_button.setToolTip('run code')
        self.Ui_runKG1LHcodes.lineEdit_writeuid.setText(self.owner)
        self.Ui_runKG1LHcodes.radioButton_d1.setChecked(
            True)  # set default debug level to 1
        self.Ui_runKG1LHcodes.radioButton_d2.setChecked(
            False)  # set default debug level to 1

        initpulse = pdmsht()

        self.Ui_runKG1LHcodes.lineEdit_pulse.setText(str(initpulse))
        self.Ui_runKG1LHcodes.checkBox_print.setChecked(True)
        self.Ui_runKG1LHcodes.KG1L_radio.setChecked(True)
        self.Ui_runKG1LHcodes.KG1H_radio.setChecked(False)
        self.Ui_runKG1LHcodes.checkBox_print.toggled.connect(
            lambda: self.checkprintstate(self.Ui_runKG1LHcodes.checkBox_print))

        self.Ui_runKG1LHcodes.lineEdit_pulse.setToolTip('select pulse')
        self.Ui_runKG1LHcodes.lineEdit_writeuid.setToolTip('use jetppf for public ppf')
        self.Ui_runKG1LHcodes.run_KG1LH_button.setToolTip('run code')

        self.Ui_runKG1LHcodes.label.setToolTip('select a debug level')
        self.Ui_runKG1LHcodes.groupBox.setToolTip('select a code')
        self.Ui_runKG1LHcodes.checkBox_print.setToolTip('print to screen code output')



    # ----------------------------
    def handle_reqco_button(self):
        """
        opens Reqco dialog and sets defaults
        email from David Grist explaining how the Reqco system works for validated pulses
        that have not been requested.

        "If there isn't a request, there's nothing to mark as complete.
         Some people have mentioned that the old system had "un-requested",
          which it was possible to set a pulse number as if
          it was done despite there being no request.
          This doesn't exactly make sense now, since validation can depend on
          any number of parameters including pulse number.
          I've heard from ROs that something similar would
          still be useful, so I will soon add a way for ROs to submit
          a "request" for certain parameter sets that is already complete
          at the time of submission, which is more or less the same thing.
          If you want I can let you know when this is ready to test."

        """
        logging.info('\n')
        logging.info('running Reqco GUI')
        self.window_reqco = QtGui.QMainWindow()
        self.ui_reqco = Ui_reqco_window()
        self.ui_reqco.setupUi(self.window_reqco)
        self.window_reqco.show()

        initpulse = pdmsht()
        self.ui_reqco.lineEdit_pulse.setText(str(initpulse))

        self.ui_reqco.radioButton_lid3.setChecked(True)

        self.ui_reqco.radioButton_lid3.setChecked(True)
        self.ui_reqco.radioButton_lid4.setChecked(False)
        self.ui_reqco.radioButton_lidall.setChecked(False)

        self.ui_reqco.done_button.setChecked(False)
        self.ui_reqco.impossible_button.setChecked(False)
        self.ui_reqco.closed_button.setChecked(False)

        self.ui_reqco.done_button.clicked.connect(self.mark_pulse_done)
        self.ui_reqco.impossible_button.clicked.connect(
            self.mark_pulse_impossible)
        self.ui_reqco.closed_button.clicked.connect(self.mark_pulse_closed)
        # self.ui_reqco.done_button.clicked.connect(lambda:self.handle_areyousure(self.ui_reqco.done_button))
        # self.ui_reqco.impossible_button.clicked.connect(lambda:self.handle_areyousure(self.ui_reqco.impossible_button))

        self.ui_reqco.run_button.clicked.connect(self.scan_reqco_database)

        self.ui_reqco.run_button.setToolTip('runs checks on the Reqco database for the selected process')
        self.ui_reqco.frame_plot_save.setToolTip('select process')
        self.ui_reqco.done_button.setToolTip('marks Reqco request for selected pulse as DONE')
        self.ui_reqco.impossible_button.setToolTip('marks Reqco request for selected pulse as IMPOSSIBLE')
        self.ui_reqco.closed_button.setToolTip('marks Reqco request for selected pulse as CLOSED')
        self.ui_reqco.lineEdit_pulse.setToolTip('insert JPN for handling single pulse request')
    # ----------------------------
    def mark_pulse_done(self):
        """
        function that manages event
        if user wants to mark request for selected pulse
        as done in  Reqco database
        """

        button = self.ui_reqco.done_button
        self.ui_reqco.done_button.setChecked(True)
        logging.debug('pressed button %s', button.text())
        logging.info('are you sure?')
        logging.info('waiting for user to click button')

        self.areyousure_window = QtGui.QMainWindow()
        self.ui_areyousure = Ui_areyousure_window()
        self.ui_areyousure.setupUi(self.areyousure_window)
        self.areyousure_window.show()

        self.ui_areyousure.pushButton_YES.clicked.connect(self.handle_yes)
        self.ui_areyousure.pushButton_NO.clicked.connect(self.handle_no)

    # ----------------------------
    def mark_pulse_impossible(self):
        """
        function that manages event
        if user wants to mark request for selected pulse
        as impossible in  Reqco database
        """

        button = self.ui_reqco.impossible_button
        self.ui_reqco.impossible_button.setChecked(True)
        logging.debug('pressed button %s', button.text())
        logging.info('are you sure?')
        logging.info('waiting for user to click button')

        self.areyousure_window = QtGui.QMainWindow()
        self.ui_areyousure = Ui_areyousure_window()
        self.ui_areyousure.setupUi(self.areyousure_window)
        self.areyousure_window.show()

        self.ui_areyousure.pushButton_YES.clicked.connect(self.handle_yes)
        self.ui_areyousure.pushButton_NO.clicked.connect(self.handle_no)
        #

    # ----------------------------
    def mark_pulse_closed(self):
        """
        function that manages event
        if user wants to mark request for selected pulse
        as closed in  Reqco database

        Essentially "closed" means it's not done, but for non-physics reasons.
        """

        button = self.ui_reqco.closed_button
        self.ui_reqco.closed_button.setChecked(True)
        logging.debug('pressed button %s', button.text())
        logging.info('are you sure?')
        logging.info('waiting for user to click button')

        self.areyousure_window = QtGui.QMainWindow()
        self.ui_areyousure = Ui_areyousure_window()
        self.ui_areyousure.setupUi(self.areyousure_window)
        self.areyousure_window.show()

        self.ui_areyousure.pushButton_YES.clicked.connect(self.handle_yes)
        self.ui_areyousure.pushButton_NO.clicked.connect(self.handle_no)
        #

    # ----------------------------
    def handle_yes(self):
        """
        functions that ask to confirm if user wants to proceed

        to set request for selected pulse as done/impossible/closed
        """
        logging.debug('pressed %s button',
                      self.ui_areyousure.pushButton_YES.text())
        if self.ui_reqco.done_button.isChecked() == True:
            logging.debug('continue')
            self.set_pulse_done()
            self.ui_reqco.done_button.setChecked(False)

        if self.ui_reqco.impossible_button.isChecked() == True:
            logging.debug('continue')
            self.set_pulse_impossible()
            self.ui_reqco.impossible_button.setChecked(False)

        if self.ui_reqco.closed_button.isChecked() == True:
            logging.debug('continue')
            self.set_pulse_closed()
            self.ui_reqco.closed_button.setChecked(False)

        self.ui_areyousure.pushButton_YES.setChecked(False)

        self.areyousure_window.hide()

    # ----------------------------
    def set_pulse_closed(self):
        """
        request for
        (pulse/process) marked as closed
        """
        if self.ui_reqco.radioButton_lid3.isChecked() == True:
            process = 'lid3'
        if self.ui_reqco.radioButton_lid4.isChecked() == True:
            process = 'lid4'
        if self.ui_reqco.radioButton_lidall.isChecked() == True:
            process = 'lidall'
        pulse = int(self.ui_reqco.lineEdit_pulse.text())

        reqs = waiting_requests_for_pulse(process, str(pulse))
        if not reqs:
            logging.error('the selected combination of process %s and pulse %s is not in Reqco database',
                process, str(pulse))
        else:

            for req in reqs:
                id = req["id"]
                logging.info('marking JPN %s as closed', str(pulse))
                if process == "lid3":
                    ppf = "KG1V/LID3"
                elif process == "lid4":
                    ppf = "KG1V/LID4"
                elif process == "lidall":
                    ppf = "KG1V"

                if yes_or_no('send message to requester? Y/N'):
                    sms = input()
                else:
                    sms = None
                r = set_request_closed(id, ppf, message=sms)

                #
                if r.status_code != 200:
                    logging.ERROR('Server returned error:')
                    logging.ERROR('%s',str(r.text))
                else:
                    logging.info('JPN %s marked as done',
                                 str(pulse))  # ----------------------------

    def set_pulse_done(self):
        """
        request for
        (pulse/process) marked as done
        """

        if self.ui_reqco.radioButton_lid3.isChecked() == True:
            process = 'lid3'
        if self.ui_reqco.radioButton_lid4.isChecked() == True:
            process = 'lid4'
        if self.ui_reqco.radioButton_lidall.isChecked() == True:
            process = 'lidall'
        pulse = int(self.ui_reqco.lineEdit_pulse.text())

        reqs = waiting_requests_for_pulse(process, str(pulse))
        if not reqs:
            logging.error('the selected combination of process %s and pulse %s is not in Reqco database',
                process, str(pulse))
        else:

            for req in reqs:
                id = req["id"]
                logging.info('marking JPN %s as done', str(pulse))
                if process == "lid3":
                    ppf = "KG1V/LID3"
                elif process == "lid4":
                    ppf = "KG1V/LID4"
                elif process == "lidall":
                    ppf = "KG1V"

                if yes_or_no('send message to requester? Y/N'):
                    sms = input()
                else:
                    sms = None
                r = set_request_done(id, ppf, message=sms)
                # r = set_request_done(id, ppf)
                #
                if r.status_code != 200:
                    logging.ERROR('Server returned error:')
                    logging.ERROR('%s',str(r.text))
                else:
                    logging.info('JPN %s marked as done',
                                 str(pulse))


    # ----------------------------
    def set_pulse_impossible(self):
        """
    request for
    (pulse/process) marked as impossible
    """


        if self.ui_reqco.radioButton_lid3.isChecked() == True:
            process = 'lid3'
        if self.ui_reqco.radioButton_lid4.isChecked() == True:
            process = 'lid4'
        if self.ui_reqco.radioButton_lidall.isChecked() == True:
            process = 'lidall'
        pulse = int(self.ui_reqco.lineEdit_pulse.text())

        reqs = waiting_requests_for_pulse(process, str(pulse))
        if not reqs:
            logging.error('the selected combination of process %s and pulse %s is not in Reqco database',
                process, str(pulse))
        else:

            for req in reqs:
                id = req["id"]
                logging.info('marking JPN %s as impossible', str(pulse))
                if process == "lid3":
                    ppf = "KG1V/LID3"
                elif process == "lid4":
                    ppf = "KG1V/LID4"
                elif process == "lidall":
                    ppf = "KG1V"
                if yes_or_no('send message to requester? Y/N'):
                    sms = input()
                else:
                    sms = None
                r = set_request_impossible(id, ppf, message=sms)




                # r = set_request_impossible(id, ppf)
                #
                if r.status_code != 200:
                    logging.ERROR('Server returned error:')
                    logging.ERROR('%s',str(r.text))
                else:
                    logging.info('JPN %s marked as impossible',
                                 str(pulse))


    # ----------------------------
    def handle_no(self):
        """
    functions that ask to confirm if user wants NOT to proceed

    to set request for selected pulse as done/impossible/closed
    """


        logging.debug('pressed %s button', self.ui_areyousure.pushButton_NO.text())
        if self.ui_reqco.done_button.isChecked() == True:
            self.ui_reqco.done_button.setChecked(False)
            logging.debug('go back')

        if self.ui_reqco.impossible_button.isChecked() == True:
            self.ui_reqco.impossible_button.setChecked(False)
            logging.debug('go back')

        self.ui_areyousure.pushButton_NO.setChecked(False)
        self.ui_reqco.impossible_button.setChecked(False)
        self.areyousure_window.hide()


    # ----------------------------
    def handle_Kg1_py_button(self):
        """
        opens Kg1_py code dialog
        user can select the option to run KG1_py code
        and create a shell script to run it.

        See KG1_py manual for further explanation
        """
        logging.info('\n')
        logging.info('running KG1_py code GUI')
        logging.info('setting up default options')
        self.window_Kg1_py = QtGui.QMainWindow()
        self.ui_Kg1_py = Ui_kg1py_window()
        self.ui_Kg1_py.setupUi(self.window_Kg1_py)
        self.window_Kg1_py.show()
        self.ui_Kg1_py.create_kg1py_script_button.clicked.connect(
            self.make_kg1py_shell_script)
        self.ui_Kg1_py.run_KG1_py_button.clicked.connect(self.run_KG1_py)
        # button to run script (that runs code) disabled until options are selected and shell
        # script is created
        self.ui_Kg1_py.run_KG1_py_button.setEnabled(False)
        # setting default/initial options
        logging.info("setting default/initial options")
        initpulse = pdmsht()
        self.ui_Kg1_py.pulse_input.setText(str(initpulse))  # pulse
        self.ui_Kg1_py.readui_input.setText('jetppf')  # read uid
        self.ui_Kg1_py.writeui_input.setText(self.owner)  # write uid
        logging.info("setting default/initial debug level to 2")
        self.ui_Kg1_py.radioButton_d2.setChecked(
            True)  # set default debug level to 2
        self.ui_Kg1_py.radioButton_plot.setChecked(
            True)  # set default debug level to 2
        if self.ui_Kg1_py.radioButton_plot.isChecked() == True:
            logging.info("by default plotting figures to screen")
            self.ui_Kg1_py.checkBox_finaldata_plot.setChecked(
                True)  # plot final data
            self.ui_Kg1_py.checkBox_datacorrection_plot.setChecked(
                True)  # plot position of correction
            self.ui_Kg1_py.checkBox_elms_plot.setChecked(False)  # no figure of elms
            self.ui_Kg1_py.checkBox_timings_plot.setChecked(
                False)  # no figure of Ip,NBI start/end
            self.ui_Kg1_py.checkBox_pellets_plot.setChecked(
                False)  # no figure of detected pellets

        # plot figure to screen
        # self.ui_Kg1_py.radioButton_plot.setChecked(True)#wants to plot figures
        # self.ui_Kg1_py.radioButton_save.setChecked(False)#does not want to save figures
        # set test mode and decimate mode
        self.ui_Kg1_py.checkBox_test.setChecked(True)  # run in test mode
        self.ui_Kg1_py.checkBox_decimate.setChecked(True)  # decimate KG1R data to KG1V (temporary caveat to work with Cormat!)
        self.ui_Kg1_py.checkBox_test.setToolTip('run in test mode')  #
        self.ui_Kg1_py.checkBox_decimate.setToolTip('decimate KG1R data to KG1V (temporary caveat to work with Cormat!)')

        self.ui_Kg1_py.radioButton_plot.toggled.connect(
            lambda: self.btnstate(self.ui_Kg1_py.radioButton_plot))
        # self.ui_Kg1_py.radioButton_save.toggled.connect(lambda: self.btnstate(self.ui_Kg1_py.radioButton_save))
        self.ui_Kg1_py.pulse_input.setToolTip('insert pulse number to correct')
        self.ui_Kg1_py.frame_debug.setToolTip('choose debug level - 0: Error, 1: Warning, 2: Info, 3: Debug, 4: Debug Plus ')
        self.ui_Kg1_py.frame_plot_save.setToolTip('save figure to file or plot to screen')
        self.ui_Kg1_py.frame_plot.setToolTip('figure to plot (or save)')
        self.ui_Kg1_py.readui_input.setToolTip('by default read public ppf (jetppf)')
        self.ui_Kg1_py.writeui_input.setToolTip('by default write private ppf - change to jetppf for a public ppf')

    # ----------------------------
    def scan_reqco_database(self):
        """
        scan Reqco database for selected process to see if there is any pulse that
        can be marked as done/impossible, i.e. if there is a pulse already validated for that process


        """
        import os
        import stat
        if self.ui_reqco.radioButton_lid3.isChecked() == True:
            process = 'lid3'
        if self.ui_reqco.radioButton_lid4.isChecked() == True:
            process = 'lid4'
        if self.ui_reqco.radioButton_lidall.isChecked() == True:
            process = 'lidall'
        logging.info('\n')
        logging.info('scanning database for process %s', process)
        cwd = os.getcwd()
        run_reqco = '../reqco/test_reqco_ver01.py'
        #run_reqco = './test_reqco_ver01.py'
        st = os.stat(run_reqco)
        os.chmod(run_reqco, st.st_mode | stat.S_IEXEC)
        os.system("{} {} ".format(run_reqco, process))


    # ----------------------------
    def checkprintstate(self, button):
        """
        option to print to stdout the output of KG1L code

        KG1H code is bugged and do not print to stdout!

        """
        if button.isChecked() == True:
            self.Ui_runKG1LHcodes.frame_debug.setEnabled(True)
            self.Ui_runKG1LHcodes.radioButton_d1.setChecked(
                True)
            self.Ui_runKG1LHcodes.radioButton_d2.setChecked(
                False)

        else:
            self.Ui_runKG1LHcodes.frame_debug.setEnabled(False)

            self.Ui_runKG1LHcodes.radioButton_d1.setChecked(
                False)
            self.Ui_runKG1LHcodes.radioButton_d2.setChecked(
                False)


    # ----------------------------
    def btnstate(self, button):
        """
        checks if user has selected to print to screen or save chosen
        figures (produced by KG1_py code)
        """

        # set plot figure defaults#
        # if b.text() == "radioButton_plot":
        if button.isChecked() == True:
            logging.info(" plotting figures to screen")
            self.ui_Kg1_py.checkBox_finaldata_plot.setChecked(
                True)  # plot final data
            self.ui_Kg1_py.checkBox_datacorrection_plot.setChecked(
                True)  # plot position of correction
            self.ui_Kg1_py.checkBox_elms_plot.setChecked(False)  # no figure of elms
            self.ui_Kg1_py.checkBox_timings_plot.setChecked(
                False)  # no figure of Ip,NBI start/end
            self.ui_Kg1_py.checkBox_pellets_plot.setChecked(
                False)  # no figure of detected pellets

            # self.ui_Kg1_py.checkBox_finaldata_plot.setChecked(False)#save final data
            # self.ui_Kg1_py.checkBox_datacorrection_plot.setChecked(False)#save position of correction
            # self.ui_Kg1_py.checkBox_elms_plot.setChecked(False)#no figure of elms
            # self.ui_Kg1_py.checkBox_timings_plot.setChecked(False)#no figure of Ip,NBI start/end
            # self.ui_Kg1_py.checkBox_pellets_plot.setChecked(False)#no figure of detected pellets

        # save figure to file (no plots)
        # if b.text() == "radioButton_save":
        #     if b.isChecked() == True:
        #         self.ui_Kg1_py.checkBox_finaldata_plot.setChecked(False)#plot final data
        #         self.ui_Kg1_py.checkBox_datacorrection_plot.setChecked(False)#plot position of correction
        #         self.ui_Kg1_py.checkBox_elms_plot.setChecked(False)#no figure of elms
        #         self.ui_Kg1_py.checkBox_timings_plot.setChecked(False)#no figure of Ip,NBI start/end
        #         self.ui_Kg1_py.checkBox_pellets_plot.setChecked(False)#no figure of detected pellets
        else:
            logging.info(" saving figures to file")
            self.ui_Kg1_py.checkBox_finaldata_plot.setChecked(
                True)  # save final data
            self.ui_Kg1_py.checkBox_datacorrection_plot.setChecked(
                True)  # save position of correction
            self.ui_Kg1_py.checkBox_elms_plot.setChecked(True)  # no figure of elms
            self.ui_Kg1_py.checkBox_timings_plot.setChecked(
                True)  # no figure of Ip,NBI start/end
            self.ui_Kg1_py.checkBox_pellets_plot.setChecked(
                True)  # no figure of detected pellets


    # ----------------------------
    def make_kg1py_shell_script(self):
        """
        once the make script button is pushed
        a bash file in KG1_code folder will be created that will run the code for a list of pulses:

        kg1_main.py -p {} -u bviola -dps data_corrections_timings_elms_data_final -t T -f {}_bviola

        ppf will be written privately as bviola or as jetppf

        the script will be saved in the logbook folder

        the button to run the code is then enabled
        """
        import stat
        import os
        import time
        from shutil import copyfile
        logging.info('\n')
        logging.info('preparing KG1py running script')

        self.kg1py_runscript_filename = self.home + '/kg1py_run_from_gui_script.sh'

        # self.pulse_input.append(str(self.InputVariable_tab2)+"/"+str(self.ExtraVariable))

        # shot = int(self.ui_Kg1_py.pulse_input.text())
        pulselist = self.ui_Kg1_py.pulse_input.text()
        pulselist = pulselist.split(',')
        pulselist = [int(i) for i in pulselist]

        inputlist = []
        for i,j in enumerate(pulselist):
            # print(i,j)
            # inputlist.append([pulselist[i],colorlist[i].strip()])
            inputlist.append([pulselist[i]])
        read_ui = self.ui_Kg1_py.readui_input.text()
        write_ui = self.ui_Kg1_py.writeui_input.text()
        if self.ui_Kg1_py.checkBox_test.isChecked() == True:

            test = '-t T'
        else:
            test = ''
        if self.ui_Kg1_py.checkBox_decimate.isChecked() == True:
            decimate = '-i T'
        else:
            decimate = ''
        # filename = 'run_pulse_' + str(shot) + '.sh'

        if self.ui_Kg1_py.radioButton_plot.isChecked() == True:
            strings = []
            plot_or_save = '-dpv'
        else:
            strings = []
            plot_or_save = '-dps'

        if self.ui_Kg1_py.checkBox_finaldata_plot.isChecked() == True:
            option1 = 'data_final'
        else:
            option1 = ''
        strings.append(option1)
        if self.ui_Kg1_py.checkBox_timings_plot.isChecked() == True:
            option2 = 'timings'
        else:
            option2 = ''
        strings.append(option2)
        if self.ui_Kg1_py.checkBox_elms_plot.isChecked() == True:
            option3 = 'elms'
        else:
            option3 = ''
        strings.append(option3)
        if self.ui_Kg1_py.checkBox_pellets_plot.isChecked() == True:
            option4 = 'pellets'
        else:
            option4 = ''
        strings.append(option4)
        if self.ui_Kg1_py.checkBox_datacorrection_plot.isChecked() == True:
            option5 = 'data_correction'
        else:
            option5 = ''
        strings.append(option5)
        
        if (self.ui_Kg1_py.checkBox_finaldata_plot.isChecked() == False &            self.ui_Kg1_py.checkBox_timings_plot.isChecked() == False &             self.ui_Kg1_py.checkBox_elms_plot.isChecked() == False &             self.ui_Kg1_py.checkBox_pellets_plot.isChecked() == False &             self.ui_Kg1_py.checkBox_datacorrection_plot.isChecked() == False):
            plot_or_save_command = ' '
        else:
            plot_or_save_options = '_'.join(filter(None, strings))
            plot_or_save_command = plot_or_save + ' ' + plot_or_save_options

        if self.ui_Kg1_py.radioButton_d0.isChecked() == True:
            debug = '-d 0'

        if self.ui_Kg1_py.radioButton_d1.isChecked() == True:
            debug = '-d 1'

        if self.ui_Kg1_py.radioButton_d2.isChecked() == True:
            debug = '-d 2'

        if self.ui_Kg1_py.radioButton_d3.isChecked() == True:
            debug = '-d 3'

        if self.ui_Kg1_py.radioButton_d4.isChecked() == True:
            debug = '-d 4'

        logging.info('Run the code with the following input parameters')
        # logging.info('%s', str(shot))

        logging.info('%s', read_ui)

        logging.info('%s', write_ui)

        logging.info('Test mode is %s', test)

        logging.info('Decimate mode is %s', decimate)

        logging.info('Print options are %s', plot_or_save_command)

        logging.info('debug option is %s', debug)

        with open(self.kg1py_runscript_filename, 'w') as f_out:
            f_out.write('#!/usr/bin/env bash\n\n')
            f_out.write(
                'export PYTHONPATH=$PYTHONPATH:/u/' + self.owner + '/work/Python/KG1_code/python\n\n')
            f_out.write(
                'export PATH=$PATH:/u/' + self.owner + '/work/Python/KG1_code/\n\n')
            home = os.getcwd()
            f_out.write('cd /u/' + self.owner + '/work/Python/KG1_code/python\n')
            for i,j in enumerate(inputlist):
                shot=inputlist[i][0]

                f_out.write('echo {}\n'.format(shot))

                self.kg1py_python_command = 'python  /u/' + self.owner + '/work/Python/KG1_code/python/kg1_main.py -p {} ' \
                                                                     '-r {} -u {} {} {} {} {}  -f {}_{}\n'.format(
                shot, read_ui, write_ui, debug, plot_or_save_command, test,
                decimate, shot,
                write_ui)


                f_out.write(self.kg1py_python_command)

            f_out.write('cd {}\n'.format(home))
        f_out.close()
        logging.info('running script stored in')
        logging.info('%s', self.kg1py_runscript_filename)

        # create backup of the file to remember how the code was run and when

        timestr = time.strftime("%Y%m%d-%H%M%S")
        st = os.stat(self.kg1py_runscript_filename)
        os.chmod(self.kg1py_runscript_filename, st.st_mode | stat.S_IEXEC)
        copyfile(self.kg1py_runscript_filename,
                 self.logbookdir + os.sep + 'kg1py_run_from_gui_script' + '_' + timestr + '.sh')

        logging.info('saving backup of the shell script in')
        logging.info('%s',
                     self.logbookdir + os.sep + 'kg1py_run_from_gui_script' + '_' + timestr + '.sh')

        self.ui_Kg1_py.run_KG1_py_button.setEnabled(True)

        return self.kg1py_runscript_filename


    # ----------------------------
    def run_KG1_py(self):
        """
           runs the KG1_py script produced
        """
        import subprocess
        logging.info('\n')
        logging.info('running KG1py code')

        curdir = os.getcwd()
        os.chdir('/u/' + self.owner + '/work/Python/KG1_code/python')
        subprocess.call(self.kg1py_runscript_filename)
        # , stdout = subprocess.PIPE
        # out,err=p.communicate()
        # logging.info('%s',out)
        os.chdir(curdir)


    # ----------------------------
    def run_KG1LH(self):
        """
           creates the KG1L/H script to run the code

           save a backup to the logbook folder

        """
        import stat
        import os
        import subprocess
        import time
        logging.info('\n')
        self.kg1lh_runscript_filename = self.home + '/kg1lh_run_from_gui_script.sh'

        userid = self.Ui_runKG1LHcodes.lineEdit_writeuid.text()

        pulse = int(self.Ui_runKG1LHcodes.lineEdit_pulse.text())

        if self.Ui_runKG1LHcodes.radioButton_d1.isChecked() == True:
            debug = '-d 1'
        if self.Ui_runKG1LHcodes.radioButton_d2.isChecked() == True:
            debug = '-d 2'

        toscreen = ''
        if self.Ui_runKG1LHcodes.checkBox_print.isChecked() == True:
            toscreen = 'screen'
            ison = 'ON'
        else:
            toscreen = ''
            ison = 'OFF'
        if self.Ui_runKG1LHcodes.KG1L_radio.isChecked() == True:
            code = 'kg1l'
        if self.Ui_runKG1LHcodes.KG1H_radio.isChecked() == True:
            code = 'kg1h'
        logging.info('Run the code with the following input parameters')
        logging.info('%s', str(pulse))

        logging.info('%s', userid)

        logging.info('output mode to screen is %s', ison)

        logging.info('debug option is %s', debug)
        with open(self.kg1lh_runscript_filename, 'w') as f_out:
            f_out.write('#!/usr/bin/env bash\n\n')
            f_out.write(
                'export PATH=$PATH:/u/' + self.owner + '/work/intershot/run/\n\n')
            f_out.write('echo {}\n'.format(pulse))
            python_command = '/u/' + self.owner + '/work/intershot/source/kg1l/{}.perl -p {} ' \
                                                  '{} {} -u {}\n'.format(
                code, pulse, toscreen, debug, userid)
            f_out.write(python_command)
        # create backup of the file to remember how the code was run and when
        logging.info('running script stored in')
        logging.info('%s', self.kg1lh_runscript_filename)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        st = os.stat(self.kg1lh_runscript_filename)
        os.chmod(self.kg1lh_runscript_filename, st.st_mode | stat.S_IEXEC)
        copyfile(self.kg1lh_runscript_filename,
                 self.logbookdir + os.sep + 'kg1lh_run_from_gui_script' + '_' + str(timestr) + '.sh')
        curdir = os.getcwd()

        logging.info('saving backup of the shell script in')
        logging.info('%s',
                     self.logbookdir + os.sep + 'kg1lh_run_from_gui_script' + '_' + timestr + '.sh')

        os.chdir('/u/' + self.owner + '/work/intershot/run')
        sys.stdout.flush()
        subprocess.call(self.kg1lh_runscript_filename)
        # out,err=p.communicate()
        logging.info('Finished running %s for pulse %s', code, str(pulse))
        os.chdir(curdir)


    # ----------------------------
    def handle_generate_button(self):
        """
        Event handler for the generate file button.
        The indices of the button groups are turned into
        indices from 0 - 5, and passed to the kg1_write_config
        class to generate the config file.
        """
        global lids_caption
        logging.info('Generate File')
        # lids_caption=['LDMETCOR','LDMET','LDDCNCOR','LDDCN','KG1RT','KG1V']

        # Qt button indices run from -2 downwards
        # so turn this into 0 - (n_buttons-1)
        to_add = np.arange(len(self.ui_lidchoose.lid1_group.buttons())) * 2 + 2
        logging.info("to add: %s", to_add)
        logging.info("checked lid 1 %s", self.ui_lidchoose.lid1_group.checkedId())

        lid1_select = self.ui_lidchoose.lid1_group.checkedId() + to_add[
            self.ui_lidchoose.lid1_group.checkedId() * -1 - 2]
        lid2_select = self.ui_lidchoose.lid2_group.checkedId() + to_add[
            self.ui_lidchoose.lid2_group.checkedId() * -1 - 2]
        lid3_select = self.ui_lidchoose.lid3_group.checkedId() + to_add[
            self.ui_lidchoose.lid3_group.checkedId() * -1 - 2]
        lid4_select = self.ui_lidchoose.lid4_group.checkedId() + to_add[
            self.ui_lidchoose.lid4_group.checkedId() * -1 - 2]
        lid5_select = self.ui_lidchoose.lid5_group.checkedId() + to_add[
            self.ui_lidchoose.lid5_group.checkedId() * -1 - 2]
        lid6_select = self.ui_lidchoose.lid6_group.checkedId() + to_add[
            self.ui_lidchoose.lid6_group.checkedId() * -1 - 2]
        lid7_select = self.ui_lidchoose.lid7_group.checkedId() + to_add[
            self.ui_lidchoose.lid7_group.checkedId() * -1 - 2]
        lid8_select = self.ui_lidchoose.lid8_group.checkedId() + to_add[
            self.ui_lidchoose.lid8_group.checkedId() * -1 - 2]

        pulse = self.ui_lidchoose.pulse_line.displayText()
        checked_ids = [lid1_select, lid2_select,
                       lid3_select, lid4_select,
                       lid5_select, lid6_select,
                       lid7_select, lid8_select]

        logging.info("CHECKED IDS: %s", checked_ids)

        logging.info('Generate File')
        logging.info('Pulse: %s', str(pulse))
        logging.info('LID1: %s', str(checked_ids[0]))
        logging.info('LID2: %s', str(checked_ids[1]))
        logging.info('LID3: %s', str(checked_ids[2]))
        logging.info('LID4: %s', str(checked_ids[3]))
        logging.info('LID5: %s', str(checked_ids[4]))
        logging.info('LID6: %s', str(checked_ids[5]))
        logging.info('LID7: %s', str(checked_ids[6]))
        logging.info('LID8: %s', str(checked_ids[7]))
        logging.info('##########################')

        # Also check whether the KG1R_PY button is checked or not
        use_kg1r_py = self.ui_lidchoose.kg1r_py_button.isChecked()

        write_config = kg1_write_config(pulse, checked_ids, self.logbookdir,
                                        is_kg1r_py=use_kg1r_py)

    # ----------------------------
    def changeCode(self):
        """
        change code
        """

        use_kg1r_py = self.ui_lidchoose.kg1r_py_button.isChecked()

        print("use {}".format(use_kg1r_py))
        if use_kg1r_py:
            logging.info("set enabled")
            self.ui_lidchoose.kg1c_button_lid1.setEnabled(1)
            self.ui_lidchoose.kg1c_button_lid2.setEnabled(1)
            self.ui_lidchoose.kg1c_button_lid3.setEnabled(1)
            self.ui_lidchoose.kg1c_button_lid4.setEnabled(1)
        else:
            logging.info("set disabled")
            self.ui_lidchoose.kg1c_button_lid1.setEnabled(0)
            self.ui_lidchoose.kg1c_button_lid2.setEnabled(0)
            self.ui_lidchoose.kg1c_button_lid3.setEnabled(0)
            self.ui_lidchoose.kg1c_button_lid4.setEnabled(0)




    def handle_statusflag_button(self):
        """
        opens status flag checker dialog
        user can select a pulse and a userid




        """
        logging.info('\n')

        logging.info('Status flag tool: setting up default options')

        self.window_statusflag = QtGui.QMainWindow()
        self.ui_statusflag = Ui_StatusFlag()
        self.ui_statusflag.setupUi(self.window_statusflag)
        self.window_statusflag.show()




        self.ui_statusflag.run_SF_button.clicked.connect(
            self.run_SF_button)
        initpulse = pdmsht()

        self.ui_statusflag.lineEdit_pulse.setText(str(initpulse))
        self.ui_statusflag.lineEdit_readuid.setText('jetppf')


    def run_SF_button(self):
        """
        the code will output the Status Flag
        related to the 8 channels of KG1V for
        selected user and pulse
        :return: status flag list
        """
        logging.info('\n')
        logging.info('checking status FLAGS ')

        ppfuid(self.ui_statusflag.lineEdit_readuid.text(), "r")

        ppfssr(i=[0, 1, 2, 3,4,5])

        channels = arange(0, 8) + 1
        SF_list = []

        pulse=int(self.ui_statusflag.lineEdit_pulse.text())


        for channel in channels:
            ch_text = 'lid' + str(channel)

            st_ch = GetSF(pulse, 'kg1v', ch_text)
            st_ch = asscalar(st_ch)
            SF_list.append(st_ch)
        logging.info('%s has the following SF %s', str(pulse), SF_list)




    #----------------------------
    def handle_help_menu(self):
        import webbrowser
        url='file://' + os.path.realpath('./docs/build/html/index.html')
        webbrowser.get(using='google-chrome').open(url,new=2);

        # ----------------------------
    def handle_pdf_open(self):
            """

            :return: open pdf file of the guide
            """
            file = os.path.realpath('./docs/kg1_tools_gui_documentation.pdf')
            import subprocess

            subprocess.Popen(['okular', file])

    # ----------------------------
    def handle_exit_button(self):
        """
        Exit the application
        """
        logging.info('\n')
        logging.info('Exit now')
        sys.exit()


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
    logger.info("Running KG1 tool.")

    app = QtGui.QApplication(argv)
    MainWindow = KG1RO_tool()
    MainWindow.show()
    app.exec_()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run GO_kg1_tools')
    parser.add_argument("-d", "--debug", type=int,
                        help="Debug level. 0: Info, 1: Warning, 2: Debug,"
                            " 3: Error; \n default level is INFO", default=0)
    parser.add_argument("-doc", "--documentation", type=str,
                        help="Make documentation. yes/no", default='no')



    args = parser.parse_args(sys.argv[1:])
    debug_map = {0: logging.INFO,
                1: logging.WARNING,
                2: logging.DEBUG,
                3: logging.ERROR}

    logger = logging.getLogger(__name__)
    fmt = MyFormatter()
    hdlr = logging.StreamHandler(sys.stdout)

    hdlr.setFormatter(fmt)
    logging.root.addHandler(hdlr)

    logging.root.setLevel(level=debug_map[args.debug])
    main()
