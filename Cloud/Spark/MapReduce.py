from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import requests
import json
import numpy
from time import perf_counter
# import couchdb


# try:#172.16.2.208
#     # Connect to CouchDB using the provided credentials and URL
#     couch = couchdb.Server('http://admin:admin@172.16.2.187:30005/')
    
#     # Check if the 'img_db' database exists, if not, create it
#     if 'img_db' not in couch:
#         db = couch.create('img_db')
#     else:
#         db = couch['img_db']
#     print("Connected to CouchDB successfully.")
# except Exception as e:
#     # Handle CouchDB connection error
#     print(f"Failed to connect to CouchDB: {e}")

# all_docs = db.view('_all_docs', include_docs=True)

# def map1(chunk):
#     ichunk={}
#     if chunk['GroundTruth']!=chunk['InferredValue']:
#         ichunk['producer_id']=1
#     else : 
#         ichunk['producer_id']=0
#     # for doc_id in chunk:
#     #     gt=chunk[doc_id]['GroundTruth']
#     #     iv=chunk[doc_id]['InferredValue']
#     #     pid=chunk[doc_id]['producer_id']
#     #     ichunks[pid].append({'id':doc_id,'GroundTruth':gt,'InferredValue':iv})
#     return ichunk

# def reduce1(a,b):
#     return set(a,b)
    

# def map2(chunk,n):
#     ichunk=[0 for i in range(n)]

    

# def reduce(chunk):
#     ichunks={}
#     for l in chunk:
#         ichunks[l]=0
#         for i in chunk[l]:
#             if i['GroundTruth']!=i['InferredValue']:
#                 ichunks[l]=ichunks[l]+1
#             # else : 
#             #     ichunks[l].append({i['GroundTruth']:0})
#     return ichunks.values()
#         # GroundTruth=chunk[doc_id]['GroundTruth']
#         # InferredValue=chunk[doc_id]['InferredValue']
#         # if GroundTruth==InferredValue:
#         #     if GroundTruth in ichunks:
#         #         ichunks[GroundTruth]=ichunks[GroundTruth]+1
#         #     else :
#         #         ichunks[GroundTruth]=1

# # def reduce(ichunks):
# #     result=0
# #     fin_result=[]
# #     for pid in ichunks:
# #         fin_result[pid]=0
# #         for i in ichunks[pid]:
# #             fin_result[pid]=fin_result[pid]+i.
# #     return result

# spark = SparkSession \
#                 .builder \
#                 .appName("MapReduce") \
#                 .config('spark.default.parallelism', t[0]) \
#                 .config('spark.sql.shuffle.partitions', t[1]) \
#                 .getOrCreate()

# docs_rdd=spark.sparkContext.parallelize(all_docs)

if __name__ == "__main__":
    rowsToRetrieve = 1000000
    getChunkSize = 200000
    putChunkSize = 2
    MRTuples = [[10, 2], [50, 5], [100, 10]]
    iterations = 1 # In order to save time for demo, we only do all the 3 sets of MR for one time
    #iterations = 10
    print('Retrieving data from CouchDB in chunks of', getChunkSize) # Get data from CouchDB, around 4 mins
    skip = 0
    limit = getChunkSize + 1
    count = 0
    data = []
    retrievestart = perf_counter()
    while skip < rowsToRetrieve:
        start = perf_counter()
        raw = requests.get(
            f'http://admin:admin@172.16.2.187:30005/img_db/_all_docs?include_docs=true&skip={skip}&limit={limit}')
        end = perf_counter()
        count += 1
        print('Chunk', count, 'Time', end - start, 's')
        tempdata = json.loads(raw.content.decode('UTF8').replace('\r', '').replace('\n', ''))['rows']
        data.extend([r['doc'] for r in tempdata])
        skip += getChunkSize
    retrieveend = perf_counter()
    print('All data retrieved in', retrieveend - retrievestart, 's')
    results = [] # MapReduce, each sets execute an average of 1.3 mins
    for t in MRTuples:
        print('Iterations =', iterations, 'M =', t[0], 'R =', t[1])
        iters = 1
        while iters <= iterations:
            spark = SparkSession \
                .builder \
                .appName("MapReduce") \
                .config('spark.default.parallelism', t[0]) \
                .config('spark.sql.shuffle.partitions', t[1]) \
                .getOrCreate()
            print('Create Spark DataFrame')
            df = spark.createDataFrame(data)
            print('Complete')
            start = perf_counter()
            reduced = df.groupby(['house_id', 'household_id', 'plug_id']).agg(
                f.avg(f.when(df.property == 0, df.value)).alias('work'),
                f.avg(f.when(df.property == 1, df.value)).alias('load')).collect()
            end = perf_counter()
            net = end - start
            results.append([t[0], t[1], iters, net])
            iters += 1
            spark.stop()
    print('Save reduced results back to CouchDB') # Send result back to CouchDB, really fast
    reduced = [r.asDict() for r in reduced]
    chunked_list = numpy.array_split(reduced, putChunkSize)
    url = f'http://admin:123456@129.114.25.15:30005/reduced/_bulk_docs'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    count = 1
    for chunk in chunked_list:
        docs = json.dumps({'docs': chunk.tolist()})
        print('Sending chunk:', count)
        res = requests.post(url, headers=headers, data=docs)
        count += 1
    print('Final results:') # Show the final result of operating time
    for result in results:
        print(f'M: {result[0]} R: {result[1]} I: {result[2]} Time: {result[3]}')
