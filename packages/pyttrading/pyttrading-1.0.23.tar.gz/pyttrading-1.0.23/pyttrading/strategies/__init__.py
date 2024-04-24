from .ema import Strategy as ema
from .rsi import Strategy as rsi
from .macd import Strategy as macd
from .sma import Strategy as sma
from .dummy import Strategy as dummy
from .selector import ModelSelector

strategies_list = ['ema', 'rsi', 'macd', 'sma', 'dummy']

intervals_list = [
        '30m',
        '1h',
        '2h',
        '4h',
        '6h',
        '8h',
    ]


strategies_dict = [
    {
        "name": "ema", 
        "long_name": "Exponential Moving Averages",
        "description": "An algorithmic trading strategy based on the Exponential Moving Averages (EMAs)."
    },
    {
        "name": "rsi",
        "long_name": "Relative Strength Index",
        "description": "The strategy we are implementing is based on the Relative Strength Index (RSI), a popular momentum oscillator."
    },
    {
        "name": "macd",
        "long_name": "Moving Average Convergence Divergence",
        "description": "A trend-following momentum indicator that shows the relationship between two moving averages of a security’s price."
    },
    {
        "name": "sma",
        "long_name": "Simple Moving Averages",
        "description": "A simple, or arithmetic, moving average that is calculated by adding the recent prices of the asset and then dividing that figure by the number of time periods in the calculation average."
    },
    {
        "name": "dummy",
        "long_name": "Dummy Strategy",
        "description": "A placeholder strategy used for testing or demonstration purposes, without any real trading logic."
    }
]
