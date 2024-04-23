from dotenv import dotenv_values
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
import pytz

config = dotenv_values(".env")

api_key = config.get('ALPACA_API_KEY')
api_secret = config.get('ALPACA_API_SECRET')
alpaca_api_url = "https://paper-api.alpaca.markets"

api = REST(api_key, api_secret, alpaca_api_url)

def _get_bars(start_time = None, symbol = "TNA", end_time = None, is_crypto = False, api = None):
    if not is_crypto:
        # end_time_adjusted = end_time - timedelta(minutes=15)
        end_time_adjusted = (end_time - timedelta(minutes=15)).replace(microsecond=0).isoformat()
        return api.get_bars(symbol, TimeFrame.Minute, start_time.isoformat(), end_time_adjusted, adjustment='raw').df
    else:
        # Fetch cryptocurrency data using Alpaca's get_crypto_bars method
        return api.get_crypto_bars(symbol, TimeFrame.Minute, start_time.isoformat(), end_time.isoformat()).df

def _adjust_time_window(start_time, symbol, end_time, is_crypto, api):
    # Check further in the past if the recent data is not accessible
    adjustment_minutes = [1000, 10000]  # Extending the window in steps
    for minutes in adjustment_minutes:
        start_time_adjusted = end_time - timedelta(minutes=minutes)
        bars = _get_bars(start_time_adjusted, symbol, end_time, is_crypto, api)
        if len(bars) > 0:
            return bars
    return None  # Return None if no bars were found

def get_assert_latest_price(symbol, date=None, is_crypto=True, api=None):

    timezone = pytz.timezone("America/New_York")
    
    if date is None:
        end_time = datetime.now(tz=timezone)
    else:
        end_time = timezone.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

    start_time = end_time - timedelta(minutes=300)
    bars = _get_bars(start_time, symbol, end_time, is_crypto, api=api)

    if len(bars) == 0: 
        bars = _adjust_time_window(start_time, symbol, end_time, is_crypto, api)

    if bars is not None and len(bars) > 0:
        price = bars.iloc[-1]
        return price
    return None  # Return None if no valid price data was found
