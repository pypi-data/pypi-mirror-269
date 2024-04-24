
import os

def test_get_market_data(pass_test :bool = False):

    import pyttrading as pytrade
    data = pytrade.get_market_data_from_playground(symbols=['TNA'], is_crypto=False)

    if len(data) > 200:
        pass_test = True
        
    assert pass_test
    
def test_get_market_crypto(pass_test :bool = False):

    import pyttrading as pytrade

    pass_test = False
    data = pytrade.get_market_data_from_playground(symbols=['AVAX/USD'], is_crypto=True)

    if len(data) > 200:
        pass_test = True

    assert pass_test


from dotenv import dotenv_values
config = dotenv_values(".env")


def test_get_market_data_alpaca(pass_test :bool = False):

    import pyttrading as tt
    api_key =  os.getenv('ALPACA_API_KEY', config.get('ALPACA_API_KEY')) 
    api_secret =  os.getenv('ALPACA_API_SECRET', config.get('ALPACA_API_SECRET')) 

    data = tt.get_market_data_from_alpaca(
        symbols="SPY",
        api_key=api_key,
        start_date = "2023-11-19",
        api_secret=api_secret,
        interval="4h",
        is_crypto=False
    )

    if len(data) > 100:
        pass_test = True 

    assert pass_test



def test_get_market_data_alpaca_crypto(pass_test :bool = False):

    import pyttrading as tt

    api_key =  os.getenv('ALPACA_API_KEY', config.get('ALPACA_API_KEY')) 
    api_secret =  os.getenv('ALPACA_API_SECRET', config.get('ALPACA_API_SECRET')) 

    data = tt.get_market_data_from_alpaca(
        symbols="BTC/USD",
        api_key=api_key,
        start_date = "2024-01-19",
        api_secret=api_secret,
        interval="4h",
        is_crypto=True
    )


    if len(data) > 100:
        pass_test = True 

    assert pass_test