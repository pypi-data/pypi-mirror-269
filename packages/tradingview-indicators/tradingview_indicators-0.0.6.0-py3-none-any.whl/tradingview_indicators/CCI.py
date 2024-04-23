from typing import Literal

import pandas as pd
import numpy as np
from .errors_exceptions import InvalidArgumentError
from .moving_average import ema


class CCI:
    """
    A class for calculating Commodity Channel Index (CCI)
    of time series data.

    Attributes:
    -----------
    source_arr : numpy.ndarray
        The input time series data as a NumPy array.
    source : pd.Series
        The input time series data as a DataFrame.
    length : int
        The number of periods to include in the CCI calculation.

    Methods:
    --------
    calculate_precice_CCI(smooth_column: str = "sma", constant: float = 0.015) -> CCI:
        Calculate CCI using a precise method.

    calculate_CCI(constant: float = 0.015, method: str = "sma") -> pd.DataFrame:
        Calculate CCI using the specified method.
    """

    def __init__(self, source: pd.Series, length: int = 20):
        """
        Initialize the CCI object.

        Parameters:
        -----------
        source : pd.Series
            The input time series data.
        length : int, optional
            The number of periods to include in the CCI calculation, by default 20.
        """
        self.source_arr = np.array(source)
        self.source = source
        self.length = length

    def calculate_precice_CCI(
        self,
        smooth_column: str = "sma",
        constant: float = 0.015,
    ) -> pd.Series:
        """
        Calculate CCI using a precise method.
        this version have more similar results from excel
        than the standard version and TA-lib.

        Parameters:
        -----------
        smooth_column : str, optional
            The column to use for smoothing, by default "sma".
        constant : float, optional
            The constant factor for CCI calculation, by default 0.015.

        Returns:
        --------
        CCI
            The CCI object.
        """

        df = pd.DataFrame()
        df["TP"] = self.source_arr
        df["sma"] = df["TP"].rolling(self.length).mean()

        df["mad"] = (
            df["TP"]
            .rolling(self.length)
            .apply(lambda x: (pd.Series(x) - pd.Series(x).mean()).abs().mean())
        )

        df["CCI"] = (
            (df["TP"] - df[smooth_column])
            / (constant * df["mad"])
        )

        return df["CCI"].dropna(axis=0, inplace=True)

    def __set_sma(self):
        """
        Set the Simple Moving Average (SMA) for the CCI calculation.

        Returns:
        --------
        CCI
            The CCI object.
        """
        self.window = np.ones(self.length) / self.length
        self.ma = np.convolve(self.source_arr, self.window, mode="valid")

        return self

    def __set_ema(self):
        """
        Set the Exponential Moving Average (EMA) for the CCI calculation.

        Returns:
        --------
        CCI
            The CCI object.
        """
        self.ma = ema(self.source, self.length).to_numpy()

        return self

    def calculate_CCI(self, constant: float = 0.015, method:Literal["ema", "sma"] = "sma") -> pd.DataFrame:
        """
        Calculate CCI using the specified method.

        Parameters:
        -----------
        constant : float, optional
            The constant factor for CCI calculation.
            (default: 0.015)
        method : str, optional
            The method to use for the moving average calculation.
            (default: "sma")

        Returns:
        --------
        pd.DataFrame
            The calculated CCI data as a DataFrame.

        Raises:
        -------
        InvalidArgumentError
            If the method is not 'sma' or 'ema'.
        """
        if method == "sma":
            self.__set_sma()
        elif method == "ema":
            self.__set_ema()
        else:
            raise InvalidArgumentError("Method must be 'sma' or 'ema'.")

        self.window = np.lib.stride_tricks.sliding_window_view(self.source_arr, self.length)
        self.mean_window = np.mean(self.window, axis=1)
        self.abs_diff = np.abs(self.window - self.mean_window[:, np.newaxis])

        self.mad = np.mean(self.abs_diff, axis=1)

        df = pd.DataFrame()
        df["source"] = self.source[self.length - 1 :]
        df["mad"] = self.mad
        df["ma"] = self.ma
        df["CCI"] = (
            (df["source"] - df["ma"])
            / (constant * df["mad"])
        )

        return df
