# from ... import pyttrading as pytrade
# from dotenv import dotenv_values
# config = dotenv_values(".env")


# import uuid
# import json 

# id_test = str(uuid.uuid4()).replace('-','')[-10:-1]

# def test_generate_list_of_experiments(pass_test: str = False):
#     experiments = pytrade.models.ExperimentMessage()
#     experiment_data = pytrade.generate_experiments_list(experiments)
#     if len(experiment_data['combinations']) > 0:
#         pass_test = True 
#     assert pass_test


# def create_experiment():

#     id_test = str(uuid.uuid4()).replace('-','')[-10:-1]

#     experiments = pytrade.models.ExperimentMessage()

#     if not experiments:
#         raise ValueError("Not found the market data")

#     experiments.experiment_name =  f'testing_{id_test}_' + experiments.experiment_name
#     experiment_data = pytrade.generate_experiments_list(experiments)
#     experiment_data['combinations'] = [experiment_data['combinations'][0]]

#     # ..... 
#     data = pytrade.get_market_data_from_playground(
#         symbols=experiments.symbol, 
#         interval=experiments.interval, 
#         start_date='9/1/2023',
#         end_date='1/5/2024',
#         is_crypto=experiments.is_crypto
#     )

#     if len(data) == 0:
#         raise ValueError("Not found the market data")
    
#     mlflow_connection = pytrade.init_mlflow_connection()

#     experiment_data.get('combinations')

#     model_name = experiment_data.get('combinations')[0].get('strategy')
#     child_name = experiment_data.get('combinations')[0].get('name')

#     model = pytrade.ModelSelector(
#                     model_name=model_name,
#                     path_model="tmp",
#                     type_model="basic",
#                     configuration=experiments, 
#                     df=data,
#                     symbol=experiments.symbol,
#                     interval=experiments.interval,
#                     mlflow=mlflow_connection
#                 )
    

#     stats_json, best_return, _, _, _, params= model.run_experiment_get_backtesting()
#     parent_experiment = None
#     experiment_id = None
#     for child_name in ['1h_sma', '1h_rsi']:
#         response = pytrade.mlflow_save(
#             mlflow_instance=mlflow_connection,
#             experiment_name=experiments.experiment_name,
#             parent_name=experiment_data['parent'],
#             child_name=child_name,
#             metrics={
#                 "best_return": best_return, 
#                 **stats_json
#             },
#             parameters={
#                 "optimized_params": json.dumps(params),
#                 "symbol": experiments.symbol,
#                 "interval": experiments.interval
#             },
#             tags = {
#                 "method": params.get('method'),
#                 "strategy_name": params.get('strategy'),
#                 "strategy": params.get('strategy')
#             },
#             parent=parent_experiment,
#             experiment_id=experiment_id
#         )
#         parent_experiment = response.get('parent_experiment')
#         experiment_id = response.get('experiment_id')

#     return response