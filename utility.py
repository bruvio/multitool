#!/usr/bin/env python
__author__ = "bruvio"
__version__ = "0.1"
import logging
import datetime
from time import strptime
import pandas as pd
import os.path
from ppf import *
from numpy import arange,asscalar,nan
import matplotlib.pyplot as plt
import sys
# sys.path.append('../')
# from status_flags.status_flag import GetSF
from time import gmtime, strftime
import getdat
from collections import OrderedDict
from matplotlib.gridspec import GridSpec
import pathlib
# from toggle import * # unlock fig from subplot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import mplcursors
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import numpy as np
from matplotlib.pylab import yticks, xticks, ylabel, xlabel
import sys
import logging
# sys.path.append('/Users/bruvio/Work/Python/fit_langmu/lib_langmu/')
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import AutoMinorLocator
from time import gmtime, strftime
# %%
from collections import OrderedDict
import json
import numbers
from math import factorial
from time import time
import matplotlib.pyplot as plt
import random as rd
from numpy.random import normal
import matplotlib.mlab as mlab
import collections
from collections import Counter
from itertools import groupby
from scipy.optimize import curve_fit
from scipy import asarray as ar, exp
import decimal
import math

from scipy.integrate import simps
from scipy import stats
from ppf import *
import numpy as np
from matplotlib import path

logger = logging.getLogger(__name__)
class Toggle():
    def __init__(self,fig):
        self.all_visible = True
        self.opos = None
        self.fig = fig

    def toggle(self,evt):
        # if evt.dblclick:
        if evt.button == 3:
                gs=GridSpec(1,1)
                if evt.inaxes:
                    if self.all_visible:
                        for ax in self.fig.axes:
                            if ax != evt.inaxes:
                                ax.set_visible(False)
                        self.opos = evt.inaxes.get_position()
                        evt.inaxes.set_position(gs[0].get_position(self.fig))
                        self.all_visible=False
                    else:
                        for ax in self.fig.axes:
                            ax.set_visible(True)

                        evt.inaxes.set_position(self.opos)
                        self.all_visible = True
                        self.opos = None
                    self.fig.canvas.draw_idle()




def read_csv(file_name):
    array_2D = []
    with open(file_name, 'r') as csvfile:
        read = csv.reader(csvfile, delimiter=',') #Assuming your csv file has been set up with the ';' delimiter - there are other options, for which you should see the first link.
        next(read)
        for row in read:
            array_2D.append(row)
    return array_2D

def read_npco_file(filename):
    dummy = np.genfromtxt(filename, skip_header=1)
    x=[]
    y=[]
    z=[]
    for i,row in enumerate(dummy):
        x.append(dummy[i][1]/100)
        y.append(dummy[i][2]/100)
        z.append(dummy[i][3]/100)
    x=np.asarray(x)
    y=np.asarray(y)
    z=np.asarray(z)

    return x,y,z


def read_pump_file(filename):
    try:
        lmap = lambda func, *iterable: list(map(func, *iterable))
        arrays = [np.array(lmap(float, line.split())) for line in
                  open(filename)]
        # dummy = np.loadtxt(filename, skiprows=1)
        r=[]
        z=[]

        for i in range(0,len(arrays)):
            if len(arrays[i])<3:
                continue
            else:

               r.append(arrays[i][0]/100)
               z.append(arrays[i][1]/100)
        r=np.asarray(r)
        z=np.asarray(z)
        pump = [r,z]
        return pump
    except:
        logging.error('this simulation has not a standard pump file.')

def read_puff_file(filename,alternativefile=None):
    dummy =[]
    if alternativefile is None:
        exists = os.path.isfile(filename)
        if exists:
            dummy = np.genfromtxt(filename, skip_header=1, dtype=float)
            return dummy
        else:
            return dummy
    else:
        exists = os.path.isfile(alternativefile)
        if exists:
            dummy = np.genfromtxt(alternativefile, skip_header=1, dtype=float)
            return dummy
        else:
            return dummy


def read_surfaces_file(filename):
    # dummy = np.genfromtxt(filename, skip_header=1,dtype=str)
    # The max column count a line in the file could have
    largest_column_count = 0

    # Loop the data lines
    with open(filename, 'r') as temp_f:
        # Read the lines
        lines = temp_f.readlines()

        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split()) + 1

            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

    # Close file
    temp_f.close()

    # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
    column_names = [i for i in range(0, largest_column_count)]
    dummy1 = pd.read_csv(filename,
                skiprows=1,dtype=str,
                delim_whitespace=True, header=None, index_col=False,
                error_bad_lines=False, warn_bad_lines=False, names=column_names, na_values = '')
    dummy1 = dummy1.fillna('')
    dummy1["combined"] = [' '.join(row.astype(str)) for row in dummy1[dummy1.columns[4:]].values]
#     dummy1['combined'].replace(
#     to_replace=['nan'],
#     value=' ',
#     inplace=True
# )
    data = pd.concat([dummy1[dummy1.columns[0:3]],dummy1["combined"]],axis=1)
    data.rename(columns={0: 'isurf', 1: 'type', 2: 'material',
                         'combined': 'description'}, inplace=True)
    # data =data.fillna(' ', inplace=True)
    # data = data.replace(np.nan, '', regex=True)
    # data = data.fillna('')
    # data.dropna(axis=1, how='all', inplace=True)

    return data




def read_elemente_file(filename):
    dummy = np.genfromtxt(filename, skip_header=1,dtype=int)
    dummy2 = dummy
    dummy = dummy[:,1:4]
    dummy = np.subtract(dummy,1)

    return dummy,dummy2

def read_transfer_file(filename,rows):
    dummy = np.genfromtxt(filename, skip_header=rows)
    dummy = dummy[:,1:]
    return dummy


def parse_csv_file_to_variable(filename):
    with open(filename, 'rt') as f:
      reader = csv.reader(f, delimiter=',')
      next(reader)
      # col = list(zip(*reader))[1]
      csv_dic = []

      for row in reader:
          csv_dic.append(row);
      # print(csv_dic)
      col1 = []
      col2 = []

      for row in csv_dic:
          col1.append(row[1])
          col2.append(row[2])
      dummy=np.array(col1)
      # print(dummy)
      dummy2=np.array(col2)
      dummy2=[float(i) for i in dummy2]
      z_ves=-np.asarray(dummy2)
      dummy=[float(i) for i in dummy]
      r_ves=np.asarray(dummy)
    f.close()
    return r_ves,z_ves


def create_database_4_dda(dda, pulse1, pulse2=None):
    """
    given a KG1 related dda and a pulse (or interval of pulses)

    :param dda:
    :param pulse1:
    :param pulse2:
    :return: a pulse list (or single pulse), a list of users that have written ppfs, \
     a list of sequences, a list of dates and a list containing the number of sequences written
    """
    maxpulse = pdmsht()
    logger.debug('max pulse is {} \n'.format(str(maxpulse)))
    ier = ppfgo()
    ppfsetdevice("JET")

    userlist = []
    numofseqlist = []
    seqlist = []
    pulseSpec = []
    datelist = []

    if pulse2 is None:

        pulse = pulse1
        pulseSpec.append(pulse)

        n, users, ier = pdlusr(pulse, dda=dda, n=1024)

        userlist.append(users)
        for u, user in enumerate(users):
            the_date=[]
            ppfuid(user, "r")
            # time, date, ier = pdstd(pulse)


            iseq, nseq, ier = ppfdda(pulse, dda, mseq=1024)
            numofseqlist.append(nseq)
            seqlist.append(iseq)
            for s, seq in enumerate(iseq):
                info, cnfo, ndda, ddal, istl, pcom, pdsn, ier = pdinfo2(pulse,
                                                                        seq)

                the_date.append(info[6])
            datelist.append(the_date)

        return pulseSpec, userlist, numofseqlist, seqlist, datelist

    else:
        pulse2 = pulse2+1
        if pulse2 > pulse1 & pulse2 < maxpulse:
            pulseSpec = arange(pulse1, pulse2, 1)

        if pulse2 > maxpulse or pulse1 > maxpulse:
            logger.error("pulse2 is greater than max pulse")
            return pulseSpec, userlist, numofseqlist, seqlist, datelist
        if pulse2 < pulse1:
            logger.error("pulse2 is lower that pulse1")
            return pulseSpec, userlist, numofseqlist, seqlist, datelist

        #

        for p, pulse in enumerate(pulseSpec):


            n, users, ier = pdlusr(pulse, dda=dda, n=1024)

            userlist.append(users)

            dummy_iseq = []
            dummy_seq = []
            for u, user in enumerate(users):
                the_date = []
                ppfuid(user, "r")
                iseq, nseq, ier = ppfdda(pulse, dda, mseq=1024)
                dummy_iseq.append(iseq)
                dummy_seq.append(nseq)
                for s, seq in enumerate(iseq):
                    info, cnfo, ndda, ddal, istl, pcom, pdsn, ier = pdinfo2(
                        pulse,
                        seq)

                    the_date.append(info[6])
                datelist.append(the_date)

                seqlist.append(dummy_iseq)
                numofseqlist.append(dummy_seq)


        return pulseSpec, userlist, numofseqlist, seqlist, datelist


def show_database_4_dda(pulseSpec, userlist, numofseqlist, seqlist, datelist):
    """

    :param pulseSpec: list of pulses
    :param userlist: list of users
    :param numofseqlist: list of number of sequences per user
    :param seqlist:  list of sequences
    :param datelist:  list of dates
    :return: for the given inputs returns  who wrote the ppfs and when


    """
    if len(pulseSpec) < 2:
        pulse = pulseSpec[0]

        # s = 0
        for k, user in enumerate(userlist[0]):
            
            logger.info(' user: {} has written {} ppf for shot {} \n'.format(user,
                                                                   numofseqlist[
                                                                       k],
                                                                   pulse))
            if user == 'jetpff' or user == 'JETPPF':
                # date = str(datelist[0])
                writtenby = 'unknown'
            else:
                writtenby = user
                # date = '00-00-00'

            for numseq in range(0, numofseqlist[k]):
                logger.info('shot: {} user: {} date: {} seq:{} by: {} \n'.format(
                    str(pulse),
                    user,
                    str(datelist[k][numseq]),
                    str(seqlist[k][numseq]),
                    writtenby))
    else:

        for i, pulse in enumerate(pulseSpec):
            # s = 0
            for k, user in enumerate(userlist[i]):
                
                logger.info('user {} has written {} ppf for shot {} \n'.format(user,
                                                                       numofseqlist[
                                                                           i][
                                                                           k],
                                                                       pulse))
                if user == 'jetpff' or user == 'JETPPF':
                    date = str(datelist[i])
                    writtenby = 'unknown'
                else:
                    writtenby = user
                    # date = '00-00-00'

                for numseq in range(0, numofseqlist[i][k]):
                    logger.info('shot: {} user: {} date: {} seq:{} by: {} \n'.format(
                        str(pulse),
                        user,
                        str(datelist[k][numseq]),
                        str(seqlist[i][k][numseq]),
                        writtenby))


def check_string_in_file(filename, string):
    """

    :param filename:
    :param string:
    :return: checks if the string is in that file
    """
    with open(filename) as myfile:
        if string in myfile.read():
            return True
        else:
            return False


def extract_cormat_history(filename, outputfile):
    """
    running this script will create a csv file containing a list of all the
    pulses that have been validated with CORMAT

    the script reads cormat.diary file in
    /home/aboboc/LIB.OUTPUT

    and writes an output file in the current working directory

    the file is formatted in this way
    shot: {} user: {} date: {} seq: {} by: {}
    user is the write user id
    by is the userid of the user of the code

    the output is appended and there is a check on duplicates

    :param filename: name of Cormat diary to be read
    :param outputfile: name of the output file
    :return:
    """


    with open(filename, 'r') as f_in:
        lines = f_in.readlines()
        for index, line in enumerate(lines):
            if "saved to" in str(line):
                dummy = lines[index].split()

                shot = int(dummy[0][1:])
                user = line[line.rfind("saved to") + 8:]
                user = user[:user.rfind("  ")]
                user = user[:7]
                writtenby = dummy[-1]

                dummy = lines[index + 1].split()
                sequence = (dummy[-1])

                date = line[line.rfind("on ") + 3:]
                date = date[:date.rfind(" by")]
                year = date[date.rfind('/') + 1:]
                date = date[:date.rfind('/')]
                month = date[date.rfind('/') + 1:]
                date = date[:date.rfind('/')]
                day = date[date.rfind('/') + 1:]
                #
                date = datetime.date(int(year), int(month), int(day))
                # #
                #
                # logger.info(shot,user,date,sequence,writtenby)
                # return
                string_to_write = "shot: {} user: {} date: {} seq: {} by: {}\n".format(
                    str(shot).strip(),
                    user.strip(),
                    str(date).strip(),
                    str(sequence).strip(),
                    writtenby.strip())
                # with open(outputfile,'a+') as f_out:
                #     f_out.write(string_to_write)
                # logger.info(string_to_write)

                if os.path.exists(outputfile):
                    if check_string_in_file(outputfile, string_to_write):
                        pass
                    else:
                        with open(outputfile, 'a+') as f_out:
                            f_out.write(string_to_write)
                        f_out.close()
                else:
                    with open(outputfile, 'a+') as f_out:
                        f_out.write(string_to_write)
                    f_out.close()

    f_in.close()


def extract_kg1lh_history(filename, outputfile):
    """
    running this script will create a csv file containing a list of all the
    ppf that have been created with KG1L/H codes

    the script reads a log file (generally in /u/user/work/intershot/kg1l/run)


    and writes an output file in the current working directory

    the file is formatted in this way
    shot: {} user: {} date: {} seq: {} by: {}
    user is the write user id
    by is the userid of the user of the code

    the output is appended and there is a check on duplicates

    if the user have never run KG1L code the file will be empty

    :param filename: name of KG1L (or KG1H) diary to be read
    :param outputfile: name of the output file
    :return:

    """
    import os
    if os.path.exists(filename):
        with open(filename, 'r') as f_in:
            lines = f_in.readlines()
            for index, line in enumerate(lines):
                if "shot" in str(line):
                    dummy = lines[index].split()

                    shot = int(dummy[1])
                    user = str(dummy[3])

                    #             dummy = lines[index + 1].split()
                    sequence = (dummy[11])

                    writtenby = (dummy[14])
                    month = (dummy[6])
                    day = (dummy[7])
                    year = (dummy[9])
                    date = datetime.date(int(year), strptime(month, '%b').tm_mon,
                                         int(day))

                    # logger.info(shot, user, date, sequence,writtenby)
                    # return
                    string_to_write = (
                        "shot: {} user: {} date: {} seq: {} by: {}\n".format(
                            str(shot).strip(),
                            user.strip(),
                            str(date).strip(),
                            str(sequence).strip(),
                            writtenby.strip()))
                    # with open(outputfile, 'a+') as f_out:
                    #     f_out.write(string_to_write)
                    #
                    if os.path.exists(outputfile):
                        if check_string_in_file(outputfile, string_to_write):
                            pass
                        else:
                            with open(outputfile, 'a+') as f_out:
                                f_out.write(string_to_write)
                            f_out.close()
                    else:
                        with open(outputfile, 'a+') as f_out:
                            f_out.write(string_to_write)
                        f_out.close()

        f_in.close()
    else:
        f_in = open(filename, "w")
        f_in.close()
        string_to_write = (
            "shot: {} user: {} date: {} seq: {} by: {}\n".format(str(00000),
                                                                 'unknown',
                                                                 str('0000-00-00'),
                                                                 str(000),
                                                                 'unknown'))
        if os.path.exists(outputfile):
            if check_string_in_file(outputfile, string_to_write):
                pass
            else:
                with open(outputfile, 'a+') as f_out:
                    f_out.write(string_to_write)
                f_out.close()
        else:
            with open(outputfile, 'a+') as f_out:
                f_out.write(string_to_write)
            f_out.close()


def extract_kg1py_history(filename, outputfile):
    """
    running this script will create a csv file containing a list of all the
    ppf that have been created with KG1_py code

    the script reads a log file (generally in /u/user/work/Python/KG1_code/python)


    and writes an output file in the current working directory

    the file is formatted in this way
    shot: {} user: {} date: {} seq: {} by: {}
    user is the write user id
    by is the userid of the user of the code
    the output is appended and there is a check on duplicates

    if the user have never run KG1_py code the file will be empty

    :param filename: name of KG1L (or KG1H) diary to be read
    :param outputfile: name of the output file
    :return:

    """
    import os
    if os.path.exists(filename):

        with open(filename, 'r') as f_in:
           lines = f_in.readlines()
           for index, line in enumerate(lines):
            if "shot" in str(line):
                dummy = lines[index].split()
                shot = int(dummy[1])
                user = str(dummy[3])
                date = str(dummy[5])

                # #             dummy = lines[index + 1].split()
                sequence = (dummy[7])

                writtenby = (dummy[10])
                # #
                #             month =(dummy[6])
                #             day =(dummy[7])
                #             year =(dummy[9])
                #             logger.info(month,day,year)
                #             date = datetime.date(int(year),strptime(month,'%b').tm_mon , int(day))

                # logger.info(shot, user, date, sequence,writtenby)
                # return
                string_to_write = (
                    "shot: {} user: {} date: {} seq: {} by: {}\n".format(
                        str(shot).strip(),
                        user.strip(),
                        str(date).strip(),
                        str(sequence).strip(),
                        writtenby.strip()))

                if os.path.exists(outputfile):
                    if check_string_in_file(outputfile, string_to_write):
                        pass
                    else:
                        with open(outputfile, 'a+') as f_out:
                            f_out.write(string_to_write)
                        f_out.close()
                else:
                    with open(outputfile, 'a+') as f_out:
                        f_out.write(string_to_write)
                    f_out.close()

        f_in.close()
    else:
        f_in = open(filename, "w")
        f_in.close()
        string_to_write = (
            "shot: {} user: {} date: {} seq: {} by: {}\n".format(str(00000),
                                                                 'unknown',
                                                                 str('0000-00-00'),
                                                                 str(000),
                                                                 'unknown'))
        if os.path.exists(outputfile):
            if check_string_in_file(outputfile, string_to_write):
                pass
            else:
                with open(outputfile, 'a+') as f_out:
                    f_out.write(string_to_write)
                f_out.close()
        else:
            with open(outputfile, 'a+') as f_out:
                f_out.write(string_to_write)
            f_out.close()



def create_database(filename,sort=False):
    """

    :param filename: name of the input file
    :param sort: if True the dataframe will be sorted by 'date'
    :return: returns a panda dataframe
    """
    f = open(filename, 'r')
    datalist = []
    dlabels = []
    for line in f:
        words = line.split(' ')

        words[-1] = words[-1][:-1]
        if len(dlabels) == 0:
            for i in range(0, len(words), 2):
                dlabels.append(words[i][:-1])
        tempL = []
        for i in range(0, len(words), 2):
            tempL.append(words[i + 1])

        datalist.append(tempL)
    f.close()
    # logger.info(dlabels)

    data = pd.DataFrame(datalist, columns=dlabels)

    #data.astype(str)
    #data['shot'].astype(int)
    #data['user'].astype(str)
    #data['date'].astype(str)
    #data['seq'].astype(str)
    #data['by'].astype(str)
    if sort is True:
        data = data.sort_values('shot', ascending=True)
    # data[data.shot.astype(int) == 91735]
    # data.loc[data['shot'] == 91735]
    # data = data.sort_values('date')
    data.name = filename[:-4]
    # from io import StringIO
    #
    # mystr = StringIO("""label1: value1 label2: string1 date: 2018-06-26 label3: value2 label4: string""")
    #
    # with open('cormat_out.txt', 'r') as mystr:
    #     with mystr as fin:
    #         data = next(fin).strip().split()
    #         data_dict = {i[:-1]: j for i, j in zip(data[::2], data[1::2])}
    #
    # # logger.info(data_dict)
    #
    # # {'date': '2018-06-26',
    # #  'label1': 'value1',
    # #  'label2': 'string1',
    # #  'label3': 'value2',
    # #  'label4': 'string'}

    return data


def check_pulse_in_database(pulse, dataframe):
    """

    :param pulse: pulse number to look for
    :param dataframe: pandas dataframe
    :return: given a pulse number and a panda dataframe \
    checks if the pulse is in that database \
    i.e. if a KG1 related ppf has been written by the user
    """
    shots_database = pd.Series(list(dataframe['shot']))
    pulse = str(pulse)
    checkinlist = shots_database.isin([pulse])
    inlist = [i for i, x in enumerate(checkinlist) if x]
    if not inlist:
        logger.info('{} is not in {} database!\n'.format(str(pulse),dataframe))
    else:
        for i in inlist:
            logger.info(
                '{} ppf created on {} by {} seq {} for pulse {} is in {}\n'.format(
                    dataframe['user'][i],
                    dataframe['date'][i],
                    dataframe['by'][i],
                    dataframe['seq'][i], pulse, dataframe.name))


def _check_pulse_in_database_list(pulse, dataframelist):
    """

    given a pulse number and a list of panda dataframes
    checks if the pulse is in any of those databases
    i.e. if a KG1 related ppf has been written by the user

    this routine as it is associated with    create_database

    :param pulse:
    :param dataframe:
    :return:
    """
    logger.info(' start looking for ppf written for pulse {}\n'.format(str(pulse)))
    for index1 in range(0, len(dataframelist)):
        name = dataframelist[index1]
        
        logger.info('looking in database {}\n'.format(name))
        dataframe = create_database(name)
        shots_database = pd.Series(list(dataframe['shot']))
        pulse = str(pulse)
        checkinlist = shots_database.isin([pulse])
        inlist = [i for i, x in enumerate(checkinlist) if x]

        if any(inlist) is True:
            logger.info('pulse {} found in database {}: \n'.format(pulse,
                                                              dataframe.name))
            for i in inlist:
                logger.info(' \t \t \t    modified on {} by {} stored as {} ppf seq {} \n'.format(
                        dataframe['date'][i], dataframe['by'][i],
                        dataframe['user'][i],
                        dataframe['seq'][i]))
        else:
            logger.info(' pulse {} not found \n'.format(str(pulse)))


def check_pulse_in_database_list(pulse, dataframelist):
    """

    updated version of check_pulse_in_database_list
    :param pulse:
    :param dataframe:
    :return:    given a pulse number and a list of panda dataframes
    checks if the pulse is in any of those databases
    i.e. if a KG1 related ppf has been written by the user
    """
    logger.info(' start looking for ppf written for pulse {} \n'.format(str(pulse)))
    for index1 in range(0, len(dataframelist)):
        name = dataframelist[index1]
        logger.info(' \n')
        logger.info(' looking in database {} \n'.format(name))
        dataframe = create_database(name,sort=True)
        index = dataframe.index

        pulse = str(pulse)

        # shots_database = pd.Series(list(dataframe['shot']))
        # checkinlist = shots_database.isin([pulse])
        # inlist = [i for i, x in enumerate(checkinlist) if x]

        #correction to find index of element in list without using pd series
        shots_database = list(dataframe['shot'])
        inlist = [i for i, x in enumerate(shots_database) if x == pulse]


        if any(inlist) is True:
            in_list=index[inlist]
            logger.info('  pulse {} found in database {}: \n'.format(pulse,
                                                              dataframe.name))

            for j,i in enumerate(in_list):
                if is_number_tryexcept(dataframe['seq'][i]):
                    logger.info(' \t \t \t    new sequence written on {} by {} stored as {} ppf seq {} \n'.format(
                        dataframe['date'][i], dataframe['by'][i],
                        dataframe['user'][i],
                        dataframe['seq'][i]))
                else:
                    logger.info(
                        '\t \t \t    modified on {} by {} stored as {} ppf seq {} \n'.format(
                            dataframe['date'][i], dataframe['by'][i],
                            dataframe['user'][i],
                            dataframe['seq'][i]))
        else:
            logger.info(' pulse {} not found \n'.format(str(pulse)))


def validated_pulses(days, dataframelist):
    """


    :param days:

    :param dataframelist:

    looks back (days) ago to look for recently validated ppf

    we intend validated pulse a KG1V ppf sequence written by cormat (or KG1py)
    where there were fringe jumps corrections. This is identified in the cormat database
    from a numeric sequence as  a validated pulse in cormat without fringe correction (just changes in status flag)
    will have ??? as sequence.
    :return: two list of unique pulses (to be reprocessed and not to be reprocessed), days


    """
    from datetime import date, timedelta
    from dateutil.relativedelta import relativedelta

    today=date.today()
    research_interval = today - relativedelta(days=days)


    starttime = today - timedelta(days=days)

    pulse_not_to_reprocess = []
    pulse_to_reprocess = []
    num_pulse_to_reprocess =0
    logger.info(
        'looking for ppf written in the last {} days (from {}) \n'.format(str(days),str(starttime)))
    for index1 in range(0, len(dataframelist)):
        name = dataframelist[index1]
        logger.info(' \n')
        logger.info(' looking in database {} \n'.format(name))
        dataframe = create_database(name, sort=True)

        #remove from data frame elements
        dataframe.drop(dataframe[dataframe['date'] == '00-00-00'].index,inplace = True)
        #convert object to date
        dataframe['date'] =  pd.to_datetime(dataframe['date'], format='%Y-%m-%d')
        #filtering database
        data = dataframe.loc[dataframe['date'].between(research_interval, today)]
        col = data.columns
        index = dataframe.index


        # correction to date format in list
        data_database = list(data['date'].apply(lambda x: x.strftime('%Y-%m-%d')))
        index = data.index
        #control loop
        if any(data_database) is True:
            if any(str(s).isdigit() for s in list(data['seq'])) is True:
                logger.info('  found pulses that need reprocess \n')
                validated_FJ_correction=[]
                validated_SF_correction=[]

                for j, i in enumerate(index):
                    if is_number_tryexcept(data['seq'][i]):
                        validated_FJ_correction.append([data['shot'][i],data['user'][i], data['date'][i].strftime('%Y-%m-%d'),
                                                        data['seq'][i],data['by'][i]])
                    else:
                        validated_SF_correction.append([data['shot'][i], data['user'][i], data['date'][i].strftime('%Y-%m-%d'),
                                                        data['seq'][i],data['by'][i]])

                df_validated_FJ = pd.DataFrame(validated_FJ_correction,columns=col)
                df_validated_SF = pd.DataFrame(validated_SF_correction,columns=col)




                for i in range(0,df_validated_FJ.__len__()):
                    pulse_to_reprocess.append(int(df_validated_FJ['shot'][i]))
                    logger.info(
                        '\t \t \t    pulse {} by {} stored as {} ppf seq {} date {}  need reprocessing \n'.format(
                            df_validated_FJ['shot'][i], df_validated_FJ['by'][i], df_validated_FJ['user'][i],
                            df_validated_FJ['seq'][i],df_validated_FJ['date'][i]))




                for i in range(0, df_validated_SF.__len__()):
                    pulse_not_to_reprocess.append(int(df_validated_SF['shot'][i]))
                    # logger.info(
                    #     '\t \t \t    pulse {} by {} stored as {} ppf seq {} date {} do NOT need reprocessing'.format(
                    #         df_validated_SF['shot'][i], df_validated_SF['by'][i], df_validated_SF['user'][i],
                    #         df_validated_SF['seq'][i],df_validated_SF['date'][i]))

            else:

                logger.info('  No pulses in the last {} days (from {}) need reprocess \n'.format(str(days),str(starttime)))
        else:

            logger.info('  No pulses in the last {} days (from {}) need reprocess \n'.format(str(days),str(starttime)))
        myset = set(pulse_to_reprocess)
        pulse_to_reprocess = list(myset)

        myset = set(pulse_not_to_reprocess)
        pulse_not_to_reprocess = list(myset)
        num_pulse_to_reprocess = len(pulse_to_reprocess)



        return pulse_to_reprocess,pulse_not_to_reprocess,days,num_pulse_to_reprocess


def read_polarimetry_file(pulselist,folder):
    pulse_struct = dict()
    for index1 in range(0, len(pulselist)):
        shot = pulselist[index1]
        filename=str(shot)+'.txt'

        with open(folder+filename, 'rt') as f_in:
            # print(f.readline())
            lines = f_in.readlines()
            channels = {}
            channels.setdefault('A', [])
            channels.setdefault('B', [])
            channels.setdefault('C', [])
            channels.setdefault('D', [])
            channels.setdefault('E', [])
            channels.setdefault('F', [])
            channels.setdefault('G', [])
            channels.setdefault('H', [])
            channels.setdefault('I', [])
            for index, line in enumerate(lines):
                if index == 0:
                    pass
                elif index ==1:
                    Pulse,MAX_IP,MAX_BVAC,MAX_LID3,MAX_TMAX =lines[index].split()
                else:
                    dummy = lines[index].split()
                    info = dummy
                    channels['A'].append(float(info[2]))
                    channels['B'].append(float(info[3]))
                    channels['C'].append(float(info[4]))
                    channels['D'].append(float(info[5]))
                    channels['E'].append(float(info[6]))
                    channels['F'].append(float(info[7]))
                    channels['G'].append(float(info[8]))
                    channels['H'].append(float(info[9]))
                    channels['I'].append(float(info[10]))

            pulse=dict()
            pulse['JPN']=shot
            pulse['MAX_IP']=MAX_IP
            pulse['MAX_BVAC']=MAX_BVAC
            pulse['MAX_LID3']=MAX_LID3
            pulse['MAX_TMAX']=MAX_TMAX
            pulse['channels'] = channels


        pulse_struct[str(shot)]=pulse


    return pulse_struct



def is_number_tryexcept(s):

    """

     :param s: input string
     :return: Returns True if string is a number.
     """
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_single_item_list(list_to_check):
    """
    Check that list is not empty
    :param list_to_check:
    :return: True or False
    """

    try:
        _ = list_to_check[0]
    except IndexError:
        return False
    # Return true if list has a single element
    try:
        _ = list_to_check[1]
    except IndexError:
        return True
    # Return False if more than one element
    return False


def plot_time_traces(diag_json,pulselist,save=False,smooth=False):
    """
    this routines plots time traces of JET diagnostics

    uses as input JSON file that contains info on the diagnostic the user wants
    to plot and info on how to plot them (i.e. what window, linestyle, marker...)



    :param diag_json: standard set containing the diagnostic the user wants to plot
    :param pulselist: list of pulses (and colors)
    :return:
    """
    logger.info(' using standard set {} \n'.format(diag_json))

    logger.info(' pulselist {} \n'.format(pulselist))


    default = True
    fold = './standard_set/'
    logger.debug('opening {} \n'.format(fold+diag_json))
    with open(fold+diag_json, mode='r', encoding='utf-8') as f:
        # Remove comments from input json
        with open(fold+"temp.json", 'w') as wf:
            for line in f.readlines():
                if line[0:2] == '//' or line[0:1] == '#':
                    continue
                wf.write(line)

    with open(fold+"temp.json", 'r') as f:
        input_dict = json.load(f, object_pairs_hook=OrderedDict)
        os.remove(fold+'temp.json')

    try:
        ppflen = (len(input_dict['ppf']))
    except:
        ppflen = 0
    try:
        jpflen = (len(input_dict['jpf']))
    except:
        jpflen = 0
    totsignal = (ppflen + jpflen)
    logger.info(' reading {} signals \n'.format(str(totsignal)))
    try:
        iColumn = int(input_dict['icolumn'])
        iRow = int(input_dict['irow'])
        linewidth = float(input_dict['linewidth'])
        markersize = float(input_dict['markersize'])
        default = False
    except:
        iColumn = 4
        iRow = int(round(totsignal / iColumn))
        linewidth = 0.5
        markersize =  1

    logger.debug('subplot {} x {} \n'.format(str(iRow),str(iColumn)))




    units = []
    names = []
    dataname = []
    pulse_list = []
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    path = '/u/bviola/work/Python/EDGE2D/exp_data'
    fig = plt.figure()

    # fig = plt.gcf()

    # fig, ax = plt.subplots(iRow, iColumn)
    # fig.subplots_adjust(hspace=0.4, wspace=0.4)
    # fig.set_size_inches(18.5, 10.5)

    for index,element in enumerate(pulselist):

        # print(pulse)
        pulse = int(pulselist[index][0])
        pulse_list.append(pulse)
        # color = (pulselist[index][1])
        logger.info(' \n')
        logger.info(' reading data for pulse %s \n', pulse)
        # indexSubPlot = 0
        indexSubPlot = 0
        # plt.figure()
        for key, value in input_dict.items():
            for value in input_dict[key]:


                system=key
                node=value
                # print(value)



                if system == 'ppf':
                    user=node.split('/')[0]
                    ppfuid(user, "r")
                    dda=node.split('/')[1]
                    dtype=node.split('/')[2]

                    # logger.debug('reading data %s ', key + '_' + dda + '_' + dtype)

                    data_name = 'data_' + key + '_' + dda + '_' + dtype
                    time_name = 't_data_' + key + '_' + dda + '_' + dtype
                    unit_name = 'units_' + '_' + dda + '_' + dtype

                    vars()[data_name], x, vars()[time_name], nd, nx, nt, vars()[
                        unit_name], xunits, tunits, desc, comm, seq, ier = \
                        ppfdata(pulse, dda, dtype, seq=0, uid=user,
                                device="JET", fix0=0, reshape=0, no_x=0, no_t=0)
                    if ier == 0 :
                        logger.info(' read data %s ', key + '_' + dda + '_' + dtype + 'seq {} \n'.format(str(seq)))
                    else:
                        logger.info(' no data \n')


                    if default == True:
                        indexSubPlot = indexSubPlot + 1
                        ax_name = 'ax_' + str(indexSubPlot)
                        marker = 'x'
                        linestyle = ':'
                        logger.debug('using default options for ppf')

                    else:
                        indexSubPlot = int(input_dict[system][value][0])
                        ax_name = 'ax_' + str(input_dict[system][value][0])
                        marker = input_dict[system][value][1]
                        linestyle = input_dict[system][value][2]
                        logger.debug('using JSON options for ppf')


                    # vars()[indexSubPlot] = fig.add_subplot(iRow, iColumn, indexSubPlot)
                    if indexSubPlot == 1:
                        ax_1 = plt.subplot(iRow, iColumn, indexSubPlot)
                    else:
                        vars()[ax_name] = plt.subplot(iRow, iColumn,indexSubPlot,sharex=ax_1)
                    if smooth is True:
                        plt.plot(vars()[time_name], savitzky_golay((np.asarray(vars()[data_name])), 33, 1),
                                     label=str(pulse) + ' ' + node, marker = marker, linestyle=linestyle, linewidth=linewidth,
                                 markersize=markersize)
                    else:
                        plt.plot(vars()[time_name],
                                 vars()[data_name],
                                 label=str(pulse) + ' ' + node, marker=marker,
                                 linestyle=linestyle, linewidth=linewidth,
                                 markersize=markersize)

                    plt.legend(loc='best', prop={'size': 6})
                    plt.xlabel('time[s]')
                    plt.ylabel(vars()[
                        unit_name])
                    # plt.hold(True)

                if system == 'jpf':
                    data_name = 'data_' + key + '_' + value
                    time_name = 't_data_' + key + '_' + value
                    unit_name = 'units_' + key + '_' + value



                    vars()[data_name], vars()[time_name], IplSigLen, IplSigTitle, vars()[
                        unit_name], ier = getdat.getdat(value,pulse)
                    if ier == 0 :
                        logger.info(' read data  ' + key + '_' + value )
                    else:
                        logger.info(' no data \n')





                    if default == True:
                        indexSubPlot = indexSubPlot + 1
                        ax_name = 'ax_' + str(indexSubPlot)
                        marker = 'x'
                        linestyle = ':'
                        logger.debug('using default options for ppf \n')

                    else:
                        indexSubPlot = int(input_dict[system][value][0])
                        ax_name = 'ax_' + str(input_dict[system][value][0])
                        marker = input_dict[system][value][1]
                        linestyle = input_dict[system][value][2]
                        logger.debug('used JSON options for jpf')




                    if indexSubPlot == 1:
                        ax_1 = plt.subplot(iRow, iColumn,indexSubPlot)

                    else:
                        vars()[ax_name] = plt.subplot(iRow, iColumn,
                                                           indexSubPlot,sharex=ax_1)
                    if smooth is True:
                        plt.plot(vars()[time_name], savitzky_golay((np.asarray(vars()[data_name])), 33, 1),
                                     label=str(pulse) + ' ' + node, marker = marker, linestyle=linestyle, linewidth=linewidth,
                                 markersize=markersize)
                    else:
                        plt.plot(vars()[time_name],
                                 vars()[data_name],
                                 label=str(pulse) + ' ' + node, marker=marker,
                                 linestyle=linestyle, linewidth=linewidth,
                                 markersize=markersize)

                    plt.legend(loc='best', prop={'size': 6})
                    # plt.ylabel(IplSigTitle)
                    plt.ylabel(vars()[
                                   unit_name])
                    plt.xlabel('time[s]')

                    # plt.hold(True)
                    # import itertools
                    # for l, ms in zip(ax_1.lines, itertools.cycle('>^+*')):
                    #     l.set_marker(ms)
                    #     l.set_color('black')
                    # #
                    # for l, ms in zip(ax_name.lines, itertools.cycle('>^+*')):
                    #     l.set_marker(ms)
                    #     l.set_color('black')
    mplcursors.cursor(hover=True)
    logger.info(' plot DONE! \n')
    if save is True:
        cwd = os.getcwd()

        pulses = "-".join(str(n) for n in pulse_list)
        # pathlib.Path(cwd + os.sep + 'figures').mkdir(parents=True,
        #                                               exist_ok=True)

        fname = diag_json[:-5]+'_'+pulses
        # plt.savefig('./figures/' + fname+'.eps', format='eps', dpi=50)
        # plt.savefig('./figures/' + fname+'.pdf', dpi=50)
        # plt.savefig('./figures/' + fname+'.png', dpi=50)
        plt.savefig(cwd+os.sep+'figures/'+fname+'.png', dpi=300)

        logger.info(' picture saved to {} \n'.format(cwd+os.sep+'figures/'+fname))
    t = Toggle(fig)
    fig.canvas.mpl_connect("button_press_event", t.toggle)
    # fig.canvas.mpl_connect("key_press_event", t.toggle)
    plt.show(block=True)
    # fig.tight_layout()


    #leave plt.show() outside

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def e2d_variables(file):
    with open(file) as f:
        lines = f.readlines()
    variables = []
    for line in lines[0:]:
        # print('line', line)
        columns = line.split()
        variables.append(columns[0])
    f.close()
    return variables


from matplotlib.collections import PatchCollection


def sqrt(s):
    return math.sqrt(s)


def initread(shot, userid, seq):
    """
    function that uses function of the ppf module
    it initialize the reading of a ppf file
    ppf file can be private, punlic or synthetic (coming from edge2d for example)

    Usage:
        initread(shot,userid,seq)

        """
    ppfsetdevice('JET')
    # print('ok')
    ppfuid(userid, 'r')
    ier = ppfgo(int(shot), int(seq))
    # @staticmethod




def compare_three_cases():
    filename_hrts_data_84600 = "/u/bviola/work/Python/EDGE2D/exp_data/hrts_84600_[51.772324]_estefan_T033_0_python.dat"
    filename_hrts_fit_84600 = "/u/bviola/work/Python/EDGE2D/exp_data/hrts_conv_84600_[51.772324]_estefan_T033_0_python.dat"
    omp_profiles = "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OMP_84600_may2518_seq#1.dat"
    ot_profiles = "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OT_84600_may2518_seq#1.dat"
    label1 = '5e21'
    # omp_profiles2= "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OMP_84600_may3018_seq#1.dat"
    # ot_profiles= "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OT_84600_may3018_seq#1.dat"

    omp_profiles2 = "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OMP_84600_may3018_seq#2.dat"
    ot_profiles = "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OT_84600_may3018_seq#2.dat"
    label2 = '1e22'
    omp_profiles3 = "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OMP_84600_jun1118_seq#1.dat"
    ot_profiles = "/u/bviola/work/Python/EDGE2D/e2d_data/84600/e2dprofiles_python_OT_84600_jun1118_seq#1.dat"
    label3 = '3.5e22'

    hrts_profiles_84600 = pd.read_csv(filename_hrts_data_84600, skiprows=3,
                                      delim_whitespace=True)
    hrts_fit_84600 = pd.read_csv(filename_hrts_fit_84600, skiprows=3,
                                 delim_whitespace=True)
    e2d_profiles = pd.read_csv(omp_profiles, skiprows=0,
                               delim_whitespace=True)
    e2d_profiles2 = pd.read_csv(omp_profiles2, skiprows=0,
                                delim_whitespace=True)
    e2d_profiles3 = pd.read_csv(omp_profiles3, skiprows=0,
                                delim_whitespace=True)

    # ot profiles
    e2d_profiles_ot = pd.read_csv(ot_profiles, skiprows=0,
                                  delim_whitespace=True)

    # plt.figure()
    # plt.scatter(hrts_profiles_84600['RmRsep'], hrts_profiles_84600['TE'] ,
    #             label='Te_omp_hrts', color='black')
    # plt.figure()
    # plt.scatter(hrts_profiles_84600['RmRsep'], hrts_profiles_84600['NE'] ,
    #             label='Te_omp_hrts', color='red')
    # plt.legend(loc=2, prop={'size': 8})

    # plt.figure()
    # plt.errorbar(hrts_profiles_84600['RmRsep'] + 0.005,
    #              hrts_profiles_84600['TE']*1e3, label='_nolegend_',
    #              yerr=hrts_profiles_84600['DTE'], fmt=None, ecolor='black')
    #
    # plt.scatter(hrts_fit_84600['Rfit'] + 0.005,
    #             hrts_fit_84600['tef5']*1e3, label='_nolegend_', color='red')
    #
    # plt.figure()
    # plt.errorbar(hrts_profiles_84600['RmRsep'] +0.005,
    #              hrts_profiles_84600['NE'], label='_nolegend_',
    #              yerr=hrts_profiles_84600['DNE'], fmt=None, ecolor='black')
    # plt.scatter(hrts_fit_84600['Rfit'] + 0.005,
    #             hrts_fit_84600['nef3'], label='_nolegend_', color='red')
    # plt.show()
    # targetfilename = 'unseeded'
    # targetfilename = 'm18-20'

    # logger.info(' plotting HRTS TE')
    shift = -1.58
    fname = '84600_Te_omp'
    fnorm = 1
    ftitle = 'Electron Temperature OMP'
    fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
    fylabel = '$T_{e,OMP}\quad keV$'

    plt.figure(num=fname)

    plt.scatter(e2d_profiles['dsrad'], e2d_profiles['te'] / 1e3, label=label1,
                marker='x')
    plt.scatter(e2d_profiles2['dsrad'], e2d_profiles2['te'] / 1e3, label=label2,
                marker='o')
    plt.scatter(e2d_profiles3['dsrad'], e2d_profiles3['te'] / 1e3, label=label3,
                marker='v')

    plt.scatter(hrts_profiles_84600['RmRsep'] + shift,
                hrts_profiles_84600['TE'] / 1, label='HRTS 84600',
                color='black')

    plt.scatter(hrts_fit_84600['Rfit'] + 0.005, hrts_fit_84600['tef5'] / 1,
                label='HRTS fit', color='blue')

    plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
    plt.axhline(y=0.1, xmin=-.15, xmax=500, linewidth=2, color='k')
    axes = plt.axes()
    axes.set_xlim([-.15, .1])
    axes.set_ylim([0, 1.0])
    axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
    axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    plt.legend(loc=2, prop={'size': 8})
    locs, labels = xticks()
    xticks(locs, list(map(lambda x: "%g" % x, locs)))
    locs, labels = yticks()
    yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
    #
    plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
    plt.ylabel(fylabel, {'color': 'k', 'size': 16})
    plt.savefig('./figures/' + fname, format='eps', dpi=300)
    plt.savefig('./figures/' + fname, dpi=300)  #
    # %%

    # logger.info(' plotting HRTS NE')
    # %%
    fname = '84600_ne_omp'
    fnorm = 1
    ftitle = 'Electron Density OMP'
    fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
    fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'

    plt.figure(num=fname)

    plt.scatter(e2d_profiles['dsrad'], e2d_profiles['denel'] / 1e19,
                label=label1, marker='x')
    plt.scatter(e2d_profiles2['dsrad'], e2d_profiles2['denel'] / 1e19,
                label=label2, marker='o')
    plt.scatter(e2d_profiles3['dsrad'], e2d_profiles3['denel'] / 1e19,
                label=label3, marker='v')

    plt.scatter(hrts_profiles_84600['RmRsep'] + shift,
                hrts_profiles_84600['NE'], label='HRTS 84600', color='black')
    plt.scatter(hrts_fit_84600['Rfit'] + 0.005, hrts_fit_84600['nef3'],
                label='HRTS fit', color='blue')

    plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
    plt.axhline(y=3.5, xmin=-.15, xmax=500, linewidth=2, color='k')

    axes = plt.axes()
    axes.set_xlim([-.15, .1])
    axes.set_ylim([0, 10.0])
    axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
    axes.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])
    plt.legend(loc=2, prop={'size': 8})
    locs, labels = xticks()
    xticks(locs, list(map(lambda x: "%g" % x, locs)))
    locs, labels = yticks()
    yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
    plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
    plt.ylabel(fylabel, {'color': 'k', 'size': 16})
    # plt.savefig('./figures/' + fname, format='eps', dpi=300)
    # plt.savefig('./figures/' + fname, dpi=300)  #

    # logger.info(' plotting HRTS NE')
    # %%
    fname = '84600_soun_omp'
    fnorm = 1
    ftitle = 'Direct Ion. source'
    fxlabel = '$R - R_{sep,LFS-mp}\quad  m$'
    # fylabel = '$n_{e,OMP}\quad 10 x 10^{19} m^{-3}})$'

    plt.figure(num=fname)

    plt.plot(e2d_profiles['dsrad'], e2d_profiles['soun'],
             label=label1, marker='x')
    plt.plot(e2d_profiles2['dsrad'], e2d_profiles2['soun'],
             label=label2, marker='o')
    plt.plot(e2d_profiles3['dsrad'], e2d_profiles3['soun'],
             label=label3, marker='v')

    plt.axvline(x=0.0, ymin=0., ymax=500, linewidth=2, color='k')
    plt.axhline(y=3.5, xmin=-.15, xmax=500, linewidth=2, color='k')

    axes = plt.axes()
    # axes.set_xlim([-.15, .1])
    # axes.set_ylim([0, 10.0])
    # axes.set_xticks([-.15, -0.1, -0.05, -0.02, 0, 0.02, 0.05, 0.1])
    # axes.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])
    plt.legend(loc=2, prop={'size': 8})
    locs, labels = xticks()
    xticks(locs, list(map(lambda x: "%g" % x, locs)))
    locs, labels = yticks()
    yticks(locs, list(map(lambda x: "%.3f" % x, locs)))
    plt.xlabel(fxlabel, {'color': 'k', 'size': 16})
    plt.ylabel(fylabel, {'color': 'k', 'size': 16})
    # plt.savefig('./figures/' + fname, format='eps', dpi=300)
    # plt.savefig('./figures/' + fname, dpi=300)  #
    plt.show()


def Getdata(pulse, dda, dtype, sequence, user):
    '''
function that reads a ppf file
    it can be used to read synthetic edge2d ppf files
    ARGS
    pulse1 :=  pulse

    dda := string e.g. 'kg1v'
    dtype:= string e.g. 'lid3'
    RETURNS
    '''
    # initialize pulse an sequence
    initread(int(pulse), user, int(sequence))
    data, x, t, nd, nx, nt, dunits, xunits, tunits, desc, comm, seq, ier = ppfdata(
        int(pulse), dda, dtype, seq=int(sequence), uid=user, device="JET",
        fix0=0, reshape=0, no_x=0, no_t=0)
    # ihdat,iwdat,data,x,t,ier=ppfget(int(pulse),dda,dtype)
    # pulse,seq,iwdat,comment,numdda,ddalist,ier=ppfinf(comlen=50,numdda=50)
    # info,cnfo,ddal,istl,pcom,pdsn,ier=pdinfo(pulse,seq)
    # istat,ier = ppfgsf(pulse,seq,dda,dtype,mxstat=1)
    return {'dunits': dunits,
            'desc': desc,
            'xunits': xunits,
            'data': data,
            'x': x,
            't': t,
            'ier': ier,
            'sequence': seq}


class Prepender(object):
    """
     class that keeps the existing file contents, and offers a write_lines method that preserves line order.
    """
    def __init__(self,
                 file_path,
                ):
        # Read in the existing file, so we can write it back later
        with open(file_path, mode='r') as f:
            self.__write_queue = f.readlines()

        self.__open_file = open(file_path, mode='w')

    def write_line(self, line):
        self.__write_queue.insert(0,
                                  "%s\n" % line,
                                 )

    def write_lines(self, lines):
        lines.reverse()
        for line in lines:
            self.write_line(line)

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.__write_queue:
            self.__open_file.writelines(self.__write_queue)
        self.__open_file.close()



def find_indices(lst, condition):
  """
  function that find the indices within an array where condition is true

  Usage:
      iy_OMP_SOL=find_indices(xdata, lambda e: e > 0)
  will return indices where the xdata[iy_OMP_SOL]>0
  """
  return [i for i, elem in enumerate(lst) if condition(elem)]

def inpolygon(xq, yq, xv, yv):
    from matplotlib import path
    shape = xq.shape
    xq = xq.reshape(-1)
    yq = yq.reshape(-1)
    xv = xv.reshape(-1)
    yv = yv.reshape(-1)
    q = [(xq[i], yq[i]) for i in range(xq.shape[0])]
    p = path.Path([(xv[i], yv[i]) for i in range(xv.shape[0])])
    return p.contains_points(q).reshape(shape)


###########
def smooth(a, WSZ):  # da studiare
    import numpy as np
    out0 = np.convolve(a, np.ones(WSZ, dtype=int), 'valid') / WSZ
    r = np.arange(1, WSZ - 1, 2)
    start = np.cumsum(a[:WSZ - 1])[::2] / r
    stop = (np.cumsum(a[:-WSZ:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))


def List(nameFile):
    # aprire il file da leggere
    List = []
    with open(nameFile) as f:
        for line in f:
            cols = [str(x) for x in line.split()]
            List.append(cols)
    return List


def DictList(List, input_dict):
    import numpy as np
    # keys per le liste
    CASEandGridDimension = ["CASE", "DATE", "dummy", "NoN so", "NW", "NH"]
    Parameters = ["rdim", "zdim", "rcentr", "rleft", "zmid", "rmaxis", "zmaxis", \
                  "simag", "sibry", "bcentr", "current", "simag", "xdum",
                  "rmaxis", "xdum", "zmaxis", \
                  "xdum", "sibry", "xdum", "xdum"]
    Parameters2 = ["nbbbs", "limitr"]
    DictParameters = {}  # Dizionario per i parametri di base (nome data dimensione griglia)
    DictCASEandGRIDDimension = {}  # Dizionario per i parametri fisici (corrente etc..)
    fpol = []
    pres = []
    ffprim = []
    pprime = []
    psirz = []
    psirzm = [[]]
    qpsi = []
    rzbbbs = []
    rbbbs = []
    zbbbs = []
    rzlim = []
    rlim = []
    zlim = []
    NameComponent = ["fpol", "pres", "ffprim", "pprime", "psirzm", "qpsi",
                     "rbbbs", "zbbbs", \
                     "rlim", "zlim"]
    DictNameComponent = {}
    fixfree = input_dict['fixfree']
    efit = input_dict['efit']
    # operazioni
    # 1 paramteri di base fisici
    k = 0
    for g in range(1, 5):
        for i in range(0, 5):
            DictParameters[Parameters[i + k]] = List[g][i]
        k += i + 1
    # 2 parametri di base
    for i in range(0, 6):
        DictCASEandGRIDDimension[CASEandGridDimension[i]] = List[0][i]
    nrgr = int(DictCASEandGRIDDimension['NW'])
    nzgr = int(DictCASEandGRIDDimension['NH'])
    rigaFinalCoefficient = int(nrgr / 5) + 1
    # print(rigaFinalCoefficient)

    # 3 fpol
    fpolrigaIniziale = 5
    fpolrigaFinale = 5 + rigaFinalCoefficient
    rigaIniziale = fpolrigaIniziale
    rigaFinale = fpolrigaFinale
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            fpol.append(float(el))
    DictNameComponent[NameComponent[0]] = fpol
    # 4 pres
    rigaIniziale = rigaFinale
    rigaFinale = rigaIniziale + rigaFinalCoefficient
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            pres.append(float(el))
    DictNameComponent[NameComponent[1]] = pres
    # 5 ffprim
    rigaIniziale = rigaFinale
    rigaFinale = rigaIniziale + rigaFinalCoefficient
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            ffprim.append(float(el))
    DictNameComponent[NameComponent[2]] = ffprim
    # 6 pprime
    rigaIniziale = rigaFinale
    rigaFinale = rigaIniziale + rigaFinalCoefficient
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            pprime.append(float(el))
    DictNameComponent[NameComponent[3]] = pprime
    # 7 psirz
    rigaIniziale = rigaFinale
    rigaFinale = len(List)
    A = [i + 1 for i in range(rigaIniziale, rigaFinale) if
         (len(List[i]) < 2 or len(List[i]) < 3 or len(List[i]) < 5)]
    rigaFinale = A[0]
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            psirz.append(float(el))

    psirzm = np.zeros((nrgr, nzgr))
    jj = 0
    jj_end = nzgr
    for j in range(0, nzgr):
        # psirzm.append(psirz[jj:jj_end])
        psirzm[0:nrgr, j] = (psirz[jj:jj_end])
        jj = jj_end
        jj_end = jj + nzgr
    psirzm = psirzm.T
    # psirzm = psirzm[1:]
    # PFM = np.zeros((nrgr,nzgr))
    # for i in range(nzgr):
    #     for g in range(nrgr):
    #         PFM[i][g] = psirzm[i][g]

    # DictNameComponent[NameComponent[4]] = PFM
    DictNameComponent[NameComponent[4]] = psirzm
    # 8 qpsi
    rigaIniziale = rigaFinale
    rigaFinale = rigaIniziale + rigaFinalCoefficient
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            qpsi.append(float(el))
    DictNameComponent[NameComponent[5]] = qpsi
    # 9 nbbbs, limitr
    rigaIniziale = rigaFinale
    i = 0
    for el in List[rigaIniziale]:
        DictParameters[Parameters2[i]] = el
        i += 1
        # print(el)
    # 10 rbbbs, zbbbs
    rigaIniziale = rigaIniziale + 1
    if fixfree:
        rigaFinale = int(rigaIniziale + 2 * int(
            DictParameters[Parameters2[0]]) / 5 + 1)  # eqdsk fixfree
    if efit:
        rigaFinale = int(rigaIniziale + 2 * int(
            DictParameters[Parameters2[0]]) / 5)  # eqdsk efit
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            rzbbbs.append(float(el))
    i = 1
    for el in rzbbbs:
        if i % 2 != 0:
            rbbbs.append(el)
        else:
            zbbbs.append(el)
        i += 1
    DictNameComponent[NameComponent[6]] = rbbbs
    DictNameComponent[NameComponent[7]] = zbbbs

    # 11 rlim, zlim
    rigaIniziale = rigaFinale
    rigaFinale = int(
        rigaIniziale + 2 * int(DictParameters[Parameters2[1]]) / 5 + 1)
    # print(rigaFinale)
    for i in range(rigaIniziale, rigaFinale):
        for el in List[i]:
            rzlim.append(float(el))
    i = 1
    for el in rzlim:
        if i % 2 != 0:
            rlim.append(el)
        else:
            zlim.append(el)
        i += 1
    DictNameComponent[NameComponent[8]] = rlim
    DictNameComponent[NameComponent[9]] = zlim

    # print(rlim[0])
    # print(rlim[-1])

    return DictParameters, DictCASEandGRIDDimension, DictNameComponent


def Vessel(nameFileVessel):
    Vessel = []
    Vessel2 = []
    with open(nameFileVessel, "r") as f:
        for line in f:
            cols = [str(x) for x in line.split()]
            Vessel.append(cols)
    Vessel2 = Vessel[40:]
    f = open("vessel_DTT_MC3.txt", "w")
    f.write("   " + str(len(Vessel2)))
    f.write("\n")
    for el in Vessel2:
        f.write(str(el[0]) + "      " + str(-float(el[1])) + "\n")
    f.close()


def smoothPSI(psirzm, nrgr, nzgr):
    """

    """
    # DictParameters,DictCASEandGRIDDimension,DictNameComponent = DictList(List(nameFile))
    # psirzm = DictNameComponent["psirzm"]
    # nrgr = int(DictCASEandGRIDDimension["NW"])
    # nzgr = int(DictCASEandGRIDDimension["NH"])
    flux2D = psirzm
    for jj in range(nzgr):
        flux2D[jj, :] = smooth(flux2D[jj, :], 5)
    for jj in range(nzgr):
        flux2D[:, jj] = smooth(flux2D[:, jj], 5)
    return flux2D


def get_axis_limits(ax, scale=.8):
    return ax.get_xlim()[1] * scale, ax.get_ylim()[1] * scale


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError as msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k ** i for i in order_range] for k in
                range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


def plot_time_traces_main(nshot, save=False):
    import pandas as pd
    import matplotlib.pyplot as plt

    for i in range(len(nshot)):

        shot = int(nshot[i])
        # init_plotting()
        # filename='/u/bviola/work/Python/EDGE2D/exp_data/Interp_Params_LID3_'+str(shot)+'_may2018.dat'
        # filename = '/u/bviola/work/Python/EDGE2D/exp_data/Interp_Params_LID3_' + str(
        #     shot) + '.dat'
        filename = '/u/bviola/work/Python/EDGE2D/exp_data/Interp_Params_LID3_' + str(
            shot) + '_python.dat'

        # Get data
        timetraces = pd.read_csv(filename, skiprows=[0, 1],
                                 delim_whitespace=True)

        fieldnames = list(timetraces.columns.values)
        fieldnames = [x.strip() for x in fieldnames]
        print(fieldnames)
        # raise SystemExit

        # x = np.asarray(timetraces['Time_LID3'])
        x = (np.asarray(timetraces['time/LID3']))

        timetraces['BOLO/TOPI'] = np.asarray(timetraces['BOLO/TOPI'])
        timetraces['BOLO/TOPI'] =timetraces['BOLO/TOPI'].astype(float).reshape(timetraces['BOLO/TOPI'].size, 1)

        timetraces['BOLO/TOBU'] = np.asarray(timetraces['BOLO/TOBU'])
        timetraces['BOLO/TOBU'] =timetraces['BOLO/TOBU'].astype(float).reshape(timetraces['BOLO/TOBU'].size, 1)

        timetraces['KG1V/LID3'] = np.asarray(timetraces['KG1V/LID3'])
        timetraces['KG1V/LID3'] =timetraces['KG1V/LID3'].astype(float).reshape(timetraces['KG1V/LID3'].size, 1)

        timetraces['EFIT/POHM'] = np.asarray(timetraces['EFIT/POHM'])
        timetraces['EFIT/POHM'] =timetraces['EFIT/POHM'].astype(float).reshape(timetraces['EFIT/POHM'].size, 1)

        timetraces['NBI/PTOT'] = np.asarray(timetraces['NBI/PTOT'])
        timetraces['NBI/PTOT'] =timetraces['NBI/PTOT'].astype(float).reshape(timetraces['NBI/PTOT'].size, 1)

        timetraces['KY4D/ITOT'] = np.asarray(timetraces['KY4D/ITOT'])
        timetraces['KY4D/ITOT'] =timetraces['KY4D/ITOT'].astype(float).reshape(timetraces['KY4D/ITOT'].size, 1)

        timetraces['KY4D/OTOT'] = np.asarray(timetraces['KY4D/OTOT'])
        timetraces['KY4D/OTOT'] =timetraces['KY4D/OTOT'].astype(float).reshape(timetraces['KY4D/OTOT'].size, 1)

        timetraces['GASM/G09R'] = np.asarray(timetraces['GASM/G09R'])
        timetraces['GASM/G09R'] =timetraces['GASM/G09R'].astype(float).reshape(timetraces['GASM/G09R'].size, 1)

        timetraces['GASM/C32R'] = np.asarray(timetraces['GASM/C32R'])
        timetraces['GASM/C32R'] =timetraces['GASM/C32R'].astype(float).reshape(timetraces['GASM/C32R'].size, 1)
        # timetraces['KT5P/POHM'] = np.asarray(timetraces['KT5P/BAR2'])
        timetraces['PT5P/BAR2'] = np.asarray(timetraces['PT5P/BAR2'])
        timetraces['PT5P/BAR2'] =timetraces['PT5P/BAR2'].astype(float).reshape(timetraces['PT5P/BAR2'].size, 1)

        timetraces['LIDX/NE0'] = np.asarray(timetraces['LIDX/NE0'])
        timetraces['LIDX/NE0'] = timetraces['LIDX/NE0'].astype(float).reshape(
            timetraces['LIDX/NE0'].size, 1)

        timetraces['LIDX/NEVL'] = np.asarray(timetraces['LIDX/NEVL'])
        timetraces['LIDX/NEVL'] = timetraces['LIDX/NEVL'].astype(float).reshape(
            timetraces['LIDX/NEVL'].size, 1)


        timetraces['SCAL/H98Y'] = np.asarray(timetraces['SCAL/H98Y'])
        timetraces['SCAL/H98Y'] = timetraces['SCAL/H98Y'].astype(float).reshape(
            timetraces['SCAL/H98Y'].size, 1)

        # fname = 'SHOT_91986_subdivpress'
        # plt.figure(fname)
        # plt.scatter(x, y10, color='red', label="PT5P/BAR2", s=10)
        # fxlabel = 'Time [s]'
        # fylabel = 'mbar'
        # # plt.show()
        # # raise SystemExit
        # ftitle = 'Time Traces - '+str(nshot[i])
        # plt.suptitle(ftitle, fontsize=11)

        # plt.ion()
        fname = 'SHOT_' + str(shot)
        fig = plt.figure(fname)
        ftitle = 'Time Traces - ' + str(nshot[i])
        plt.suptitle(ftitle, fontsize=11)


        # f, (ax1, ax2, ax3,ax4,ax5,ax6,ax7,ax8) = plt.subplots(8, sharex=True)
        # PLOT 1
        ax1 = plt.subplot(811)
        # xy = get_axis_limits(ax1)
        # print(xy)

        plt.text(0.15, 0.85, "A", fontweight="bold", transform=ax1.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay((np.asarray(timetraces['KG1V/LID3'])), 17, 1),
                    color='red', label="KG1V", s=10)
        fxlabel = 'Time [s]'
        fylabel = '$part/m^{-2}$'
        plt.locator_params(axis='y', nbins=4)
        # plt.locator_params(axis='y',nbins=4)
        # plt.xlabel(fxlabel,{'color': 'k','size': 11})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # plt.setp(ax1.get_xticklabels(), visible=False)
        plt.legend(loc=0, prop={'size': 8})
        # ax1.yaxis.set_minor_locator(AutoMinorLocator())
        # ax1.xaxis.set_minor_locator(AutoMinorLocator())
        # end plot 1
        # PLOT 2

        ax2 = plt.subplot(812, sharex=ax1)
        plt.text(0.15, 0.85, "B", fontweight="bold", transform=ax2.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['EFIT/POHM']), 33, 1),
                    color='red', label="POHM", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['NBI/PTOT']), 33, 1),
                    color='blue', label="NBI", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['SCAL/PRAD']), 7, 1),
                    color='blue', label="PRAD", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['BOLO/TOPI']), 33, 1),
                    color='yellow', label="TOPI", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['BOLO/TOBU']), 33, 1),
                    color='green', label="TOBU", s=4)
        fxlabel = 'Time [s]'
        fylabel = 'MW'
        plt.locator_params(axis='y', nbins=4)
        # plt.xlabel(fxlabel,{'color': 'k','size': 11})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # plt.setp(ax2.get_xticklabels(), visible=False)
        plt.legend(loc=0, prop={'size': 8})
        # start, end = ax2.get_xlim()
        # ax2.yaxis.set_ticks(np.arange(0, end, 4))
        ax2.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax2.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.1f" % x, locs * 1E-6)))
        # end plot 2
        # PLOT 3
        ax3 = plt.subplot(813, sharex=ax1)
        plt.text(0.15, 0.85, "C", fontweight="bold", transform=ax3.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['KY4D/ITOT']), 17, 1),
                    color='red', label="iTOT", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['KY4D/OTOT']), 17, 1),
                    color='blue', label="oTOT", s=4)
        fxlabel = 'Time [s]'
        fylabel = '$10^{22} part/s$'
        plt.locator_params(axis='y', nbins=4)
        # plt.xlabel(fxlabel,{'color': 'k','size': 11})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # plt.setp(ax3.get_xticklabels(), visible=False)
        plt.legend(loc=0, prop={'size': 8})
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.1f" % x, locs * 1E-22)))
        ax3.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax3.xaxis.set_minor_locator(AutoMinorLocator(4))
        # end plot 3
        # PLOT 4
        # share x only
        ax4 = plt.subplot(814, sharex=ax1)
        plt.text(0.15, 0.85, "D", fontweight="bold", transform=ax4.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['GASM/G09R']), 17, 1),
                    color='red', label="G09R", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['GASM/C32R']), 17, 1),
                    color='blue', label="C32R", s=4)
        # make these tick labels invisible
        # plt.setp(ax4.get_xticklabels(), fontsize=8)
        fxlabel = 'Time [s]'
        fylabel = '$10^{22} part/s$'
        plt.locator_params(axis='y', nbins=4)
        plt.xlabel(fxlabel, {'color': 'k', 'size': 8})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        ax4.yaxis.set_label_position("right")
        ax4.yaxis.tick_right()
        # locs,labels = xticks()
        # xticks(locs, map(lambda x: "%.3f" % x, locs))
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.1f" % x, locs * 1e-22)))
        # ax4.tick_params(axis='x',which='minor',bottom='off')
        ax4.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax4.xaxis.set_minor_locator(AutoMinorLocator(4))
        plt.legend(loc=0, prop={'size': 8})

        # PLOT 5
        # share x only
        ax5 = plt.subplot(815, sharex=ax1)

        plt.text(0.15, 0.85, "E", fontweight="bold", transform=ax5.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['LIDX/TE0']), 17, 1),
                    color='red', label="TE0", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['LIDX/TEVL']), 17, 1),
                    color='blue', label="TEVL", s=4)
        # make these tick labels invisible
        # plt.setp(ax5.get_xticklabels(), fontsize=8)
        fxlabel = 'Time [s]'
        fylabel = 'keV'
        plt.locator_params(axis='y', nbins=4)
        plt.xlabel(fxlabel, {'color': 'k', 'size': 8})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # locs,labels = xticks()
        # xticks(locs, map(lambda x: "%.3f" % x, locs))
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.1f" % x, locs * 1e-3)))
        # ax4.tick_params(axis='x',which='minor',bottom='off')
        ax5.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax5.xaxis.set_minor_locator(AutoMinorLocator(4))
        plt.legend(loc=0, prop={'size': 8})

        # PLOT 6
        # share x only
        ax6 = plt.subplot(816, sharex=ax1)

        plt.text(0.15, 0.85, "F", fontweight="bold", transform=ax6.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['LIDX/NE0']), 17, 1),
                    color='red', label="NE0", s=4)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['LIDX/NEVL']), 17, 1),
                    color='blue', label="NEVL", s=4)
        # make these tick labels invisible
        # plt.setp(ax6.get_xticklabels(), fontsize=8)
        fxlabel = 'Time [s]'
        fylabel = '$10^{19} m^{-3}$'
        plt.locator_params(axis='y', nbins=4)
        plt.xlabel(fxlabel, {'color': 'k', 'size': 8})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # locs,labels = xticks()
        # xticks(locs, map(lambda x: "%.3f" % x, locs))
        locs, labels = yticks()
        yticks(locs, list(map(lambda x: "%.1f" % x, locs * 1e-19)))
        # ax4.tick_params(axis='x',which='minor',bottom='off')
        ax6.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax6.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax6.yaxis.set_label_position("right")
        ax6.yaxis.tick_right()
        plt.legend(loc=0, prop={'size': 8})

        # PLOT 7
        # share x only
        ax7 = plt.subplot(817, sharex=ax1)
        # print(timetraces['KT5P/BAR2'])
        # raise SystemExit
        plt.text(0.15, 0.85, "G", fontweight="bold", transform=ax7.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['PT5P/BAR2']), 3,
                                   1) * 1e4,
                    color='red', label="PT5P/BAR2", s=4)
        # make these tick labels invisible
        # plt.setp(ax6.get_xticklabels(), fontsize=8)
        fxlabel = 'Time [s]'
        fylabel = '$10^{-4} mbar$'
        plt.locator_params(axis='y', nbins=4)
        plt.xlabel(fxlabel, {'color': 'k', 'size': 8})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # locs,labels = xticks()
        # xticks(locs, map(lambda x: "%.3f" % x, locs))
        # locs, labels = yticks()
        # yticks(locs, list(map(lambda x: "%.1f" % x, locs * 1e4)))
        # ax4.tick_params(axis='x',which='minor',bottom='off')
        # ax7.yaxis.set_minor_locator(AutoMinorLocator(4))
        # ax7.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax7.set_ylim([max(savitzky_golay(np.asarray(timetraces['PT5P/BAR2']), 3,
                                         1)) * 1e4 / 1.2,
                      max(savitzky_golay(np.asarray(timetraces['PT5P/BAR2']), 3,
                                         1)) * 1e4])
        # ax7.yaxis.set_label_position("right")
        # ax7.yaxis.tick_right()
        plt.legend(loc=0, prop={'size': 8})

        # PLOT 7
        ax8 = plt.subplot(818, sharex=ax1)
        plt.text(0.15, 0.85, "H", fontweight="bold", transform=ax8.transAxes)
        plt.scatter(x - 40,
                    savitzky_golay(np.asarray(timetraces['SCAL/H98Y']), 17, 1),
                    color='red', label="H98Y", s=8)
        fxlabel = 'Time [s]'
        fylabel = ''
        plt.locator_params(axis='y', nbins=4)
        plt.xlabel(fxlabel, {'color': 'k', 'size': 11})
        plt.ylabel(fylabel, {'color': 'k', 'size': 8})
        # plt.setp(ax7.get_xticklabels(), visible=False)
        plt.legend(loc=0, prop={'size': 8})
        ax8.yaxis.set_label_position("right")
        ax8.yaxis.tick_right()
        ax8.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax8.xaxis.set_minor_locator(AutoMinorLocator(4))

        plt.subplots_adjust(wspace=0, hspace=0)
        if save is True:
            plt.savefig('./figures/' + fname + '.eps', format='eps')
            plt.savefig('./figures/' + fname)
        t = Toggle(fig)
        fig.canvas.mpl_connect("button_press_event", t.toggle)
        plt.show()
        # continue
        #
        # # if i==1:
        # #     cut = (x-40 == 40.8) & (x-40 == 10.8) & (x-40 == 12) & (x-40 == 13)
        # # else:
        # #     cut = (x - 40 == 9) & (
        # #     x - 40 == 10) & (
        # #           x - 40 == 11) & (
        # #           x - 40 == 12)
        #
        #
        # if i==0:
        #     cut1=[10,11]
        #     x1=0.4
        #     x2=0.7
        #     cut2=[12.3,13]
        # else:
        #     cut1=[8.5,9.5]
        #     x1=0.2
        #     x2=0.55
        #     cut2=[11,12]
        # for i in range(0,len(cut1)):
        #
        #     ax1.axvline(x=cut1[i],ymin=-1.2,ymax=1,  c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax2.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax3.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax4.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax5.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax6.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax7.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #     ax8.axvline(x=cut1[i],ymin=-1.2,ymax=1, c="black", linewidth=2, zorder=0, linestyle="dashed")
        #
        #     ax1.axvline(x=cut2[i],ymin=-1.2,ymax=1,  c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax2.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax3.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax4.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax5.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax6.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax7.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        #     ax8.axvline(x=cut2[i],ymin=-1.2,ymax=1, c="red", linewidth=2, zorder=0, linestyle="dashed")
        # plt.text(x1, 0.95, "LFE", fontweight="bold", color="black", transform=ax8.transAxes)
        # plt.text(x2, 0.95, "HFE", fontweight="bold", color="red", transform=ax7.transAxes)

        # plt.subplots_adjust(wspace=0, hspace=0)
        # plt.savefig('./figures/'+fname+'.eps', format='eps')
        # plt.savefig('./figures/'+fname)
        # plt.show()


def find_nearest(array, value):
    """

    :param array:
    :param value:
    :return: returns value and index of the closest element in the array to the value
    """
    import numpy as np
    import math

    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (
            idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(
            value - array[idx])):
        return array[idx - 1], idx - 1
    else:
        return array[idx], idx


def find_psol(nshot, ntime):
    import pandas as pd
    import numpy as np

    psol_dict = dict()
    for i in range(len(nshot)):

        shot = int(nshot[i])
        time = float(ntime[i])
        delta = 0.5
        # print(shot,time)
        # init_plotting()
        # filename='/u/bviola/work/Python/EDGE2D/exp_data/Interp_Params_LID3_'+str(shot)+'_may2018.dat'
        filename = '/u/bviola/work/Python/EDGE2D/exp_data/Interp_Params_LID3_' + str(
            shot) + '.dat'

        # Get data
        timetraces = pd.read_csv(filename, skiprows=[0, 1],
                                 delim_whitespace=True)

        fieldnames = list(timetraces.columns.values)
        fieldnames = [x.strip() for x in fieldnames]
        if i == 0:
            print(fieldnames)

        # raise SystemExit
        x = timetraces['Time_LID3'].values
        value_1, index_t1 = find_nearest(x, time - delta)
        value_2, index_t2 = find_nearest(x, time + delta)

        TOPI = timetraces['BOLO/TOPI'].values  # total radiation
        TOBU = timetraces['BOLO/TOBU'].values  # bulk radiation
        # ii=isinstance([x for x in TOBU], numbers.Number)
        # TOBU=TOBU[ii]

        # TOBU = timetraces['BOLO/TOBU'].values # bulk radiation
        # TOBU_clean = [x for x in TOBU if x.isdigit()]
        # TOBU = [x for x in TOBU if x.isdigit()]
        # TOBU = [float(x) for x in TOBU if ]

        # y1 = timetraces['KG1V/LID3']
        POHM = timetraces['EFIT/POHM'].values
        PTOT = timetraces['NBI/PTOT'].values
        # y6 = timetraces['KY4D/ITOT']
        # y7 = timetraces['KY4D/OTOT']
        # y8 = timetraces['GASM/G09R']
        # y9 = timetraces['GASM/C32R']
        # y10 = timetraces['KT5P/BAR2']

        average_topi = np.median(TOPI[index_t1:index_t2])
        # TOBU_subset = [float(x) for x in TOBU[index_t1:index_t2]]
        average_tobu = np.median(TOBU[index_t1:index_t2])
        average_pohm = np.median(POHM[index_t1:index_t2])
        average_ptot = np.median(PTOT[index_t1:index_t2])

        Psol = average_ptot + average_pohm - (average_topi - average_tobu)

        psol_dict[str(shot)] = [Psol, time]
    return psol_dict


def read_eqdsk(nameFile, input_dict):
    import numpy as np
    import matplotlib.pyplot as plt

    print(nameFile)
    print(input_dict)
    # nameFileVessel = 'vessel_DTT.txt'
    nameFileVessel = '/u/bviola/work/JET/m15-20/exp/vessel_JET_csv.txt'
    DictParameters, DictCASEandGRIDDimension, DictNameComponent = DictList(
        List(nameFile), input_dict)
    #

    rdim = float(DictParameters["rdim"])
    rleft = float(DictParameters["rleft"])
    zmid = float(DictParameters["zmid"])
    zdim = float(DictParameters["zdim"])
    bcentr = float(DictParameters["bcentr"])
    rcentr = float(DictParameters["rcentr"])
    sibry = float(DictParameters["sibry"])
    simag = float(DictParameters["simag"])
    current = float(DictParameters["current"])
    fpol = [float(el) for el in DictNameComponent["fpol"]]
    rlim = DictNameComponent["rlim"]
    zlim = DictNameComponent["zlim"]
    fpol = DictNameComponent["fpol"]
    rbbbs = DictNameComponent["rbbbs"]
    zbbbs = DictNameComponent["zbbbs"]
    psirzm = DictNameComponent["psirzm"]
    rmaxis = float(DictParameters["rmaxis"])
    zmaxis = float(DictParameters["zmaxis"])
    psinorm = (psirzm - simag + sibry) / (-simag + sibry);
    nrgr = int(DictCASEandGRIDDimension["NW"])
    nzgr = int(DictCASEandGRIDDimension["NH"])
    rmax = rdim + rleft
    rmin = rleft
    zmax = (2 * zmid + zdim) / 2
    zmin = (2 * zmid - zdim) / 2
    Smoothpsirz = smoothPSI(psirzm, nrgr, nzgr)
    r_rect = np.linspace(rmin, rmax, nrgr)
    z_rect = np.linspace(zmin, zmax, nzgr)

    # XML_FILE(r_rect,z_rect,Smoothpsirz)
    # print(len(rbbbs))
    # print(len(zbbbs))
    # fig, ax = plt.subplots()
    # ax.contour(r_rect, z_rect, Smoothpsirz, 100)
    # # ax.contour(r_rect,z_rect,psirzm,100)
    # ax.plot(rbbbs, zbbbs, "ro")
    # ax.plot(rlim, zlim, "bo")
    # plt.show()

    return rdim, rleft, zmid, zdim, bcentr, current, rcentr, sibry, simag, fpol, rlim, zlim, fpol, \
           rbbbs, zbbbs, psirzm, psinorm, nrgr, nzgr, rmax, rmin, zmax, zmin, Smoothpsirz, r_rect, z_rect, rmaxis, zmaxis


####

def get_magnetic_data_from_eqdsk(namefile, input_dict, filename):
    import numpy as np
    import pickle

    rdim, rleft, zmid, zdim, bcentr, current, rcentr, sibry, simag, fpol, rlim, zlim, fpol, rbbbs, zbbbs, psirzm, psinorm, nrgr, nzgr, rmax, rmin, zmax, zmin, Smoothpsirz, r_rect, z_rect, rmaxis, zmaxis = read_eqdsk(
        namefile, input_dict)
    # rdim,rleft,zmid,zdim,bcentr,rcentr,sibry,simag,fpol,rlim,zlim,fpol,rbbbs,zbbbs, psirzm,psinorm,nrgr,nzgr,rmax,rmin,zmax,zmin,Smoothpsirz,r_rect,z_rect = read_eqdsk(namefile,input_dict)
    #
    r2D = np.zeros((nrgr, nzgr))
    z2D = np.zeros((nrgr, nzgr))

    for ii in range(0, nrgr):
        r2D[ii, :] = r_rect
    for ii in range(0, nzgr):
        z2D[ii, :] = z_rect
    z2D = np.transpose(z2D)
    # %compute fields
    # %add sibry, that is the boundary flux ->> level Psi=sibry is the separatrix
    psirz = (psirzm + sibry)
    # print(psirz.shape)
    n_fpol = len(fpol)
    Psi = np.transpose(np.linspace(sibry, simag, n_fpol))

    # Br
    dz = z_rect[2] - z_rect[0]
    Br = np.zeros((nrgr, nzgr))
    for ii in range(1, nzgr - 1):
        # %Br(:,jj)=-((psirz(:,jj+1)-psirz(:,jj-1))/(z_rect(jj+1)-z_rect(jj-1)))./r_rect;
        # %Br(ii,:)=smooth(-((psirz(ii+1,:)-psirz(ii-1,:))/(z_rect(ii+1)-z_rect(ii-1)))./r_rect,0.1,'rloess');
        # Br[ii,:]=smooth(-((psirz[ii+1,:]-psirz[ii-1,:])/(z_rect[ii+1]-z_rect[ii-1]))/r_rect[ii],5)
        Br[ii, :] = -((psirz[ii + 1, :] - psirz[ii - 1, :]) / (
                    z_rect[ii + 1] - z_rect[ii - 1]) / r_rect)

    # %    Br(:,jj)=-((psirz(:,jj+1)-psirz(:,jj-1))/dz)./r_rect';

    Br[0, :] = -((psirz[1, :] - psirz[0, :]) / (z_rect[1] - z_rect[0])) / r_rect
    Br[-1, :] = -((psirz[-1, :] - psirz[-2, :]) / (
                z_rect[-1] - z_rect[-2])) / r_rect
    # for jj in range(0,nrgr):
    #     # Br[:,jj]=smooth(Br[:,jj],5)
    #     Br[:,jj]=Br[:,jj]
    # return Br
    #
    #     #Bz
    Bz = np.zeros((nrgr, nzgr))
    for ii in range(1, nzgr - 1):
        #     #%Bz(:,jj)=-((psirz(:,jj+1)-psirz(:,jj-1))/(z_rect(jj+1)-z_rect(jj-1)))./r_rect;
        #     #%Bz(ii,:)=smooth(-((psirz(ii+1,:)-psirz(ii-1,:))/(z_rect(ii+1)-z_rect(ii-1)))./r_rect,0.1,'rloess');
        #         Bz[ii,:]=smooth(-((psirz[ii+1,:]-psirz[ii-1,:])/(z_rect[ii+1]-z_rect[ii-1]))/r_rect[ii],5)
        Bz[:, ii] = ((psirz[:, ii + 1] - psirz[:, ii - 1]) / (
                    r_rect[ii + 1] - r_rect[ii - 1])) / r_rect
    #     #%    Br(:,jj)=-((psirz(:,jj+1)-psirz(:,jj-1))/dz)./r_rect';
    #
    Bz[:, 0] = -(
                (psirz[:, 1] - psirz[:, 0]) / (r_rect[1] - r_rect[0])) / r_rect;
    Bz[:, -1] = ((psirz[:, -1] - psirz[:, -2]) / (r_rect[-1] - r_rect[-2])) / \
                r_rect[-1]
    # for jj in range(0,nzgr):
    # Bz[jj,:]=smooth(Bz[jj,:],5);
    # Bz[jj,:]=Bz[jj,:]
    #
    #
    # % d_psi=(f_max-sibry)/(n_fpol-1);
    d_psi = (simag - sibry) / (n_fpol - 1);
    # %enlarge the vector fpol to avoid problem at the boundary
    # fpol_tot=np.concatenate(fpol, fpol[-1]);
    fpol_tot = fpol.append(fpol[-1]);
    # %set vacuum toroidal field everywhere
    Bphi = np.ones((nrgr, nzgr)) * bcentr * rcentr / r2D

    pts_in = inpolygon(np.array(r2D), np.array(z2D), np.array(rbbbs),
                       np.array(zbbbs))
    #

    for ii in range(0, nrgr):
        for jj in range(0, nzgr):
            if pts_in[ii, jj] is True:
                ind = floor(
                    (psirz[ii, jj] - sibry) / (simag - sibry) * n_fpol) + 1
                if ind <= 0:
                    ind = 1
                if ind == 102:
                    ind = 101
                Bphi[ii, jj] = (fpol_tot[ind] + (
                            fpol_tot[ind + 1] - fpol_tot[ind]) * (
                                            psirz[ii, jj] - Psi[ind]) / d_psi) / \
                               r_rect[jj];

    #     #%definition of the input
    #     #%N.B: normalize the flux function to 2*pi!!!!!!!
    #     #% flux2D=-psirz/2/pi;
    #     #% flux2D=psirz/2/pi;
    flux2D = psirz;
    fluxnorm = psinorm;
    #
    # %smooth of the flux function
    # for jj in range(0,nzgr):
    #     flux2D[jj,:]=smooth(flux2D[jj,:],5);
    # %flux2D(jj,:)=smooth(flux2D(jj,:),0.1,'rloess');

    #
    # for jj in range(0,nzgr):
    #     flux2D[:,jj]=smooth(flux2D[:,jj],5);
    # %flux2D(:,jj)=smooth(flux2D(:,jj),0.1,'rloess');
    #
    #
    Br2D = Br;
    Bz2D = Bz;
    Bphi2D = Bphi;
    B_pol = np.sqrt(Br ** 2 + Bz ** 2);
    B_tot = np.sqrt(Br ** 2 + Bz ** 2 + Bphi2D ** 2);
    SH = B_pol / B_tot;
    #
    #

    with open('field_' + filename + '.pkl', 'wb') as f:
        pickle.dump(
            [B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2D,
             z2D, r_rect, z_rect], f)
    f.close()

    with open('mag_axis_coord_' + filename + '.pkl', 'wb') as f:
        pickle.dump([rmaxis, zmaxis], f)
    f.close()
    return B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2D, z2D, r_rect, z_rect, rmaxis, zmaxis


# def sprintf(buf, fmt, *args):
#     buf.write(fmt % args)

def write_magnetic_data(file_pickle, fileout, psioffset, invert=False,
                        normalize=False):
    import pickle
    import numpy.matlib
    import sys
    from math import pi

    with open('field_' + file_pickle + '.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        [B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2D,
         z2D, r_rect, z_rect] = pickle.load(f)
    f.close()

    with open('mag_axis_coord_' + file_pickle + '.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        [rmaxis, zmaxis] = pickle.load(f)
    f.close()
    if invert is True:
        flux2D = -flux2D

    if normalize is True:
        print('normalizing flux as  \n flux2D * (2 * pi)')

        flux2D = flux2D * (2 * pi)
        #

    flux2D = flux2D + psioffset

    with open('psi' + fileout, 'w') as f:
        # fmt=[np.matlib.repmat(' %1.4e', 1, flux2D.shape[1])]
        # np.savetxt(f, -np.transpose(flux2D),  '%1.4e')

        np.savetxt(f, (flux2D), '%1.4e')
        # sprintf(f,fmt,-np.transpose(flux2D))
    f.close()

    with open('r' + fileout, 'w') as f:
        # fmt=[np.matlib.repmat(' %1.4e', 1), '\n']
        np.savetxt(f, np.transpose(r_rect), ' %1.4e')
    f.close()

    with open('z' + fileout, 'w') as f:
        # fmt=[np.matlib.repmat(' %1.4e', 1), '\n']
        np.savetxt(f, np.transpose(z_rect), ' %1.4e')
        # sprintf(f,fmt,np.transpose(z_rect))
    f.close()

    return B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2D, \
           z2D, r_rect, z_rect, rmaxis, zmaxis


def define_input_matrix_for_mesh(filein):
    import scipy.interpolate as interp
    import numpy as np
    from numpy.matlib import repmat
    from math import pi

    R = np.loadtxt('r' + filein)

    Z = np.loadtxt('z' + filein)

    PSI = np.loadtxt('psi' + filein)

    Rstep = (R[-1] - R[0]) / (len(R) - 1) / 3;
    # R1=[R[0]:Rstep:R[-1]];

    R1 = np.arange(R[0], R[-1], Rstep)
    Zstep = (Z[-1] - Z[0]) / (len(Z) - 1) / 3;
    # Z1=np.transpose([Z[0]:Zstep:Z[-1]]);
    Z1 = np.transpose((np.arange(Z[0], Z[-1], Zstep)))

    psifun = interp.interp2d(R, Z, PSI)
    PSI1 = psifun(R1, Z1)
    # [dPSI1dR, dPSI1dz] = np.gradient(PSI1, R1, Z1);
    # if I run [dPSI1dR, dPSI1dz] = np.gradient(PSI1) it returns same values as
    # Matlab but the variables must be switched
    [dPSI1dz, dPSI1dR] = np.gradient(PSI1, Z1, R1);

    # [dPSI1dR,dPSI1dz]=gradient(PSI1,R1,Z1);
    Rmatr = repmat(R1, len(Z1), 1);
    Zmatr = repmat(Z1, 1, len(R1));
    BR1 = -dPSI1dz / (2 * pi * Rmatr);
    Bz1 = dPSI1dR / (2 * pi * Rmatr);
    # % if block in case R[0] == 0
    if (R[0] < 1.e-03):
        BR1[:, 0] = BR1[:, 1] + (BR1[:, 1] - BR1[:, 2]) * (R[0] - R[1]) / (
                    R[1] - R[2]);
        Bz1[:, 0] = Bz1[:, 1] + (Bz1[:, 1] - Bz1[:, 2]) * (R[0] - R[1]) / (
                    R[1] - R[2]);

    [dBR1dz, dBR1dR] = np.gradient(BR1, Z1, R1);
    [dBz1dz, dBz1dR] = np.gradient(Bz1, Z1, R1);

    # recomputing values over smaller matrices
    dPSIdRfun = interp.interp2d(R1, Z1, dPSI1dR)
    dPSIdR = dPSIdRfun(R, Z)

    dPSIdZfun = interp.interp2d(R1, Z1, dPSI1dz)
    dPSIdz = dPSIdZfun(R, Z)

    BRfun = interp.interp2d(R1, Z1, BR1)
    BR = BRfun(R, Z)

    Bzfun = interp.interp2d(R1, Z1, Bz1)
    Bz = Bzfun(R, Z)

    dBRdRfun = interp.interp2d(R1, Z1, dBR1dR)
    dBRdR = dBRdRfun(R, Z)

    dBRdzfun = interp.interp2d(R1, Z1, dBR1dz)
    dBRdz = dBRdzfun(R, Z)

    dBzdRfun = interp.interp2d(R1, Z1, dBz1dR)
    dBzdR = dBzdRfun(R, Z)

    dBzdzfun = interp.interp2d(R1, Z1, dBz1dz)
    dBzdz = dBzdzfun(R, Z)

    magdata = np.concatenate(
        (PSI, BR, Bz, dPSIdR, dPSIdz, dBRdR, dBRdz, dBzdR, dBzdz), 0);

    np.savetxt('mag_data_py', magdata, ' %1.4e')
    Rmesh = np.transpose(R);
    np.savetxt('R_mesh_py', Rmesh, ' %1.4e')
    np.savetxt('Z_mesh_py', Z, ' %1.4e')

    return R, Z, PSI, BR, Bz, dPSIdR, dPSIdz, dBRdR, dBRdz, dBzdR, dBzdz


def read_vessel(filename):
    """
    reads vessel file written as two column separated by ;

    first line is a comment
    :param filename:
    :return:
    """
    with open(filename, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        # col = list(zip(*reader))[1]
        csv_dic = []

        for row in reader:
            csv_dic.append(row);
        # print(csv_dic)
        col1 = []
        col2 = []

        for row in csv_dic:
            col1.append(row[0])
            col2.append(row[1])
        dummy = np.array(col1)
        # print(dummy)
        dummy2 = np.array(col2)
        dummy2 = [float(i) for i in dummy2]
        z_ves = -np.asarray(dummy2)
        dummy = [float(i) for i in dummy]
        r_ves = np.asarray(dummy)
    f.close()
    return r_ves, z_ves



def initread(shot,userid,seq):
  """
  function that uses function of the ppf module
  it initialize the reading of a ppf file
  ppf file can be private, punlic or synthetic (coming from edge2d for example)

  Usage:
  initread(shot,userid,seq)

  """
  ppfsetdevice('JET')
  #print('ok')
  ppfuid(userid,'r')
  ier=ppfgo(int(shot),int(seq))
#@staticmethod

def getdata(shot,dda,dtype,uid=None,seq=None):
    if seq is None:
        ier = ppfgo(shot, seq=0)
    else:
        ier = ppfgo(shot, seq=seq)
    if uid is None:
        ppfuid('jetppf', rw="R")
    else:
        ppfuid(uid, rw="R")
    ihdata, iwdata, data, x, time, ier = ppfget(shot, dda, dtype)
    pulse, seq, iwdat, comment, numdda, ddalist, ier = ppfinf(comlen=50,
                                                              numdda=50)

    name=dict()
    name['ihdata']=ihdata
    name['iwdata']=iwdata
    name['data']=data
    name['x']=x
    name['time']=time
    name['ier']=ier
    name['seq']=seq
    name['pulse']=pulse
    name['dda']=dda
    name['dtype']=dtype
    return name,seq


def Getdata(pulse, dda,dtype,sequence,user):

    '''
     function that reads a ppf file
    it can be used to read synthetic edge2d ppf files
    ARGS
    pulse1 :=  pulse

    dda := string e.g. 'kg1v'
    dtype:= string e.g. 'lid3'
    RETURNS
    '''
    #initialize pulse an sequence
    initread(int(pulse),user,int(sequence))
    data,x,t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier=ppfdata(int(pulse),dda,dtype,seq=int(sequence),uid=user,device="JET",fix0=0,reshape=0,no_x=0,no_t=0)
    #ihdat,iwdat,data,x,t,ier=ppfget(int(pulse),dda,dtype)
    #pulse,seq,iwdat,comment,numdda,ddalist,ier=ppfinf(comlen=50,numdda=50)
    # info,cnfo,ddal,istl,pcom,pdsn,ier=pdinfo(pulse,seq)
    # istat,ier = ppfgsf(pulse,seq,dda,dtype,mxstat=1)
    return{'dunits':dunits,
            'desc':desc,
          'xunits':xunits,
          'data':data,
          'x':x,
          't':t,
          'ier':ier,
          'sequence':seq}
###############################################
def write_interp_data(pulse,diag_json=None, tmin=None,tmax=None):
    if diag_json is None:
        diag_json ='diag_list.json'
    else:
        diag_json=diag_json

    if tmin is None:
        tmin =48
    else:
        tmin=tmin

    if tmax is None:

        tmax = 54
    else:
        tmax=tmax

    ppfuid("jetppf", "r")

    with open(diag_json, mode='r', encoding='utf-8') as f:
    # Remove comments from input json
        with open("temp.json", 'w') as wf:
            for line in f.readlines():
                if line[0:2] == '//' or line[0:1] == '#':
                    continue
                wf.write(line)

    with open("temp.json", 'r') as f:
        input_dict = json.load(f, object_pairs_hook=OrderedDict)

    ihdat, iwdat, lid3, x_data, lid3_time, \
        ier = ppfget(pulse, 'kg1v', 'lid3')
    units = []
    names = []
    dataname = []
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    path = '/u/bviola/work/Python/EDGE2D/exp_data'
    filename='Interp_Params_LID3_'+str(pulse)+'_python.dat'
    ncol = 0

    dataDF = pd.DataFrame()
    for key, value in input_dict.items():
        for value in input_dict[key]:
            ncol = ncol+1
            dda=key
            dtype=value


            data_name =   'data_'+key+ '_'+value
            time_name =   't_data_'+key+ '_'+value
            unit_name =   'units_'+key+ '_'+value

            vars()[data_name],x,vars()[time_name],nd,nx,nt,vars()[unit_name],xunits,tunits,desc,comm,seq,ier = \
                ppfdata(pulse,dda,dtype,seq=0,uid="jetppf",device="JET",fix0=0,reshape=0,no_x=0,no_t=0)
    #
            if ((dda == 'KG1V') & (dtype == 'LID3')):
                #
                dummy,ix1 = find_nearest(lid3_time,tmin)
                dummy, ix2 = find_nearest(lid3_time,tmax)
                nrow = ix2 - ix1 + 1
                #find_indices doesn't work well with floats
                # ix1 = find_indices(lid3_time, lambda e: e == tmin)
                # ix2 = find_indices(lid3_time, lambda e: e == tmax)
                # nrow = max(ix2) - min(ix1) + 1
    #
            vars()[data_name+ '_interp'] = np.zeros(np.size(lid3_time))
            if vars()[data_name].size:
                vars()[data_name + '_interp'] = np.interp(lid3_time,vars()[time_name],vars()[data_name])
    #
            units.append(vars()[unit_name])
            names.append(key + '/' + value)
            dataname.append('data_'+key+ '_'+value)

            data = pd.Series(vars()[data_name + '_interp'])
            dataDF[key + '/' + value] = data.values


    units.insert(0,'s')
    dataDF['Time_LID3'] = lid3_time

    # get a list of columns
    cols = list(dataDF)
    # move the column to head of list using index, pop and insert
    cols.insert(0, cols.pop(cols.index('time/LID3')))
    dataDF = dataDF.ix[:,cols]

    dataDF = dataDF.iloc[ix1:ix2]

    dataDF.to_csv(path + '/' +filename, index=False, header=True, sep='\t',float_format='%.5f')
    units = '\t '.join(units)
    title = '\t '.join([str(pulse) , str(tmin) , str(tmax) , str(ncol), str(nrow), filename, str(time)])

    with Prepender(path + '/' +filename) as f:
        #write lines in reversed order
        f.write_line(str(units))
        f.write_line(str(title))


    # list(dataDF)
    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.plot(dataDF['time/LID3'], dataDF['S3AD/AD35'])
    # plt.plot(dataDF['time/LID3'], dataDF['EDG8/TBEO'])
    # plt.show()


    print('Interpolated traces written to ... ' \
           , path + '/' + filename )


def test_routine_eqdsk():
    # m15-20
    # nshot = ['91986','92121','92123']
    # m18-20
    nshot = ['84600', '84599', '84598']
    ntime = ['51.77', '51.27203', '51.422127']

    # plot_time_traces(nshot,save=False)

    psol_dict = find_psol(nshot, ntime)
    for keys, values in psol_dict.items():
        print(keys)
        print(values)

    # raise SystemExit

    # nameFile = '/u/bviola/work/JET/m15-20/exp/g_p92121_t51.7325_mod.eqdsk'
    # nameFile = '/u/bviola/work/JET/m15-20/exp/g_p92121_t49.445_mod.eqdsk';
    nameFile = '/u/bviola/work/JET/90541/90541_t61d000_Clone_CNL_eq.mat_33x33-JET.eqdsk'
    vessel = '/u/bviola/work/JET/m15-20/exp/vessel_JET_csv.txt'

    # input_dict = {'fixfree': False, 'efit': True}
    # nameFile = '/u/bviola/work/JET/m15-20/exp/92121/g_p92121_t51.7325'
    # nameFile = '/u/bviola/work/JET/m15-20/81472/eqdsk_81472_HFE.eqdsk'
    input_dict={'fixfree': True, 'efit': False}

    # read eqdsk
    # rdim, rleft, zmid, zdim, bcentr, current, rcentr, sibry, simag, fpol, rlim, zlim, fpol, rbbbs, zbbbs, psirzm, psinorm, nrgr, nzgr, rmax, rmin, zmax, zmin, Smoothpsirz, r_rect, z_rect, rmaxis, zmaxis = read_eqdsk(nameFile, input_dict)

    # get_magnetic_data_from_eqdsk(nameFile, input_dict,'HFE_81472')

    B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2D, z2D, r_rect, z_rect, rmaxis, zmaxis = get_magnetic_data_from_eqdsk(
        nameFile, input_dict, 'LFE_81472')

    # plot contour to find offset
    # r_ves, z_ves = read_vessel(vessel)
    # from math import pi
    # fig, ax = plt.subplots()
    # psioffset=8.219 # HFE
    psioffset = 7.4032  # RFE

    # # CS = ax.contour(r_rect, z_rect, flux2D + psioffset,
    # #                 [1.15, 1.16, 1.17, 1.18, 1.2])
    # # CS = ax.contour(r_rect, z_rect, -(flux2D/ (2 * pi)) + psioffset,40)
    # CS = ax.contour(r_rect, z_rect, -(flux2D) + psioffset,180)
    # plt.clabel(CS, inline=1, fontsize=10)
    # ax.contour(r_rect,z_rect,psirzm,100)
    # ax.plot(r_ves, z_ves, "k")
    # ax.plot(rbbbs, zbbbs, "ro")
    # ax.plot(rlim, zlim, "bo")
    # plt.show()

    # write magnetic data
    B_pol, B_tot, Bphi2D, B_pol, Br2D, Bz2D, flux2D, fluxnorm, SH, r2, z2D, \
    r_rect, z_rect, rmaxis, zmaxis = write_magnetic_data('LFE_81472',
                                                         'LFEexp_JET_python',
                                                         psioffset,
                                                         invert=True,
                                                         normalize=True)
    # raise SystemExit

    # pulselist = [90000, 90001, 90002, 90004]
    # pulselist = [90004]
    # folder = '/home/bviola/ccfepc/T/mvoinea/2MA/'
    # read_polarimetry_file(pulselist,folder)
    #
    R, Z, PSI, BR, Bz, dPSIdR, dPSIdz, dBRdR, dBRdz, dBzdR, dBzdz = define_input_matrix_for_mesh(
        'LFEexp_JET_python')

    # raise SystemExit
    # print(SH[0,0:5])
    # 84600
    # [5195251.2989958655, 51.77]
    # 84598
    # [10439263.829129374, 51.422127]
    # 84599
    # [6778612.634441204, 51.27203]
    # print(psol_dict)
    # plot_time_traces(nshot)
    #
def test_write_interp_data(pulse):
    write_interp_data(pulse, diag_json=None, tmin=None, tmax=None)

def main():
    """
    Main function, for use in testing or for command line use
    """



if __name__== "__main__":

    debug_map = {0: logging.INFO,
                1: logging.WARNING,
                2: logging.DEBUG,
                3: logging.ERROR}

    logger = logging.getLogger(__name__)


    logging.root.setLevel(level=debug_map[0])


    # pulselist = []
    # # pulselist.append([91986,'black'])
    # # pulselist.append([92121,'red'])
    # # pulselist.append([92123,'blue'])
    # pulselist.append([92877])
    #
    # # filename = 'vert_ch.json'
    # # filename = 'vert_ch_new2.json'
    # filename = 'comparison-KG1_jetppf_bviola.json'
    # # filename = 'horz_ch_new.json'
    # # filename = 'main_parameters_new.json'
    # print('reading {} '.format(filename))
    # plot_time_traces(filename,pulselist)
    #
    #
    # plt.show()
    # raise SystemExit
    # #dda='KG1V'
    # #pulse1=92026
    # ## pulse2=92028
    # ## pulseSpec, userlist, numofseqlist, seqlist,datelist=create_database_4_dda(dda,pulse1,pulse2)
    # ##
    #
    # #pulseSpec, userlist, numofseqlist, seqlist,datelist=create_database_4_dda(dda,pulse1,pulse2=None)
    # ## print(pulseSpec)
    # ## print(userlist)
    # ## print(numofseqlist)
    # ## print(seqlist)
    # ## print(datelist)
    #
    # #show_database_4_dda(pulseSpec, userlist, numofseqlist, seqlist,datelist)
    #
    # #raise SystemExit
    # # # extract_cormat_history("/home/aboboc/LIB.OUTPUT/diary.2016",'cormat_out.txt')
    # # extract_cormat_history("/home/aboboc/LIB.OUTPUT/diary.2017",
    # #                        'cormat_out.txt')
    # # extract_cormat_history("/home/aboboc/LIB.OUTPUT/cormat.diary",
    # #                        'cormat_out.txt')
    # #
    # # extract_kg1lh_history('/work/bviola/intershot/run/kg1l/logbook.txt',
    # #                       'kg1l_out.txt')
    # # extract_kg1lh_history('/work/bviola/intershot/run/kg1h/logbook.txt',
    # #                       'kg1h_out.txt')
    # # extract_kg1py_history('/work/bviola/Python/KG1_code/python/run_out.txt',
    # #                       'kg1py_out.txt')
    # # # raise SystemExit
    # #
    # # cormat_DF = create_database('/common/chain1/kg1/cormat_out.txt')
    # # kg1l_DF = create_database('/common/chain1/kg1/kg1l_out.txt')
    # # kg1h_DF = create_database('/common/chain1/kg1/kg1h_out.txt')
    # # kg1py_DF = create_database('/common/chain1/kg1/kg1py_out.txt')
    # # pulse = 92025
    # # pulse = 90652
    # # pulse = 90998
    # pulse = 90344
    # # check_pulse_in_database(pulse,cormat_DF)
    # # check_pulse_in_database(pulse,kg1l_DF)
    # # check_pulse_in_database(pulse,kg1h_DF)
    # # check_pulse_in_database(pulse,kg1py_DF)
    # # #
    database_list = []
    # # database_list.append('./test_cormat_database.txt')
    database_list.append('/common/chain1/kg1/cormat_out.txt')
    database_list.append('/common/chain1/kg1/kg1l_out.txt')
    database_list.append('/common/chain1/kg1/kg1h_out.txt')
    database_list.append('/common/chain1/kg1/kg1py_out.txt')
    # #
    #
    # check_pulse_in_database_list(pulse, database_list)
    #
    # database_list = []
    #
    # database_list.append('/common/chain1/kg1/cormat_out.txt')
    # database_list.append('/common/chain1/kg1/kg1py_out.txt')
    #
    days=15
    #
    pulse_to_reprocess, pulse_not_to_reprocess, days,num = validated_pulses(days, database_list)
    print(pulse_to_reprocess, pulse_not_to_reprocess, days,num)
    raise SystemExit



    pulselist = [90000, 90001, 90002, 90004]
    # pulselist = [90004]
    folder = '/home/bviola/ccfepc/T/mvoinea/2MA/'
    mydictionary = read_polarimetry_file(pulselist, folder)
    # print(mydictionary)
    JPNlist = []
    det_coeff = []
    for key in mydictionary:
    # print("key: %s , value: %s" % (key, mydictionary[key]))
        print("JPN: %s" % key)
        JPNlist.append(int(key))
        if mydictionary[key]['channels']['I']:
            det_coeff.append(mydictionary[key]['channels']['I'][0])
        else:
            det_coeff.append(nan)
    print(det_coeff)
    print(JPNlist)
    from matplotlib.ticker import ScalarFormatter, FormatStrFormatter


    # plt.ticklabel_format(useOffset=False)
    # plt.figure()
    plt.plot(JPNlist,det_coeff,'*')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    plt.show()


    # test_routine_eqdsk()

    # input_dict=test_write_interp_data(92123)
    # input_dict=test_write_interp_data(92121)
    # plot_time_traces_main([92123])

    # dataframe=database_list[0]
    # data=create_database(dataframe)
    # print('database list of shots',data['shot'])
    # # shots_database = pd.Series(list(data['shot']))
    # shots_database = list(data['shot'])
    # print('extracted list of shots',shots_database)
    # inlist = [i for i,x in enumerate(shots_database) if x == str(pulse)]
    # print(inlist)
    # index = data.index
    # in_list=index[inlist]
    # print(in_list)
    # print(data.loc[in_list])

    # inlist = [i for i, x in enumerate(checkinlist) if x]
    # print('index of selected shot in list',inlist)
    # dataframe
    # check_pulse_in_database_list(pulse, database_list)
    # check_pulse_validated_recently(pulse, database_list,date=None)

    #
    #
    # logging.info('')
    # logging.info('checking status FLAGS ')
    #
    # ppfuid('jetppf', "r")
    #
    # ppfssr(i=[0, 1, 2, 3])
    #
    # channels = arange(0, 8) + 1
    # SF_list = []
    #
    #
    #
    #
    # for channel in channels:
    #     ch_text = 'lid' + str(channel)
    #
    #     st_ch = GetSF(pulse, 'kg1v', ch_text)
    #     st_ch = asscalar(st_ch)
    #     SF_list.append(st_ch)
    # logging.info('%s has the following SF %s', str(pulse), SF_list)
    
    
    
    # raise SystemExit
    #
    # ier = ppfgo()
    # ppfsetdevice("JET")
    # user='jetppf'
    # # pulse=92123
    # ppfuid(user, "r")
    # # time, date, ier = pdstd(pulse)
    # # datelist.append(date)
    # #
    # # iseq, nseq, ier = ppfdda(pulse, dda, mseq=1024)
    # # numofseqlist.append(nseq)
    # # seqlist.append(iseq)
    # shot = 90146
    # seq=144
    # # info, cnfo, ddal, istl, pcom, pdsn, err = pdinfo2(shot, seq)
    # info, cnfo, ndda, ddal, istl, pcom, pdsn, ier= pdinfo2(shot, seq)
    #
    # the_date = info[6]
    # the_time = info[5]
    # print(the_date)
    # print(the_time)
    # shot_date = info[1]
    # print(shot_date)
