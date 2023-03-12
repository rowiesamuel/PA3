from project import functions
import os
import h5py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

data_file = 'pa-ws2223-stud/project/data/data_230209_GdD_PA3_Datensatz_Kennfeldmessung_Exzenterschneckenpumpe_Sirupmischanlage_Logan.hdf5' 
features_of_interest = ['cyan_dp','cyan_q']

run_id = 1
index = ['deg16.5', 'deg18', 'deg24', 'deg36', 'deg60']
pump_speeds = [1260, 540, 780]
list = functions.gen_path_for_multi_speeds(run_id, index, pump_speeds)
print(list)


def main():
    path = '/run1/'
    run_id = 1
    #feature = "\'Kennlinie_ESP_c_1260_deg16.5\'" 
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

    plot_data_copy = plot_data.copy()
    pump_speed_hz = []
    pump_speed_hz = functions.convert_rpm_to_hz(pump_speeds)
    

    functions.dataframe_dedimension(df_copy, pump_speeds, attribute_dict)
    #3a
    first_dp = new_df["dp_1260_mean"].to_list()
    second_dp = new_df["dp_540_mean"].to_list()
    third_dp = new_df["dp_780_mean"].to_list()

    first_q = new_df["q_1260_mean"].to_list()
    second_q = new_df["q_540_mean"].to_list()
    third_q = new_df["q_780_mean"].to_list()

    first_dp_std = new_df["dp_1260_std"].to_list()
    second_dp_std = new_df["dp_540_std"].to_list()
    third_dp_std = new_df["dp_780_std"].to_list()

    first_q_std = new_df["q_1260_std"].to_list()
    second_q_std = new_df["q_1260_std"].to_list()
    third_q_std = new_df["q_1260_std"].to_list()

    temperature = functions.read_group_metadata(data_file, "run1", "foerdermedium_temperatur")
    unit_temperature = functions.read_group_metadata(data_file, "run1", "foerdermedium_temperatur_einheit")
    unit_temperature = unit_temperature.decode("utf-8")
    pumps = functions.read_group_metadata(data_file, "run1", "pumpentyp")
    pumps = pumps.decode("utf-8")
    viscosity = functions.read_group_metadata(data_file, "run1", "foerdermedium_dynamische_viskositaet")
    unit_viscosity = functions.read_group_metadata(data_file, "run1", "foerdermedium_dynamische_viskositaet_einheit")
    unit_viscosity = unit_viscosity.decode("utf-8)")

    label_pump = "Pumpentyp" + pumps
    label_viscosity = "Viskositaet" + str(viscosity) + unit_viscosity
    label_temperature = "Temperatur" + str(temperature) + unit_temperature

    fig, ax = plt.subplot()
    ax.plot(first_q, first_dp, label = "speed 1260")
    ax.plot(second_q, second_dp, label = "speed 540")
    ax.plot(third_q, third_dp, label = "speed 780")

    ax.errrorbar(first_q, first_dp, yerr = first_dp_std, xerr = first_q_std)
    ax.errrorbar(second_q, second_dp, yerr = second_dp_std, xerr = second_q_std)
    ax.errrorbar(third_q, third_dp, yerr = third_dp_std, xerr = third_q_std)


    ax.set_ylabel("Druckdifferenz")
    ax.set_xlabel("Volumenstrom")
    ax.legend()

    ax.text(1, 4, label_pump, fontsize = 5)
    ax.text(1, 4, label_viscosity, fontsize = 5)
    ax.text(1, 4, label_temperature, fontsize = 5)
    plt.show()

    #3b
    new_dimension = functions.dataframe_dedimension(new_df, pump_speeds, attribute_list)

    first_psi = new_dimension["psi_1260"].to_list()
    second_psi = new_dimension["psi_540"].to_list()
    third_psi = new_dimension["psi_780"].to_list()

    first_phi = new_dimension["phi_1260"].to_list()
    second_phi = new_dimension["phi_540"].to_list()
    third_phi = new_dimension["phi_780"].to_list()

    first_psi_uncertainty = new_dimension["psi_1260_uncertainty"].to_list()
    second_psi_uncertainty = new_dimension["psi_540_uncertainty"].to_list()
    third_psi_uncertainty = new_dimension["psi_780_uncertainty"].to_list()

    first_phi_uncertainty = new_dimension["phi_1260_uncertainty"].to_list()
    second_phi_uncertainty = new_dimension["phi_540_uncertainty"].to_list()
    third_phi_uncertainty = new_dimension["phi_780_uncertainty"].to_list()

    fig, ax = plt.subplot()
    ax.plot(first_phi,first_psi, label_temperature = "speed 1260")
    ax.plot(second_phi,second_psi, label_temperature = "speed 540")
    ax.plot(third_phi,third_psi, label_temperature = "speed 780")

    ax.errorbar(first_phi, first_psi, yerr = first_psi_uncertainty, xerr = first_phi_uncertainty)
    ax.errorbar(second_phi, second_psi, yerr = second_psi_uncertainty, xerr = second_phi_uncertainty)
    ax.errorbar(third_phi, third_psi, yerr = third_psi_uncertainty, xerr = second_phi_uncertainty)

    ax.set_ylabel_("Druckzahl")
    ax.set_xlabel ("Durchflusszahl")
    plt.show()


if __name__ == "__main__":
    main()

    
   
