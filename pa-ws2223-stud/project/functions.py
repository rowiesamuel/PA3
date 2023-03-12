from typing import Union
import numpy as np
import pandas as pd
import h5py
import math


def gen_path_for_multi_speeds(
    run_id: int, index: list[str], pump_speeds: list[float]
) -> list[str]:
    temp = ""
    path_list=[]
    for i in index :
        for p in pump_speeds:
            temp = '/run' + str(run_id)+'/Kennlinie_ESP_c_'+str(p)+"_"+str(i)+"/"
            path_list.append(temp)

    return path_list

def read_dataframe_metadata(
    file: str, path: str, att_key: str
) -> Union[np.float64, np.int32, np.bytes_, None]:
    hdf = pd.HDFStore(file,mode ='r')
    df = hdf.get_storer(path)


    try:
        return df[att_key]._metadata[0].encode('utf-8')
    except KeyError:
        print("fehler aufgetreten")

def read_group_metadata(
    file: str, path: str, att_key: str
) -> Union[np.float64, np.int32, np.bytes_, None]:
    with h5py.File(file,"r") as f:
        return f[path].attrs[att_key]
   


def get_df(file: str, path: str) -> pd.DataFrame:
   hdf = pd.HDFStore(file, mode='r')
   df = hdf.get(path)
   return df


def check_col_signum(df: pd.DataFrame, col: str, threshold: int) -> None:
    if (df[col] >= threshold).any():
        return True
    else:
        raise ValueError("Value does not meet criterion 1.")


def check_number_of_measurements(
    df: pd.DataFrame, col: str, f: float, t: float
) -> None:
    if(len(df[col] == f*t)):
        return True
    else:
        raise ValueError("Value does not meet criterion 2.")

   


def gen_plotdata(
    file_path: str,
    path_list: list,
    cols: list,
    output_size: tuple,
) -> np.ndarray:
    

    att_1 = "cyan_dp_unsicherheitsintervall"
    att_2 = "cyan_q_unsicherheitsintervall"

    final_list = []
    path_list_length = len(path_list)

    for i in range(path_list_length):
        df = get_df(file_path, path_list[i])

        dp_speed_mean = get_average_value(df, cols[0])
        dp_metadata = read_dataframe_metadata(file_path, path_list[i], att_1)
        dp_normal_std = std_uniform_to_normal(dp_metadata)
        dp_std = total_uncertainty(dp_metadata, dp_normal_std)

        q_speed_mean = get_average_value(df, cols[1])
        q_metadata = read_dataframe_metadata(file_path, path_list[i], att_2)
        q_normal_std = std_uniform_to_normal(q_metadata)
        q_std = total_uncertainty(q_metadata, q_normal_std)

        final_list.append(dp_speed_mean)
        final_list.append(dp_std)
        final_list.append(q_speed_mean)
        final_list.append(q_std)

    final = np.reshape(final_list, output_size)

    return final

        


def get_average_value(df: pd.DataFrame, col: str) -> float:
    return df[col].mean()


def get_std_deviation(df: pd.DataFrame, col: str) -> float:
    return df[col].std()


def std_uniform_to_normal(std_uniform: float) -> float:
    return std_uniform / math.sqrt(3)


def total_uncertainty(stat: float, sys: float) -> float:
    return math.sqrt((stat * stat) + (sys * sys))


def convert_bar_to_pa(v: pd.Series) -> pd.Series:
    return v * 100000


def convert_lpm_to_qmps(v: pd.Series) -> pd.Series:
    return v * ((5/3) * 0.00001)


def dataframe_dedimension(
    plot_data: pd.DataFrame,
    pump_speeds: list,
    metadata: dict,
) -> pd.DataFrame:

    pump_speed_hz = []
    for rpm in pump_speeds:
        new_pump_speeds = convert_rpm_to_hz(rpm)
        pump_speed_hz.append(new_pump_speeds) 

    final = pd.DataFrame(columns=['psi_1260', 'psi_1260_uncertainty, phi_1260', 'phi_1260_uncertainty', 'psi_780', 'psi_780_uncertainty', 'phi_780', 'phi_780_uncertainty',
                                        'psi_540', 'psi_540_uncertainty', 'phi_540', 'phi_540_uncertainty'])

    plot_data_copy = plot_data.copy()

    pump_speed_hz = []
    for rpm in pump_speeds:
        new_pump_speeds = convert_rpm_to_hz(rpm)
        pump_speed_hz.append(new_pump_speeds)

    #delta_p = dp_1260_mean
    #n = pump_speeds (already hertz)
    #d = metadata.cyan_pumpe_char_laenge
    #rho = metadata.foerdermedium_dichte


    #start loop here
    for i in range(5):

        first_delta_p = plot_data_copy['dp_1260_mean'].iloc[i]
        third_delta_p = plot_data_copy['dp_780_mean'].iloc[i]
        second_delta_p = plot_data_copy['dp_540_mean'].iloc[i]
        first_n = pump_speed_hz[0] #arrange according to speed (assumption 1260)
        third_n = pump_speed_hz[1] #arrange according to speed (assumption 540)
        second_n = pump_speed_hz[2] #arrange according to speed (assumption 780)
        d = metadata.get('cyan_pumpe_char_laenge')
        rho = metadata.get('foerdermedium_dichte')

        psi_1260 = calc_pressure_number(first_delta_p, first_n, d, rho)
        psi_780 = calc_pressure_number(second_delta_p, second_n, d, rho)
        psi_540 = calc_pressure_number(third_delta_p, third_n, d, rho)

        first_q = plot_data_copy['q_1260_mean'].iloc[i]
        second_q = plot_data_copy['q_540_mean'].iloc[i]
        third_q = plot_data_copy['q_780_mean'].iloc[i]



        phi_1260 = calc_flow_number(first_q, first_n, d)
        phi_540 = calc_flow_number(second_q, second_n, d)
        phi_780 = calc_flow_number(third_q, third_n, d)

        first_total_uncertainty_p = plot_data_copy['dp_1260_std'].iloc[i]
        second_total_uncertainty_p = plot_data_copy['dp_540_std'].iloc[i]
        third_total_uncertainty_p = plot_data_copy['dp_780_std'].iloc[i]

        total_uncertainty_rho = metadata.get('foerdermedium_dichte_unsicherheitsintervall')
        total_uncertainty_n = metadata.get('cyan_pumpe_drehzahl_unsicherheitsintervall')
        total_uncertainty_d = metadata.get('cyan_pumpe_char_laenge_unsicherheitsintervall')

        psi_1260_uncertainty = uncertainty_pressure_number(first_total_uncertainty_p, first_delta_p, total_uncertainty_rho, rho, total_uncertainty_n, first_n, total_uncertainty_d,
                                                        d, psi_1260)
        psi_540_uncertainty = uncertainty_pressure_number(second_total_uncertainty_p, second_delta_p, total_uncertainty_rho, rho, total_uncertainty_n, second_n, total_uncertainty_d,
                                                        d, psi_540)
        psi_780_uncertainty = uncertainty_pressure_number(third_total_uncertainty_p, third_delta_p, total_uncertainty_rho, rho, total_uncertainty_n, third_n, total_uncertainty_d,
                                                        d, psi_780)

        first_total_uncertainty_q = plot_data_copy['q_1260_std'].iloc[i]
        second_total_uncertainty_q = plot_data_copy['q_540_std'].iloc[i]
        third_total_uncertainty_q = plot_data_copy['q_780_std'].iloc[1]

        phi_1260_uncertainty = uncertainty_flow_number(first_total_uncertainty_q, first_q, total_uncertainty_n, first_n, total_uncertainty_d, d, phi_1260)
        phi_540_uncertainty = uncertainty_flow_number(second_total_uncertainty_q, second_q, total_uncertainty_n, second_n, total_uncertainty_d, d, phi_540)
        phi_780_uncertainty = uncertainty_flow_number(third_total_uncertainty_q, third_q, total_uncertainty_n, third_n, total_uncertainty_d, d, phi_780)

        temp_list = []
        temp_list.append(psi_1260, psi_1260_uncertainty, phi_1260, phi_1260_uncertainty, psi_780, psi_780_uncertainty, phi_780, phi_780_uncertainty, psi_540, psi_540_uncertainty, phi_540, phi_540_uncertainty)

        final.loc[i] = temp_list


    #end loop 

    return final
    

    
    

    



def convert_rpm_to_hz(v: float) -> float:
    return v / 60


def calc_pressure_number(
    delta_p: float,
    n: float,
    d: float,
    rho: float,
) -> float:
    return (2 * delta_p)/((n * n)*(d * d) * rho) 


def calc_flow_number(q: float, n: float, d: float) -> float:
    return (4 * q) / (np.pi * np.pi * n * d * d * d)


def uncertainty_pressure_number(
    total_uncertainty_p: float,
    p: float,
    total_uncertainty_rho: float,
    rho: float,
    total_uncertainty_n: float,
    n: float,
    total_uncertainty_d: float,
    d: float,
    psi: float,
) -> float:
    return psi * math.sqrt((total_uncertainty_p / p)**2 + (total_uncertainty_rho / rho)**2 + ((2 * total_uncertainty_n / n)**2) + (2 * total_uncertainty_d / d)**2)


def uncertainty_flow_number(
    total_uncertainty_q: float,
    q: float,
    total_uncertainty_n: float,
    n: float,
    total_uncertainty_d: float,
    d: float,
    phi: float,
) -> float:
    return phi * math.sqrt((total_uncertainty_q / q)**2 + (total_uncertainty_n / n)**2 + (3 * total_uncertainty_d / d)**2)


def main():
    # DEBUG und Test
    pass


if __name__ == "__main__":
    main()
