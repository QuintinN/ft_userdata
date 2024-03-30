import talib.abstract as ta
from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy

class MACDStrategy(IStrategy):
    """
    This strategy utilizes the MACD indicator to identify potential buy and sell signals.
    Buy signal: MACD line crosses above the MACD signal line.
    Sell signal: MACD line crosses below the MACD signal line.
    """
    
    INTERFACE_VERSION = 3
    can_short: bool = False

    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04
    }

    stoploss = -0.10
    trailing_stop = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macd'] > dataframe['macdsignal']) &  # MACD line crosses above signal line
                (dataframe['volume'] > 0)  # Ensure there is volume
            ),
            'enter_long'] = 1

        # Optional: if the strategy can go short
        # dataframe.loc[
        #     (
        #         (dataframe['macd'] < dataframe['macdsignal']) &  # MACD line crosses below signal line
        #         (dataframe['volume'] > 0)  # Ensure there is volume
        #     ),
        #     'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macd'] < dataframe['macdsignal']) &  # MACD line crosses below signal line
                (dataframe['volume'] > 0)  # Ensure there is volume
            ),
            'exit_long'] = 1

        # Optional: if the strategy can go short
        # dataframe.loc[
        #     (
        #         (dataframe['macd'] > dataframe['macdsignal']) &  # MACD line crosses above signal line
        #         (dataframe['volume'] > 0)  # Ensure there is volume
        #     ),
        #     'exit_short'] = 1

        return dataframe
