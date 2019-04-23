
import numpy as np
# import scipy.io as io
import os, errno
import json, pickle
# http://lmfit.github.io/lmfit-py/parameters.html
from lmfit import minimize, Parameters, fit_report
import os
import sys
import contextlib

from pyproc.process import ProcessEdgeSim
from pyproc.pyADASread import adas_adf11_read, adas_adf15_read, continuo_read
from pyproc.atomic import get_ADAS_dict

class AnalyseSynthDiag(ProcessEdgeSim):
    """
        Inherits from ProcessEdgeSim and adds methods for analysis of synthetic spectra
    """
    def __init__(self, input_dict):
        self.input_dict = input_dict

        tmpstr = input_dict['tranfile'].replace('/','_')

        if tmpstr[:3] == '_u_':
            tmpstr = tmpstr[3:-5]
        elif tmpstr[:6] == '_work_':
            tmpstr = tmpstr[6:-5]
        else:
            tmpstr = tmpstr[1:-5]

        savedir = input_dict['save_dir'] + tmpstr + '/'

        # Create dir from tran file, if it does not exist
        try:
            os.makedirs(savedir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.data2d_save_file = savedir +'pyproc.2ddata.pkl'
        self.synth_diag_save_file = savedir + 'pyproc.synth_diag.json'
        self.proc_synth_diag_save_file = savedir+ 'pyproc.proc_synth_diag.json'
        self.spec_line_dict = input_dict['spec_line_dict']

        # Location of adf15 and adf11 ADAS data modified for Ly-series opacity with escape factor method
        if 'read_ADAS_lytrap' in input_dict:
            self.adas_lytrap = input_dict['read_ADAS_lytrap']
            self.spec_line_dict_lytrap = self.adas_lytrap['spec_line_dict']
            self.ADAS_dict_lytrap = get_ADAS_dict(savedir,
                                                  self.spec_line_dict_lytrap,
                                                  restore=not input_dict['read_ADAS_lytrap']['read'],
                                                  adf11_year = self.adas_lytrap['adf11_year'],
                                                  lytrap_adf11_dir=self.adas_lytrap['adf11_dir'],
                                                  lytrap_pec_file=self.adas_lytrap['pec_file'])
        else:
            self.ADAS_dict_lytrap = None
            self.spec_line_dict_lytrap = None

        # Also get standard ADAS data
        self.ADAS_dict = get_ADAS_dict(input_dict['save_dir'],
                                       self.spec_line_dict, adf11_year=12, restore=not input_dict['read_ADAS'])

        super().__init__(self.ADAS_dict, ADAS_dict_lytrap = self.ADAS_dict_lytrap, tranfile=input_dict['tranfile'],
                         machine=input_dict['machine'],
                         pulse=input_dict['pulse'],
                         interactive_plots = input_dict['interactive_plots'],
                         spec_line_dict=self.spec_line_dict,
                         spec_line_dict_lytrap = self.spec_line_dict_lytrap,
                         diag_list=input_dict['diag_list'],
                         calc_synth_spec_features=input_dict['run_options']['calc_synth_spec_features'],
                         calc_NII_afg_feature=input_dict['run_options']['calc_NII_afg_feature'],
                         save_synth_diag=True,
                         synth_diag_save_file=self.synth_diag_save_file,
                         data2d_save_file=self.data2d_save_file)

        if self.input_dict['run_options']['analyse_synth_spec_features']:
            # Read synth diag saved data
            try:
                with open(self.synth_diag_save_file, 'r') as f:
                    res_dict = json.load(f)
                self.analyse_synth_spectra(res_dict)
            except IOError as e:
                raise


    # Analyse synthetic spectra
    def analyse_synth_spectra(self, res_dict):

        # Estimate parameters and update res_dict. Call order matters since ne and Te
        # are needed as constraints
        #
        # Electron density estimate from Stark broadening of H6-2 line
        self.recover_line_int_Stark_ne(res_dict)

        # Electron temperature estimate from ff+fb continuum
        self.recover_line_int_ff_fb_Te(res_dict)

        # Recombination and Ionization
        self.recover_line_int_particle_bal(res_dict, sion_H_transition=['2','1'], ne_scal=1.0)

        # delL * neutral density from Ly-alpha assuming excitation dominated
        self.recover_delL_atomden_product(res_dict)

        if self.proc_synth_diag_save_file:
            with open(self.proc_synth_diag_save_file, mode='w', encoding='utf-8') as f:
                json.dump(res_dict, f, indent=2)

    @staticmethod
    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return idx, array[idx]

    @staticmethod
    def residual_lorentz_52(params, x, data=None, eps_data=None):

        cwl = params['cwl'].value
        area = params['area'].value
        stark_fwhm = params['stark_fwhm'].value

        model = 1. / (np.power(np.abs(x - cwl), 5. / 2.) + np.power(stark_fwhm / 2.0, 5. / 2.))

        model_area = np.trapz(model, x=x)
        amp_scal = area / model_area
        model *= amp_scal

        if data is None:
            return model
        if eps_data is None:
            return (model - data)
        return (model - data) / eps_data

    @staticmethod
    def residual_continuo(params, wave, data=None, eps_data=None):
        delL = params['delL'].value
        te = params['te_360_400'].value
        ne = params['ne'].value

        model_ff, model_ff_fb = continuo_read.adas_continuo_py(wave, te, 1, 1)
        model_ff = model_ff * ne * ne * delL
        model_ff_fb = model_ff_fb * ne * ne * delL

        if data is None:
            return model_ff_fb
        if eps_data is None:
            return (model_ff_fb - data)
        return (model_ff_fb - data) / eps_data

    # @staticmethod
    # @contextlib.contextmanager
    # def stdchannel_redirected(stdchannel, dest_filename):
    #     """
    #     https://stackoverflow.com/questions/977840/redirecting-fortran-called-via-f2py-output-in-python
    #
    #     A context manager to temporarily redirect stdout or stderr
    #
    #     e.g.:
    #
    #
    #     with stdchannel_redirected(sys.stderr, os.devnull):
    #         if compiler.has_function('clock_gettime', libraries=['rt']):
    #             libraries.append('rt')
    #     """
    #
    #     try:
    #         oldstdchannel = os.dup(stdchannel.fileno())
    #         dest_file = open(dest_filename, 'w')
    #         os.dup2(dest_file.fileno(), stdchannel.fileno())
    #
    #         yield
    #     finally:
    #         if oldstdchannel is not None:
    #             os.dup2(oldstdchannel, stdchannel.fileno())
    #         if dest_file is not None:
    #             dest_file.close()

    # @staticmethod
    # def get_ADAS_dict(save_dir, spec_line_dict, num_samples=100, restore=False, lytrap=False,
    #                   adf11_year = 12, lytrap_adf11_dir=False, lytrap_pec_file=False):
    #
    #     if restore:
    #         # Try to restore ADAS_dict
    #         if lytrap:
    #             try:
    #                 with open(save_dir + 'ADAS_dict_lytrap.pkl', 'rb') as f:
    #                     ADAS_dict = pickle.load(f)
    #             except IOError as e:
    #                 print('ADAS dictionary not found. Set [read_ADAS_lytrap] to True.')
    #                 raise
    #         else:
    #             try:
    #                 with open(save_dir + 'ADAS_dict.pkl', 'rb') as f:
    #                     ADAS_dict = pickle.load(f)
    #             except IOError as e:
    #                 print('ADAS dictionary not found. Set [read_ADAS] to True.')
    #                 raise
    #
    #         # Does the restored ADAS_dict contain all of the requested lines?
    #         for atnum, atnumdict in spec_line_dict.items():
    #             for ionstage, stagedict in atnumdict.items():
    #                 for line, val in stagedict.items():
    #                     found_line = False
    #                     for adas_atnum, adas_atnumdict in ADAS_dict['adf15'].items():
    #                         for adas_ionstage, adas_stagedict in adas_atnumdict.items():
    #                             if atnum == adas_atnum and ionstage == adas_ionstage:
    #                                 for adas_line, val in adas_stagedict.items():
    #                                     if line == adas_line[:-5]:  # strip 'recom', 'excit'
    #                                         found_line = True
    #                     if not found_line:
    #                         print(atnum, ' ', ionstage, ' ', line,
    #                               ' not found in restored ADAS_dict. Set [read_ADAS] to True and try again.')
    #                         return
    #         if lytrap:
    #             print('ADAS Ly trapping dictionary restored.')
    #         else:
    #             print('ADAS dictionary restored.')
    #     else:
    #         with AnalyseSynthDiag.stdchannel_redirected(sys.stderr, os.devnull):
    #             with AnalyseSynthDiag.stdchannel_redirected(sys.stdout, os.devnull):
    #                 # Read all necessary ADAS data here and store in dict
    #                 ADAS_dict = {}
    #                 Te_rnge = [0.2, 5000]
    #                 ne_rnge = [1.0e11, 1.0e15]
    #                 num_samples = 100
    #                 ADAS_dict['adf15'] = adas_adf15_read.get_adas_imp_PECs_interp(spec_line_dict, Te_rnge,
    #                                                                               ne_rnge, npts=num_samples,
    #                                                                               npts_interp=1000,
    #                                                                               lytrap_pec_file=lytrap_pec_file)
    #                 # Also get adf11 for the ionisation balance fractional abundance. No Te_arr, ne_arr interpolation
    #                 # available in the adf11 reader at the moment, so generate more coarse array (sloppy!)
    #                 # TODO: add interpolation capability to the adf11 reader so that adf15 and adf11 are on the same Te, ne grid
    #                 Te_arr_adf11 = np.logspace(np.log10(Te_rnge[0]), np.log10(Te_rnge[1]), 500)
    #                 ne_arr_adf11 = np.logspace(np.log10(ne_rnge[0]), np.log10(ne_rnge[1]), 30)
    #                 ADAS_dict['adf11'] = {}
    #                 for atnum in spec_line_dict:
    #                     if int(atnum) > 1:
    #                         ADAS_dict['adf11'][atnum] = adas_adf11_read.get_adas_imp_adf11(int(atnum), Te_arr_adf11,
    #                                                                                        ne_arr_adf11)
    #                     elif int(atnum) == 1:
    #                         ADAS_dict['adf11'][atnum] = adas_adf11_read.get_adas_H_adf11_interp(Te_rnge, ne_rnge,
    #                                                                                             npts=num_samples,
    #                                                                                             npts_interp=1000,
    #                                                                                             pwr=True,
    #                                                                                             year=adf11_year,
    #                                                                                             custom_dir=lytrap_adf11_dir)
    #                 # Pickle ADAS dictionary to save_dir
    #                 if lytrap_adf11_dir:
    #                     output = open(save_dir + 'ADAS_dict_lytrap.pkl', 'wb')
    #                 else:
    #                     output = open(save_dir + 'ADAS_dict.pkl', 'wb')
    #                 pickle.dump(ADAS_dict, output)
    #                 output.close()
    #
    #     return ADAS_dict

    @staticmethod
    def recover_line_int_ff_fb_Te(res_dict):
        """
            RECOVER LINE-AVERAGED ELECTRON TEMPERATURE FROM FF-FB CONTINUUM SPECTRA
            Balmer edge ratio estimate: 360 nm and 400 nm
            Balmer ff-fb below edge ratio: 300 nm and 400 nm
            Balmer ff-fb above edge ratio: 400 nm and 500 nm
        """
        cont_ratio_360_400 = continuo_read.get_fffb_intensity_ratio_fn_T(360.0, 400.0, 1.0, save_output=False, restore=True)
        cont_ratio_300_360 = continuo_read.get_fffb_intensity_ratio_fn_T(300.0, 360.0, 1.0, save_output=False, restore=True)
        cont_ratio_400_500 = continuo_read.get_fffb_intensity_ratio_fn_T(400.0, 500.0, 1.0, save_output=False, restore=True)

        for diag_key in res_dict.keys():
            for chord_key in res_dict[diag_key].keys():

                print('Fitting ff+fb continuum spectra, LOS id= :', diag_key, ' ', chord_key)

                wave_fffb = np.asarray(res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['wave'])
                synth_data_fffb = np.asarray(
                    res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['intensity'])
                idx_300, val = AnalyseSynthDiag.find_nearest(wave_fffb, 300.0)
                idx_360, val = AnalyseSynthDiag.find_nearest(wave_fffb, 360.0)
                idx_400, val = AnalyseSynthDiag.find_nearest(wave_fffb, 400.0)
                idx_500, val = AnalyseSynthDiag.find_nearest(wave_fffb, 500.0)
                ratio_360_400 = synth_data_fffb[idx_360] / synth_data_fffb[idx_400]
                ratio_300_360 = synth_data_fffb[idx_300] / synth_data_fffb[idx_360]
                ratio_400_500 = synth_data_fffb[idx_400] / synth_data_fffb[idx_500]
                icont_ratio, vcont_ratio = AnalyseSynthDiag.find_nearest(cont_ratio_360_400[:, 1], ratio_360_400)
                fit_te_360_400 = cont_ratio_360_400[icont_ratio, 0]
                icont_ratio, vcont_ratio = AnalyseSynthDiag.find_nearest(cont_ratio_300_360[:, 1], ratio_300_360)
                fit_te_300_360 = cont_ratio_300_360[icont_ratio, 0]
                icont_ratio, vcont_ratio = AnalyseSynthDiag.find_nearest(cont_ratio_400_500[:, 1], ratio_400_500)
                fit_te_400_500 = cont_ratio_400_500[icont_ratio, 0]

                ##### Add fit Te result to dictionary
                res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum'] = {
                    'fit': {'fit_te_360_400': fit_te_360_400, 'fit_te_300_360': fit_te_300_360,
                            'fit_te_400_500': fit_te_400_500, 'units': 'eV'}}

                ###############################################################
                # CALCULATE EFFECTIVE DEL_L USING LINE-INT ne AND Te VALUES AND CONTINUUM
                ###############################################################
                if res_dict[diag_key][chord_key]['los_int']['stark']['fit']['ne']:
                    params = Parameters()
                    params.add('delL', value=0.5, min=0.0001, max=10.0)
                    params.add('te_360_400', value=fit_te_360_400)
                    fit_ne = res_dict[diag_key][chord_key]['los_int']['stark']['fit']['ne']
                    params.add('ne', value=fit_ne)
                    params['te_360_400'].vary = False
                    params['ne'].vary = False

                    fit_result = minimize(AnalyseSynthDiag.residual_continuo, params, args=(wave_fffb, synth_data_fffb),
                                          method='leastsq')
                    data_fit_ff_fb = AnalyseSynthDiag.residual_continuo(fit_result.params, wave_fffb, None, None)

                    fit_report(fit_result)

                    vals = fit_result.params.valuesdict()

                    ##### Add fit delL result to dictionary
                    res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['fit']['delL_360_400'] = \
                        vals['delL']

    @staticmethod
    def recover_line_int_Stark_ne(res_dict):
        """
            RECOVER LINE-AVERAGED ELECTRON DENSITY FROM H6-2 STARK BROADENED SPECTRA
        """
        mmm_coeff = {'6t2': {'C': 3.954E-16, 'a': 0.7149, 'b': 0.028}}

        for diag_key in res_dict.keys():
            for chord_key in res_dict[diag_key].keys():

                print('Fitting Stark broadened H6-2 spectra, LOS id= :', diag_key, ' ', chord_key)

                for H_line_key in res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'].keys():

                    if res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'][H_line_key][0] == '6' and \
                                    res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'][H_line_key][1] == '2':

                        wave_stark = np.asarray(res_dict[diag_key][chord_key]['los_int']['stark']['wave'])
                        synth_data_stark = np.asarray(res_dict[diag_key][chord_key]['los_int']['stark']['intensity'])

                        # print(wave_stark)
                        # print(synth_data_stark)

                        params = Parameters()
                        params.add('cwl', value=float(H_line_key) / 10.0)
                        params.add('area', value=float(
                            res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['excit'] +
                            res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['recom']))
                        params.add('stark_fwhm', value=0.15, min=0.0001, max=10.0)

                        params['cwl'].vary = True
                        params['area'].vary = True

                        fit_result = minimize(AnalyseSynthDiag.residual_lorentz_52, params,
                                              args=(wave_stark,), kws={'data':synth_data_stark}, method='leastsq')
                        data_fit_ne = AnalyseSynthDiag.residual_lorentz_52(fit_result.params, wave_stark)

                        fit_report(fit_result)

                        vals = fit_result.params.valuesdict()

                        # Assume Te = 1 eV
                        fit_ne = np.power((vals['stark_fwhm'] / mmm_coeff['6t2']['C']),
                                          1. / mmm_coeff['6t2']['a'])

                        ##### Add fit ne result to dictionary
                        res_dict[diag_key][chord_key]['los_int']['stark']['fit'] = {'ne': fit_ne, 'units': 'm^-3'}

    def recover_line_int_particle_bal(self, res_dict, sion_H_transition=['3','2'], ne_scal=1.0):
        """
            ESTIMATE RECOMBINATION/IONISATION RATES USING ADF11 ACD, SCD COEFF
        """

        # Use ADAS adf15,11 data taking into account Ly-series trapping and hence a modification
        # to the ionization/recombination rates.
        if self.ADAS_dict_lytrap:
            ADAS_dict_local = self.ADAS_dict_lytrap
            spec_line_dict_key = 'spec_line_dict_lytrap'
        else:
            ADAS_dict_local = self.ADAS_dict
            spec_line_dict_key = 'spec_line_dict'

        for diag_key in res_dict.keys():
            for chord_key in res_dict[diag_key].keys():

                if (res_dict[diag_key][chord_key]['los_int']['stark']['fit']['ne'] and
                    res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['fit']['fit_te_360_400']):

                    fit_ne = ne_scal*res_dict[diag_key][chord_key]['los_int']['stark']['fit']['ne']
                    fit_Te = res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['fit']['fit_te_360_400']
                    # Use highest Te estimate from continuum (usually not available from experiment)
                    # fit_Te = res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['fit']['fit_te_400_500']

                    print('Ionization/recombination, LOS id= :', diag_key, ' ', chord_key)

                    # area_cm2 = 2*pi*R*dW
                    w2unmod = res_dict[diag_key][chord_key]['chord']['w2']
                    # area_cm2 = 1.0e04 * 2.*np.pi*res_dict[diag_key][chord_key]['chord']['d2unmod']*res_dict[diag_key][chord_key]['coord']['v2'][0]
                    area_cm2 = 1.0e04 * 2. * np.pi * w2unmod * \
                               res_dict[diag_key][chord_key]['chord']['p2'][0]
                    idxTe, Te_val = self.find_nearest(self.ADAS_dict['adf11']['1'].Te_arr, fit_Te)
                    idxne, ne_val = self.find_nearest(self.ADAS_dict['adf11']['1'].ne_arr, fit_ne * 1.0E-06)

                    # Recombination:
                    # NOTE: D7-2 line must be read from standard ADAS adf15 data as it is above the
                    # max transition available in the Ly-trapped adf15 files
                    for H_line_key in res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'].keys():
                        if res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'][H_line_key][0] == '7' and \
                                        res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'][H_line_key][1] == '2':
                            h72 = res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['excit'] + \
                                  res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['recom']
                            srec = 1.0E-04 * area_cm2 * h72 * 4. * np.pi * \
                                   self.ADAS_dict['adf11']['1'].acd[idxTe, idxne] / \
                                   self.ADAS_dict['adf15']['1']['1'][H_line_key + 'recom'].pec[idxTe, idxne]

                            # Add to results dict
                            res_dict[diag_key][chord_key]['los_int']['adf11_fit'] = {'Srec': srec, 'units': 's^-1'}

                    # Ionization:
                    # Use Ly-trapping adf15,11 data if available
                    for H_line_key in res_dict[diag_key][chord_key][spec_line_dict_key]['1']['1'].keys():
                        if res_dict[diag_key][chord_key][spec_line_dict_key]['1']['1'][H_line_key][0] == sion_H_transition[0] and \
                                        res_dict[diag_key][chord_key][spec_line_dict_key]['1']['1'][H_line_key][1] == sion_H_transition[1]:
                            h_excit = res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['excit']
                            sion = 1.0E-04 * area_cm2 * h_excit * 4. * np.pi * \
                                   ADAS_dict_local['adf11']['1'].scd[idxTe, idxne] / \
                            ADAS_dict_local['adf15']['1']['1'][H_line_key + 'excit'].pec[idxTe, idxne]

                            # Add to results dict
                            res_dict[diag_key][chord_key]['los_int']['adf11_fit']['Sion'] = sion



    def recover_delL_atomden_product(self, res_dict):
        """
            ESTIMATE DEL_L * ATOMIC DENSITY PRODUCT FROM LY-ALPHA ASSUMING EXCITATION DOMINATED
        """
        for diag_key in res_dict.keys():
            for chord_key in res_dict[diag_key].keys():

                if (res_dict[diag_key][chord_key]['los_int']['stark']['fit']['ne'] and
                        res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['fit']['fit_te_360_400']):

                    fit_ne = res_dict[diag_key][chord_key]['los_int']['stark']['fit']['ne']
                    fit_Te = res_dict[diag_key][chord_key]['los_int']['ff_fb_continuum']['fit']['fit_te_360_400']

                    print('delL * n0 from Ly-alpha, LOS id= :', diag_key, ' ', chord_key)

                    for H_line_key in res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'].keys():
                        if res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'][H_line_key][0] == '2' and \
                                        res_dict[diag_key][chord_key]['spec_line_dict']['1']['1'][H_line_key][1] == '1':
                            h21 = res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['excit'] + \
                                  res_dict[diag_key][chord_key]['los_int']['H_emiss'][H_line_key]['recom']
                            idxTe, Te_val = self.find_nearest(
                                self.ADAS_dict['adf15']['1']['1'][H_line_key + 'recom'].Te_arr, fit_Te)
                            idxne, ne_val = self.find_nearest(
                                self.ADAS_dict['adf15']['1']['1'][H_line_key + 'recom'].ne_arr, fit_ne * 1.0E-06)
                            n0delL_Lya_tmp = 4. * np.pi * 1.0e-04 * h21 / (
                                self.ADAS_dict['adf15']['1']['1'][H_line_key + 'excit'].pec[idxTe, idxne] * ne_val)
                            n0delL_Lya_tmp = n0delL_Lya_tmp * 1.0e06 * 1.0e-02  # convert to m^-2
                            ##### Add fit n0*delL result to dictionary
                            res_dict[diag_key][chord_key]['los_int']['Ly_alpha_fit'] = {'n0delL': n0delL_Lya_tmp,
                                                                             'units': 'm^-2'}
