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

import matplotlib.pyplot as plt
import numpy as np

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
    logger.debug('max pulse is {}'.format(str(maxpulse)))
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
            logger.info('\n')
            logger.info('user: {} has written {} ppf for shot {}'.format(user,
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
                logger.info('shot: {} user: {} date: {} seq:{} by: {}'.format(
                    str(pulse),
                    user,
                    str(datelist[k][numseq]),
                    str(seqlist[k][numseq]),
                    writtenby))
    else:

        for i, pulse in enumerate(pulseSpec):
            # s = 0
            for k, user in enumerate(userlist[i]):
                logger.info('\n')
                logger.info('user {} has written {} ppf for shot {}'.format(user,
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
                    logger.info('shot: {} user: {} date: {} seq:{} by: {}'.format(
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
        logger.info('{} is not in {} database!'.format(str(pulse),dataframe))
    else:
        for i in inlist:
            logger.info(
                '{} ppf created on {} by {} seq {} for pulse {} is in {}'.format(
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
    logger.info('start looking for ppf written for pulse {}'.format(str(pulse)))
    for index1 in range(0, len(dataframelist)):
        name = dataframelist[index1]
        logger.info('\n')
        logger.info('looking in database {}'.format(name))
        dataframe = create_database(name)
        shots_database = pd.Series(list(dataframe['shot']))
        pulse = str(pulse)
        checkinlist = shots_database.isin([pulse])
        inlist = [i for i, x in enumerate(checkinlist) if x]

        if any(inlist) is True:
            logger.info(' pulse {} found in database {}: \n'.format(pulse,
                                                              dataframe.name))
            for i in inlist:
                logger.info('\t \t \t    modified on {} by {} stored as {} ppf seq {}'.format(
                        dataframe['date'][i], dataframe['by'][i],
                        dataframe['user'][i],
                        dataframe['seq'][i]))
        else:
            logger.info('pulse {} not found'.format(str(pulse)))


def check_pulse_in_database_list(pulse, dataframelist):
    """

    updated version of check_pulse_in_database_list
    :param pulse:
    :param dataframe:
    :return:    given a pulse number and a list of panda dataframes
    checks if the pulse is in any of those databases
    i.e. if a KG1 related ppf has been written by the user
    """
    logger.info('start looking for ppf written for pulse {}'.format(str(pulse)))
    for index1 in range(0, len(dataframelist)):
        name = dataframelist[index1]
        logger.info('\n')
        logger.info('looking in database {}'.format(name))
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
            logger.info(' pulse {} found in database {}: \n'.format(pulse,
                                                              dataframe.name))

            for j,i in enumerate(in_list):
                if is_number_tryexcept(dataframe['seq'][i]):
                    logger.info('\t \t \t    new sequence written on {} by {} stored as {} ppf seq {}'.format(
                        dataframe['date'][i], dataframe['by'][i],
                        dataframe['user'][i],
                        dataframe['seq'][i]))
                else:
                    logger.info(
                        '\t \t \t    modified on {} by {} stored as {} ppf seq {}'.format(
                            dataframe['date'][i], dataframe['by'][i],
                            dataframe['user'][i],
                            dataframe['seq'][i]))
        else:
            logger.info('pulse {} not found'.format(str(pulse)))


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
        'looking for ppf written in the last {} days (from {})'.format(str(days),str(starttime)))
    for index1 in range(0, len(dataframelist)):
        name = dataframelist[index1]
        logger.info('\n')
        logger.info('looking in database {}'.format(name))
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
                logger.info(' found pulses that need reprocess \n')
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
                        '\t \t \t    pulse {} by {} stored as {} ppf seq {} date {}  need reprocessing'.format(
                            df_validated_FJ['shot'][i], df_validated_FJ['by'][i], df_validated_FJ['user'][i],
                            df_validated_FJ['seq'][i],df_validated_FJ['date'][i]))

                logger.info('\n')


                for i in range(0, df_validated_SF.__len__()):
                    pulse_not_to_reprocess.append(int(df_validated_SF['shot'][i]))
                    # logger.info(
                    #     '\t \t \t    pulse {} by {} stored as {} ppf seq {} date {} do NOT need reprocessing'.format(
                    #         df_validated_SF['shot'][i], df_validated_SF['by'][i], df_validated_SF['user'][i],
                    #         df_validated_SF['seq'][i],df_validated_SF['date'][i]))

            else:
                logger.info('\n')
                logger.info(' No pulses in the last {} days (from {}) need reprocess \n'.format(str(days),str(starttime)))
        else:
            logger.info('\n')
            logger.info(' No pulses in the last {} days (from {}) need reprocess \n'.format(str(days),str(starttime)))
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


def plot_time_traces(diag_json,pulselist,save=False):
    """
    this routines plots time traces of JET diagnostics

    uses as input JSON file that contains info on the diagnostic the user wants
    to plot and info on how to plot them (i.e. what window, linestyle, marker...)



    :param diag_json: standard set containing the diagnostic the user wants to plot
    :param pulselist: list of pulses (and colors)
    :return:
    """
    logger.info('using standard set {}'.format(diag_json))

    logger.info('pulselist {}'.format(pulselist))


    default = True
    fold = './standard_set/'
    logger.debug('opening {}'.format(fold+diag_json))
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
    logger.info('reading {} signals'.format(str(totsignal)))
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

    logger.debug('subplot {} x {}'.format(str(iRow),str(iColumn)))




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
        logger.info('\n')
        logger.info('reading data for pulse %s ', pulse)
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
                        logger.info('read data %s ', key + '_' + dda + '_' + dtype + 'seq {}'.format(str(seq)))
                    else:
                        logger.info('no data')


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

                    plt.plot(vars()[time_name], vars()[data_name],
                                 label=str(pulse) + ' ' + node, marker = marker, linestyle=linestyle, linewidth=linewidth,
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
                        logger.info('read data  ' + key + '_' + value )
                    else:
                        logger.info('no data')





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
                        logger.debug('used JSON options for jpf')




                    if indexSubPlot == 1:
                        ax_1 = plt.subplot(iRow, iColumn,indexSubPlot)

                    else:
                        vars()[ax_name] = plt.subplot(iRow, iColumn,
                                                           indexSubPlot,sharex=ax_1)
                    plt.plot(vars()[time_name], vars()[data_name],
                                 label=str(pulse) + ' ' + value, marker = marker, linestyle=linestyle, linewidth=linewidth,
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

    logger.info('plot DONE')
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

        logger.info('picture saved to {}'.format(cwd+os.sep+'figures/'+fname))
    t = Toggle(fig)
    fig.canvas.mpl_connect("button_press_event", t.toggle)
    # fig.canvas.mpl_connect("key_press_event", t.toggle)
    plt.show(block=True)
    # fig.tight_layout()


    #leave plt.show() outside



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
    # logging.info('\n')
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
