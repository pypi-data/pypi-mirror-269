from ..brokers import AlpacaTrading
import logging
from ..models import TradingConfig
log_format = '%(asctime)s| [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
log = logging.getLogger(__name__)



def get_alpaca_strategy_profit(trading_config :TradingConfig, limit :int = 20):

    alpaca_trading = AlpacaTrading(
        trading_config.broker.api_key, 
        trading_config.broker.api_secret
        )

    orders = alpaca_trading.get_orders_list_filter(
        symbol=trading_config.trading.symbol,
        limit=limit
    )
    
    found = None
    profit_list = []
    profit_percentage = []
    order_sell = None
    for order in orders:
        
        if order.get('side') == 'sell' and not found:
            found = True
            order_sell = order
        elif order.get('side') == 'buy' and order.get('status') != 'canceled' and order_sell:

            qty_sell = float(order_sell.get('filled_qty'))
            filled_avg_price_sell =  float(order_sell.get('filled_avg_price'))

            found = None
            filled_qty_buy = float(order.get('filled_qty'))
            filled_avg_price_buy = float(order.get('filled_avg_price'))

            national = float(order.get('notional'))

            # Calcula el costo total de compra y el ingreso total de venta
            national_buy = national
            national_sell = filled_avg_price_sell * qty_sell

            # Calcula el profit absoluto
            profit = national_sell - national_buy
            profit_list.append(profit)

            profit_p = 100 * (national_sell - national_buy)/national_buy
            profit_percentage.append(profit_p)

            log.info(f"PROFIT {trading_config.trading.symbol} {profit} {profit_p}%")

            order_sell = None


    percentage = sum(profit_percentage)

    return percentage, profit_percentage