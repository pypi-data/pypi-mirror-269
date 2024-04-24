import mlflow
from dotenv import dotenv_values
import mlflow
import os


def init_mlflow_connection(mlflow_username :str = None, mlflow_token :str = None, mlflow_host :str = None):
    
    if not mlflow_username:
        config = dotenv_values(".env")  
        mlflow_username = os.getenv('MLFLOW_USERNAME', config.get("MLFLOW_USERNAME"))  
        mlflow_token = os.getenv('MLFLOW_TOKEN', config.get("MLFLOW_TOKEN"))
        mlflow_host = os.getenv('MLFLOW_HOST', config.get("MLFLOW_HOST"))
    
    os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_token
    os.environ['MLFLOW_TRACKING_URI'] = mlflow_host

    mlflow_connection = mlflow
    mlflow_connection.set_tracking_uri(mlflow_host)

    return mlflow_connection