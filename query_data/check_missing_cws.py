import universal_functions as uf
import time

fs, db = uf.getConnection(use_dotenv=True)

sample_ids_cursor = db['sampled_articles'].aggregate([{"$project": {"_id": 1}}])
sample_ids= [x['_id'] for x in list(sample_ids_cursor)]

cw_ids_cursor = db['context_windows'].aggregate([{"$match":{"article_id":{"$in":sample_ids}}},{"$project": {"article_id": 1}}])
cw_ids = [x['article_id'] for x in list(cw_ids_cursor)]

missing = []
for i in range(len(sample_ids)): # exported at 140365
    if sample_ids[i] not in cw_ids:
        missing.append(sample_ids[i])

uf.export_as_json('missing_context_windows.json',{'content': missing,
                                                  'metadata': time.time()})
