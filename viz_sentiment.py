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
    columns = ['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']

    if category_type == 'all':
        df = combine_data_dictionaries(data, columns)
    else:
        df = pd.DataFrame(data=data[category_type][1:], columns=columns)
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
                            v = df.loc[(df['partisanship']==p) & (df['year']==yr)]['sentiment'].mean()
                            y.append(v)
                        plt.plot(x,y,label=p)
                    plt.show()




plot_sentiment(x_axis='time',time_frame='year',y_axis='avg_sentiment',by='partisanship',category='all')
plot_sentiment(x_axis='time',time_frame='month',y_axis='avg_sentiment',by='partisanship',category='all')

plot_sentiment(x_axis='time',time_frame='year',y_axis='avg_sentiment',by='category')
plot_sentiment(x_axis='time',time_frame='month',y_axis='avg_sentiment',by='category')


plot_sentiment(x_axis='time',time_frame='year',y_axis='num_articles',by='sentiment',category='Immigration')
plot_sentiment(x_axis='partisanship',y_axis='num_articles',by='sentiment',category='Immigration')