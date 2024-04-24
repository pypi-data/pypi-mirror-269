from pyttrading import models
from ..utils.logs import log 
import mlflow

def mlflow_save(
        experiment_name: str = "ExperimentName", 
        parent_name: str = "ParentName",
        child_name: str = "ChildName", 
        mlflow_instance=None,
        metrics=None, 
        parameters=None,
        tags=None,
        parent=None,
        experiment_id=None
    ):
    if mlflow_instance is None:
        mlflow_instance = mlflow
    
    log.info(f"Register Experiment {experiment_name}")

    if not experiment_id:
        try:
            experiment_id = mlflow_instance.create_experiment(experiment_name)
        except:
            raise EnvironmentError("Experiment Name not permited, was deleted and is bloqued")

    mlflow_instance.set_experiment(experiment_name)

    if not parent:
        parent = mlflow_instance.start_run(run_name=parent_name)

    with mlflow_instance.start_run(nested=True, run_name=child_name) as child:
        if metrics:
            for key, value in metrics.items():
                key_s = key.replace(" ", '').replace('[%]', '').replace('.', '').replace('&', '').replace('[$]', '').replace('(', '').replace(')', '').replace('#', '')
                if '_' not in key_s:
                    try:
                        mlflow_instance.log_metric(key_s, value)
                    except Exception:
                        pass
        if parameters:
            for key, value in parameters.items():
                key_s = key.replace(" ", '').replace('[%]', '').replace('.', '').replace('&', '').replace('[$]', '').replace('(', '').replace(')', '').replace('#', '')
                mlflow_instance.log_param(key_s, value)
        if tags:
            for key, value in tags.items():
                key_s = key.replace(" ", '').replace('[%]', '').replace('.', '').replace('&', '').replace('[$]', '').replace('(', '').replace(')', '').replace('#', '')
                mlflow_instance.set_tag(key_s, value) 


    try:
        del metrics['_strategy']
        del metrics['_equity_curve']
        del metrics['_trades']
    except:
        pass


    
    return {
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



def mlflow_read(
        experiment_name :str = None,
        parent_name :str = None
    ):

    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(name=experiment_name)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
    )
    
    run_selected = None
    data = None
    for run in  runs:
        info = run.info
        run_name = info.run_name
        if parent_name == run_name:
            run_selected = run
            break
        data = run #TODO verify

    return data



            


