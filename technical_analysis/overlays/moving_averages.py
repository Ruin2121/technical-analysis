import numpy as np
import pandas as pd
from typing import Union


class SimpleMovingAverage:
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
        if window <= 0:
            raise ValueError("Window size must be a positive integer.")
        if window > len(data):
            raise ValueError("Window size cannot be greater than the length of the input data.")
        self.__raw_data = data
        self.__window = window
        self.__numpy_data = self.__to_numpy()
        self.__sma = None
        self.__simple_moving_average()

    def __to_numpy(self) -> np.ndarray:
        """
            Converts the input data to a NumPy array.

            Returns:
                A NumPy array containing the input data.

            Raises:
                TypeError: If the input data type is not supported (list, NumPy array, or Pandas series).
        """
        if isinstance(self.__raw_data, list):
            return np.array(self.__raw_data)
        elif isinstance(self.__raw_data, np.ndarray):
            return self.__raw_data
        elif isinstance(self.__raw_data, pd.Series):
            return self.__raw_data.to_numpy()
        else:
            raise TypeError("Input data type not supported. Please provide a list, NumPy array, or Pandas series.")

    def __simple_moving_average(self):
        """
            Calculates the simple moving average of the input data.

            Sets the calculated moving average to the object's __sma attribute.
        """
        weights = np.repeat(1.0, self.__window) / self.__window
        sma = np.convolve(self.__numpy_data, weights, 'full')[:len(self.__numpy_data)]
        self.__sma = sma

    def to_list(self) -> list:
        """
            Returns the calculated moving average as a native Python list.

            Returns:
                A list containing the calculated moving average.
        """
        return self.__sma.tolist()

    def to_np_array(self) -> np.ndarray:
        """
            Returns the calculated moving average as a NumPy array.

            Returns:
                A NumPy array containing the calculated moving average.
        """
        return self.__sma

    def to_pd_series(self) -> pd.Series:
        """
            Returns the calculated moving average as a Pandas series.

            Returns:
                A Pandas series containing the calculated moving average.
        """
        return pd.Series(self.__sma)
