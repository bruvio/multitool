import os
import sys
import unittest
import subprocess
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# sys.path.append("../")

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
import bruvio_tools
from magSurfGA_SL import Ui_magsurf_window
from edge2d_window import Ui_edge2d_window
from eqdsk_window import Ui_eqdsk_window



def run_init():
    # first authenticate
    result = bruvio_tool(QMainWindow, bruvio_tools.Ui_MainWindow)
    return result



class ProjectTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        super(ProjectTests, self).tearDown()

    ########################
    #### helper methods ####
    ########################

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = run_init()

        assert response == True





if __name__ == "__main__":
    import xmlrunner

    runner = xmlrunner.XMLTestRunner(output="tests/test-reports")
    unittest.main(testRunner=runner)
    ###########################################
    unittest.main()
