import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd

# data = uf.import_json('../initial_subsample/output/subsample_sentiment_count.json')
data = uf.import_json('../sample/output/sample_sentiment_count_4900.json')['content']
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
        if time_frame=='month':
            if by == 'partisanship':
                for p in partisanships:
                    x, y = [], []
                    for yr in range(2016, 2023):
                        for m in range(1,13):
                            articles = df.loc[(df['partisanship'] == p) & (df['year'] == yr) & (df['month']==m)]['article_id'].unique()
                            for a in articles:
                                avg_sent = df.loc[(df['partisanship'] == p) & (df['year'] == yr) & (df['article_id'] == a) & (df['month']==m)][
                                    'sentiment_value'].mean()
                                x.append(f"{m}/{yr}")
                                y.append(avg_sent)
                    plt.scatter(x, y, label=p)
                plt.legend()
                plt.xlabel('Partisanship')
                plt.ylabel('Average Sentiment of Each Article')
                plt.show()
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
                    plt.title('Average Sentiment over time by partisanship')
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
                    plt.title('Average Sentiment over time by Category')
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
                    plt.title('Number of Articles with keywords of a certain sentiment over time')
                    plt.show()
            if y_axis =='avg_sentiment_per_article':
                if by=='partisanship':
                    for p in partisanships:
                        x, y = [], []
                        for yr in range(2016,2023):
                            articles =df.loc[(df['partisanship']==p) & (df['year']==yr)]['article_id'].unique()
                            for a in articles:
                                avg_sent = df.loc[(df['partisanship']==p) & (df['year']==yr) &(df['article_id']==a)]['sentiment_value'].mean()
                                x.append(yr)
                                y.append(avg_sent)
                        plt.scatter(x,y,label=p)
                    plt.legend()
                    plt.xlabel('Partisanship')
                    plt.ylabel('Average Sentiment of Each Article')
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
                plt.title(f'{category}: Number of Articles with Keywords of a certain sentiment over partisanship')
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
                plt.title('Average Sentiment over Partisanship by Category')
                plt.show()
        if y_axis=='avg_sentiment_per_article':
            if by=='category':
                for c in categories:
                    x,y = [],[]
                    for p in partisanships:
                        articles =df.loc[(df['partisanship']==p) & (df['category']==c)]['article_id'].unique()
                        for a in articles:
                            avg_sent = df.loc[(df['partisanship']==p) & (df['category']==c) &(df['article_id']==a)]['sentiment_value'].mean()
                            x.append(p)
                            y.append(avg_sent)
                    plt.scatter(x,y,label=c)
                plt.legend()
                plt.xlabel('Partisanship')
                plt.ylabel('Average Sentiment of Each Article')
                plt.show()

    # (x_axis='partisanship', y_axis='avg_sentiment_per_article', by='category', category='all', time_frame='')
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

plot_sentiment(x_axis='partisanship',y_axis='avg_sentiment_per_article',by='category',category='all',time_frame='')
plot_sentiment(x_axis='time',y_axis='avg_sentiment_per_article',by='partisanship',category='all',time_frame='year')
plot_sentiment(x_axis='time',y_axis='avg_sentiment_per_article',by='partisanship',category='all',time_frame='month')

# average sentiment by partisanship?