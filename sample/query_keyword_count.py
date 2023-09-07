import universal_functions as uf
from bson import ObjectId

# TODO: have it take as input the already reviewed data

def fetch_sample(db, prev_ids):
    c = list(db['sampled_articles'].find({"_id":{"$nin": prev_ids}}))
    # Should eventually be 248,724 documents
    print(f"Sample is short {248724-len(c)} documents, {(len(c)/248724)*100}% done")
    return c

def fetch_cw_data(db,ids):
    c = db['context_windows'].find({'article_id' : {"$in": ids}})
    return list(c)

def export_missing_elts(cw_data, ids):
    cw_ids = [x["article_id"] for x in cw_data]
    missing_ids = [x for x in ids if x not in cw_ids]
    uf.export_list('output/Sample_Missing_CW_article_ids.csv',missing_ids)

def get_num_unique_keywords(cw_data, category):
    if category in cw_data['context_windows'].keys():
        num = len(cw_data['context_windows'][category])
    else:
        num = 0
    return num

def get_num_keywords(cw_data, category):
    if category in cw_data['context_windows'].keys():
        num = sum([len(cw_data['context_windows'][category][kw]['spans']) for kw in cw_data['context_windows'][category].keys()])
    else:
        num =0
    return num

def sentiment_exists(cw_data):
    if len(cw_data['context_windows'])==0:
        return True
    for k in cw_data['context_windows'].keys():
        if 'sentiment' in  cw_data['context_windows'][k].keys():
            return True
    return False


def count_keyword_in_sample(db):
    sample_filename = 'output/sample_keyword_count.json'
    results = uf.import_json(sample_filename)
    prev_sample_ids = [ObjectId(x[0]['$oid']) for k in results.keys() for x in results[k][1:]]

    sample = fetch_sample(db, prev_sample_ids)
    sample_ids = [x['_id'] for x in sample]

    cw_data = fetch_cw_data(db, sample_ids)
    # export_missing_elts(cw_data, sample_ids)

    # results = {"Immigration": [['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']],
    #            "Islamophobia": [['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']],
    #            "Transphobia":[['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']],
    #            "Anti-semitism":[['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']]}
    missing_sentiment = []
    for i in range(len(cw_data)):
        cw_elt = cw_data[i]
        art_elt = [x for x in sample if x['_id']==cw_elt['article_id']][0]
        if sentiment_exists(cw_elt) is not True:
            missing_sentiment.append(cw_elt['_id'])

        for cate in results.keys():
            num_unique_kw = get_num_unique_keywords(cw_elt, cate)
            num_keywords = get_num_keywords(cw_elt, cate)

            month = art_elt['sample_id'].split('.')[1]
            year = "20"+art_elt['sample_id'].split('.')[0]
            part = art_elt['sample_id'].split('.')[2]
            outcome = [cw_elt['article_id'], num_unique_kw, num_keywords, month, year, part]
            results[cate].append(outcome)
        if str(i).endswith('00'):
            uf.export_as_json(sample_filename, results)
    uf.export_as_json(sample_filename, results)
    uf.export_list('output/Sample_Missing_sentiment_ids.csv',missing_sentiment)

fs, db = uf.getConnection(use_dotenv=True)
count_keyword_in_sample(db)
