from technical_analysis.basic_indicators.overlays.SimpleMovingAverage import SimpleMovingAverage
from technical_analysis.composite_indicators.overlays.MovingAverageCrossover import MovingAverageCrossover
from technical_analysis.baseclasses import BaseIndicatorClass


class SMA50CrossSMA200(BaseIndicatorClass):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self._calculation()

    def _calculation(self):
        func_args = {
            'ma1': {
                'ma_class': SimpleMovingAverage,
                'window': 50
                },
            'ma2': {
                'ma_class': SimpleMovingAverage,
                'window': 200
                }
            }
        func = MovingAverageCrossover(data=self.data, **func_args)
        results = func.to_np_array()

        self._output_data = results
