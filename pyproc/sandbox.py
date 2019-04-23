
# Import external modules

import matplotlib.pyplot as plt
import numpy as np
import json
import scipy.io as io
# from pyJETPPF.JETPPF import JETPPF
from pyproc.plot import PyprocPlot
from pyproc.analyse import PyprocAnalyse
from collections import OrderedDict
from pyJETPPF.JETPPF import JETPPF

font = {'family': 'normal',
        'weight': 'normal',
        'size': 14}
import matplotlib
matplotlib.rc('font', **font)
import matplotlib.font_manager as font_manager
# path = '/usr/share/fonts/msttcore/arial.ttf'
path = '/usr/share/fonts/gnu-free/FreeSans.ttf'
# path = '/home/bloman/fonts/msttcore/arial.ttf'
prop = font_manager.FontProperties(fname=path)
matplotlib.rcParams['font.family'] = prop.get_name()
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = prop.get_name()
matplotlib.rc('lines', linewidth=1.2)
matplotlib.rc('axes', linewidth=1.2)
matplotlib.rc('xtick.major', width=1.2)
matplotlib.rc('ytick.major', width=1.2)
matplotlib.rc('xtick.minor', width=1.2)
matplotlib.rc('ytick.minor', width=1.2)

def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def get_exp_data(exp_pulse_details):

    exp_save_file = exp_pulse_details['exp_save_file']
    try:
        with open(exp_save_file, 'r') as f:
            exp_res = json.load(f)
    except IOError as e:
        raise

    # CONVERT LISTS TO ARRAYS
    exp_res['kt3a_time'] = np.asarray(exp_res['kt3a_time'])
    exp_res['ky4v_time'] = np.asarray(exp_res['ky4v_time'])
    exp_res['ky4v_te'] = np.asarray(exp_res['ky4v_te'])
    exp_res['ky4v_ne'] = 1.e20 * np.asarray(exp_res['ky4v_ne'])
    exp_res['ky4v_js'] = 1.e06 * np.asarray(exp_res['ky4v_js'])
    exp_res['ky4v_rcoord'] = np.asarray(exp_res['ky4v_rcoord'])
    exp_res['kt3a_dne'] = np.asarray(exp_res['kt3a_dne'])
    exp_res['kt3a_coord'] = np.asarray(exp_res['kt3a_coord'])
    exp_res['kt3a_contTe'] = np.asarray(exp_res['kt3a_contTe'])
    exp_res['kt3a_contTe_err'] = np.asarray(exp_res['kt3a_contTe_err'])
    exp_res['kt3a_rec_rate_Ly_per_delL_m'] = np.asarray(exp_res['kt3a_rec_rate_Ly_per_delL_m'])
    exp_res['kt3a_rec_rate_Ly_per_delL_m_err'] = np.asarray(exp_res['kt3a_rec_rate_Ly_per_delL_m_err'])
    exp_res['kt3a_delL'] = np.asarray(exp_res['kt3a_delL'])
    exp_res['kt3a_delL_err'] = np.asarray(exp_res['kt3a_delL_err'])
    exp_res['Srec_adf11'] = np.asarray(exp_res['Srec_adf11'])
    exp_res['Sion_adf11'] = np.asarray(exp_res['Sion_adf11'])
    exp_res['Srec_adf11_err'] = np.asarray(exp_res['Srec_adf11_err'])
    exp_res['Sion_adf11_err'] = np.asarray(exp_res['Sion_adf11_err'])
    exp_res['Srec_adf11_tot'] = np.asarray(exp_res['Srec_adf11_tot'])
    exp_res['Sion_adf11_tot'] = np.asarray(exp_res['Sion_adf11_tot'])
    exp_res['Srec_adf11_tot_err'] = np.asarray(exp_res['Srec_adf11_tot_err'])
    exp_res['Sion_adf11_tot_err'] = np.asarray(exp_res['Sion_adf11_tot_err'])
    exp_res['kt3a_delL'] = np.asarray(exp_res['kt3a_delL'])
    exp_res['kt3e_n0_D42'] = np.asarray(exp_res['kt3e_n0_D42'])
    exp_res['kt3e_n0_D42_err'] = np.asarray(exp_res['kt3e_n0_D42_err'])
    exp_res['kt3e_d42_meas'] = np.asarray(exp_res['kt3e_d42_meas'])
    exp_res['kt3e_d52_meas'] = np.asarray(exp_res['kt3e_d52_meas'])
    exp_res['kt3e_Iexc_D72delL'] = np.asarray(exp_res['kt3e_Iexc_D72delL'])
    exp_res['kt3e_Irec_D72delL'] = np.asarray(exp_res['kt3e_Irec_D72delL'])
    exp_res['kt3e_Iexc_D72delL_err'] = np.asarray(exp_res['kt3e_Iexc_D72delL_err'])
    exp_res['kt3e_Irec_D72delL_err'] = np.asarray(exp_res['kt3e_Irec_D72delL_err'])

    if 'kt1v_h21' in exp_res.keys():
        exp_res['kt1v_trange'] = np.asarray(exp_res['kt1v_trange'])
        exp_res['kt1v_Rcoord'] = np.asarray(exp_res['kt1v_Rcoord'])
        exp_res['kt1v_h21'] = np.asarray(exp_res['kt1v_h21'])
        exp_res['kt1v_h32'] = np.asarray(exp_res['kt1v_h32'])
        exp_res['kt1v_h21_err'] = np.asarray(exp_res['kt1v_h21_err'])
        exp_res['kt1v_h32_err'] = np.asarray(exp_res['kt1v_h32_err'])

    if exp_res['icls2017_kt3a_Siz']:
        exp_res['icls2017_kt3a_Siz'] = np.asarray(exp_res['icls2017_kt3a_Siz'])
        exp_res['icls2017_kt3a_Siz_err'] = np.asarray(exp_res['icls2017_kt3a_Siz_err'])
        exp_res['icls2017_kt3a_coord'] = np.asarray(exp_res['icls2017_kt3a_coord'])
    if exp_res['icls2017_kt3e_Srec']:
        exp_res['icls2017_kt3e_Srec'] = np.asarray(exp_res['icls2017_kt3e_Srec'])
        exp_res['icls2017_kt3e_Srec_err'] = np.asarray(exp_res['icls2017_kt3e_Srec_err'])
        exp_res['icls2017_kt3e_coord'] = np.asarray(exp_res['icls2017_kt3e_coord'])

    if 'kt3a_n3a' in exp_res:
        # ** APPLY ABS CAL CORRECTION FACTOR OF 1/1.6 TO ALL KT3A AND KT3B MEASUREMENTS!
        # TODO: THIS NEEDS TO BE DONE IN THE ORIGINAL CODE B15_09_divspec_analysis.py
        kt3ab_scal = 1. / 1.6
        # NIV multiplet at 348 nm
        exp_res['kt3a_n3a'] = np.asarray(exp_res['kt3a_n3a']) * kt3ab_scal
        exp_res['kt3a_n3a_err'] = np.asarray(exp_res['kt3a_n3a_err']) * kt3ab_scal
        exp_res['kt3a_n3b'] = np.asarray(exp_res['kt3a_n3b']) * kt3ab_scal
        exp_res['kt3a_n3b_err'] = np.asarray(exp_res['kt3a_n3b_err']) * kt3ab_scal
        exp_res['kt3a_n3c'] = np.asarray(exp_res['kt3a_n3c']) * kt3ab_scal
        exp_res['kt3a_n3c_err'] = np.asarray(exp_res['kt3a_n3c_err']) * kt3ab_scal
        # NIII doublet at 410 nm
        exp_res['kt3a_n2a'] = np.asarray(exp_res['kt3a_n2a']) * kt3ab_scal
        exp_res['kt3a_n2a_err'] = np.asarray(exp_res['kt3a_n2a_err']) * kt3ab_scal
        exp_res['kt3a_n2b'] = np.asarray(exp_res['kt3a_n2b']) * kt3ab_scal
        exp_res['kt3a_n2b_err'] = np.asarray(exp_res['kt3a_n2b_err']) * kt3ab_scal
        # NII multiplet at 404 nm
        exp_res['kt3a_n1a'] = np.asarray(exp_res['kt3a_n1a']) * kt3ab_scal
        exp_res['kt3a_n1a_err'] = np.asarray(exp_res['kt3a_n1a_err']) * kt3ab_scal
        exp_res['kt3a_n1b'] = np.asarray(exp_res['kt3a_n1b']) * kt3ab_scal
        exp_res['kt3a_n1b_err'] = np.asarray(exp_res['kt3a_n1b_err']) * kt3ab_scal
        exp_res['kt3a_n1c'] = np.asarray(exp_res['kt3a_n1c']) * kt3ab_scal
        exp_res['kt3a_n1c_err'] = np.asarray(exp_res['kt3a_n1c_err']) * kt3ab_scal
        exp_res['kt3a_n1d'] = np.asarray(exp_res['kt3a_n1d']) * kt3ab_scal
        exp_res['kt3a_n1d_err'] = np.asarray(exp_res['kt3a_n1d_err']) * kt3ab_scal
        exp_res['kt3a_n1e'] = np.asarray(exp_res['kt3a_n1e']) * kt3ab_scal
        exp_res['kt3a_n1e_err'] = np.asarray(exp_res['kt3a_n1e_err']) * kt3ab_scal

    return exp_res

if __name__=='__main__':

    # Results sets
    # B15-09 NITROGEN CASES: seeding locations outboard only, corresponding (but noexactly) to GIM 9
    # cases = {
    #     '90425': {
    #         'ne_sep_omp':21e18, 'sim_color': 'b', 'exp_color': 'r','sim_zo': 10,
    #         'exp_zo': 1,
    #         'case':'bloman_cmg_catalog_edge2d_jet_81472_sep1717_seq#2',
    #         'exp_pulse_details': {
    #             'JPN': 90425,
    #             'trange': [55.75, 56.25],
    #             'exp_save_file': '/home/bloman/python_bal/jet_analysis/B15-09/results/icls2017/90425_D4567_ref_kt3aabscorr.json'
    #         }
    #     },
    #     '90423': {
    #         'ne_sep_omp': 21e18, 'sim_color': 'b', 'exp_color': 'r', 'sim_zo': 10,
    #         'exp_zo': 1,
    #         'case':'bloman_cmg_catalog_edge2d_jet_81472_sep2417_seq#2',
    #         'exp_pulse_details': {
    #             'JPN': 90423,
    #             'trange': [55.75, 56.25],
    #             'exp_save_file': '/home/bloman/python_bal/jet_analysis/B15-09/results/icls2017/90423_D4567_ref_kt3aabscorr.json'
    #         }
    #     },
    # }


    # cases = {
    #     '1': {
    #         'ne_sep_omp': 21e18, 'sim_color': 'r', 'exp_color': 'b', 'sim_zo': 10,
    #         'exp_zo': 1,
    #         'case': 'bloman_cmg_catalog_edge2d_jet_81472_oct1317_seq#1',
    #         'exp_pulse_details': {
    #             'JPN': 90425,
    #             'trange': [55.75, 56.25],
    #             'exp_save_file': '/home/bloman/python_bal/jet_analysis/B15-09/results/icls2017/90425_D4567_ref_kt3aabscorr.json'
    #         }
    #     },
    # }

    cases = {
        '1': {
            'ne_sep_omp': 21e18, 'sim_color': 'r', 'exp_color': 'b', 'sim_zo': 10,
            'exp_zo': 1,
            'case': 'bloman_cmg_catalog_edge2d_jet_81472_oct2117_seq#3',

        },
    }

    # setup plot figures
    left  = 0.2  # the left side of the subplots of the figure
    right = 0.95    # the right side of the subplots of the figure
    bottom = 0.15   # the bottom of the subplots of the figure
    top = 0.93      # the top of the subplots of the figure
    wspace = 0.25   # the amount of width reserved for blank space between subplots
    hspace = 0.15  # the amount of height reserved for white space between subplots

    fig1, ax1 = plt.subplots(nrows=4, ncols=1, figsize=(6,12), sharex=True)
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    fig2, ax2 = plt.subplots(nrows=4, ncols=1, figsize=(6,12), sharex=True)
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    fig3, ax3 = plt.subplots(nrows=3, ncols=1, figsize=(6,12), sharex=True)
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    fig4, ax4 = plt.subplots(nrows=8, ncols=1, figsize=(6,12), sharex=True, sharey=True)
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    fig5, ax5 = plt.subplots(nrows=2, ncols=1, figsize=(9,12))
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    workdir = '/u/bviola/work/Python/EDGE2D/e2d_data/'

    """
    JET Regions:
        hfs_sol
        lfs_sol
        hfs_div
        lfs_div
        xpt_conreg
        hfs_lower
        lfs_lower
        rhon_09_10
    """

    icase = 0
    for casekey, case in cases.items():

        icase+=1

        Hlines_dict = OrderedDict([
            ('1215.2', ['2', '1']),
            ('6561.9', ['3', '2']),
            ('4339.9', ['5', '2']),
            ('3969.5', ['7', '2'])
        ])

        Hlines_dict_lytrap = OrderedDict([
            ('1215.67', ['2', '1']),
            ('1025.72', ['3', '2']),
            ('6564.57', ['5', '2']),
        ])

        nitrogen_lines_dict = OrderedDict([
            ('2', {'4042.07': ['4f', '3d']}),
            # ('2', {'3996.13': ['4f', '3d']}),
            ('3', {'4100.51': ['3p', '3s']}),
            ('4', {'3481.83': ['3p', '3s']}),
        ])

        spec_line_dict = {
            '1': # HYDROGEN
                {'1': Hlines_dict},
            '7': nitrogen_lines_dict
        }

        spec_line_dict_lytrap = {
            '1': # HYDROGEN
                {'1': Hlines_dict_lytrap}
        }

        plot_dict = {
            'spec_line_dict':spec_line_dict,
            # 'spec_line_dict_lytrap': spec_line_dict_lytrap,
            'prof_param_defs': {'diag': 'KT1V', 'axs': ax1,
                                'include_pars_at_max_ne_along_LOS': False,
                                'include_sum_Sion_Srec': False,
                                'include_target_vals': False,
                                'coord': 'R',  # 'angle' 'R' 'Z'
                                'color': case['sim_color'], 'zorder': 10},
            'prof_Hemiss_defs': {'diag': 'KT1V',
                                 'lines': spec_line_dict['1']['1'],
                                # 'lines_lytrap': spec_line_dict_lytrap['1']['1'],
                                 'excrec': False,
                                 'axs': ax2,
                                 'coord': 'R',  # 'angle' 'R' 'Z'
                                 'color': case['sim_color'],
                                 'zorder': 10},
            'prof_impemiss_defs': {'diag': 'KT1V',
                                   'lines': spec_line_dict,
                                   'excrec': False,
                                   'axs': ax3,
                                   'coord': 'R',  # 'angle' 'R' 'Z'
                                   'color': [case['sim_color']],
                                   'zorder': 10},
             'imp_rad_coeff': {'region': 'rhon_09_10',
                               'atnum': 7,
                               'ion_stages': [1, 2, 3, 4, 5, 6, 7],
                               'axs': ax4,
                               'color': case['sim_color'],
                               'zorder': 10},
            'imp_rad_dist': {'region': 'rhon_09_10',
                              'atnum': 7,
                              'te_nbins': 10,
                              'axs': ax5,
                              'color': case['sim_color'],
                              'zorder': 10},
            # 'los_param_defs':{'diag':'KT3A', 'axs':ax1, 'color':'blue', 'zorder':10},
            # 'los_Hemiss_defs':{'diag':'KT3A', 'axs':ax1, 'color':'blue', 'zorder':10},
            # 'los_impemiss_defs':{'diag':'KT3A', 'axs':ax1, 'color':'blue', 'zorder':10},
            # '2d_defs': {'lines': spec_line_dict,
            #             'diagLOS': ['KT3'],
            #             'Rrng': [2.36, 2.96],
            #             'Zrng': [-1.73, -1.29],
            #             'save': False}
        }

        o = PyprocPlot(workdir, case['case'], plot_dict=plot_dict, icase=icase)

        # print available regions
        print('Region powers: ', case['case'])
        for name, region in o.data2d.regions.items():
            print('Region, Prad_H, Prad_imp1, Prad_imp2: ', name, region.Prad_H, region.Prad_imp1, region.Prad_imp2)
        print('')

        o.data2d.plot_region(name = 'lfs_div')

        # EXP RESULTS
        if 'exp_pulse_details' in case:
            exp_res = get_exp_data(case['exp_pulse_details'])

            # GET TIME SLICE FOR COMPARISON WITH MODEL
            tvec = np.arange(0, 200, 20)
            idx, time = find_nearest(exp_res['kt3a_time'], np.average(case['exp_pulse_details']['trange']))
            dum, frame = find_nearest(tvec, idx)
            frame_ky4v, time_ky4v = find_nearest(exp_res['ky4v_time'], np.average(case['exp_pulse_details']['trange']))

            # GET EFIT OSP LOCATION
            efit = JETPPF(case['exp_pulse_details']['JPN'], sequence=0, dda='EFIT', uid='JETPPF', items=['RSOL'])
            efit_tidx, = np.where(np.logical_and(efit.signals['RSOL'].time >= case['exp_pulse_details']['trange'][0],
                                                 efit.signals['RSOL'].time <= case['exp_pulse_details']['trange'][1]))
            efit_rsol = np.average(efit.signals['RSOL'].data[efit_tidx])

            # CORRECT EXP COORDS BY DIFF IN EXP AND MODEL OSP POSITION
            # exp_coord_corr = -1.0*(efit_rsol - e2d_data.osp[0])
            irview_rsol = 2.73  # for V5/C B15-09 and H16-09 pulses from IR data
            exp_coord_corr = -1.0 * (irview_rsol - o.data2d.osp[0])

            exp_c = case['exp_color']

            # DENSITY
            yerr = 0.1 * exp_res['kt3a_dne'][frame]
            ax1[0].plot(exp_res['kt3a_coord'] + exp_coord_corr, exp_res['kt3a_dne'][frame], '-',
                        c=exp_c, linewidth=2, zorder=1)
            ax1[0].plot([0, 0], [0, 0], c=exp_c, linewidth=2, label='experiment', zorder=1)
            ax1[0].fill_between(exp_res['kt3a_coord'] + exp_coord_corr,
                                exp_res['kt3a_dne'][frame] + yerr,
                                exp_res['kt3a_dne'][frame] - yerr, facecolor=exp_c,
                                edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)

            # Te from ICLS2017 continuum (preliminary)
            yhi = exp_res['icls2017_kt3a_contThi']
            ylo = exp_res['icls2017_kt3a_contTlo']
            yerr = exp_res['kt3a_contTe_err'][frame]
            ax1[1].plot(exp_res['icls2017_kt3a_coord'] + exp_coord_corr, yhi, c=exp_c, linewidth=2,
                                      zorder=1)
            ax1[1].plot(exp_res['icls2017_kt3a_coord'] + exp_coord_corr, ylo, c=exp_c, linewidth=2,
                                      zorder=1)
            ax1[1].fill_between(exp_res['icls2017_kt3a_coord'] + exp_coord_corr, yhi, ylo, facecolor=exp_c,
                                              edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)

            # Ionization from KT1 Ly-alpha (arb scal) and recombination from ICLS2017 Tlo continuum (preliminary)
            scal_Siz_Lya = 8.1932961577e+22 / 1794.  # based on 90425 t 48.17-48.2 Siz D-alpha vs Ly-beta comparion at low recycling (no recombination, no opacity)
            ax1[2].plot(0, 0, c='k', linewidth=2, label='Ionization')
            ax1[2].plot(0, 0, '--', c='k', linewidth=2, label='Recombination')
            y = exp_res['icls2017_kt3a_Siz']
            yerr = exp_res['icls2017_kt3a_Siz_err']
            ax1[2].plot(exp_res['icls2017_kt3a_coord'] + exp_coord_corr, y, c=exp_c, linewidth=2,
                                      zorder=1)
            ax1[2].fill_between(exp_res['icls2017_kt3a_coord'] + exp_coord_corr, y + yerr, y - yerr,
                                              facecolor=exp_c, edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)
            y = exp_res['icls2017_kt3e_Srec']
            yerr = exp_res['icls2017_kt3e_Srec_err']
            ax1[2].plot(exp_res['icls2017_kt3e_coord'] + exp_coord_corr, y, c=exp_c, linestyle='--',
                                      linewidth=2, zorder=1)
            ax1[2].fill_between(exp_res['icls2017_kt3e_coord'] + exp_coord_corr, y + yerr, y - yerr,
                                              facecolor=exp_c, edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)

            # D-alpha, Ly-alpha
            ax2[0].plot(exp_res['kt1v_Rcoord'] + exp_coord_corr, scal_Siz_Lya * exp_res['kt1v_h21'][0], '-',
                        color=exp_c, lw=5, zorder=1)
            ax2[1].plot(exp_res['kt1v_Rcoord'] + exp_coord_corr, exp_res['kt1v_h32'][0], '-', color=exp_c,
                        lw=5, zorder=1)


            if 'kt3a_n3a' in exp_res:
                niv_3p_3s_arr = exp_res['kt3a_n3a'] + exp_res['kt3a_n3b'] + exp_res['kt3a_n3c']
                niii_3p_3s_arr = exp_res['kt3a_n2a'] + exp_res['kt3a_n2b']
                nii_4f_3d_arr = exp_res['kt3a_n1a'] + exp_res['kt3a_n1b'] + exp_res['kt3a_n1c'] + \
                                exp_res['kt3a_n1d'] + exp_res['kt3a_n1e']
                niv_3p_3s_err_arr = np.sqrt(
                    exp_res['kt3a_n3a_err'] ** 2 + exp_res['kt3a_n3b_err'] ** 2 + exp_res['kt3a_n3c_err'] ** 2)
                niii_3p_3s_err_arr = np.sqrt(exp_res['kt3a_n2a_err'] ** 2 + exp_res['kt3a_n2b_err'] ** 2)
                nii_4f_3d_err_arr = np.sqrt(
                    exp_res['kt3a_n1a_err'] ** 2 + exp_res['kt3a_n1b_err'] ** 2 + exp_res['kt3a_n1c_err'] ** 2 + \
                    exp_res['kt3a_n1d_err'] ** 2 + exp_res['kt3a_n1e_err'] ** 2)

                # 90423 kt3a 399.5 intensity at t=56 s. Temporary. TODO: add to exp save files!
                # nii_4f_3d_arr = np.array((6.62e17, 8.62e17, 1.00e18, 1.81e18, 3.70e18, 3.16e18, 2.48e18, 2.17e18, 2.06e18,
                #                           1.88e18, 1.65e18, 1.47e18, 1.31e18, 1.12e18, 9.14e17, 9.22e17, 8.84e17, 9.94e17,
                #                           9.94e17))
                # nii_4f_3d_err_arr = 0.02 * nii_4f_3d_arr

                # axes_dict['nitrogen'][0].plot(exp_res['kt3a_coord'][1:]+exp_coord_corr, niv_3p_3s_arr[frame,1:], '-', color=exp_c, lw=2)
                # axes_dict['nitrogen'][1].plot(exp_res['kt3a_coord'][1:]+exp_coord_corr, niii_3p_3s_arr[frame,1:], '-', color=exp_c, lw=2)
                # axes_dict['nitrogen'][2].plot(exp_res['kt3a_coord'][1:]+exp_coord_corr, nii_4f_3d_arr[frame,1:], '-', color=exp_c, lw=2)

                start_trk = 1
                coord = exp_res['kt3a_coord'][start_trk:]
                print(coord)
                y = niv_3p_3s_arr[frame, start_trk:]
                yerr = niv_3p_3s_err_arr[frame, start_trk:]
                ax3[2].plot(exp_res['kt3a_coord'][start_trk:] + exp_coord_corr, y, '-', color=exp_c, lw=2)
                ax3[2].fill_between(exp_res['kt3a_coord'][start_trk:] + exp_coord_corr, y + yerr, y - yerr,
                                                      facecolor=exp_c, edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)

                y = niii_3p_3s_arr[frame, start_trk:]
                yerr = niii_3p_3s_err_arr[frame, start_trk:]
                ax3[1].plot(exp_res['kt3a_coord'][start_trk:] + exp_coord_corr, y, '-', color=exp_c, lw=2)
                ax3[1].fill_between(exp_res['kt3a_coord'][start_trk:] + exp_coord_corr, y + yerr, y - yerr,
                                                      facecolor=exp_c, edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)

                y = nii_4f_3d_arr[frame,start_trk:]
                yerr = nii_4f_3d_err_arr[frame,start_trk:]
                ax3[0].plot(exp_res['kt3a_coord'][start_trk:] + exp_coord_corr, y, '-', color=exp_c, lw=2)
                ax3[0].fill_between(exp_res['kt3a_coord'][start_trk:] + exp_coord_corr, y + yerr, y - yerr,
                                                      facecolor=exp_c, edgecolor=exp_c, alpha=0.25, linewidth=0, zorder=1)

    # Print out results dictionary tree
    # PyprocPlot.pprint_json(o.res_dict['KT3A']['1']['los_int'])

    plt.show()
