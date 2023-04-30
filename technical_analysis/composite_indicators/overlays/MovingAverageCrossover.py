from technical_analysis.baseclasses import BaseMovingAverageClass, BaseIndicatorClass
from typing import Union
import pandas as pd
import numpy as np


class MovingAverageCrossover(BaseIndicatorClass):
    """
    This class implements the Moving Average Crossover (MACross) indicator.

    Parameters
    ----------
    data : Union[list, np.ndarray, pd.Series]
        The input data.
    **kwargs : dict
        See Examples Section.

    Inherited Methods
    -----------------
    to_list()
        returns the output of the indicator calculation as a list.
    to_np_array()
        returns the output of the indicator calculation as a NumPy array.
    to_pd_series()
        returns the output of the indicator calculation as a Pandas Series.

    Examples
    --------
    The **kwargs argument should be a dictionary conforming to the example below. Dict keys "ma1"
    and "ma2" are required. They should each contain an "ma_class" key that specifies the moving
    average class to be used along with keys for each parameter of the moving average class.

    >>> func_args = {
    >>>     "ma1": {
    >>>         "ma_class": SimpleMovingAverage,
    >>>         "window": 50,
    >>>     },
    >>>     "ma2": {
    >>>         "ma_class": SimpleMovingAverage,
    >>>         "window": 200,
    >>>     }
    >>> }
    >>> func = MovingAverageCrossover(data, **func_args)
    """

    def __init__(self, data: Union[list, np.ndarray, pd.Series], **kwargs):
        """
        Initializes the Moving Average Crossover (MACross) indicator.
        """
        super().__init__()
        self.__ma1_args = kwargs.get("ma1", {})
        self.__ma2_args = kwargs.get("ma2", {})
        self.__numpy_data = self._to_numpy(data)
        self.__ma1 = self.__ma1_args.pop("ma_class", None)
        self.__ma2 = self.__ma2_args.pop("ma_class", None)
        self._handle_common_errors(self.__numpy_data)
        self._handle_additional_errors()
        self._calculation()

    def _calculation(self):
        """
        Calculates the moving average crossover.
        """
        # Instantiate the first moving average
        ma1 = self.__ma1(self.__numpy_data, **self.__ma1_args)

        # Instantiate the second moving average
        ma2 = self.__ma2(self.__numpy_data, **self.__ma2_args)

        # Calculate the moving averages
        ma1_values = ma1.to_np_array()
        ma2_values = ma2.to_np_array()

        # Extract window size of moving averages
        ma1_window = ma1.return_window()
        if ma1_window is None:
            ma1_window = 0
        ma2_window = ma2.return_window()
        if ma2_window is None:
            ma2_window = 0

        # Initialize an array to store the results
        results = np.zeros_like(self.__numpy_data)

        # Detects where crossovers occur and sets those values in the results array
        # When ma1 crosses above ma2
        results[1:][
            np.logical_and(
                ma1_values[:-1] < ma2_values[:-1], ma1_values[1:] > ma2_values[1:]
            )
        ] = 1

        # When ma1 crosses below ma2
        results[1:][
            np.logical_and(
                ma1_values[:-1] > ma2_values[:-1], ma1_values[1:] < ma2_values[1:]
            )
        ] = 2

        results[: max(ma1_window, ma2_window)] = 0

        self._output_data = results

    def _handle_additional_errors(self):
        """
        Handles any additional errors that may occur during the calculation.

        Raises
        ------
        TypeError
            If ma1 or ma2 is not a subclass of BaseMovingAverageClass.
        """
        if not issubclass(self.__ma1, BaseMovingAverageClass):
            raise TypeError("ma1 must be a subclass of BaseMovingAverageClass")
        if not issubclass(self.__ma2, BaseMovingAverageClass):
            raise TypeError("ma2 must be a subclass of BaseMovingAverageClass")
