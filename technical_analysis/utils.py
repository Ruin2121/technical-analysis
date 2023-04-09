from typing import Union

import numpy as np
import pandas as pd


def to_numpy(data: Union[list, np.ndarray, pd.Series]) -> np.ndarray:
    """
    Converts a list, pandas series, or numpy array to a numpy array.

    Parameters:
    -----------
    data: Union[list, np.ndarray, pd.Series]
        A list, pandas series, or numpy array.

    Returns:
    --------
    np.ndarray
        A numpy array of the input data.

    Raises:
    -------
    ValueError:
        Raised if input data is an invalid type.
    """
    if isinstance(data, np.ndarray):
        return data
    elif isinstance(data, pd.Series):
        return data.to_numpy()
    elif isinstance(data, list):
        return np.array(data)
    else:
        raise ValueError('Invalid data type: {}'.format(type(data)))


def pre_return_conversion(data: np.ndarray, return_type: str) -> Union[object, np.ndarray, pd.Series]:
    """
    Converts a numpy array to the designated return type.

    Parameters:
    -----------
    data: np.ndarray
        A numpy array.
    return_type: str
        The return type requested by the user.

    Returns:
    --------
    Union[object, np.ndarray, pd.Series]
        A python list, pandas series, or numpy array containing the given values.

    Raises:
    -------
    ValueError:
        Raised if return_type is invalid.
    """
    if return_type == "list":
        return data.tolist()
    elif return_type == "numpy":
        return data
    elif return_type == "pandas":
        return pd.Series(data)
    else:
        raise ValueError('Invalid return_type: {}'.format(return_type))
