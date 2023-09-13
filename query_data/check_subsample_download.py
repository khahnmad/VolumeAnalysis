import universal_functions as uf
import pandas as pd

def get_unique_articles_per_category(data:list,sentiment:bool)->list:
    if sentiment:
        columns= ['keyword', 'sentiment', 'article_id', 'partisanship', 'month', 'year']
    else:
        columns = ['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year','partisanship']

    df = pd.DataFrame(data=data[1:],columns=columns)
    df['article_id'] = df.apply(lambda x: x['article_id']["$oid"], axis=1)
    unique_ids = list(df['article_id'].unique())
    return unique_ids

def get_unique_articles(data:dict, sentiment:bool)->int:
    unique_articles = []
    for k in data.keys():
        cat_unique = get_unique_articles_per_category(data[k], sentiment)

        for v in cat_unique:
            if v not in unique_articles:
                unique_articles.append(v)
    return len(unique_articles)


fs, db = uf.getConnection(use_dotenv=True)

subsample_size = db['sampled_articles'].count_documents({"initial_subsample": True})

downloaded_subsample_keyword = uf.import_json('../initial_subsample/output/subsample_keyword_count.json')
downloaded_subsample_sentiment = uf.import_json('../initial_subsample/output/subsample_sentiment_count.json')

keyword_size = get_unique_articles(downloaded_subsample_keyword, sentiment=False)
sentiment_size = get_unique_articles(downloaded_subsample_sentiment, sentiment=True)

print(f"Keyword size is {keyword_size}, Missing {subsample_size-keyword_size}")
print(f"Sentiment size is {sentiment_size}, Missing {subsample_size-sentiment_size}")

"""
Last run: 9/11 11:37
keyword missing 136, sentiment missing 11041
"""