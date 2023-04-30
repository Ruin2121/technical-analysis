import numpy as np
import pandas as pd
from typing import Union
from technical_analysis.baseclasses import BaseMovingAverageClass


class SimpleMovingAverage(BaseMovingAverageClass):
    """
    Implementation of Simple Moving Average (SMA) calculation.

    Parameters
    ----------
    data: Union[list, np.ndarray, pd.Series]
        A list, NumPy array, or Pandas series containing the data to be analyzed.
    window: int
        An integer representing the size of the window used for the moving average.

    Inherited Methods
    -----------------
    to_list()
        returns the output of the indicator calculation as a list.
    to_np_array()
        returns the output of the indicator calculation as a NumPy array.
    to_pd_series()
        returns the output of the indicator calculation as a Pandas Series.
    return_window()
        Returns the window of the moving average.
    """

    def __init__(self, data: Union[list, np.ndarray, pd.Series], window: int):
        """
        Initializes the Simple Moving Average class.
        """
        super().__init__()
        self._window = window
        self.__numpy_data = self._to_numpy(data)
        self._handle_common_errors(self.__numpy_data, window)
        self._calculation()

    def _calculation(self):
        """
        Performs the calculation of the Simple Moving Average.
        """
        weights = np.repeat(1.0, self._window) / self._window
        sma = np.convolve(self.__numpy_data, weights, "full")[: len(self.__numpy_data)]
        self._output_data = sma
