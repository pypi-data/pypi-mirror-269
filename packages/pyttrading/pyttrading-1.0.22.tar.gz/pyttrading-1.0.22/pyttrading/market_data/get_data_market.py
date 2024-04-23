from .opensearch_collector import OpensearchCollector
import os
from dotenv import dotenv_values

config = dotenv_values(".env")


def get_market_data_from_playground(
        symbols: list = ['TNA', 'SPY'],
        opensearch_host :str = os.getenv('URL_OPENSEARCH', 'http://localhost:9200'),
        playground_host :str = os.getenv('URL_PLAYGROUND', 'http://localhost:5001'), 
        start_date :str = '9/1/2023', 
        end_date: str = '1/5/2024',
        interval: str = "1h",
        is_crypto: bool = False,
        use_playground: bool = False
    ):

    if isinstance(symbols, list):
        symbols = symbols[0]


    if use_playground:
        collector = OpensearchCollector(
                url_opensearch=opensearch_host,
                url_playground=playground_host,
        )

        data =  collector.market_data(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                interval=interval, 
                is_crypto=is_crypto
            )
    
    else:
        date_obj = datetime.strptime(start_date, '%m/%d/%Y')
        formatted_date = date_obj.strftime('%Y-%-m')            
        data = get_market_data_from_alpaca(
            symbols=symbols,
            api_key=config.get('ALPACA_API_KEY'),
            api_secret=config.get('ALPACA_API_SECRET'),
            start_date=str(formatted_date),
            interval=interval,
            is_crypto=is_crypto
        )

        data['date'] = data.index


        # data.reset_index(drop=True, inplace=True)




    return data

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockQuotesRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import pandas as pd
from alpaca.data import StockHistoricalDataClient, TimeFrame


def get_market_data_from_alpaca(
        symbols: list = 'SPY',
        api_key :str = os.getenv('API_KEY'),
        api_secret :str = os.getenv('API_SECRET'), 
        start_date :str = "2023-11-19",
        interval: str = "1h",
        is_crypto: bool = False,
        
        ):
    
    if isinstance(symbols, list):
        symbols = symbols[0]

    start_time = pd.to_datetime(start_date).tz_localize('America/New_York')


    if interval == "minutes":
        timeframe = TimeFrame.Minute
    else:
        timeframe = TimeFrame.Hour

    if not is_crypto:

        data_client = StockHistoricalDataClient(api_key, api_secret)

        request_params = StockBarsRequest(
                symbol_or_symbols=symbols,
                timeframe=timeframe,
                start=start_time
        )

        data = data_client.get_stock_bars(request_params).df.tz_convert('America/New_York', level=1)

    else: 

        # client = CryptoHistoricalDataClient(api_key, api_secret)
        client = CryptoHistoricalDataClient(api_key, api_secret)

        request_params = CryptoBarsRequest(
                        symbol_or_symbols=symbols,
                        timeframe=timeframe,
                        start=start_time
                 )

                
        data = client.get_crypto_bars(request_params)
        data = data.df

    # Resampleamos los datos al intervalo especificado
    if interval:
        if interval.endswith('h') and interval != "1h":
            data.index = pd.to_datetime(data.index.get_level_values(1))
            interval_hours = int(interval[:-1])  # Extraemos la parte numérica del intervalo
            data = data.resample(f'{interval_hours}H').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
        else:
            data.index = pd.to_datetime(data.index.get_level_values(1))

    data['date'] = data.index
    # data.reset_index(drop=True, inplace=True)
    return data


