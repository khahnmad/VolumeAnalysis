import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from scipy.stats import pearsonr

# data = uf.import_json('subsample_keyword_count_w_pubtime_no_duplicates.json')
data = uf.import_json('sample_keyword_count_w_pubtime_no_duplicates.json')

partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']
num_bins = 171

def prep_dataframe(data, category):
    df = pd.DataFrame(data[category][1:],
                      columns=['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year','partisanship','time'])
    df['month'] = df['month'].astype(int)
    df['year'] = df['year'].astype(int)
    df['time'] = pd.to_datetime(df['time'], format='ISO8601')
    df['time_index'] = None


    start = datetime.datetime(year=2016, month=1, day=1)
    for i in range(1,num_bins+1):

        end = start + datetime.timedelta(days=15)
        df.loc[(df['time'] >= start) & (df['time'] < end), 'time_index'] = i
        start = end

    return df

def plot_farright(category,metric):
    df = prep_dataframe(data, category)

    x,y =[],[]
    for i in range(num_bins+1):
        if metric == 'num_articles':
            v =len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == i) & (df['partisanship'] == 'FarRight')])
        else:
            v= df.loc[(df['time_index'] == i) & (df['partisanship'] == 'FarRight')]['num_keywords'].sum()

        x.append(i)
        y.append(v)

    plt.plot(x,y,label='FarRight')



def plot_partisanship_overlap(partisanship,category,metric):
    df = prep_dataframe(data, category)

    displacement = 1 # 15 days
    timeframe = 12 # 6 month period

    highly_correlated = []
    for start_time in range(1,num_bins-timeframe+1):

        x, y = [list(range(timeframe)), []], [list(range(timeframe)), []]
        for i in range(start_time + 1, start_time + timeframe + 1):
            if metric == 'num_articles':
                x[1].append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == i) & (df['partisanship'] == 'FarRight')]))
            else:
                x[1].append(df.loc[(df['time_index'] == i) & (df['partisanship'] == 'FarRight')]['num_keywords'].sum())

        for j in range(start_time + displacement + 1, start_time + timeframe + displacement + 1):
            if metric == 'num_articles':
                y[1].append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == j) & (df['partisanship'] == partisanship)]))
            else:
                y[1].append(df.loc[(df['time_index'] == j) & (df['partisanship'] == partisanship)]['num_keywords'].sum())

        r = pearsonr(x[1], y[1])
        if r.correlation > 0.6:
            if len(highly_correlated)> 0 and highly_correlated[-1][1] > start_time+displacement:
                highly_correlated[-1][1]=start_time+timeframe+displacement
            else:
                highly_correlated.append([start_time+displacement, start_time+timeframe+displacement])
    xx, yy = [], []
    for time_range in highly_correlated:

        for ti in range(time_range[0], time_range[1]+1):
            xx.append(ti-displacement)
            if metric=='num_articles':
                yy.append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == ti) & (df['partisanship'] == partisanship)]))
            else:
                yy.append(df.loc[(df['time_index'] == ti) & (df['partisanship'] == partisanship)]['num_keywords'].sum())
        xx.append(None)
        yy.append(None)

    plt.plot(xx,yy,label=partisanship)



def send_plot(category, count_type):
    plt.legend()
    plt.title(f"{category} {count_type}")
    plt.show()


# STARTER EXAMPLE
# Plot Far Right number of articles over time in 15 day segments
# plot_farright('Immigration','num_keywords')
# # Plot the Right number of articles over time where correlation > 0.6
# plot_partisanship_overlap('Right','Immigration','num_keywords')
# send_plot('Immigration', 'num_keywords')

# ALL COMBOS
for metric in ['num_keywords','num_articles']:
    for c in categories:
        plot_farright(c, metric)
        for p in partisanships[:-1]:
            plot_partisanship_overlap(p, c, metric)
        send_plot(c,metric)