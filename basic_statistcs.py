import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from collections import Counter
import seaborn as sns
import calendar
import datetime

data = uf.import_json('initial_subsample/output/subsample_sentiment_count.json')

partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']
num_bins = 84

def prep_dataframe(data,category):
    columns = ['keyword','sentiment','article_id','partisanship','month','year']
    if category =='all':
        df = pd.DataFrame(data=data['Immigration'][1:], columns=columns)
        df['category'] = "Immigration"
        for k in list(data.keys())[1:]:
            next_df = pd.DataFrame(data=data[k][1:], columns=columns)
            next_df['category'] = k
            df = pd.concat([df, next_df])
    else:
        df = pd.DataFrame(data[category][1:],
                          columns=columns)
    sent_conversion = {'positive': 1, 'negative': -1, 'neutral': 0, '999': None, 999: None}
    df['sentiment_value'] = df.apply(lambda x: sent_conversion[x['sentiment']], axis=1)
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['article_id'] = df.apply(lambda x: x['article_id']["$oid"], axis=1)
    df['time_index'] = None
    count = 0
    for yr in range(2016, 2023):
        for m in range(1, 13):
            count += 1
            df.loc[(df['month'] == m) & (df['year'] == yr), 'time_index'] = count
    return df

def find_unique_to_partisanship(partisanship, data):
    df = prep_dataframe(data,'all')
    part_words = list(df.loc[df['partisanship']==partisanship]['keyword'].unique())

    other_words = []
    for p in [x for x in partisanships if x !=partisanship]:
        other_words +=list(df.loc[df['partisanship']==p]['keyword'].unique())

    unique_to_part = [w for w in part_words if w not in other_words]
    return unique_to_part



def find_first_appears_in_partisanship_time(partisanship, start_time, duration):
    df = prep_dataframe(data, 'all')
    part_words = list(df.loc[(df['partisanship'] == partisanship) & (df['time_index'] >=start_time) &
                             (df['time_index'] <=start_time+duration)]['keyword'].unique())

    other_words = []
    for p in [x for x in partisanships if x != partisanship]:
        other_words += list(df.loc[(df['partisanship'] == p) &
                             (df['time_index'] <=start_time+duration)]['keyword'].unique())

    unique_to_part = [w for w in part_words if w not in other_words]
    return unique_to_part

def plot_word_over_time(keyword, partisanship, data_df):
    x, y = [],[]
    for i in range(1,num_bins+1):
        x.append(i)
        y.append(len(data_df.loc[(data_df['keyword']==keyword) & (data_df['partisanship']==partisanship)&
                                 (data_df['time_index']==i)]))
    plt.plot(x,y,label=partisanship)



# for p in partisanships:
#     unique = find_unique_to_partisanship(p, data)
#     print('')
already = []
for i in range(1,85):
    duration = 6
    outcome = find_first_appears_in_partisanship_time('FarRight',i,duration)
    print(f"{i}-{i+6}: {outcome}\n")
    df = prep_dataframe(data, 'all')

    for w in outcome:
        if w in already:
            continue
        already.append(w)
        # Plot appearances in all partisanhips and times
        for p in partisanships:
            plot_word_over_time(w, p, df)

        plt.legend()
        plt.title(f"{w}")
        plt.show()

