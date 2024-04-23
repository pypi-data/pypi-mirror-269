from ..brokers import get_alpaca_strategy_profit
from ..models import StatusBot, TradingConfig
from ..brokers import AlpacaTrading
from ..utils import read_mlflow_model

def  get_status_bot(trading_config :TradingConfig, mlflow_connection=None):

    alpaca_trading = AlpacaTrading(trading_config.broker.api_key, trading_config.broker.api_secret)

    percentage, profit_percentage = get_alpaca_strategy_profit(trading_config)
    
    status_bot = StatusBot(
        orders_percentage=percentage,
        profit_history={
            "percentage": percentage,
            "profit_percentage": profit_percentage
        }, 
        replicate_latest_strategy_buy_action=True
    )

    if len(profit_percentage) == 0:
        status_bot.history_orders = False
    else:
        status_bot.history_orders = True

    if percentage > 0.0:
        status_bot.is_winner = True

    ## Get Registred Model data -----------------
    
    try:
        model_parameters = read_mlflow_model(
            symbol=trading_config.trading.symbol, 
            tag=trading_config.model.tag,
            stage=trading_config.model.stage, 
            mlflow_connection=mlflow_connection
        )

        if model_parameters: 
            status_bot.is_registred_model = True
            status_bot.model_parameters = model_parameters
    except Exception as e:
        print("Model not eixt")
        status_bot.is_registred_model = False
        status_bot.model_parameters = {}


    # Verify if exist the position
        
    
    positions = alpaca_trading.get_open_positions()
    for position in positions:
        if position.get('symbol') == trading_config.trading.symbol.replace('/', ''):
            status_bot.is_open_positions = True 

            market_value = float(position['market_value'])
            cost_basis = float(position['cost_basis'])
            profit_position = market_value - cost_basis
            status_bot.profit_position = profit_position


            profit_percentage_positions = (profit_position / cost_basis) * 100
            status_bot.profit_percentage_positions = profit_percentage_positions
            
            if profit_percentage_positions > 0.0:
                status_bot.is_winner = True

            break


    orders = alpaca_trading.get_orders_list_filter(status='accepted', symbol=trading_config.trading.symbol)
    for order in orders:
        if order.get('symbol') == trading_config.trading.symbol.replace('/', ''):
            status_bot.is_open_order = True

    return status_bot
