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
# from kg1_tools.status_flags.status_flag import GetSF
# from kg1_tools.kg1_tools_gui.utility import *
# from reqco.test_reqco_ver01 import *
# from smtpexample_fork import mail

from numpy import arange,asscalar
import matplotlib.pyplot as plt
plt.rcParams["savefig.directory"] = os.chdir(os.getcwd())

class bruvio_tool(QtGui.QMainWindow, bruvio_tools.Ui_MainWindow):
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
        super(bruvio_tool, self).__init__(parent)
        self.setupUi(self)
        logging.debug('start')
        self.exit_button.clicked.connect(self.handle_exit_button)






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
    logger.info("Running bruvio tool.")
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = bruvio_tool()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run GO_bruvio_tools')
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
