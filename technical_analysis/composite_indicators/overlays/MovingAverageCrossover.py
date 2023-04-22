from technical_analysis.baseclasses import BaseMovingAverageClass, BaseIndicatorClass
from typing import Union
import pandas as pd
import numpy as np


class MovingAverageCrossover(BaseIndicatorClass):
    def __init__(self, data: Union[list, np.ndarray, pd.Series], **kwargs):
        super().__init__()
        self.ma1_args = kwargs.get('ma1', {})
        self.ma2_args = kwargs.get('ma2', {})
        self.__numpy_data = self._to_numpy(data)
        self.ma1 = self.ma1_args.pop('ma_class', None)
        self.ma2 = self.ma2_args.pop('ma_class', None)
        self._handle_common_errors(self.__numpy_data)
        self._handle_additional_errors()
        self._calculation()

    def _calculation(self):
        # Instantiate the first moving average
        ma1 = self.ma1(self.__numpy_data, **self.ma1_args)

        # Instantiate the second moving average
        ma2 = self.ma2(self.__numpy_data, **self.ma2_args)

        # Calculate the moving averages
        ma1_values = ma1.to_np_array()
        ma2_values = ma2.to_np_array()

        # Detects when ma1 crosses above ma2
        ma1_cross_up = np.where(ma1_values > ma2_values, 1, 0)

        # Detects when ma1 crosses below ma2
        ma1_cross_down = np.where(ma1_values < ma2_values, 2, 0)

        # Initialize an array to store the results
        results = np.zeros_like(self.__numpy_data)

        # Detects where crossovers occur and sets those values in the results array
        # When ma1 crosses above ma2
        results[1:][np.logical_and(ma1_values[:-1] < ma2_values[:-1], ma1_values[1:] > ma2_values[1:])] = 1

        # When ma1 crosses below ma2
        results[1:][np.logical_and(ma1_values[:-1] > ma2_values[:-1], ma1_values[1:] < ma2_values[1:])] = 2

        self._output_data = results

    def _handle_additional_errors(self):
        if not issubclass(self.ma1, BaseMovingAverageClass):
            raise TypeError("ma1 must be a subclass of BaseMovingAverageClass")
        if not issubclass(self.ma2, BaseMovingAverageClass):
            raise TypeError("ma2 must be a subclass of BaseMovingAverageClass")
