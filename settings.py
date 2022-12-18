import os
from dotenv import load_dotenv, find_dotenv

if os.path.exists('.env'):
    load_dotenv(find_dotenv())

TOTAL_THREADS = int(os.getenv('TOTAL_THREADS') or 12)

LOCAL_MONGO_HOST = str(os.getenv('LOCAL_MONGO_HOST') or 'localhost')
LOCAL_MONGO_PORT = int(os.getenv('LOCAL_MONGO_PORT') or 27017)
LOCAL_MONGO_USER = str(os.getenv('LOCAL_MONGO_USER') or 'root')
LOCAL_MONGO_PASSWORD = str(os.getenv('LOCAL_MONGO_PASSWORD') or 'password')
LOCAL_MONGO_DB = str(os.getenv('LOCAL_MONGO_DB') or 'ams')
LOCAL_MONGO_COLLECTION = str(os.getenv('LOCAL_MONGO_COLLECTION') or 'articles')
LOCAL_MONGO_CONN_STRING = "mongodb://{user}:{password}@{server_url}:{port}/".format(user=LOCAL_MONGO_USER, 
                                                                        password=LOCAL_MONGO_PASSWORD, 
                                                                        server_url=LOCAL_MONGO_HOST, 
                                                                        port=LOCAL_MONGO_PORT)

LOCAL_ELASTIC_HOST = str(os.getenv('ELASTIC_HOST') or 'localhost')
LOCAL_ELASTIC_PORT = int(os.getenv('ELASTIC_PORT') or 9200)
LOCAL_ELASTIC_USER = str(os.getenv('ELASTIC_USER') or 'root')
LOCAL_ELASTIC_PASSWORD = str(os.getenv('ELASTIC_PASSWORD') or 'password')
ELASTIC_INDEX = str(os.getenv('ELASTIC_INDEX') or 'articles_index_reindex')
LOCAL_ELASTIC_CONNECTION_STRING = '{protocol}://{username}:{password}@{host}:{port}/'.format(
    protocol="https",
    username=LOCAL_ELASTIC_USER,
    password=LOCAL_ELASTIC_PASSWORD,
    host=LOCAL_ELASTIC_HOST,
    port=LOCAL_ELASTIC_PORT
)