import requests
from pymongo import MongoClient
import arrow


client = MongoClient('localhost', 27017)
db = client.alexandria
otx_collection = db.otx_collection
OTX_API_KEY = "null"

def search_otx(data):
    url = "https://otx.alienvault.com/api/v1/indicators/{}/{}/general".format(data[0],data[1])
    print url
    headers = {
        'x-otx-api-key': OTX_API_KEY,
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)
    try:
        doc = response.json()
        doc['iss_retrieval'] = arrow.utcnow().format('X')
        return (doc)
    except Exception as e:
        print "{} call returned with {}".format(e,response.status_code)
        
        
def search_otx_collection(data):
    return otx_collection.find_one({"indicator":data[1]})

def search_elastic():
    pass

def put_doc(doc):
    otx_collection.update( {'indicator': doc['indicator'] }, doc, upsert=True)
 

data = ("IPv4", "1.1.1.1")
result = search_otx_collection(data) 
if result:
    print "{} {} found in database since {}".format(data[1], data[0], arrow.get(result['iss_retrieval']).humanize())
else:
    print "Search OTX"
    put_doc(search_otx(data))



