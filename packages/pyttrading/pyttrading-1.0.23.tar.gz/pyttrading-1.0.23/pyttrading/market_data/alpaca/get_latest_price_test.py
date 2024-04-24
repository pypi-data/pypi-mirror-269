
from dotenv import dotenv_values
from alpaca_trade_api.rest import REST
from .get_latest_price import get_assert_latest_price

config = dotenv_values(".env")

api_key = config.get('ALPACA_API_KEY')
api_secret = config.get('ALPACA_API_SECRET')
alpaca_api_url = "https://paper-api.alpaca.markets"

api = REST(api_key, api_secret, alpaca_api_url)

def test_get_assert_latest_price_stock():
    symbol = 'TNA'
    date = '2023-10-03 10:00:00'
    price = get_assert_latest_price(symbol, date, is_crypto=False, api=api)
    assert price is not None, "Should retrieve a valid price for stock with a specific date"

def test_get_assert_latest_price_crypto():
    symbol = 'AVAX/USD'
    date = '2023-10-03 10:00:00'
    price = get_assert_latest_price(symbol, date, is_crypto=True, api=api)
    assert price is not None, "Should retrieve a valid price for cryptocurrency with a specific date"

def test_get_price_without_date_stock():
    symbol = 'META'
    price = get_assert_latest_price(symbol, is_crypto=False, api=api)
    assert price is not None, "Should retrieve a valid price for stock without specifying date"

def test_get_price_without_date_crypto():
    symbol = 'AVAX/USD'
    price = get_assert_latest_price(symbol, is_crypto=True, api=api)
    assert price is not None, "Should retrieve a valid price for cryptocurrency without specifying date"
