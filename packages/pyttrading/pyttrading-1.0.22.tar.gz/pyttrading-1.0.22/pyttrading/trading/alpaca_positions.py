import uuid
from bson import ObjectId
from .. import get_assert_latest_price

async def create_position(
        symbol=None,
        quantity=None,
        position_type='long', 
        date=None, 
        bot_id = None, 
        project_id=None, 
        db=None,
        api=None,
        symbol_data=None
    ):

    positions_collection = db['positions']

    if not symbol_data:
        raise AssertionError("Symbol not found")
    
    is_crypto = symbol_data.get('class', 'not') == 'crypto'

    # Get Date
    price = get_assert_latest_price(
        symbol=symbol, 
        date=date, 
        is_crypto=is_crypto,
        api=api
    )
    price = price.vwap


    if not date:
        raise ValueError("Date not found")

    position_data = {
        "type": position_type,
        "invested_usd": quantity,
        "price_open": price,
        "price_close": 0,
        "profit": 0,
        "symbol": symbol,
        "symbol_id": symbol_data.get('_id'),
        "quantity": quantity / price,
        "status": "open",
        "create_at": date,
        "update_at": date,
        "is_crypto": is_crypto
    }

    if bot_id:
        position_data["bot_id"] = ObjectId(bot_id)
    if project_id:
        position_data["project_id"] = ObjectId(project_id)

    response = await positions_collection.insert_one(position_data)

    return str(response.inserted_id)

async def close_position(position_id, date=None, db=None, api=None):

    try:

        positions_collection = db['positions']
        orders_collection = db['orders']

        position = await db['positions'].find_one({"_id": ObjectId(position_id), "status": "open"})
        
        price = get_assert_latest_price(
            symbol=position.get('symbol'), 
            date=date, 
            is_crypto=position.get('is_crypto'),
            api=api
        )
        price_close = price.vwap

        
        if not position:
            return "No open position found with the given ID."

        if position['type'] == 'long':  # Long
            profit = (price_close - position['price_open']) * position['quantity']
        elif position['type'] == 'short':  # Short
            profit = (position['price_open'] - price_close) * position['quantity']


        order_data = {
            "_id": ObjectId(position_id),
            "type": position['type'],
            "invested_usd": position['invested_usd'],
            "price_open": position['price_open'],
            "price_close": price_close,
            "profit": profit,
            "symbol": position['symbol'],
            "quantity": position['quantity'],
            "status": "closed",
            "create_at": position['create_at'],
            "update_at": date,
            # "is_winner": str(profit > 0.0) 
        }

        if position.get('bot_id'):
            order_data["bot_id"] = position.get('bot_id')
        if position.get('project_id'):
            order_data["project_id"] = position.get('project_id')

        orders_insert_result = await orders_collection.insert_one(order_data)
        if orders_insert_result.inserted_id:
            try:
                response =  positions_collection.delete_one({"_id": ObjectId(position_id)})
                print(response)
                return response
            except Exception as e:
                return f"Error during deletion: {str(e)}"
        else:
            return f"Failed to insert the closed order for position ID {position_id}."
    except Exception as e:
        return f"An error occurred: {str(e)}"

