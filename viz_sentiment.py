import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd

data = uf.import_json('initial_subsample/output/subsample_sentiment_count.json')
# data = uf.import_json('sample/output/sample_keyword_count.json')
partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']

def combine_data_dictionaries(data, columns):
    df = pd.DataFrame(data=data['Immigration'][1:], columns=columns)
    df['category'] = "Immigration"

    for k in list(data.keys())[1:]:
        next_df = pd.DataFrame(data=data[k][1:], columns=columns)
        next_df['category'] = k
        df = pd.concat([df, next_df])
    return df

def fetch_dataframe(category_type, data):
    columns = ['keyword', 'sentiment', 'article_id', 'partisanship', 'month', 'year']

    if category_type == 'all':
        df = combine_data_dictionaries(data, columns)
    else:
        df = pd.DataFrame(data=data[category_type][1:], columns=columns)

    sent_conversion = {'positive': 1, 'negative': -1, 'neutral': 0, '999': None, 999: None}
    # df['sentiment_value'] = sent_conversion[df['sentiment']]
    df['sentiment_value'] = df.apply(lambda x: sent_conversion[x['sentiment']], axis=1)
    df['year']=df['year'].astype(int)
    df['month']=df['month'].astype(int)
    df['article_id'] = df.apply(lambda x: x['article_id']["$oid"], axis=1)
    return df

def plot_sentiment(x_axis:str,time_frame,y_axis,by,category):
    df = fetch_dataframe(category, data)

    if x_axis=='time':
        if time_frame=='year':
            x = list(range(2016,2023))

            if y_axis=='avg_sentiment':
                if by=='partisanship':
                    for p in partisanships:
                        y = []
                        for yr in x:
                            v = df.loc[(df['partisanship']==p) & (df['year']==yr)]['sentiment_value'].mean()
                            y.append(v)
                        plt.plot(x,y,label=p)
                    plt.legend()
                    plt.xlabel('Time')
                    plt.ylabel('Average Sentiment')
                    plt.show()
                if by=='category':
                    for c in categories:
                        y = []
                        for yr in x:
                            v = df.loc[(df['category']==c) & (df['year']==yr)]['sentiment_value'].mean()
                            y.append(v)
                        plt.plot(x,y,label=c)
                    plt.legend()
                    plt.xlabel('Time')
                    plt.ylabel('Average Sentiment')
                    plt.show()
            if y_axis=='num_articles':
                if by=='sentiment':
                    for s in ['positive','negative','neutral']:
                        y = []
                        for yr in x:
                            v = len(df.loc[ (df['year'] == yr) & (df['sentiment']==s)]['article_id'].unique())
                            y.append(v)
                        plt.plot(x, y, label=s)
                    plt.legend()
                    plt.xlabel('Time')
                    plt.ylabel('Number of Articles')
                    plt.show()
    if x_axis=='partisanship':
        if y_axis=='num_articles':
            if by=='sentiment':
                for s in ['positive', 'negative', 'neutral']:
                    y = []
                    for p in partisanships:
                        v = len(df.loc[(df['partisanship'] == p) & (df['sentiment'] == s)]['article_id'].unique())
                        y.append(v)
                    plt.plot(partisanships, y, label=s)
                plt.legend()
                plt.xlabel('Partisanship')
                plt.ylabel('Number of Articles')
                plt.show()
        if y_axis=='avg_sentiment':
            if by=='category':
                for c in categories:
                    y = []
                    for p in partisanships:
                        v = df.loc[(df['category'] == c) & (df['partisanship'] == p)]['sentiment_value'].mean()
                        y.append(v)
                    plt.plot(partisanships, y, label=c)
                plt.legend()
                plt.xlabel('Partisanship')
                plt.ylabel('Average Sentiment')
                plt.show()

    # (x_axis='partisanship', y_axis='avg_sentiment', by='category', category='all', time_frame='')

plot_sentiment(x_axis='time',time_frame='year',y_axis='avg_sentiment',by='partisanship',category='all')
# plot_sentiment(x_axis='time',time_frame='month',y_axis='avg_sentiment',by='partisanship',category='all')
#
plot_sentiment(x_axis='time',time_frame='year',y_axis='avg_sentiment',by='category',category='all')
# plot_sentiment(x_axis='time',time_frame='month',y_axis='avg_sentiment',by='category')
#

plot_sentiment(x_axis='time',time_frame='year',y_axis='num_articles',by='sentiment',category='Immigration')
plot_sentiment(x_axis='partisanship',y_axis='num_articles',by='sentiment',category='Immigration',time_frame='')
plot_sentiment(x_axis='partisanship',y_axis='num_articles',by='sentiment',category='Transphobia',time_frame='')

plot_sentiment(x_axis='partisanship',y_axis='avg_sentiment',by='category',category='all',time_frame='')