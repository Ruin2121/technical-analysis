from typing import Union

import numpy as np
import pandas as pd

from utils import to_numpy, pre_return_conversion


def simple_moving_average(data: Union[list, np.ndarray, pd.Series], window: int, output_type: str = "numpy") -> Union[
    list, np.ndarray, pd.Series]:
    """
    Calculates the Simple Moving Average (SMA) of a python list, pandas series, or numpy array.

    Parameters:
    -----------
    data : Union[list, np.ndarray, pd.Series]
        The input array of values.
    window : int
        The size of the window used to calculate the SMA.
    output_type : str, optional
        Specifies the desired output type. Must be "list", "numpy", or "pandas".

    Returns:
    --------
    Union[list, np.ndarray, pd.Series]
        The array of SMA values, with NaN values in the first (window-1) positions.

    Raises:
    -------
    ValueError:
        Raised if the window is either not a positive integer or if the window size is greater than the length of the data.
        Raised if the input data contains NaN or infinite values.
        Raised if the input data is not numeric.
    """
    if not isinstance(window, int) or window <= 0:
        raise ValueError("Window must be a positive integer.")
    if window > len(data):
        raise ValueError("Window size cannot be greater than the length of the data.")

    data_arr = to_numpy(data)

    if not np.isfinite(data_arr).all():
        raise ValueError("Input data contains NaN or infinite values.")
    if not np.issubdtype(data_arr.dtype, np.number):
        raise ValueError("Input data must be numeric.")

    weights = np.repeat(1.0, window) / window
    sma_values = np.convolve(data_arr, weights, 'valid')
    sma_values = np.concatenate((np.full(window - 1, np.nan), sma_values), axis=0)
    return_values = pre_return_conversion(sma_values, output_type)
    return return_values
