# import pyttrading as pytrade
# from dotenv import dotenv_values
# config = dotenv_values(".env")

# def run_experiment(strategy :str = 'rsi'):

#     experiment = pytrade.ExperimentMessage(
#         symbol='TNA',
#         intervals=[
#             '1h'
#         ],
#         strategies_list=[
#             strategy,
#         ],
#         is_crypto=False
#     )

#     data = pytrade.get_market_data_from_playground(
#         symbols=experiment.symbol, 
#         interval=experiment.interval, 
#         start_date='9/1/2023',
#         end_date='1/5/2024',
#         is_crypto=experiment.is_crypto
#     )

#     if len(data) == 0:
#         raise ValueError("Not found the market data")
    
#     strategies_name = strategy

#     mlflow_connection = pytrade.init_mlflow_connection()

#     model = pytrade.ModelSelector(
#                     model_name=strategies_name,
#                     path_model="tmp",
#                     type_model="basic",
#                     configuration=experiment, 
#                     df=data,
#                     symbol=experiment.symbol,
#                     interval=experiment.intervals[0],
#                     mlflow=mlflow_connection
#                 )
    

#     _, best_return, _, _, _, _= model.run_experiment_get_backtesting()
   
#     return best_return
