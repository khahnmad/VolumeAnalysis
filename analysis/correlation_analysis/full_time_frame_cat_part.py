"For the full time frame, which category * partisanship had the largest correlation with the Far Right? "
import numpy as np
import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from collections import Counter
import seaborn as sns

data = uf.import_json('../../initial_subsample/output/subsample_keyword_count.json')

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

def fetch_correlation(category, partisanship, displacement,w_plot:bool=False, metric='num_articles'):
    df = prep_dataframe(data, category)
    largest_month = df['time_index'].max()
    x_source = df.loc[(df['partisanship'] == 'FarRight') & (df['time_index']<=largest_month-displacement)]
    y_source = df.loc[(df['partisanship'] == partisanship) & (df['time_index']>=displacement)]



    x, y = [list(range(largest_month)), []], [list(range(largest_month)), []]
    for i in range(1, largest_month+1):
        if metric=='num_articles':
            x[1].append(len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['time_index'] == i)]))
        else:
            x[1].append(x_source.loc[x_source['time_index'] == i]['num_keywords'].sum())
    for j in range(displacement+1, largest_month+displacement+1):
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

outcome = []
for c in categories:
    for p in partisanships[:-1]:
        displacement = 1
        correlation = fetch_correlation(c, p, displacement,metric='num_articles')
        outcome.append([p, c, correlation])
df = pd.DataFrame(data=outcome, columns=['Partisanship','Category','Correlation'])


sns.catplot(
    x="Partisanship",       # x variable name
    y="Correlation",       # y variable name
    hue="Category",  # group variable name
    data=df,     # dataframe to plot
    kind="bar",
)
plt.show()
"""
NUMBER OF KEYWORDS
Immi:  Left
Islam: Left
Trans: Center
Anti: Right

Far Left: Immi
Left: Immi
CenterLeft: Immi
Center: Immi
CenterRight: IImmi 
Right: Immi

NUMBER OF ARTICLES 
Immi: Far Left: 0.25
Islam: Right: 0.284
Trans: Left: -0.05
Anti: Right: 0.20

Far Left: Immi
Left: Islam
CenterLeft: Islam
Center: Islam
CenterRight: Islam 
Right: Islam
"""

# Plot results
# Articles with keywords
# fetch_correlation('Immigration','FarLeft',1,w_plot=True)
# fetch_correlation('Islamophobia','Right',1,w_plot=True)
# fetch_correlation('Transphobia','Left',1,w_plot=True)
# fetch_correlation('Anti-semitism','Right',1,w_plot=True)

# OVerall num keywords
# fetch_correlation('Immigration','Left',1,w_plot=True,metric='num_keywords')
# fetch_correlation('Islamophobia','Left',1,w_plot=True,metric='num_keywords')
# fetch_correlation('Transphobia','Center',1,w_plot=True,metric='num_keywords')
# fetch_correlation('Anti-semitism','Right',1,w_plot=True,metric='num_keywords')