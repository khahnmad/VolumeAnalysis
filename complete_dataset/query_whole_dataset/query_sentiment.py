# Find keyword frequency by category, month, year, partisanship
import datetime
from bson import ObjectId
import gridfs
from dotenv import load_dotenv
import os
import pymongo as pm
import time
import universal_functions as uf


def getConnection(
    connection_string: str = "", database_name: str = "", use_dotenv: bool = False
):
    "Returns MongoDB and GridFS connection"

    # Load config from config file
    if use_dotenv:
        load_dotenv()
        connection_string = os.getenv("CONNECTION_STRING")
        database_name = os.getenv("DATABASE_NAME")

    # Use connection string
    conn = pm.MongoClient(connection_string)
    db = conn[database_name]
    fs = gridfs.GridFS(db)

    return fs, db

def fetch_cw_data(db, category:str,last_logged_date)->dict:
    dt = datetime.datetime.fromtimestamp(last_logged_date)+datetime.timedelta(hours=2)
    cw_query = {"$and": [{f'uploadDate': {'$lte': dt}}, {f"context_windows.{category}": {"$exists": True}}]}
    cursor = db['context_windows'].find(cw_query)
    cw_data = {}
    for elt in cursor:
        outcome = {key: elt['context_windows'][category][key]['sentiment'] for key in elt['context_windows'][category] if 'sentiment' in  elt['context_windows'][category][key].keys()}
        if outcome != {}:
            cw_data[elt['article_id']] = outcome
    return cw_data


def get_time_frame(yr, month) -> tuple:
    start_date = datetime.datetime(year=yr, month=month, day=1)
    if month == 12:
        end_date = datetime.datetime(year=yr+1, month=1, day=1) - datetime.timedelta(seconds=1)
    else:
        end_date = datetime.datetime(year=yr, month=month + 1, day=1) - datetime.timedelta(seconds=1)
    return start_date, end_date

def fetch_article_data(article):
    _id = article['_id']
    collection = article['imported_from'].split('_')[0]
    return _id, collection


def reformat_elt(collection, cw_elt):
    collection_conversion = {'HL': 'FarLeft',
                             'FR': 'FarRight',
                             'CE19': 'Center',
                             'CL19': 'CenterLeft',
                             "RR19": 'Right',
                             'CR19': 'CenterRight',
                             'CO': 'FarRight', 'LL19': 'Left', 'HR': 'FarRight'}
    new_elt = {'collection': collection,
               'partisanship': collection_conversion[collection],
               'keywords': cw_elt}

    return new_elt

fs,db = getConnection(use_dotenv=True)

categories = ['Immigration','Islamophobia','Transphobia','Anti-semitism']


for c in categories:
    cat_results = {}

    a = time.time()

    article_ids = fetch_cw_data(db, c,1692631159.101)

    for y in range(2016,2023):
        print(f"Year: {y}")
        for m in range(1,13):
            print(f'    Month: {m}')

            start,end = get_time_frame(y, m)

            articles_query = {"$and": [{'_id': {'$in': list(article_ids.keys()) }},{'publish_date': {"$gte": start}}, {'publish_date': {
                "$lte":end}}]}

            art_cursor = db['articles'].find(articles_query)

            articles = list(art_cursor)
            if len(articles) <10:
                print('Something may be wrong with the query')

            for a in articles:
                art_id, collection = fetch_article_data(a)
                article_ids[str(art_id)] = reformat_elt( collection, article_ids[art_id])
    not_updated = [x for x in article_ids if 'collection' not in article_ids[x].keys()]
    uf.export_as_json(f"{c}_Sentiment.json",article_ids)