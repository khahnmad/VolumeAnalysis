import universal_functions as uf
import time

fs, db = uf.getConnection(use_dotenv=True)

sample_ids_cursor = db['sampled_articles'].aggregate([{"$project": {"_id": 1}}])
sample_ids= [x['_id'] for x in list(sample_ids_cursor)]

cw_cursor = db['context_windows'].find({"article_id": {"$in": sample_ids}})
cw_content = list(cw_cursor)

a = time.time()
missing = []
for i in range(len(cw_content)):
    dv = False
    if 'context_windows' in cw_content[i]:
        for k in cw_content[i]['context_windows'].keys(): # Iterate through categories
            for j in cw_content[i]['context_windows'][k].keys(): # Iterate through keywords
                if 'sentiment' not in cw_content[i]['context_windows'][k][j].keys():
                    dv = True
    if dv==True:
        missing.append(cw_content[i]['article_id'])
b = time.time()

print(f"Took {(b-a)/60} minutes to run, found {len(missing)} missing")
uf.export_as_json('missing_sentiment_ids.json',{'content':missing,
                                                'metadata': time.time()})