import json

def save_best_model_mlflow(best_results=None, model_name :str = None, stage :str = "Staging"):

    #TODO fix
    import pyttrading as tt
    from mlflow.tracking import MlflowClient

    log = tt.utils.log

    best_response = best_results.get('mlflow_save')
    
    output = {
        "best_candidate": best_results['best_return'],
        "parms": best_results['params'],
    }

    run_id = best_response.get('child').get('run_id')
    model_uri = f"runs:/{run_id}/model"

    log.info("Saving model")

    metrics = best_response.get('metrics')
    del metrics['_strategy']
    del metrics['_equity_curve']
    del metrics['_trades']

    mlflow_connection = tt.init_mlflow_connection()


    result = mlflow_connection.register_model(
            model_uri=model_uri,
            name= model_name,
            tags={
                "tags": json.dumps(best_response.get('tags')),
                "parameters": json.dumps(best_response.get('parameters')),
                "metrics": json.dumps(best_response.get('metrics'))
            }
        )
    client = MlflowClient()
    
    result_model = client.transition_model_version_stage(
            name=result.name,
            version=result.version,
            stage=stage,
            archive_existing_versions=True
        )  

    profit_factor = round(best_response.get('metrics').get("Profit Factor", -1.001), 2)
    interval = best_response.get('parameters').get('interval')
    client.set_registered_model_tag(result.name, f'{stage}', f"{profit_factor}/{interval}")

    return result_model

