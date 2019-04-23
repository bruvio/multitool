#!/bin/env python
# -*- coding: utf-8 -*-
from EDGE2DAnalyze import *
import json, os, sys
import matplotlib.pyplot as plt
import argparse, logging
from collections import OrderedDict
from class_sim import *
import os.path



def run_edge2danalysis(input_dict_str1,input_dict_str2=None):
    input_dict = read_json(input_dict_str1)

    # os.remove('temp.json')

    pulse1=shot(input_dict)


    # print(pulse1.compare)

    # print(pulse1.unseeded)
    if pulse1.unseeded == "True":
        logging.info('plotting HRTS and LP profiles')

        pulse1.unseeded_analysis()


    if pulse1.plot_bolo == "True":
        logging.info('plotting bolometry profiles')
        pulse1.plot_bolo_hv(ms = 20, lw = 1,vert=True,bound=1.0e6)
        pulse1.plot_bolo_hv(ms = 20, lw = 1,vert=False,bound=1.6e6)

    # print(pulse1.plot_spectro)
    if pulse1.plot_spectro == "True":
        logging.info('plotting spectro')
        pulse1.plot_spectr()


    if pulse1.compare == "True":
        plt.close('all')
        logging.info('comparing pulses profiles')
        try:
            logging.info('second input JSON %s',str(input_dict_str2))

            input_dict2 = read_json(input_dict_str2)


            pulse2 = shot(input_dict2)

            logging.info('read second input JSON OK')




            logging.info('compare profiles omp & ot')
            shot.compare_profiles(pulse1,pulse2,ms = None, lw = None,color1=None,color2=None)
            # print(pulse2.pulse)
            logging.info('compare bolo')
            shot.compare_bolo(pulse1,pulse2,ms = None, lw = None,vert=True,color1=None,color2=None,bound=None)
            logging.info('compare spectr')
            shot.compare_spectr(pulse1,pulse2,ms = None, lw = None,color1=None,color2=None)

        except:
            logging.error('failed to compare')



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




if __name__=='__main__':

    # Parse the input arguments
    parser = argparse.ArgumentParser(description='Run edge2danalysis')
    parser.add_argument('input_dict1',type=str, help="pulse JSON to run.")
    parser.add_argument('--input_dict2', type=str, help="pulse JSON to compare.", required=False)


    # parser.add_argument("-d", "--debug", type=int,
    #                     help="Debug level. 0: Error, 1: Warning, 2: Info, 3: Debug", default=3)
    parser.add_argument("-d", "--debug", type=int,
                        help="Debug level. 0: Info, 1: Warning, 2: Debug,"
                            " 3: Error; \n default level is INFO", default=2)
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

    # Handle the input arguments
    # input_dict_file1 = args.input_dict1
    # input_dict_file2 = args.input_dict2
    if os.path.isfile(args.input_dict1):
        logger.info('Found input dictionary: %s', args.input_dict1)
        run_edge2danalysis(args.input_dict1,args.input_dict2)
        logging.info('FINISHED')
    else:
        logging.error(args.input_dict1 , '%s not found')
        logging.error(args.input_dict1 + '%s  not found')