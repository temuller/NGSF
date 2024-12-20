import os
import csv
import glob
import numpy as np
from pathlib import Path
from astropy.io import ascii

import NGSF
from NGSF.params import Parameters, data
ngsf_path = Path(NGSF.__path__[0])

def JD(mjd):
    return float(mjd) + 2400000.5

def list_folders(path):
    if path[-1] != '/':
        path=path+'/'

    folders=[]
    dirs=glob.glob(path+'*')
    for dir in dirs:
        if os.path.isdir(dir):
            folders.append(dir)

    return folders

class Metadata(object):

    def __init__(self):

        parameters = Parameters(data)

        mjd_max_brightness = Path(ngsf_path, 'mjd_of_maximum_brightness.csv')

        with open(mjd_max_brightness, mode='r') as inp:
            reader = csv.reader(inp)
            band_dictionary = {rows[0]:rows[2] for rows in reader}


        with open(mjd_max_brightness, mode='r') as inp:
            reader = csv.reader(inp)
            MJD_dictionary = {rows[0]:rows[1] for rows in reader}




        folders = [str(ngsf_path) + '/bank/original_resolution/sne/'+ x for x in parameters.temp_sn_tr]
        have_wiserep=[]
        no_wiserep=[]
        z_dic={}
        path_dic={}
        dictionary_all_trunc_objects ={}
        JD_dic={}
        coord_dic={}
        spec_file_dic={}
        inst_dic={}
        obs_date_dict={}
        shorhand_dict={}
        Type_dic={}
        subfolders=[]
        short_path_dict={}
        for folder in folders:
            subs=list_folders(folder)
            for sub in subs:
                subpath=sub
                idx=subpath.rfind('/')
                sub=subpath[(idx+1):]
                subfolders.append(subpath)
                idx2=subpath[0:idx].rfind('/')
                sn_type=subpath[idx2+1:idx]
                Type_dic[sub]=sn_type
                if os.path.exists(subpath+'/wiserep_spectra.csv'):
                    have_wiserep.append(subpath)
                    wise=ascii.read(subpath+'/wiserep_spectra.csv')
                    path_dic[sub]=subpath
                    z_dic[sub]=wise['Redshift'][0]
                    coord_dic[sub]=np.array(list(wise['Obj. RA','Obj. DEC'][0]))



                    JD_dic[sub]=np.array(wise['JD'][:])
                    obs_date_dict[sub]=np.array(wise['Obs-date'][:])
                    spec_file_dic[sub]=np.array(wise['Ascii file'][:])
                    inst_dic[sub]=np.array(wise['Instrument'][:])
                    lis=[]
                    for i,spec_file in enumerate(spec_file_dic[sub]):



                        if float(MJD_dictionary[sub]) == -1:

                            phase = 'u'

                        else:

                            phase = float(wise['JD'][i]) - JD(float(MJD_dictionary[sub]))

                            phase = round(phase,2)


                        if parameters.epoch_high == parameters.epoch_low:

                            band = band_dictionary[sub]

                            shorhand_dict[spec_file]=sn_type + '/' + sub + '/' + wise['Instrument'][i]+' phase-band : '+ str(phase) + str(band)

                            short_path_dict[shorhand_dict[spec_file]]=spec_file

                            dictionary_all_trunc_objects[spec_file] = str(ngsf_path) + '/bank/original_resolution/sne/' + sn_type +'/'+ sub + '/' + spec_file



                        else:

                            if phase!='u' and phase >= parameters.epoch_low and phase <= parameters.epoch_high:

                                band = band_dictionary[sub]

                                shorhand_dict[spec_file]=sn_type + '/' + sub + '/' + wise['Instrument'][i]+' phase-band : '+ str(phase) + str(band)

                                short_path_dict[shorhand_dict[spec_file]]=spec_file

                                dictionary_all_trunc_objects[spec_file] = str(ngsf_path) + '/bank/original_resolution/sne/' + sn_type +'/'+ sub + '/' + spec_file



                else:
                    no_wiserep.append(subpath)

        self.shorhand_dict = shorhand_dict
        self.no_wiserep = no_wiserep
        self.dictionary_all_trunc_objects = dictionary_all_trunc_objects
