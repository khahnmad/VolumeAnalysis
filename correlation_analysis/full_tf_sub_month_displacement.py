import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from collections import Counter
import seaborn as sns
import calendar
import datetime

# data = uf.import_json('subsample_keyword_count_w_pubtime_no_duplicates.json')
# data = uf.import_json('sample_keyword_count_w_pubtime_no_duplicates.json')

partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']


def prep_dataframe(data, category):
    df = pd.DataFrame(data[category][1:],
                      columns=['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year','partisanship','time'])
    df['month'] = df['month'].astype(int)
    df['year'] = df['year'].astype(int)
    df['time'] = pd.to_datetime(df['time'], format='ISO8601')
    df['time_index'] = None

    # # To make the bin size 1 day long
    # count = 0
    # for yr in range(2016, 2023):
    #     for m in range(1, 13):
    #         for day in range(1,calendar.monthrange(yr,m)[1]):
    #             start_day = datetime.datetime(year=yr,month=m,day=day)
    #             end_day = datetime.datetime(year=yr,month=m,day=day,hour=23, minute=59,second=59)
    #             count += 1
    #             df.loc[(df['time']>=start_day) & (df['time']<=end_day),'time_index']= count
    # To make the bin size 1 week long
    # count = 0
    # for yr in range(2016, 2023):
    #     for m in range(1, 13):
    #         weeks = calendar.monthcalendar(yr, m)
    #         for week in weeks:
    #             week = [x for x in week if x!=0] # Remove zeros from the week
    #             start_day = datetime.datetime(year=yr, month=m, day=week[0])
    #             end_day = datetime.datetime(year=yr, month=m, day=week[-1], hour=23, minute=59, second=59)
    #             count += 1
    #             df.loc[(df['time'] >= start_day) & (df['time'] <= end_day), 'time_index'] = count
    # To make the bins 15 days long
    start = datetime.datetime(year=2016, month=1, day=1)
    for i in range(1,172):

        end = start + datetime.timedelta(days=15)
        df.loc[(df['time'] >= start) & (df['time'] < end), 'time_index'] = i
        start = end

    return df



def fetch_correlation(category, partisanship, displacement,w_plot:bool=False, metric='num_articles'):
    df = prep_dataframe(data, category)
    largest_index = df['time_index'].max()
    x_source = df.loc[(df['partisanship'] == 'FarRight') & (df['time_index']<=largest_index-displacement)]
    y_source = df.loc[(df['partisanship'] == partisanship) & (df['time_index']>=displacement)]



    x, y = [list(range(largest_index)), []], [list(range(largest_index)), []]
    for i in range(1, largest_index+1):
        if metric=='num_articles':
            x[1].append(len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['time_index'] == i)]))
        else:
            x[1].append(x_source.loc[x_source['time_index'] == i]['num_keywords'].sum())
    for j in range(displacement+1, largest_index+displacement+1):
        if metric == 'num_articles':
            y[1].append(len(y_source.loc[(y_source['num_keywords'] > 0) &  (y_source['time_index'] == j)]))
        else:
            y[1].append(y_source.loc[y_source['time_index'] == j]['num_keywords'].sum())


    r = pearsonr(x[1], y[1])

    if w_plot==True:
        print(f"Category: {category}, Far Right + {partisanship}, diplacement={displacement} days")
        print(r.correlation)
        plt.scatter(x[0], x[1],label='FarRight')
        plt.scatter(y[0], y[1],label=partisanship)
        plt.xlabel('Time in months')
        if metric=='num_articles':
            plt.ylabel(f"Number of Articles with Keywords")
        else:
            plt.ylabel(f"Number of Keywords")
        plt.legend()
        plt.title(f"{category}: diplacement={displacement} days., correlation={r.correlation}")
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
