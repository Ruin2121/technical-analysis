import pandas as pd
import numpy as np
from technical_analysis.custom_exceptions import InvalidInstanceError


class Analysis:
    """
    Primary class for all analysis methods. Though intended for stock analysis, any numerical data
    works.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe. Column names will be automatically converted to lower case.

    Attributes
    ----------
    input_df : pd.DataFrame
        Contains the input data.
    analysis_df : pd.DataFrame
        Contains all calculated data.

    Methods
    -------
    simple_moving_average(column_name: str, window: int) -> pd.Series
        Implementation of simple moving average.
    moving_average_crossover(**kwargs) -> pd.Series
        Implementation of moving average crossover.

    Raises
    ------
    TypeError
        If df is not a Pandas DataFrame.
    """

    def __init__(self, df: pd.DataFrame):
        # Initialize Dataframes
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame. " f"Got {type(df)} instead."
            )
        self.input_df = df
        self.input_df.columns = self.input_df.columns.str.lower()
        self._data_checks()
        self.analysis_df = pd.DataFrame()

    @staticmethod
    def _to_numpy(data: pd.Series) -> np.ndarray:
        """
        Converts a pandas Series to a numpy array.

        Parameters
        ----------
        data : pd.Series

        Returns
        -------
        np.ndarray
        """
        return data.to_numpy()

    @staticmethod
    def _to_pandas_series(data: np.ndarray) -> pd.Series:
        """
        Converts a numpy array to a pandas Series.

        Parameters
        ----------
        data : np.ndarray

        Returns
        -------
        pd.Series
        """
        return pd.Series(data)

    def _data_checks(self):
        """
        Checks that the input data is valid.
        """
        for column in self.input_df.columns:
            data = self.input_df[column]
            self._input_checks(data)

    def _input_checks(self, data_raw: pd.Series):
        """
        Checks that the input data is valid.
        """
        data = self._to_numpy(data_raw)
        if data is not None:
            if len(data) < 1:
                raise ValueError(f"Input Data ({data_raw.name}) contains no values.")
            if np.isnan(data).any():
                raise ValueError(f"Input Data ({data_raw.name}) contains NaN values.")
            if np.isinf(data).any():
                raise ValueError(
                    f"Input Data ({data_raw.name}) contains infinite values."
                )
            if not np.issubdtype(data.dtype, np.number) or np.issubdtype(
                data.dtype, np.timedelta64
            ):
                raise ValueError(
                    f"Input Data ({data_raw.name}) contains non-numeric values."
                )

    def simple_moving_average(self, window: int, column: str = "close") -> pd.Series:
        """
        Implementation of Simple Moving Average (SMA) calculation.

        Parameters
        ----------
        window: int
            An integer representing the size of the window used for the moving average.
        column: str
            The name of the column to calculate the moving average of.

        Returns
        -------
        pd.Series

        Raises
        ------
        TypeError
            If window is not an integer.
        ValueError
            If window is less than 1.
            If window is greater than the length of the input data.
        """
        column_name = f"{column}_sma_{window}"
        if column_name in self.analysis_df.columns:
            return self.analysis_df[column_name]

        numpy_data = self._to_numpy(self.input_df[column])

        if not isinstance(window, int):
            raise TypeError("Window must be an integer.")
        if window <= 0:
            raise ValueError("Window must be a positive integer.")
        if window > len(numpy_data):
            raise ValueError(
                "Window cannot be greater than the length of the input data."
            )

        weights = np.repeat(1.0, window) / window
        sma = np.convolve(numpy_data, weights, "full")[: len(numpy_data)]
        self.analysis_df[column_name] = self._to_pandas_series(sma)

        return self.analysis_df[column_name]

    def moving_average_crossover(self, **kwargs) -> pd.Series:
        """
        Implementation of Moving Average Crossover (MACross) calculation.

        Encodes a cross upwards as a '1' and a cross downwards as a '2', else '0'.

        Meaning of '1' and '2' is dependent on user input.

        Parameters
        ----------
        **kwargs: dict
            See Example below.

        Returns
        -------
        pd.Series

        Raises
        ------
        InvalidInstanceError
            If both functions do not belong to the same instance as the calling class instance.

        Examples
        --------
        The **kwargs argument should be a dictionary conforming to the example below. Dict keys
        "ma1" and "ma2" are required. They should each contain an "ma_func" key that specifies the
        moving average function to be used along with keys for each parameter of the moving average
        function. Note that the "ma_func" key must explicitly refer to the class instance, which in
        this example is "example".

        >>> example = Analysis(data)
        >>> func_args = {
        >>>     "ma1": {
        >>>         "ma_func": example.simple_moving_average,
        >>>         "window": 50,
        >>>         "column": "close",
        >>>     },
        >>>     "ma2": {
        >>>         "ma_func": example.simple_moving_average,
        >>>         "window": 200,
        >>>         "column": "close",
        >>>     }
        >>> }
        >>> result = example.moving_average_crossover(**func_args)
        """
        ma1_args = kwargs.get("ma1", {})
        ma2_args = kwargs.get("ma2", {})
        ma1 = ma1_args.pop("ma_func", None)
        ma2 = ma2_args.pop("ma_func", None)
        if self is not ma1.__self__ or self is not ma2.__self__:
            # Might want to improve this error message.
            raise InvalidInstanceError(
                "Both functions must belong to the same instance as the calling class instance."
            )

        # Need to decide on a good way to store and pull the data from analysis_df.
        # column_name = f"{column}_sma_{window}"
        # if column_name in self.analysis_df.columns:
        #     return self.analysis_df[column_name]

        # Calculate or retrieve the moving averages
        ma1_values = self._to_numpy(ma1(**ma1_args))
        ma2_values = self._to_numpy(ma2(**ma2_args))

        # Extract window size of moving averages
        ma1_window = ma1_args["window"] if "window" in ma1_args else 0
        ma2_window = ma2_args["window"] if "window" in ma2_args else 0

        # Initialize an array to store the results
        results = np.zeros_like(ma1_values)

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

        return self._to_pandas_series(results)
