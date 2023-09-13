"""
Time index is based on 15 day bins (171 total) from 01-01-2016 to end 2022
Displacment is set to 15 days, and the time frames investigated are in 6 month chunks

"""
import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from scipy.stats import pearsonr

#### GLOBAL VARIABLES ######
SUB_OR_SAMPLE = 'Sample'
if SUB_OR_SAMPLE=='Subsample':
    DATA = uf.import_json('subsample_keyword_count_w_pubtime_no_duplicates.json')
else:
    DATA = uf.import_json('sample_keyword_count_w_pubtime_no_duplicates.json')

PARTISANSHIPS = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
CATEGORIES =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']
NUM_BINS = 171
DISPLACEMENT = 1 # 15 days
TIMEFRAME = 12 # 6 month period
CORRELATION_THRESHOLD = 0.6


def prep_dataframe(data:dict, category:str):
    """Given the data source and the category, create a dataframe with a time index"""
    df = pd.DataFrame(data[category][1:],
                      columns=['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year','partisanship','time'])
    df['month'] = df['month'].astype(int)
    df['year'] = df['year'].astype(int)
    df['time'] = pd.to_datetime(df['time'], format='ISO8601')
    df['time_index'] = None

    # Create a time index base on 15 day increments
    start = datetime.datetime(year=2016, month=1, day=1)
    for i in range(1, NUM_BINS + 1):

        end = start + datetime.timedelta(days=15)
        df.loc[(df['time'] >= start) & (df['time'] < end), 'time_index'] = i
        start = end

    return df


def plot_farright(df,metric:str):

    # Count narrative quantity for each time index
    x,y =[],[]
    for i in range(1,NUM_BINS + 1):
        if metric == 'num_articles':
            # Conditions: article has > 0 keywords, time_index matches, partisanship is FarRight
            v =len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == i) & (df['partisanship'] == 'FarRight')])
        else:
            # Conditions: time_index matches, partisanship is FarRight
            v= df.loc[(df['time_index'] == i) & (df['partisanship'] == 'FarRight')]['num_keywords'].sum()

        x.append(i)
        y.append(v)

    # Send plot
    plt.plot(x,y,label='FarRight')
    return y


def plot_partisanship_overlap(df, partisanship:str,metric:str, fr_y:list):
    highly_correlated = []

    # Iterate through from start of dataset to that last point possible with the displacement
    for start_time in range(NUM_BINS - TIMEFRAME):

        # Find the narrative quantity for the Far Right given this start_time
        x, y = [list(range(1,1+TIMEFRAME)), []], [list(range(1,1+TIMEFRAME)), []]

        # Iterate through from the start time to the end for the timeframe
        for i in range(start_time + 1, start_time + TIMEFRAME + 1):
            x[1].append(fr_y[i-1])

        # Iterate through from start time to the end for the time frame, with the displacement
        for j in range(start_time + DISPLACEMENT + 1, start_time + TIMEFRAME + DISPLACEMENT + 1):
            if metric == 'num_articles':
                y[1].append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == j) & (df['partisanship'] == partisanship)]))
            else:
                y[1].append(df.loc[(df['time_index'] == j) & (df['partisanship'] == partisanship)]['num_keywords'].sum())

        r = pearsonr(x[1], y[1]) # calculate correlation

        if r.correlation > CORRELATION_THRESHOLD: # If the correlation is sufficiently high
            # if there's been a previously high correlation period that overlaps with this one:
            if len(highly_correlated)> 0 and highly_correlated[-1][1] > start_time+DISPLACEMENT:
                highly_correlated[-1][1]= start_time + TIMEFRAME + DISPLACEMENT
            else:
                highly_correlated.append([start_time + DISPLACEMENT, start_time + TIMEFRAME + DISPLACEMENT])

    xx, yy = [], []
    for time_range in highly_correlated:

        for ti in range(time_range[0], time_range[1]+1):
            xx.append(ti - DISPLACEMENT)
            if metric=='num_articles':
                yy.append(len(df.loc[(df['num_keywords'] > 0) & (df['time_index'] == ti) & (df['partisanship'] == partisanship)]))
            else:
                yy.append(df.loc[(df['time_index'] == ti) & (df['partisanship'] == partisanship)]['num_keywords'].sum())
        xx.append(None)
        yy.append(None)

    plt.plot(xx,yy,label=partisanship)



def send_plot(category, count_type):
    plt.legend()
    plt.title(f"{SUB_OR_SAMPLE}: {category} {count_type}")
    plt.show()


# ALL COMBOS
for metric in ['num_keywords','num_articles']:
    for c in CATEGORIES:
        cat_df = prep_dataframe(data=DATA, category=c) # prepare df for this category
        print(f'Created df for {c}')
        fr_y= plot_farright(cat_df, metric) # send the plot for the far right
        print(f'Sent FR plot')
        for p in PARTISANSHIPS[:-1]: # excluding the far right, iterate through partisanships
            # find high correlation periods and plot them
            plot_partisanship_overlap(df=cat_df, partisanship=p, metric=metric, fr_y=fr_y)
            print(f"Sent {p} plot")
        send_plot(c,metric,) # dress the plot and show it