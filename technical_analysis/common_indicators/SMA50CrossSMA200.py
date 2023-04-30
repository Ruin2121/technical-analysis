from technical_analysis.basic_indicators.overlays.SimpleMovingAverage import (
    SimpleMovingAverage,
)
from technical_analysis.composite_indicators.overlays.MovingAverageCrossover import (
    MovingAverageCrossover,
)
from technical_analysis.baseclasses import BaseIndicatorClass
from typing import Union
import numpy as np
import pandas as pd


class SMA50CrossSMA200(BaseIndicatorClass):
    """
    Calculates the MACross using SMA50 and SMA200.

    Parameters
    ----------
    data : Union[list, np.ndarray, pd.Series]
        Input data.
    """

    def __init__(self, data: Union[list, np.ndarray, pd.Series]):
        """
        Initializes the class.
        """
        super().__init__()
        self.__data = data
        self._calculation()

    def _calculation(self):
        """
        Calculates the MACross using SMA50 and SMA200.
        """
        func_args = {
            "ma1": {"ma_class": SimpleMovingAverage, "window": 50},
            "ma2": {"ma_class": SimpleMovingAverage, "window": 200},
        }
        func = MovingAverageCrossover(data=self.__data, **func_args)
        results = func.to_np_array()

        self._output_data = results
