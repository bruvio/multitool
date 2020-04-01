import os
import sys
import unittest
import subprocess
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pdb
# sys.path.append("../")

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from GO_bruvio_tools import bruvio_tool
import bruvio_tools
from magSurfGA_SL import Ui_magsurf_window
from edge2d_window import Ui_edge2d_window
from eqdsk_window import Ui_eqdsk_window





class ProjectTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    # def setUp(self):
    #     app.config["TESTING"] = True
    #     app.config["DEBUG"] = False
    #     self.app = app.test_client()
    #
    #     self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        super(ProjectTests, self).tearDown()

    def test_run_init(self):
        # pdb.set_trace()
        # app = QApplication(sys.argv)
        # MainWindow = bruvio_tool()
        # print('initialization value', MainWindow.value)
        print('initialization value')
        assert MainWindow.value == 1

    # def test_run_edg2d(self):
    #     app = QApplication(sys.argv)
    #     MainWindow = bruvio_tool()
    #     result = MainWindow.handle_edge2d_button()
    #     assert result == 1
    #
    # def test_run_plot_data(self):
    #     app = QApplication(sys.argv)
    #     MainWindow = bruvio_tool()
    #     result = MainWindow.handle_readdata_button()
    #     # print(result)
    #     assert result == 1
    #
    # def test_run_magssurf(self):
    #     app = QApplication(sys.argv)
    #     MainWindow = bruvio_tool()
    #     result = MainWindow.handle_magsurf_button()
    #     # print(result)
    #     assert result == 1
    # #
    # def test_eqdsk(self):
    #     app = QApplication(sys.argv)
    #     MainWindow = bruvio_tool()
    #     result = MainWindow.handle_eqdsk_button()
    #     # print(result)
    #     assert result == 1

    ########################
    #### helper methods ####
    ########################

    ###############
    #### tests ####
    ###############





if __name__ == "__main__":
    import xmlrunner

    runner = xmlrunner.XMLTestRunner(output="tests/test-reports")
    unittest.main(testRunner=runner)
    ###########################################
    unittest.main()
