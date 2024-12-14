from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import requests
import json
import numpy
from time import perf_counter

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
            f'http://admin:123456@129.114.25.15:30005/cloudpa4/_all_docs?include_docs=true&skip={skip}&limit={limit}')
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
