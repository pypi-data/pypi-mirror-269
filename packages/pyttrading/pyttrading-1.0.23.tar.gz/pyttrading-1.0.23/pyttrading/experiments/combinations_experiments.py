from pyttrading import models
from ..utils.logs import log
import uuid
id_test = str(uuid.uuid4()).replace('-','')[-10:-1]


def generate_experiments_list(experiments : models.ExperimentMessage, debug_mode :bool=False):

    combinations = []

    for interval in experiments.intervals:
        for strategy in experiments.strategies_list:
            combinations.append({
                "name": f"{interval}_{strategy}",
                "interval": interval, 
                "strategy": strategy
            })


    if debug_mode:
        if len(combinations) > 1:
            combinations = [combinations[0], combinations[1]]
        else:
            combinations = [combinations[0]]


            
    experiments_all = {
        experiments.experiment_name: {
            f"{experiments.start_date}-{experiments.end_date}": combinations
        }
    }

    experiments_data = {
        "combinations": combinations, 
        "parent": f"{experiments.start_date}-{experiments.end_date}",
        "experiment": experiments.experiment_name,
        "all": experiments_all
    }

    return experiments_data