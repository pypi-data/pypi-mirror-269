import json
from .logs import log
from .get_datetime_now_trade import get_datetime_now_trade
from ..market_data import get_market_data_from_playground
from ..strategies import ModelSelector
from . import init_mlflow_connection

import uuid
id_test = str(uuid.uuid4()).replace('-','')[-10:-1]

import mlflow


def eval_strategy_latest(parameters=None, get_action_latest :bool = False):

    symbol = parameters.get('symbol')
    interval = parameters.get('interval')
    is_crypto = parameters.get('is_crypto')
    start_date, end_date, now_ny = get_datetime_now_trade()
    optimized_params = json.loads(parameters.get('optimized_params'))
    parms = optimized_params.get('params')

    data = get_market_data_from_playground(
        symbols=symbol, 
        interval=interval, 
        start_date=str(start_date),
        end_date=str(end_date),
        is_crypto=is_crypto
    )

    if len(data) == 0:
        raise ImportError("Not found data")
    

    model = ModelSelector(
                    model_name=optimized_params.get("strategy"),
                    path_model="tmp",
                    type_model="basic",
                    configuration=parameters, 
                    df=data,
                    symbol=symbol,
                    interval=interval,
                    mlflow=mlflow
                )
    
    strategy_model = model.basic_models()
    strategy = strategy_model()

    df_action = strategy.eval(df=data, params=parms)

    
    if not get_action_latest:
        actions = df_action['actions'].iloc[-1]
    else:
        actions = [accion for accion in df_action['actions'].iloc[-100:-1] if accion != 0]
        actions = actions[-1]


    action = None
    if actions == 1:
        action = 'open-long'
        message = f"🟢 BUY: {action}"
    elif actions == 2:
        action = 'close-long'
        message = f"🟠 SELL: {action}"
    elif actions == 0:
        action = 'keep'
        message = f"🔵 KEEP: {action}"

    close_price = round(df_action['close'].iloc[-1],2)
    log.info(f"{message} [{interval}] {parameters} START: {start_date} END:{end_date}  CLOSE: {close_price}")

    return action


def read_mlflow_model(symbol, tag, mlflow_connection, stage):
    model_name = f"{symbol}_{tag}"

    log.info(f"Starting Eval model: {model_name}")

    results = mlflow_connection.search_registered_models(filter_string=f"name='{model_name}'")
    model_selected = None
    if len(results) == 0:
        raise AssertionError(f"Not found model, {symbol}/{stage}/{tag}")
    
    for model in results[0].latest_versions:
        current_stage = model.current_stage
        if current_stage == stage:
            model_selected = model 
            break

    tags_selected = model_selected.tags
    if model_selected:
        parameters = json.loads(tags_selected.get('parameters'))
        return parameters
    
    return False


def eval_mlflow_model_strategy(symbol :str, stage :str, tag: str, mlflow_connection=None, get_action_latest :bool = False):

    model_name = f"{symbol}_{tag}"

    log.info(f"Starting Eval model: {model_name}")

    results = mlflow_connection.search_registered_models(filter_string=f"name='{model_name}'")
    model_selected = None
    if len(results) == 0:
        raise AssertionError(f"Not found model, {symbol}/{stage}/{tag}")
    
    for model in results[0].latest_versions:
        current_stage = model.current_stage
        if current_stage == stage:
            model_selected = model 
            break

    tags_selected = model_selected.tags
    if model_selected:
        parameters = json.loads(tags_selected.get('parameters'))
        action = eval_strategy_latest(parameters, get_action_latest)

    return action


def get_model_tags(symbol :str, stage :str, tag: str, mlflow_connection=None):

    model_name = f"{symbol}_{tag}"

    log.info(f"Starting Eval model: {model_name}")

    results = mlflow_connection.search_registered_models(filter_string=f"name='{model_name}'")
    model_selected = None
    if len(results) == 0:
        raise AssertionError(f"Not found model, {symbol}/{stage}/{tag}")
    
    for model in results[0].latest_versions:
        current_stage = model.current_stage
        if current_stage == stage:
            model_selected = model 
            break

    tags_selected = model_selected.tags

    return tags_selected