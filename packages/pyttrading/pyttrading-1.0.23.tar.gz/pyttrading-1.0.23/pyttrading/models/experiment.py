from pydantic import BaseModel
from .. import intervals_list, strategies_list
from datetime import datetime, timedelta
import pytz
from enum import Enum

import config 

# 'America/New_York'
def get_datetime_now_trade(timezone :str = 'America/New_York', delay_minutes = 15, days_ago = 100):
    
    ny_timezone = pytz.timezone(timezone)
    now_ny = datetime.now(ny_timezone)
    start_date_ny = now_ny - timedelta(days=days_ago)
    start_date_ny = start_date_ny.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date_ny = start_date_ny.strftime('%m/%d/%Y')
    end_date_ny = now_ny - timedelta(minutes=delay_minutes)
    end_date_ny = end_date_ny.strftime('%m/%d/%Y %H:%M')
 
    return start_date_ny, end_date_ny, now_ny

start_date, end_date, now_ny =  get_datetime_now_trade(delay_minutes=int(config.delay_minutes))

class StrategyParams(BaseModel):

    symbol: str = "TNA"
    interval: str = "1h"
    is_crypto: bool = False

class Trade(StrategyParams):
    start_date: str = str(start_date)
    end_date: str = str(end_date)
    time_amount: int = 10
    indicators: list = [
                        "boll_ub",
                        "boll_lb",
                        "close_10_sma",
                        "close_12_ema",
                        "close_16_ema"
                        ]


class Experiment(Trade):
    
    version :str = "2.0.0"
    tag :str='algo'
    experiment_name: str = f"{Trade().symbol}_{tag}_{version}"

class ExperimentMessage(Experiment):

    intervals: list = intervals_list
    strategies_list: list = strategies_list
    start_date: str = '9/1/2023'
    end_date: str = '1/5/2024'



class ExperimentOne(Experiment):
    tag: str = "rest"
    interval: str ='1h'
    start_date: str = '9/1/2023'
    end_date: str = '1/5/2024'
    strategy: str =  'rsi'



class StageEnum(str, Enum):
    Production = "Production"
    Staging = "Staging"
    Archived = "Archived"