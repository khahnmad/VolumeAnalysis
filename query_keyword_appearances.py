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

def fetch_cw_data(db, category:str)->dict:
    cw_query = {f'context_windows.{category}': {'$exists': True}}
    cursor = db['context_windows'].find(cw_query)
    cw_data = {}
    for elt in cursor:
        cw_data[elt['article_id']] = {'num_unique_kw_per_art':len(elt['context_windows'][category]),
                                          'num_keywords' : sum([len( elt['context_windows'][category][x]['windows']) for x in elt['context_windows'][category]])}
    return cw_data


def get_time_frame(yr, month) -> tuple:
    start_date = datetime.datetime(year=yr, month=month, day=1)
    if month == 12:
        end_date = datetime.datetime(year=yr, month=1, day=1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.datetime(year=yr, month=month + 1, day=1) - datetime.timedelta(days=1)
    return str(start_date), str(end_date)

def fetch_article_data(article):
    _id = article['_id']
    collection = article['imported_from'].split('_')[0]
    return _id, collection

fs,db = getConnection(use_dotenv=True)

categories = ['Immigration','Islamophobia','Transphobia','Anti-semitism']
collection_conversion = {'HL':'FarLeft',
                         'FR':'FarRight',
                         'CE19':'Center',
                         'CL19': 'CenterLeft',
                         "RR19": 'Right',
                         'CR19': 'CenterRight',
                         'CO':'FarRight','LL19':'Left','HR':'FarRight'}
for c in categories:
    cat_results = [['article_id','num_unique_kw_per_art','num_keywords','month','year','collection','partisanship']]

    a = time.time()

    article_ids = fetch_cw_data(db, c)

    for y in range(2016,2023):
        print(f"Year: {y}")
        for m in range(1,13):
            print(f'    Month: {m}')

            start,end = get_time_frame(y, m)

            articles_query = {"$and": [{'_id': {'$in': list(article_ids.keys()) }},{'publish_date': {"$gte": str(start)}}, {'publish_date': {
                "$lt": str(end)}}]}

            art_cursor = db['articles'].find(articles_query)

            articles = list(art_cursor)

            for a in articles:
                art_id, collection = fetch_article_data(a)
                num_unique_kw_per_art = article_ids[art_id]['num_unique_kw_per_art']
                num_keywords =  article_ids[art_id]['num_keywords']
                cat_results.append([art_id,num_unique_kw_per_art, num_keywords, m,y,collection,collection_conversion[collection]])

    uf.export_nested_list(f"{c}_Keyword_Count.csv",cat_results)