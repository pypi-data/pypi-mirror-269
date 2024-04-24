
from dotenv import dotenv_values
import mlflow
config = dotenv_values(".env")
import uuid
import json 
from mlflow.tracking import MlflowClient

# from tests.functions.create_experiment import create_experiment

id_test = str(uuid.uuid4()).replace('-','')[-10:-1]



def test_generate_list_of_experiments(pass_test: str = False):

    import pyttrading as pytrade
    experiments = pytrade.models.ExperimentMessage()
    experiment_data = pytrade.generate_experiments_list(experiments)
    if len(experiment_data['combinations']) > 0:
        pass_test = True 
    assert pass_test


def create_experiment():

    import pyttrading as pytrade

    id_test = str(uuid.uuid4()).replace('-','')[-10:-1]

    experiments = pytrade.models.ExperimentMessage()

    if not experiments:
        raise ValueError("Not found the market data")

    experiments.experiment_name =  f'testing_{id_test}_' + experiments.experiment_name
    experiment_data = pytrade.generate_experiments_list(experiments)
    experiment_data['combinations'] = [experiment_data['combinations'][0]]

    # ..... 
    data = pytrade.get_market_data_from_playground(
        symbols=experiments.symbol, 
        interval=experiments.interval, 
        start_date='9/1/2023',
        end_date='1/5/2024',
        is_crypto=experiments.is_crypto
    )

    if len(data) == 0:
        raise ValueError("Not found the market data")
    
    mlflow_connection = pytrade.init_mlflow_connection()

    experiment_data.get('combinations')

    model_name = experiment_data.get('combinations')[0].get('strategy')
    child_name = experiment_data.get('combinations')[0].get('name')

    model = pytrade.ModelSelector(
                    model_name=model_name,
                    path_model="tmp",
                    type_model="basic",
                    configuration=experiments, 
                    df=data,
                    symbol=experiments.symbol,
                    interval=experiments.interval,
                    mlflow=mlflow_connection
                )
    

    stats_json, best_return, _, _, _, params= model.run_experiment_get_backtesting()
    parent_experiment = None
    experiment_id = None
    for child_name in ['1h_sma', '1h_rsi']:
        response = pytrade.mlflow_save(
            mlflow_instance=mlflow_connection,
            experiment_name=experiments.experiment_name,
            parent_name=experiment_data['parent'],
            child_name=child_name,
            metrics={
                "best_return": best_return, 
                **stats_json
            },
            parameters={
                "optimized_params": json.dumps(params),
                "symbol": experiments.symbol,
                "interval": experiments.interval
            },
            tags = {
                "method": params.get('method'),
                "strategy_name": params.get('strategy'),
                "strategy": params.get('strategy')
            },
            parent=parent_experiment,
            experiment_id=experiment_id
        )
        parent_experiment = response.get('parent_experiment')
        experiment_id = response.get('experiment_id')

    return response



id_test = str(uuid.uuid4()).replace('-','')[-10:-1]


def test_generate_list_of_experiments(pass_test: str = False):

    import pyttrading as pytrade


    experiments = pytrade.models.ExperimentMessage()
    experiment_data = pytrade.generate_experiments_list(experiments)
    if len(experiment_data['combinations']) > 0:
        pass_test = True 
    assert pass_test


def test_run_experiment_and_save_mlflow(pass_test: str = False):
    response = create_experiment()
    if response.get('child').get('run_id'):
        pass_test = True
        client = MlflowClient()
        client.delete_experiment(experiment_id=response.get('parent').get('experiment_id'))

    assert pass_test

def test_experiment_to_model(pass_test: str = False):

    import pyttrading as pytrade
    response = create_experiment()

    id_test = str(uuid.uuid4()).replace('-','')[-10:-1]
    experiments = pytrade.models.ExperimentMessage()
    best_run_id = response.get('child').get('run_id')

    model_uri = f"runs:/{best_run_id}/model"


    result = mlflow.register_model(
            model_uri=model_uri,
            name= 'testing_'+ experiments.symbol + '_' + experiments.tag + '_' + experiments.version + '_' + id_test,
            tags={
                "tags": json.dumps(response.get('tags')),
                "parameters": json.dumps(response.get('parameters')),
                "metrics": json.dumps(response.get('metrics'))
            }
        )
    
    client = MlflowClient()

    result_model = client.transition_model_version_stage(
            name=result.name,
            version=result.version,
            stage="Staging",
            archive_existing_versions=True
        )   
    
    if result_model.current_stage == 'Staging':
        pass_test = True
        client.delete_registered_model(name=result.name)
        client.delete_experiment(experiment_id=response.get('child').get('experiment_id'))

    assert pass_test


def test_run_sync_multi_experiment(pass_test: str = False):
    import pyttrading as pytrade

    experiment = pytrade.models.ExperimentMessage()
    mlflow_connection = pytrade.init_mlflow_connection()

    experiment.experiment_name = f"test_{id_test}_{experiment.experiment_name}"

    best_results, experiments_result = pytrade.execute_multi_experiment(experiment=experiment, debug_mode=True, mlflow_connection=mlflow_connection)

    if len(experiments_result) == 2:
        pass_test = True

    return pass_test


def test_run_sync_multi_experiment_nested(pass_test: str = False):

    import pyttrading as pytrade

    experiment = pytrade.models.ExperimentMessage()
    mlflow_connection = pytrade.init_mlflow_connection()

    experiment.experiment_name = f"test7_{experiment.experiment_name}"
    
    start_date_ny, end_date_ny, _ = pytrade.get_datetime_now_trade()
    experiment.start_date = start_date_ny
    experiment.end_date = end_date_ny
    best_results, experiments_result = pytrade.execute_multi_experiment(experiment=experiment, debug_mode=True, mlflow_connection=mlflow_connection)

    if len(experiments_result) == 2:
        pass_test = True

    return pass_test