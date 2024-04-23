

from . import AlpacaTrading
from ..models.trading import Trading

# from alpaca.trading.client import TradingClient

# import alpaca.trading as alpaca_trading



def alpaca_open_long(trading :Trading, api_key, api_secret, tag :str ="algo"):

    strategy_name = f"{trading.symbol}_{tag}"

    if  trading.time_in_force == "":
        if trading.is_crypto: 
            trading.time_in_force = 'gtc'
        else: 
            trading.time_in_force = 'day'

    alpaca_trading = AlpacaTrading(api_key, api_secret)

    client_order_id = alpaca_trading.open_position(
        symbol=trading.symbol, 
        quantity=trading.notional,
        stop_loss=trading.stop_loss, 
        strategy_name=strategy_name, 
        return_client_order_id=True, 
        time_in_force=trading.time_in_force
    )
    
    return client_order_id


def alpaca_close_long(symbol, api_key, api_secret, tag="test"):


    alpaca_trading = AlpacaTrading(api_key, api_secret)

    strategy_name = f"{symbol}_{tag}"

    client_order_id = alpaca_trading.close_position(
        symbol=symbol, 
        strategy_name=strategy_name
    )

    return client_order_id