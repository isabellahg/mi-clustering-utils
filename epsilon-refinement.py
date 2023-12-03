import os
import numpy as np
import pandas as pd
import re


INITIAL_RUNS = ''

def get_new_config(configuration, scale):
    match = re.search(r'-E (\d+(\.\d+)?)', configuration)
    if match:
        current_epsilon = float(match.group(1))
        new_epsilon = current_epsilon * scale
        
        new_config = re.sub(r'-E \d+(\.\d+)?', f'-E {new_epsilon:.2f}', configuration)
        return new_config
    else:
        print(f"No epsilon found in configuration: {configuration}")


def refine_epsilon():
    df = pd.read_csv(INITIAL_RUNS)
    configurations_by_dataset = {}
    
    for index, row in df.iterrows():
        dataset = row['Dataset']
        configuration = row['Configuration']
        if  row['Clusters'] == 2:
            continue
        if dataset not in configurations_by_dataset:
            configurations_by_dataset[dataset] = []
        if row['Clusters'] < 2: # 1 OR 0 CLUSTERS => decrease epsilon
            new_config = get_new_config(configuration, 0.5)
            configurations_by_dataset[dataset].append(new_config)
            print(f"Original: {configuration}\nRefined Down: {new_config}\n")
        if row['Clusters'] > 2: # TOO MANY CLUSTERS => increase epsilon
            new_config = get_new_config(configuration, 1.5)
            configurations_by_dataset[dataset].append(new_config)
            print(f"Original: {configuration}\nRefined Up: {new_config}\n")

    print(configurations_by_dataset)
