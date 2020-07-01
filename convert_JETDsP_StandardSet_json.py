def extract_jetdsp_signals(filename):
    tag = 'URL'
    jpf_signal_list = []
    ppf_signal_list = []
    number = 0

    dictionary = {}
    dictionary['ppf'] = {}
    dictionary['jpf'] = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):

            if tag in str(line):
                # storing line
                signal_type = line.split()[1].split('/')[0]
                signal = line.split()[1].split('/')[1:]

                if signal_type.lower() =='ppf':
                    DDA = signal[1]
                    DTYPE = signal[2]
                    if 'UID' in DTYPE:
                        uid = DTYPE.split('=')[-1]
                        DTYPE = DTYPE.split('?')[0]
                    else:
                        uid = 'JETPPF'
                    if 'X=' in DTYPE:
                        no_x = DTYPE.split('=')[-1]
                        DTYPE = DTYPE.split('?')[0]
                        DTYPE = DTYPE+'/'+no_x



                    ppf_signal_list.append(DDA+'/'+DTYPE)
                    number +=1
                    dictionary['ppf'][uid+'/'+DDA+'/'+DTYPE] = [str(number), ".", ":"]
                if signal_type.lower() =='jpf':
                    SUBSYSTEM = signal[1]
                    DTYPE = signal[2]
                    jpf_signal_list.append(SUBSYSTEM+'/'+DTYPE)
                    number += 1
                    dictionary['jpf'][SUBSYSTEM + '/' + DTYPE] = [str(number), ".", ":"]

    column, mod = divmod(number, 10)

    div, mod = divmod(number,column)

    dictionary["icolumn"]=str(column)
    dictionary["irow"] = str(div + mod)
    dictionary["linewidth"] = str(0.5)
    dictionary["markersize"] = str(1)

    return jpf_signal_list, ppf_signal_list, dictionary


if __name__ == "__main__":
                # break

    jpf_signal_list, ppf_signal_list, dictionary = extract_jetdsp_signals(
        '/home/bviola/.jetdsp/StandardSets/MainParameters_7.jss')
    import json
    with open("/u/bviola/work/Python/bruvio_tool/standard_set/MainParameters_7_converted.json","w") as f:
        json.dump(dictionary,f,indent=4)