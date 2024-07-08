import numpy as np
import json
import os
import glob

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def group_metrics(data):
    tooth_group = {1: '1-3', 2: '1-3', 3: '1-3', 4: '4-5', 5: '4-5', 7: '7-8', 8: '7-8'}
    quadrant_group = {1: 'Q1-2', 2: 'Q1-2', 3: 'Q3-4', 4: 'Q3-4'}
    grouped_metrics = {}
    tooth_group_key = tooth_group.get(data['tooth'], None)
    quadrant_group_key = quadrant_group.get(data['quadrant'], None)
    if tooth_group_key and quadrant_group_key:
        group_key = f"{tooth_group_key}, {quadrant_group_key}"
        if group_key not in grouped_metrics:
            grouped_metrics[group_key] = []
        grouped_metrics[group_key].append(data)
    return grouped_metrics

def average_metrics(grouped_data):
    results = {}
    for group, metrics_list in grouped_data.items():
        summed_metrics = {}
        count = 0
        for metrics in metrics_list:
            for metric_type, values in metrics.items():
                if metric_type == 'tooth' or metric_type == 'quadrant':
                    continue  # Skip non-numeric data
                if metric_type not in summed_metrics:
                    # Initialize as empty arrays using the shape of the first occurrence
                    summed_metrics[metric_type] = {k: np.zeros_like(v) for k, v in values.items()}
                # Assume values is a dict of arrays/lists; update each key
                for k, v in values.items():
                    summed_metrics[metric_type][k] += np.array(v)
            count += 1
        # Average the summed values
        averaged_metrics = {metric_key: {k: (v / count).tolist() for k, v in metric_values.items()} for metric_key, metric_values in summed_metrics.items()}
        results[group] = averaged_metrics
    return results

# Set candidate and directories
candidate = "noorlag"
metrics_directory = f'data/metrics/{candidate}'

all_metrics = []

# Process each translated data file
for file_path in glob.glob(os.path.join(metrics_directory, '*.json')):
    metrics_data = load_data_from_json(file_path)
    all_metrics.append(metrics_data)

# Group metrics by tooth groups
grouped_data = {}
for data in all_metrics:
    group = group_metrics(data)
    for key, value in group.items():
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].extend(value)

# Calculate the average metrics for each group
results = average_metrics(grouped_data)

# Print the results
for group, metrics in results.items():
    print(f"The average results for tooth and quadrant group {group} are: {metrics}\n")
