
from pydantic import BaseModel


class Broker(BaseModel):
    id :str = ""
    provider :str = "alpaca"
    api_key :str = "******"
    api_secret :str = "***********"

class Owner(BaseModel):
    username :str = "username"
    surname :str = "surname"
    id :str = "00000001"

class Symbol(BaseModel):
    symbol: str = "TNA"
    is_crypto: bool = False
    description :str = "Symbol description"

class Model(BaseModel):
    tag: str = "algo"
    stage: str = "Staging"
    version: str = "0.0.1"
    provider :str = "mlflow"

class Trading(Symbol):
    id :str = "123123123123"
    notional: float = 200.0
    side :str = 'buy'
    type :str = 'market'
    time_in_force :str = 'market'
    stop_loss :float = 100.0
    client_order_id :str = 'Client Id'
    is_paper :bool = True

class TradingConfig(BaseModel):
    active :bool = True 
    replicate_latest_open_long_signal :bool = False 
    calculate_best_stop_loss :bool = True
    broker_id :str
    trading :Trading 
    model :Model = Model()

class StatusBot(BaseModel):

    # Controller Variables -----
    is_open_order :bool = False
    is_registred_model :bool = False 
    is_open_positions :bool = False
    is_winner :bool = False

    # DataSaved 
    model_parameters :dict = {}

    # Controller Value
    profit_factor_limit :float = 1.2

    new_strategy :bool = False
    history_orders: bool = False

    profit_history :dict = {}
    best_experiment :float = 0.0
    orders_percentage :float = 0.0

    replicate_latest_strategy_buy_action :bool = False
    profit_percentage_positions :float = 0.0
    profit_position :float = 0.0

    experiment_profit_factor :float = 0.0
    experiment_profit_factor_sl :float = 0.0


    experiment_best_return :float = 0.0
    experiment_best_return_stop_loss :float = 0.0
    experiment_best_stop_loss :float = 0.0
    experiment_return :float = 0.0

