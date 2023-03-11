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
    plot_data_copy = plot_data.copy()

    plot_data = pd.DataFrame (plot_data, columns = ['psi_<1260>', 'psi_<1260>_uncertainty', 'phi_<1260>', 'phi_<1260>_uncertainty', 'psi_<540>', 'psi_<540>_uncertainty', 'phi_<540>', 'phi_<540>_uncertainty', 'psi_<780>', 'psi_<780>_uncertainty', 'phi_<780>', 'phi_<780>_uncertainty'])
    
    


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
