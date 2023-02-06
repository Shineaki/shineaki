import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', '[YOUR ENDPOINT]'),
    'master_key': os.environ.get('ACCOUNT_KEY', '[YOUR KEY]'),
    'database_id': os.environ.get('COSMOS_DATABASE', '[YOUR DATABASE]'),
    'container_id': os.environ.get('COSMOS_CONTAINER', '[YOUR CONTAINER]'),
    'tenant_id': os.environ.get('TENANT_ID', '[YOUR TENANT ID]'),
    'client_id': os.environ.get('CLIENT_ID', '[YOUR CLIENT ID]'),
    'client_secret': os.environ.get('CLIENT_SECRET', '[YOUR CLIENT SECRET]'),
}

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

HOST = settings['host']
MASTER_KEY = settings['master_key']
DATABASE_ID = settings['database_id']
CONTAINER_ID = settings['container_id']

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
db = client.create_database_if_not_exists(id=DATABASE_ID)
container = db.create_container_if_not_exists(id=CONTAINER_ID, partition_key=PartitionKey(path='/id', kind='Hash'))
tst = list(container.read_all_items())
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME",tst[0]["id"])
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)