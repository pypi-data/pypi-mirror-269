from  .combinations_experiments import generate_experiments_list
from ..models import ExperimentMessage
from ..utils.logs import log
from ..market_data import get_market_data_from_playground
from ..strategies import ModelSelector
from ..experiments import mlflow_save
import json 
import mlflow
import uuid
id_test = str(uuid.uuid4()).replace('-','')[-10:-1]
import traceback

def execute_multi_experiment(experiment :ExperimentMessage, debug_mode :bool=False, mlflow_connection=None):

    log.info(experiment.dict())
    print(experiment.dict())

    experiment_data = generate_experiments_list(experiments=experiment, debug_mode=debug_mode)

    interval_selected = None
    experiments_result = []
    exp_best_return = float('-inf')
    best_results = {}
    parent_experiment = None
    parent_name=experiment_data.get('parent')
    experiment_name=experiment.experiment_name

    try:
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
    except Exception:
        experiment_id = mlflow.create_experiment(experiment_name)

    try:
        mlflow.set_experiment(experiment_name)
    except Exception as e:
        assert ConnectionResetError(f"(MLFLOW) ERROR SERVICE: {e}")
    
    with mlflow.start_run(run_name=parent_name) as parent:
        for combination in experiment_data.get('combinations'):
            child_name = combination.get('name')

            print(f">>> COMBINATION:  {combination}")

            with mlflow.start_run(nested=True, run_name=child_name) as child:
                interval_experiment = combination.get('interval')


                for key, value in combination.items():
                    mlflow.set_tag(key, value)


                if not interval_selected or interval_selected != interval_experiment:
                    log.info(f"Search market data with {experiment.symbol} interval {interval_experiment}")
                    data = get_market_data_from_playground(
                        symbols=experiment.symbol, 
                        interval=interval_experiment, 
                        start_date=experiment.start_date,
                        end_date=experiment.end_date,
                        is_crypto=experiment.is_crypto
                    )

                interval_selected = interval_experiment

                model = ModelSelector(
                                model_name=combination.get('strategy'),
                                path_model="tmp",
                                type_model=experiment.tag,
                                configuration=experiment, 
                                df=data,
                                symbol=experiment.symbol,
                                interval=interval_experiment,
                                mlflow=mlflow_connection
                            )

                try:
                    stats_json, best_return, best_return_short, best_parameters, df_actions, params = model.run_experiment_get_backtesting()

                    for key, value in stats_json.items():
                        try:
                            mlflow.log_metric(key, value)
                        except:
                            pass 


                    log.info(f"Experiment: {experiment_name}/{parent_name}/child_name {interval_selected} best_return: {best_return} ")

                    metrics={
                    "best_return": best_return, 
                    **stats_json
                    }

                    for key, value in metrics.items():
                        try:
                            mlflow.log_metric(key, value)
                        except:
                            pass 
                        
                    parameters={
                        "optimized_params": json.dumps(params),
                        "symbol": experiment.symbol,
                        "interval": interval_selected,
                        "is_crypto": experiment.is_crypto
                    }


                    tags = {
                        "method": params.get('method'),
                        "strategy_name": params.get('strategy'),
                        "strategy": params.get('strategy')
                    }
                    response = {
                        "parent": {
                            "run_id": parent.info.run_id,
                            "experiment_id": experiment_id,
                            "status": parent.info.status,
                            "run_name": parent.info.run_name,
                            "status": parent.info.status
                        },
                        "child": {
                            "run_id": child.info.run_id,
                            "experiment_id": experiment_id,
                            "status": child.info.status,
                            "run_name": child.info.run_name,
                            "status": child.info.status
                        }, 
                        "parent_experiment": parent,
                        "experiment_id": experiment_id,
                        "parameters": parameters,
                        "tags": tags, 
                        "metrics": metrics
                    }
        # self.mlflow.set_tag("strategy", self.model_name)
        # self.mlflow.set_tag("method", self.params.get('method'))
        # self.mlflow.log_param("optimized_params", json.dumps(self.params))
        # self.mlflow.log_metric('best_return',  self.params.get('best_return'))

                    if best_return > exp_best_return:
                        exp_best_return = best_return
                        best_results = {
                            "stats_json": stats_json,
                            "best_return": best_return,
                            "best_return_short": best_return_short,
                            "best_parameters": best_parameters,
                            "df_actions": df_actions,
                            "params": params,
                            "experiment_id": experiment_id,
                            "mlflow_save": response
                        }

                    experiments_result.append({
                                "best_return": best_return,
                                "name": combination.get('name'),
                            })
                except Exception as e:
                    log.error(f"EXPERIMENT ERROR: {combination}. Detalles del error:\n{traceback.format_exc()}")
                
    mlflow.end_run()

    return best_results, experiments_result