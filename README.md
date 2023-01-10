## How to run

* python3 -m venv ./venv
* source ./venv/bin/activate
* pip install -r requirements.txt
* sudo chmod -x main.py
* sudo chmod -x start_script.sh
* create .env file based on .env.example
* sudo nohup /bin/sh ./start_script.sh &

## Important env values explained
* TOTAL_THREADS - number of total threads, which will used in python program
* START_DOCUMENT - order number of the first document, which will be retreived from MongoDB, cleaned and indexed in Elastic
* UPDATE_DOCUMENTS - total number of documents, which will be retrieved, cleaned and indexed in one run of main.py
