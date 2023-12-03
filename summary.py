import os
import re
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


SOURCE_DIR = 'to-generate'
NO_SEEDS = os.path.join(SOURCE_DIR,'no-seeds')
SEEDS = os.path.join(SOURCE_DIR,'seeds')

SUMMARY_DIR = 'generated-summary'
PLOTS_DIR = os.path.join(SUMMARY_DIR, 'plots')
OUTPUT_EXCEL = os.path.join(SUMMARY_DIR, 'summary.xlsx')

METRICS_COLUMNS = [
    'XB',
	'DB',
	'S_Dbw',
	'DBCV',
	'Entropy',	
    'Purity',
	'Rand index',
	'Precision',
	'Recall',
	'F1',
	'Specificity',
	'Time',
]


def get_all_executions(dir):
    all_dataframes = []  
    unique_configurations = set()

    for file_name in os.listdir(dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(dir, file_name)
            df = pd.read_csv(file_path)
            df = df[~df['Configuration'].isin(unique_configurations)]
            unique_configurations.update(df['Configuration'])
            all_dataframes.append(df)

    merged_dataframe = pd.concat(all_dataframes, ignore_index=True)
    return merged_dataframe

def filter_bad_executions(df):
    df = df[df['Clusters'] == 2]
    return df

def create_excel_with_sheets(dataframe, average_results, output_excel_path):
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        average_results.to_excel(writer, sheet_name='Summary', index=False)
        datasets = dataframe['Dataset'].unique()

        for dataset in datasets:
            df_subset = dataframe[dataframe['Dataset'] == dataset]
            df_subset.to_excel(writer, sheet_name=dataset, index=False)

        print(f"Excel file saved to {output_excel_path}")

def calculate_global_averages(all_executions):
    global_averages = all_executions.groupby(['Algorithm', 'Distance Function'])[METRICS_COLUMNS].mean().reset_index()
    return global_averages

def seed_average(data):
    def remove_seed(configuration):
        return re.sub(r'-S \d+', '', configuration)
    data['Configuration'] = data['Configuration'].apply(remove_seed)

    average_metrics = data.groupby(['Dataset', 'Distance Function', 'Algorithm', 'Configuration'])[METRICS_COLUMNS].mean()
    average_metrics = average_metrics.reset_index()
    return average_metrics

# 1. read all csvs in seeds folder, get a dataframe 
# of all executions and get the average metrics of all executions of the same config

# 2. read all csvs in no seeds folder (DBSCAN executions with refinements).
# 3. delete executions with clusters different than 2
# 4. join the seed executions and the dbscan executions
# 5. make sheets for each dataset
# 6. make a summary sheet 
# 7. make plots
def make():
    all_executions_with_seeds = get_all_executions(SEEDS)
    all_executions_with_seeds[METRICS_COLUMNS] = all_executions_with_seeds[METRICS_COLUMNS].replace([np.inf, -np.inf], np.nan) # mean ignores nan but not inf
    no_seeds = seed_average(all_executions_with_seeds) # each metric is the average of all executions
    all_dbscan_executions = get_all_executions(NO_SEEDS)
    good_dbscan_executions = filter_bad_executions(all_dbscan_executions)
    all_executions = pd.concat([no_seeds, good_dbscan_executions]).reset_index(drop=True)
    all_executions[METRICS_COLUMNS] = all_executions[METRICS_COLUMNS].replace([np.inf, -np.inf], np.nan) # mean ignores nan but not inf
    average_by_algorithm_and_distance = calculate_global_averages(all_executions)
    
    if os.path.exists(SUMMARY_DIR):
        shutil.rmtree(SUMMARY_DIR)
        os.makedirs(SUMMARY_DIR)

    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)
    
    create_excel_with_sheets(all_executions, average_by_algorithm_and_distance, OUTPUT_EXCEL)
    generate_boxplots_and_save(all_executions)




def read_excel_sheets(file_path):
    return pd.read_excel(file_path, sheet_name=None)




def create_metric_boxplot(df, metric, file_name):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Algorithm', y=metric, hue='Distance Function', data=df)
    plt.title(f'{metric} Score vs Algorithm for Each Distance Function')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=45)
    plt.tight_layout()
    file_path = os.path.join(PLOTS_DIR, f'{file_name}.png')
    plt.savefig(file_path)
    plt.close()
    print(file_path)
    return file_path


def generate_boxplots_and_save(all_executions):
    plots = []
    for metric in METRICS_COLUMNS:
        file_name = metric.replace(" ", "_").replace("/", "_").lower()
        image_path = create_metric_boxplot(all_executions, metric, file_name)
        plots.append(image_path)

    pdf_file_path = os.path.join(SUMMARY_DIR, 'boxplots_report.pdf')
    pdf_pages = PdfPages(pdf_file_path)
    
    for image_path in plots:
        plt.figure(figsize=(11.69, 8.27)) 
        plt.imshow(plt.imread(image_path))
        plt.axis('off')
        pdf_pages.savefig(plt.gcf())
        plt.close()
    pdf_pages.close()

    print(f"Boxplots saved in: {PLOTS_DIR}")
    print(f"PDF report created at: {SUMMARY_DIR}")

make()