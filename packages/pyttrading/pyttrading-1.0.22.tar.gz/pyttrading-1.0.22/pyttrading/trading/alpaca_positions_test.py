from dotenv import dotenv_values
from pymongo import MongoClient
from alpaca_trade_api.rest import REST
import config
from .alpaca_positions import create_position, close_position
config = dotenv_values(".env")

client = MongoClient(config.get('MONGO_URI'))
db = client[config.get('MONGO_DB_NAME')]
api_key = config.get('ALPACA_API_KEY')
api_secret = config.get('ALPACA_API_SECRET')
alpaca_api_url = "https://paper-api.alpaca.markets"
api = REST(api_key, api_secret, alpaca_api_url)

positions_collection = db['positions']
orders_collection = db['orders']


def test_open_long_position():
    
    position_id = create_position(
        symbol='AAPL', 
        quantity=1000, 
        position_type='long',
        date='2023-10-03 10:00:00',
        db=db,
        api=api,
    )

    position = positions_collection.find_one({'position_id': position_id})

    assert position is not None
    assert position['status'] == 'open'
    assert position['type'] == 'long'
    assert position['symbol'] == 'AAPL'


import pytest


@pytest.mark.asyncio
async def test_close_long_position():

    symbol='AAPL'

    symbol_data = await db['assets'].find_one({"_id": symbol.lower().replace('/','-')})

    position_id = create_position(
        symbol='AAPL', 
        quantity=1000, 
        position_type='long',
        date='2023-10-03 10:00:00',
        db=db, 
        api=api,
        symbol_data=symbol_data
    )

    close_position(
        position_id=position_id,
        date='2023-12-03 10:00:00',
        db=db,
        api=api
    )
    
    order = orders_collection.find_one({'position_id': position_id})

    assert order is not None
    assert order['status'] == 'closed'
    assert order['profit'] == 120.97822000000008  # 10 * (160 - 150)

def test_open_short_position():

    position_id = create_position(
        symbol='AAPL', 
        quantity=1000, 
        position_type='short',
        date='2023-10-03 10:00:00',
        db=db, 
        api=api
    )
    
    position = positions_collection.find_one({'position_id': position_id})
    assert position is not None
    assert position['status'] == 'open'
    assert position['type'] == 'short'
    assert position['symbol'] == 'AAPL'
    assert position['quantity'] == 6.666666666666667
    assert position['price_open'] == 173.174959

def test_close_short_position():

    position_id = create_position(
        symbol='AAPL', 
        quantity=1000, 
        position_type='short',
        date='2023-10-03 10:00:00',
        db=db, 
        api=api
    )
    close_position(
        position_id=position_id,
        date='2023-12-03 10:00:00',
        db=db, 
        api=api
    )
    order = orders_collection.find_one({'position_id': position_id})
    assert order is not None
    assert order['status'] == 'closed'
    assert order['profit'] == -120.97822000000008  # 10 * (150 - 140)

