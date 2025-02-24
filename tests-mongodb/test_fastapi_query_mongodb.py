import json
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util

if " __name__ == '__main__'":
    if len(sys.argv) < 2:
        print("Usage: python test_fastapi_query_mongodb.py <collection>")
        sys.exit(1)
    collection = sys.argv[1].lower()
    print(f"Query MongoDB collection={collection}")
    # Connect to MongoDB (default host: localhost, port: 27017)
    client = MongoClient("mongodb://localhost:27017/")
    # Select (or create) a database
    db = client["mongo_rest_api"]
    # collection = db["mongo_ror_collection"]
    # Select (or create) a collection (equivalent to a table in SQL)
    collection = db[collection]
    print(f"Connected to MongoDB with collection {collection}!")
    # Count the number of documents in the collection
    count = collection.count_documents({})
    print(f"Total documents: {count}")
    # Query the collection
    # query = {"TestResult": test_result}
    # results = collection.find(query)
    # for result in results:
    #     print(result)
    # client.close() 
    # Query and filter if "TestResult" is eq to input result and output readable format
    results = collection.find()
    # filtered_results = [record for record in results if record.get("TestResult") == test_result]
    # print(f"Total Tests matching condation {test_result}: {len(filtered_results)}")
    print("----------------------------------------------------------")
    json_docs = [json.dumps(doc, default=json_util.default,indent=4) for doc in results]
    for json_doc in json_docs:
        print(json_doc)
    client.close()






















