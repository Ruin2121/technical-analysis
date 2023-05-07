# This test code was partially written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

# TODO Need to create tests for the following functions:
# Analysis.moving_average_crossover()

import hypothesis
import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra._array_helpers import array_shapes
from hypothesis.extra.numpy import arrays, scalar_dtypes
from pandas import Series
import pandas as pd

from technical_analysis import Analysis

MAX_SETTINGS = 100


@st.composite
def validated_inputs_simple_moving_average(draw):
    df = pd.DataFrame()
    df["close"] = draw(
        st.one_of(
            st.builds(list),
            arrays(
                dtype=scalar_dtypes(), shape=array_shapes(max_dims=1, max_side=1000)
            ),
            st.builds(Series),
        )
        .filter(lambda x: len(x) > 1)
        .filter(lambda x: np.issubdtype(x.dtype, np.number))
        .filter(lambda x: not np.issubdtype(x.dtype, np.timedelta64))
        .filter(lambda x: not np.isinf(x).any())
        .filter(lambda x: not np.isnan(x).any())
    )
    window = draw(st.integers(min_value=1, max_value=len(df["close"])))
    return df, window


@settings(
    max_examples=MAX_SETTINGS,
    suppress_health_check=[
        hypothesis.HealthCheck.too_slow,
    ],
)
@given(validated_inputs_simple_moving_average())
def test_simple_moving_average(df_window) -> None:
    df, window = df_window
    tests = Analysis(df)
    run1 = tests.simple_moving_average(window=window)
    run2 = tests.simple_moving_average(window=window)
    assert run1.all() == run2.all()
