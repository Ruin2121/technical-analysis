import numpy as np
import pandas as pd
from typing import Union
from technical_analysis.baseclasses import BaseMovingAverageClass


class SimpleMovingAverage(BaseMovingAverageClass):
    """
        A class that calculates the simple moving average of a given data set.

        Args:
            data: A list, NumPy array, or Pandas series containing the data to be analyzed.
            window: An integer representing the size of the window used for the moving average.

        Returns:
            A list, NumPy array, or Pandas series containing the calculated moving average.

        Raises:
            TypeError: If the input data type is not supported (list, NumPy array, or Pandas series).
            ValueError: If the window size is not a positive integer.
            ValueError: If the window size is greater than the length of the input data.
    """
    def __init__(self, data: Union[list, np.ndarray, pd.Series], window: int):
        """
            Initializes a SimpleMovingAverage object.

            Args:
                data: A list, NumPy array, or Pandas series containing the data to be analyzed.
                window: An integer representing the size of the window used for the moving average.

            Raises:
                TypeError: If the input data type is not supported (list, NumPy array, or Pandas series).
                ValueError: If the window size is not a positive integer.
                ValueError: If the window size is greater than the length of the input data.
        """
        super().__init__()
        self._window = window
        self.__numpy_data = self._to_numpy(data)
        self._handle_common_errors(self.__numpy_data, window)
        self._calculation()

    def _calculation(self):
        """
            Calculates the simple moving average of the input data.

            Sets the calculated moving average to the object's _output_data attribute.
        """
        weights = np.repeat(1.0, self._window) / self._window
        sma = np.convolve(self.__numpy_data, weights, 'full')[:len(self.__numpy_data)]
        self._output_data = sma
