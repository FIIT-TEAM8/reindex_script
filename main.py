import os
import json
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import html2text
import settings

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

local_mongo = MongoClient(settings.LOCAL_MONGO_CONN_STRING)
local_db = local_mongo[settings.LOCAL_MONGO_DB]
local_collection = local_db[settings.LOCAL_MONGO_COLLECTION]
local_es = Elasticsearch(hosts=settings.LOCAL_ELASTIC_CONNECTION_STRING, verify_certs=False, max_retries=10, retry_on_timeout=True)

# waiting for elastic
while not local_es.ping():
    print("Elastic still not up. Waiting 10 seconds...")
    time.sleep(10)

# retrieve articles from remote MongoDB for seeding local MongoDB container and indexing in local Elasticsearch container
cursor = local_collection.find({})
print('Articles was successfully retrieved from remote MongoDB.')

# create index if not exists
if not local_es.indices.exists(index=settings.ELASTIC_INDEX):
    # firstly load index configuration
    with open(os.getcwd() + '/' + "index_config.json") as articles_config_file:
        configuration = json.load(articles_config_file)
        # create index
        res = local_es.indices.create(index=settings.ELASTIC_INDEX, settings=configuration["settings"])
        # make sure index was created
        if not res['acknowledged']:
            print('Index wasn\'t created')
            print(res)
            exit(1)
        else:
            print('Index successfully created.')


print('Indexing in Elasticsearch...')

# iterate through each article form remote collection and perform indexing
for article in cursor:
    article_id = str(article['_id'])
    article.pop('_id', None)

    html = article.pop('html')
    title = article.pop('title')

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    clean_text = h.handle(title + ' ' + html)
    clean_text = clean_text.replace('\n', ' ')

    article['title_and_html'] = clean_text

    local_es.index(index=settings.ELASTIC_INDEX, id=article_id, document=json.dumps(article))

resp = local_es.search(index=settings.ELASTIC_INDEX, query={"match_all": {}})

print('Indexing finished.')
