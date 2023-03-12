from project import functions
import os
import h5py
from pathlib import Path
import pandas as pd


def main():
   pass

if __name__ == "__main__":
    main()

    
   
data_file = 'pa-ws2223-stud/project/data/data_230209_GdD_PA3_Datensatz_Kennfeldmessung_Exzenterschneckenpumpe_Sirupmischanlage_Logan.hdf5' 
features_of_interest = ['cyan_dp','cyan_q']

run_id = 1
index = ['deg16.5', 'deg18', 'deg24', 'deg36', 'deg60']
pump_speeds = [1260, 540, 780]
list = functions.gen_path_for_multi_speeds(run_id, index, pump_speeds)
print(list)

#feature = "\'Kennlinie_ESP_c_1260_deg16.5\'" 
path = '/run1/'
#print(functions.read_group_metadata(data_file,path,feature))
df0 = functions.get_df(data_file, path[0]) #1260, 16.5
df1 = functions.get_df(data_file, path[1]) #540, 16.5
df2 = functions.get_df(data_file, path[2]) #780, 16.5
df3 = functions.get_df(data_file, path[3]) #1260, 18
df4 = functions.get_df(data_file, path[4]) #540, 18
df5 = functions.get_df(data_file, path[5]) #780, 18
df6 = functions.get_df(data_file, path[6]) #1260, 24
df7 = functions.get_df(data_file, path[7]) #540, 24
df8 = functions.get_df(data_file, path[8]) #780, 24
df9 = functions.get_df(data_file, path[9]) #1260, 36
df10 = functions.get_df(data_file, path[10]) #540, 36
df11 = functions.get_df(data_file, path[11]) #780, 36
df12 = functions.get_df(data_file, path[12]) #1260, 60
df13 = functions.get_df(data_file, path[13]) #540, 60
df14 = functions.get_df(data_file, path[14]) #780, 60

print(functions.check_col_signum(df0, 'cyan_dp', 0))
print(functions.check_col_signum(df1, 'cyan_dp', 0))
print(functions.check_col_signum(df2, 'cyan_dp', 0))
print(functions.check_col_signum(df3, 'cyan_dp', 0))
print(functions.check_col_signum(df4, 'cyan_dp', 0))
print(functions.check_col_signum(df5, 'cyan_dp', 0))
print(functions.check_col_signum(df6, 'cyan_dp', 0))
print(functions.check_col_signum(df7, 'cyan_dp', 0))
print(functions.check_col_signum(df8, 'cyan_dp', 0))
print(functions.check_col_signum(df9, 'cyan_dp', 0))
print(functions.check_col_signum(df10, 'cyan_dp', 0))
print(functions.check_col_signum(df11, 'cyan_dp', 0))
print(functions.check_col_signum(df12, 'cyan_dp', 0))
print(functions.check_col_signum(df13, 'cyan_dp', 0))
print(functions.check_col_signum(df14, 'cyan_dp', 0))

measure_duration = 3.0
sampling_frequency = 1000.0

print(len(df0))
print(len(df1))
print(len(df2))
print(len(df3))
print(len(df4))
print(len(df5))
print(len(df6))
print(len(df7))
print(len(df8))
print(len(df9))
print(len(df10))
print(len(df11))
print(len(df12))
print(len(df13))
print(len(df14))

print(functions.check_number_of_measurements(df0, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df1, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df2, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df3, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df4, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df5, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df6, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df7, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df8, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df9, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df10, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df11, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df12, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df13, 'cyan_dp', sampling_frequency, measure_duration))
print(functions.check_number_of_measurements(df14, 'cyan_dp', sampling_frequency, measure_duration))

o_size = (5, 12)
    
new_array = functions.gen_plotdata(data_file, path, features_of_interest, o_size)

new_df = pd.DataFrame(new_array, columns = ['dp_1260_mean', 'dp_1260_std', 'q_1260_mean', 'q_1260_std', 'dp_540_mean', 'dp_540_std', 'q_540_mean', 'q_540_std',
                                                'dp_780_mean', 'dp_780_std', 'q_780_mean', 'q_780_std'])
df_copy = new_df.copy()


attribute_list = []
value_list = []
path = '/run1/'
with h5py.File(data_file, "r") as f:
        #print(f[path].attrs[att_key])
        for a in f[path].attrs :
            attribute_list.append(a)
            #print(f[path].attrs[a])
            value = functions.read_group_metadata(data_file, path, a)
            value_list.append(value)

        #print(f[path].attrs)


attribute_dict = {k:v for k,v in zip(attribute_list, value_list)}
print(attribute_dict)

functions.dataframe_dedimension(df_copy, pump_speeds, attribute_dict)
    


