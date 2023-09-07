"""
x axis start time
y axis correlation
"""
import numpy as np
import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from collections import Counter
import seaborn as sns

data = uf.import_json('../initial_subsample/output/subsample_keyword_count.json')

partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']


def prep_dataframe(data, category):
    df = pd.DataFrame(data[category][1:],
                      columns=['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship'])
    df['month'] = df['month'].astype(int)
    df['year'] = df['year'].astype(int)
    df['time_index'] = None

    count = 0
    for yr in range(2016, 2023):
        for m in range(1, 13):
            count += 1
            df.loc[(df['month'] == m) & (df['year'] == yr),'time_index']= count

    return df

def fetch_correlation(category, partisanship,timeframe, start_time, displacement,w_plot:bool=False, metric='num_articles'):
    df = prep_dataframe(data, category)
    largest_month = df['time_index'].max()
    x_source = df.loc[(df['partisanship'] == 'FarRight') & (df['time_index']>=start_time) & (df['time_index']<=start_time+timeframe)]
    y_source = df.loc[(df['partisanship'] == partisanship) & (df['time_index']>=start_time+displacement) & (df['time_index']<=start_time+displacement+timeframe)]


    x, y = [list(range(timeframe)), []], [list(range(timeframe)), []]
    for i in range(start_time+1, start_time+timeframe+1):
        if metric=='num_articles':
            x[1].append(len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['time_index'] == i)]))
        else:
            x[1].append(x_source.loc[x_source['time_index'] == i]['num_keywords'].sum())
    for j in range(start_time+displacement+1, start_time+timeframe+displacement+1):
        if metric == 'num_articles':
            y[1].append(len(y_source.loc[(y_source['num_keywords'] > 0) &  (y_source['time_index'] == j)]))
        else:
            y[1].append(y_source.loc[y_source['time_index'] == j]['num_keywords'].sum())


    r = pearsonr(x[1], y[1])

    if w_plot==True:
        print(f"Category: {category}, Far Right + {partisanship}, diplacement={displacement} months")
        print(r.correlation)
        plt.plot(x[0], x[1],label='FarRight')
        plt.plot(y[0], y[1],label=partisanship)
        plt.xlabel('Time in months')
        if metric=='num_articles':
            plt.ylabel(f"Number of Articles with Keywords")
        else:
            plt.ylabel(f"Number of Keywords")
        plt.legend()
        plt.title(f"{category}: diplacement={displacement} mo., correlation={r.correlation}")
        plt.show()
    return r.correlation



def plot_w_local_context(category, primary_part):
    x, y = [],[]
    for i in range(72):
        timeframe=6
        displacement = 1
        correlation = fetch_correlation(category, primary_part,timeframe,i, displacement,metric='num_articles')
        x.append(i)
        y.append(correlation)
    global_max = max(y)
    global_max_tf = [i for i in range(len(y)) if y[i]==global_max][0]
    global_max_range = [x[global_max_tf-4], x[global_max_tf],  x[global_max_tf+4]]
    plt.plot(x,y,label=primary_part)

    for p in [j for j in partisanships[:-1] if j!=primary_part]:
        x, y = [], []
        for i in global_max_range:
            timeframe = 6
            displacement = 1
            correlation = fetch_correlation(category, p, timeframe, i, displacement, metric='num_articles')
            # outcome.append([p, c, correlation])
            x.append(i)
            y.append(correlation)
        plt.plot(x, y, label=p)
    plt.xlabel('start time')
    plt.ylabel('correlation')
    plt.title(f"{category}")
    plt.legend()
    plt.show()


outcome = []
for c in categories:
    for p in ['Right','CenterRight',"FarLeft"]:
        x, y = [],[]
        for i in range(72):
            timeframe=6
            displacement = 1
            correlation = fetch_correlation(c, p,timeframe,i, displacement,metric='num_articles')
            # outcome.append([p, c, correlation])
            x.append(i)
            y.append(correlation)

        plt.plot(x,y,label=p)
    plt.xlabel('start time')
    plt.ylabel('correlation')
    plt.title(f"{c}")
    plt.legend()
    plt.show()



category = 'Immigration'
primary_part = "Right"

for c in categories:
    for p in partisanships[:-1]:
        plot_w_local_context(c, p)

# LOOK for the global max and min at each part * cat intersection graph. What are the other parts doing here? Is there
# a larger trend of the left being up while the right is down or anything?

# FL gfoes with R & CR
