import subprocess
import json
import pandas as pd
import numpy as np
import optuna
from kneebow.rotor import Rotor

from constants import *

params = {
    DATASETKEY: DATASETS[0],
    STANDARDIZATIONKEY: '-z5',
    DISTANCEFUNCTIONKEY: HausdorffDistance,
    DISTANCEFUNCTIONTYPEKEY: HausdorffTypes[0],
    CLUSTERINGKEY: DBSCAN
}





def get_eps(distances):
    distances = np.sort(np.array(distances))
    curve_xy = np.vstack((np.arange(len(distances)), distances)).T
    rotor = Rotor()
    rotor.fit_rotate(curve_xy)
    index = rotor.get_elbow_index()
    result = distances[index]
    return result

def set_parameters(parameters, minPoints, epsilon):
    param_str = []
    for key, value in parameters.items():
        param_str.append(f"-{key} {value}")

    param_str.append(f"-{EPSILONKEY} {epsilon}")
    param_str.append(f"-{MINPOINTSKEY} {minPoints}")
    return ' '.join(param_str)


def getKdistances(minPoints):
    command = f"java -jar {JAR_NAME} -{DISTANCEANALYSIS} {DISTANCEANALYSIS} {set_parameters(params, minPoints, 0)}"
    result = subprocess.run(command, capture_output=True, text=True)
    result = extract_json(result.stdout)
    return result.get("kDistances", [])

def execute_method(parameters, minPoints, epsilon):
    command = f"java -jar {JAR_NAME} {set_parameters(parameters, minPoints, epsilon)}"
    result = subprocess.run(command, capture_output=True, text=True)
    metrics = extract_json(result.stdout)
    return metrics


def extract_json(output):
    marker_start = "###JSON_START###"
    marker_end = "###JSON_END###"
    try:
        json_str = output.split(marker_start)[1].split(marker_end)[0].strip()
        return json.loads(json_str)
    except IndexError:
        raise ValueError("JSON markers not found in the output")

def is_float_like(value):
    try:
        float(value) 
        return True
    except ValueError:
        return False
    
class Optimizer:

    MAX_MINPOINTS = 10

    def __init__(self, objectives, directions, bag_count):
        self.params = params
        self.distance_metrics = {}  # Dictionary to store metrics for each minPoints
        self.objectives = objectives
        self.diretions = directions

        self.distancesN = getKdistances(bag_count)
        self.distances2 = getKdistances(2)
        self.other_metrics = set()


    def get_epsilon_range(self, params, minPoints, trial):
        """
        Determine the range for the epsilon parameter in DBSCAN based on k-distances and suggest a value within this range,
        taking outliers into account by using percentiles.

        :param params: Dictionary containing parameters for the dataset.
                    Expected to have a key 'dataset' with the dataset name or identifier.
        :param minPoints: The value of the minPoints parameter for DBSCAN.
        :param trial: The Optuna trial object used for suggesting hyperparameters.
        :return: A suggested epsilon value within the calculated range.
        """

        
        lower_percentile = 5   # 5th percentile
        upper_percentile = 95  # 95th percentile
        min_distance = np.percentile(self.distances2, lower_percentile)
        max_distance = np.percentile(self.distancesN, upper_percentile)
        
        # elbow_point = get_eps(self.kDistances)

        epsilon_lower = min_distance
        epsilon_upper = max_distance

        epsilon_range = epsilon_upper - epsilon_lower
        step_size = epsilon_range * 0.05  # 5% of the range
        step_size = max(step_size, 0.001)
        
        self.distance_metrics[minPoints] = {
            'min_distance': min_distance,
            'max_distance': max_distance,
            'actual_min': min(self.distances2),
            'actual_max': max(self.distancesN),
        }

        return trial.suggest_float(EPSILONKEY, epsilon_lower, epsilon_upper, step=step_size)

    def objective(self, trial):
        minPoints = trial.suggest_int(MINPOINTSKEY, 2, self.MAX_MINPOINTS)
        epsilon =self.get_epsilon_range(params, minPoints, trial)
        metrics =execute_method(params, minPoints, epsilon)
        
        results = []
        for metric_name in self.objectives:
            results.append(float(metrics.get(metric_name, 0.0)))

        for metric_name, value in metrics.items():
            # add only floats
            if metric_name not in self.objectives and is_float_like(value):
                trial.set_user_attr(metric_name, float(value))
                self.other_metrics.add(metric_name)
        return results

    def plot_slices(self, study, objectives):
        """
        Generate slice plots for each metric in the study and return them as a list.

        :param study: The Optuna study object.
        :param objectives: List of metric names to plot.
        :return: A list of plot figures.
        """
        plot_figures = []
        for i, objective in enumerate(objectives):
            fig = optuna.visualization.plot_slice(study, target=lambda t: t.values[i], target_name=objective)
            plot_figures.append(fig)

        return plot_figures


    def get_study(self, n_trials):
        study = optuna.create_study(directions=self.diretions, sampler=optuna.samplers.TPESampler())
        study.optimize(self.objective, n_trials=n_trials)
        return study

def main():
    print(getKdistances(DATASETS[0], 'z5', 2))

if __name__ == "__main__":
    main()
