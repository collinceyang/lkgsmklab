import json
import time
import sys
import requests
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util

# this utility is to query test case Pass/Fail
if " __name__ == '__main__'":
    if len(sys.argv) < 3:
        print("Usage: python util_fastapi_query_mongodb.py <collection> <result>")
        sys.exit(1)
    collection = sys.argv[1].lower()
    test_result = sys.argv[2].lower()
    test_result = test_result.lower() == "true"
    print(f"Query MongoDB collection={collection} for TestStatus={test_result}")

    # Connect to MongoDB (default host: localhost, port: 27017)
    client = MongoClient("mongodb://localhost:27017/")
    # Select (or create) a database
    db = client["mongo_rest_api"]
    # Select (or create) a collection (equivalent to a table in SQL)
    collection = db[collection]
    print("Connected to MongoDB!")
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
    filtered_results = [record for record in results if record.get("TestResult") == test_result]
    print(f"Total Tests matching condation {test_result}: {len(filtered_results)}")
    print("----------------------------------------------------------")
    json_docs = [json.dumps(doc, default=json_util.default,indent=4) for doc in filtered_results]
    for json_doc in json_docs:
        print(json_doc)
    client.close()






















