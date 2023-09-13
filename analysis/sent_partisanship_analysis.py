"""
What are the most positive and negative words?
Which are uniquely neg/ pos on the far right vs fr left vs others? 
"""
import pandas as pd
import universal_functions as uf

DATA = uf.import_json('../sample/output/sample_sentiment_count_5500.json')['content']
PARTISANSHIPS = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
CATEGORIES =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']


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
    df['sentiment_value'] = df.apply(lambda x: sent_conversion[x['sentiment']], axis=1)
    df['year']=df['year'].astype(int)
    df['month']=df['month'].astype(int)
    df['article_id'] = df.apply(lambda x: x['article_id']["$oid"], axis=1)
    return df


def most_pos_word(datafr, partisanship=None):
    keywords = list(datafr['keyword'].unique())
    _max = [-99999, '']
    for k in keywords:
        if partisanship:
            avg_score = datafr.loc[(datafr['keyword'] == k) &
                                   (datafr['partisanship'] == partisanship)]['sentiment_value'].mean()
        else:
            avg_score = datafr.loc[datafr['keyword'] == k]['sentiment_value'].mean()
        if avg_score > _max[0]:
            _max = [avg_score, k]
    return _max

def most_neg_word(datafr, partisanship=None):
    keywords = list(datafr['keyword'].unique())
    _min = [99999, '']
    for k in keywords:
        if partisanship:
            avg_score = datafr.loc[(datafr['keyword'] == k) & (datafr['partisanship']==partisanship)]['sentiment_value'].mean()
        else:
            avg_score = datafr.loc[datafr['keyword'] == k]['sentiment_value'].mean()
        if avg_score < _min[0]:
            _min = [avg_score, k]
    return _min


df = fetch_dataframe('all',DATA)
print('')
# Overall most positive words
most_pos = most_pos_word(df)

# Overall most negative words
most_neg = most_neg_word(df)

# Most positive words given partisanship
part_polarity = [['partisanship','pos_word','pos_word_score','neg_word','neg_word_score']]
for p in PARTISANSHIPS:
    pos_response = most_pos_word(df, p)
    neg_response = most_neg_word(df, p)
    part_polarity.append([p, pos_response[1], pos_response[0], neg_response[1], neg_response[0]])
print('')

# Most posibie words given category

# Most positive words given year