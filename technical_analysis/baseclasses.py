import abc
import numpy as np
import pandas as pd


class BaseIndicatorClass(abc.ABC):
    def __init__(self):
        self._output_data = None

    @property
    def output_data(self):
        if self._output_data is None:
            raise AttributeError("output_data must be set")
        return self._output_data

    @output_data.setter
    def output_data(self, value):
        self._output_data = value

    @staticmethod
    def _to_numpy(data) -> np.ndarray:
        """
            Converts the input data to a NumPy array.

            Returns:
                A NumPy array containing the input data.

            Raises:
                TypeError: If the input data type is not supported (list, NumPy array, or Pandas series).
        """
        if isinstance(data, list):
            return np.array(data)
        elif isinstance(data, np.ndarray):
            return data
        elif isinstance(data, pd.Series):
            return data.to_numpy()
        else:
            raise TypeError("Input data must be a list, NumPy array, or Pandas Series")

    @abc.abstractmethod
    def _calculation(self):
        """
            The calculations for the indicator should go hear.

            Should set self._output_data.

            Should not return anything.
        """
        pass

    def to_list(self) -> list:
        """
            Returns the calculated moving average as a native Python list.

            Returns:
                A list containing the calculated moving average.
        """
        return self._output_data.tolist()

    def to_np_array(self) -> np.ndarray:
        """
            Returns the calculated moving average as a NumPy array.

            Returns:
                A NumPy array containing the calculated moving average.
        """
        return self._output_data

    def to_pd_series(self) -> pd.Series:
        """
            Returns the calculated moving average as a Pandas series.

            Returns:
                A Pandas series containing the calculated moving average.
        """
        return pd.Series(self._output_data)

    @staticmethod
    def _handle_common_errors(numpy_data: np.ndarray = None, window_size: int = None):
        if numpy_data is not None:
            if len(numpy_data) < 1:
                raise ValueError("Input Data contains no values.")
            if np.isnan(numpy_data).any():
                raise ValueError("Input data contains NaN values.")
            if np.isinf(numpy_data).any():
                raise ValueError("Input data contains infinite values.")
            if not np.issubdtype(numpy_data.dtype, np.number) or np.issubdtype(numpy_data.dtype, np.timedelta64):
                raise ValueError("Input data contains non-numeric values.")

        if window_size is not None:
            if not isinstance(window_size, int):
                raise TypeError("Window size must be an integer.")
            if window_size <= 0:
                raise ValueError("Window size must be a positive integer.")

        if numpy_data is not None and window_size is not None:
            if window_size > len(numpy_data):
                raise ValueError("Window size cannot be greater than the length of the input data.")


class BaseMovingAverageClass(BaseIndicatorClass):
    def __init__(self):
        super().__init__()
        self._window = None

    def return_window(self):
        return self._window
