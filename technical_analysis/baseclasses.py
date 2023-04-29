"""
    This module defines a base class for technical indicators and subclasses
    to use for type checking.
"""
from abc import ABC, abstractmethod
from typing import Union
import numpy as np
import pandas as pd


class BaseIndicatorClass(ABC):
    """
    This is an abstract base class for technical indicators. To create a new
    indicator, subclass this class and implement the abstract method
    `_calculation`.

    Attributes:
        _output_data: a NumPy array that holds the calculated values of the
        indicator. This must be set in order to extract data from the class.

    Methods:
        _to_numpy(data: Union[list, np.ndarray, pd.Series]) -> np.ndarray:
            Converts the input data to a NumPy array. All other methods assume
            the input data is a NumPy array, so this method should be called
            to preprocess the data.

        _handle_common_errors(numpy_data: np.ndarray, optional, window_size:
        int, optional):
            A utility function to handle common errors in technical indicators.
            Checks for missing, NaN, and infinite values, non-numeric values,
            and invalid window sizes. Though not required, it is a good idea
            to use this or create your own similar method.

        _calculation():
            An abstract method that calculates the values of the indicator.
            This method should set self._output_data but should not return
            anything. For consistency, all primary calculations for the
            indicator should occur within this function.

        to_list() -> list:
            Returns the calculated indicator as a native Python list.

        to_np_array() -> np.ndarray:
            Returns the calculated indicator as a NumPy array.

        to_pd_series() -> pd.Series:
            Returns the calculated indicator as a Pandas series.
    """

    def __init__(self):
        """
            Should only initialize variables that all indicators are expected
            to have.
        """
        self._output_data = None

    @staticmethod
    def _to_numpy(data: Union[list, np.ndarray, pd.Series]) -> np.ndarray:
        """
            Converts the input data to a NumPy array.

            Returns:
                A NumPy array containing the input data.

            Raises:
                TypeError: If the input data type is not supported (list,
                NumPy array, or Pandas series).
        """
        if isinstance(data, list):
            return np.array(data)
        if isinstance(data, np.ndarray):
            return data
        if isinstance(data, pd.Series):
            return data.to_numpy()
        raise TypeError(
            "Input data must be a list, NumPy array, or Pandas Series")

    @abstractmethod
    def _calculation(self):
        """
            The calculations for the indicator should go hear.

            Should set self._output_data.

            Should not return anything.
        """

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
    def _handle_common_errors(  # noqa
        numpy_data: np.ndarray = None,
            window_size: int = None):
        """
            Checks for common input errors and raises an exception if any are
            found.

            Args:
                numpy_data (numpy.ndarray, optional): A NumPy array of input
                data. Defaults to None.
                window_size (int, optional): The window size for calculations.
                Defaults to None.

            Raises:
                ValueError: If the input data contains no values, contains NaN
                or infinite values,
                    or contains non-numeric values, or if the window size is
                    greater than the length
                    of the input data.
                TypeError: If the window size is not an integer.
        """
        if numpy_data is not None:
            if len(numpy_data) < 1:
                raise ValueError("Input Data contains no values.")
            if np.isnan(numpy_data).any():
                raise ValueError("Input data contains NaN values.")
            if np.isinf(numpy_data).any():
                raise ValueError("Input data contains infinite values.")
            if not np.issubdtype(numpy_data.dtype, np.number) or np.issubdtype(
                    numpy_data.dtype, np.timedelta64):
                raise ValueError("Input data contains non-numeric values.")

        if window_size is not None:
            if not isinstance(window_size, int):
                raise TypeError("Window size must be an integer.")
            if window_size <= 0:
                raise ValueError("Window size must be a positive integer.")

        if numpy_data is not None and window_size is not None:
            if window_size > len(numpy_data):
                raise ValueError(
                    """Window size cannot be greater than the length of the
                    input data.""")


class BaseMovingAverageClass(BaseIndicatorClass, ABC):
    """
        This is a base class for moving average indicators, which inherits
        from `BaseIndicatorClass`.

        Attributes:
            _window (int): The window size for the moving average calculation.

        Methods:
            __init__(self): Initializes the object with _window set to None.
            return_window(self): Returns the window size used for the moving
            average calculation.

        Inherited Attributes:
            _output_data (numpy.ndarray): The output data from the indicator
            calculation.

        Inherited Methods:
            _to_numpy(data: Union[list, np.ndarray, pd.Series]) -> np.ndarray:
                Converts the input data to a NumPy array.
            _handle_common_errors(numpy_data: numpy.ndarray = None,
                window_size: int = None): Handles common errors.
            _calculation(self): Abstract method for the indicator calculation.
            to_list(self) -> list: Returns the calculated moving average as a
            native Python list.
            to_np_array(self) -> numpy.ndarray: Returns the calculated moving
            average as a NumPy array.
            to_pd_series(self) -> pandas.Series: Returns the calculated moving
            average as a Pandas series.
    """

    def __init__(self):
        """
            Should only initialize variables that all moving average
            indicators are expected to have.
        """
        super().__init__()
        self._window = None

    def return_window(self):
        """
            Returns the window size used for the moving average calculation.

            Returns:
                self._window
        """
        return self._window
