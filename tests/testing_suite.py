# This test code was partially written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.
import hypothesis
import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra._array_helpers import array_shapes
from hypothesis.extra.numpy import arrays, scalar_dtypes
from pandas import Series
import technical_analysis

MAX_SETTINGS = 100


@st.composite
def validated_inputs(draw):
    data = draw(st.one_of(
        st.builds(list),
        arrays(dtype=scalar_dtypes(), shape=array_shapes(max_dims=1, max_side=1000)),
        st.builds(Series),
        ).filter(lambda x: len(x) > 1).filter(lambda x: np.issubdtype(x.dtype, np.number)).filter(
        lambda x: not np.isinf(x).any()).filter(lambda x: not np.isnan(x).any()).filter(lambda x: not np.issubdtype(x.dtype, np.timedelta64)))
    window = draw(st.integers(min_value=1, max_value=len(data)))
    return data, window


@settings(max_examples=MAX_SETTINGS, suppress_health_check=[hypothesis.HealthCheck.too_slow, ])
@given(validated_inputs())
def test_fuzz_simple_moving_average(data_window) -> None:
    data, window = data_window
    technical_analysis.SimpleMovingAverage(data=data, window=window)
