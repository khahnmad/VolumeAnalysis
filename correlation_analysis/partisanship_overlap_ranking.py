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

# def plot_farright(category,metric):
#     df = prep_dataframe(data, category)
#
#     x,y =[],[]
#     for i in range(num_bins+1):
#         if metric == 'num_articles':
#             v =len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == i) & (df['partisanship'] == 'FarRight')])
#         else:
#             v= df.loc[(df['time_index'] == i) & (df['partisanship'] == 'FarRight')]['num_keywords'].sum()
#
#         x.append(i)
#         y.append(v)
#
#     plt.plot(x,y,label='FarRight')



def get_high_correlation_period_length(prim_part, second_part:str,category:str,metric:str,t:float)->int:
    df = prep_dataframe(data, category)

    displacement = 1 # 15 days
    timeframe = 12 # 6 month period

    highly_correlated = []
    for start_time in range(1,num_bins-timeframe+1):

        x, y = [list(range(timeframe)), []], [list(range(timeframe)), []]
        for i in range(start_time + 1, start_time + timeframe + 1):
            if metric == 'num_articles':
                x[1].append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == i) & (df['partisanship'] == prim_part)]))
            else:
                x[1].append(df.loc[(df['time_index'] == i) & (df['partisanship'] == prim_part)]['num_keywords'].sum())

        for j in range(start_time + displacement + 1, start_time + timeframe + displacement + 1):
            if metric == 'num_articles':
                y[1].append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == j) & (df['partisanship'] == second_part)]))
            else:
                y[1].append(df.loc[(df['time_index'] == j) & (df['partisanship'] == second_part)]['num_keywords'].sum())

        r = pearsonr(x[1], y[1])
        if r.correlation > t:
            if len(highly_correlated)> 0 and highly_correlated[-1][1] > start_time+displacement:
                highly_correlated[-1][1]=start_time+timeframe+displacement
            else:
                highly_correlated.append([start_time+displacement, start_time+timeframe+displacement])
    count = 0
    for h in highly_correlated:
        count += h[1]-h[0]
    return count



correlation_threshold = 0.7
# ALL COMBOS
for metric in ['num_keywords','num_articles']:
    print(metric.upper())
    for c in categories:
        print(c.upper())
        for primary_part in partisanships:
            output =[ ['secondary_partisanship','length']]
            for secondary_part in [x for x in partisanships if x!=primary_part]:
                c_length = get_high_correlation_period_length(prim_part=primary_part, second_part=secondary_part,
                                                              t=correlation_threshold,category=c,metric=metric)
                output.append([secondary_part, c_length])
            df = pd.DataFrame(data=output[1:], columns=output[0])
            print(primary_part.upper())
            print(df.sort_values(by=['length']))

