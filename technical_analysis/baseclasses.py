"""
This file contains baseclasses for use throughout the rest of the library.
"""
from abc import ABC, abstractmethod
from typing import Union
import numpy as np
import pandas as pd


class BaseIndicatorClass(ABC):
    """
    An abstract base class which should be used for all technical indicators.

    Attributes
    ----------
    _output_data : np.ndarray
        The output of the indicator calculation.

    Methods
    -------
    to_list()
        returns the output of the indicator calculation as a list.
    to_np_array()
        returns the output of the indicator calculation as a NumPy array.
    to_pd_series()
        returns the output of the indicator calculation as a Pandas Series.
    """

    def __init__(self):
        """
        Initializes the class.
        """
        self._output_data = None

    @staticmethod
    def _to_numpy(data: Union[list, np.ndarray, pd.Series]) -> np.ndarray:
        """
        Helper function to convert a list, NumPy array, or Pandas Series to a NumPy array.

        Parameters
        ----------
        data : Union[list, np.ndarray, pd.Series]
            The data to convert.

        Returns
        -------
        np.ndarray
            The converted data.

        Raises
        ------
        TypeError
            If the input data is not a list, NumPy array, or Pandas Series.
        """
        if isinstance(data, list):
            return np.array(data)
        if isinstance(data, np.ndarray):
            return data
        if isinstance(data, pd.Series):
            return data.to_numpy()
        raise TypeError("Input data must be a list, NumPy array, or Pandas Series")

    @abstractmethod
    def _calculation(self):
        """
        Calculates the output of the indicator.
        """
        pass

    def to_list(self) -> list:
        """
        Returns the output of the indicator calculation as a list.

        Returns
        -------
        list
            The output of the indicator calculation as a list.
        """
        return self._output_data.tolist()

    def to_np_array(self) -> np.ndarray:
        """
        Returns the output of the indicator calculation as a NumPy array.

        Returns
        -------
        np.ndarray
            The output of the indicator calculation as a NumPy array.
        """
        return self._output_data

    def to_pd_series(self) -> pd.Series:
        """
        Returns the output of the indicator calculation as a Pandas Series.

        Returns
        -------
        pd.Series
            The output of the indicator calculation as a Pandas Series.
        """
        return pd.Series(self._output_data)

    @staticmethod
    def _handle_common_errors(  # noqa
        numpy_data: np.ndarray = None, window: int = None
    ):
        """
        Helper function to handle common errors.

        Parameters
        ----------
        numpy_data : np.ndarray, optional
        window : int, optional

        Raises
        ------
        ValueError
            If the input data contains no values, NaN values, infinite values, or other non-numeric
            values.
            If the window is not a positive integer or if it is longer than the length of the input
            data.
        TypeError
            If the window is not an integer.
        """
        if numpy_data is not None:
            if len(numpy_data) < 1:
                raise ValueError("Input Data contains no values.")
            if np.isnan(numpy_data).any():
                raise ValueError("Input data contains NaN values.")
            if np.isinf(numpy_data).any():
                raise ValueError("Input data contains infinite values.")
            if not np.issubdtype(numpy_data.dtype, np.number) or np.issubdtype(
                numpy_data.dtype, np.timedelta64
            ):
                raise ValueError("Input data contains non-numeric values.")

        if window is not None:
            if not isinstance(window, int):
                raise TypeError("Window must be an integer.")
            if window <= 0:
                raise ValueError("Window must be a positive integer.")

        if numpy_data is not None and window is not None and window > len(numpy_data):
            raise ValueError(
                """Window cannot be greater than the length of the
                    input data."""
            )


class BaseMovingAverageClass(BaseIndicatorClass, ABC):
    """
    An abstract base class which should be used for all moving averages.

    Attributes
    ----------
    _output_data : np.ndarray
        The output of the indicator calculation.
    _window : int
        The window of the moving average.

    Methods
    -------
    return_window()
        Returns the window of the moving average.
    """

    def __init__(self):
        """
        Initializes the class.
        """
        super().__init__()
        self._window = None

    def return_window(self):
        """
        Returns the window of the moving average.

        Returns
        -------
        int
            The window of the moving average.
        """
        return self._window
