import universal_functions as uf
from bson import ObjectId

def fetch_pub_times(article_ids):
    cursor = db['sampled_articles'].aggregate([{"$match": {"_id": { "$in":article_ids}}},
                                                {"$project": {'publish_date':1}}])
    return list(cursor)

fs,db = uf.getConnection(use_dotenv=True)

def get_pubtimes_for_subsample():
    data = uf.import_json('../initial_subsample/output/subsample_keyword_count.json')
    for k in data.keys():
        data[k] = uf.remove_duplicates(data[k])

        art_ids = [ObjectId(x[0]["$oid"]) for x in data[k][1:]]
        pub_times = fetch_pub_times(art_ids)
        for i in range(len(pub_times)):
            matching_item = [x for x in data[k][1:] if ObjectId(x[0]["$oid"]) == pub_times[i]['_id']][0]
            matching_item.append(pub_times[i]['publish_date'])

    uf.export_as_json('subsample_keyword_count_w_pubtime_no_duplicates.json',data)

def get_pubtimes_for_sample():
    data = uf.import_json('../sample/output/sample_keyword_count.json')
    for k in data.keys():
        data[k] = uf.remove_duplicates(data[k])

        art_ids = [ObjectId(x[0]["$oid"]) for x in data[k][1:]]
        pub_times = fetch_pub_times(art_ids)
        for i in range(len(pub_times)):
            matching_item = [x for x in data[k][1:] if ObjectId(x[0]["$oid"]) == pub_times[i]['_id']][0]
            matching_item.append(pub_times[i]['publish_date'])

    uf.export_as_json('sample_keyword_count_w_pubtime_no_duplicates.json', data)
    print('Export complete')

get_pubtimes_for_sample()