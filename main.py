import os
import json
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor
import settings
import lxml.html

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def retrieve_documents(skip, limit):
    print('retrieving')
    local_mongo = MongoClient(settings.LOCAL_MONGO_CONN_STRING)
    local_db = local_mongo[settings.LOCAL_MONGO_DB]
    local_collection = local_db[settings.LOCAL_MONGO_COLLECTION]
    documents = list(local_collection.find().skip(skip).limit(limit))
    return documents


def process_documents(documents):
    print('processing articles')

    articles = []

    # iterate through each article form remote collection and perform indexing
    for article in documents:
        article_id = str(article['_id'])
        del article['_id']
        html = article.pop('html')
        title = article.pop('title')
        article.pop('link')

        doc = lxml.html.fromstring(title + ' ' + html)
        clean_text = doc.text_content()

        article['title_and_html'] = clean_text

        articles.append(
            { "index": { "_index": settings.ELASTIC_INDEX, "_id": article_id } }
        )
        articles.append(article)

    return articles


def index_articles(articles):
    print('indexing started.')

    local_es = Elasticsearch(hosts=settings.LOCAL_ELASTIC_CONNECTION_STRING, verify_certs=False, max_retries=10, retry_on_timeout=True)

    while not local_es.ping():
        print('Elastic still not up. Waiting 10 seconds...')
        time.sleep(10)

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

    local_es.bulk(index=settings.ELASTIC_INDEX, body=articles)


total_threads = settings.TOTAL_THREADS

local_mongo = MongoClient(settings.LOCAL_MONGO_CONN_STRING)
local_db = local_mongo[settings.LOCAL_MONGO_DB]
local_collection = local_db[settings.LOCAL_MONGO_COLLECTION]

document_count = local_collection.estimated_document_count()
batch_size = int(document_count / total_threads) + 1

with ThreadPoolExecutor(max_workers=total_threads) as executor:
    document_futures = []

    for batch_index in range(total_threads):
        skip = batch_index * batch_size
        limit = batch_size
        document_futures.append(executor.submit(retrieve_documents, skip, limit))

    articles_futures = []

    for future in document_futures:
        documents = future.result()

        articles_futures.append(executor.submit(process_documents, documents))

    for future in articles_futures:
        articles = future.result()
        index_articles(articles)
