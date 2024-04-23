

def mlflow_get_models_by_interval(stage :str = "Staging", interval :str = "1h", mlflow_connection=None):

    models = mlflow_connection.search_registered_models()
    models_interval = []
    for model in models:
        tag = model.tags.get(stage)
        interval_model = tag.split('/')[1]

        if interval == interval_model:
            models_interval.append(model)

    return models_interval

def get_intervals_from_models(stage :str = "Staging", mlflow_connection=None):
    
    models = mlflow_connection.search_registered_models()
    intervals = []
    for model in models:
        tag = model.tags.get(stage)
        interval = tag.split('/')[1]
        intervals.append(interval)

    intervals = list(set(intervals))

    return intervals