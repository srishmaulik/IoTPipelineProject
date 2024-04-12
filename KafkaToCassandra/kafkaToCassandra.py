from astrapy.rest import create_client, http_methods
import json
import uuid
import os
import time
from kafka import KafkaConsumer
import sys

if len(sys.argv) != 2:
    print("Usage: python3 kafkaToCassandra.py <PUBLIC IPV4 OF BROKER TO KAFKA>")
    sys.exit(1)

ASTRA_DB_ID = "bb4ffbd3-30a3-46f6-9c51-c59c943aa425"  
ASTRA_DB_REGION = "us-east-1"
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:nKXLJoKycTFzdLIyXDJzjWrx:e60b0ca440d563f3b7352304a3bc92c8fe6dcc73d66d52ea13fbb3a514c26172"
ASTRA_DB_KEYSPACE = "keyspace_name"
COLLECTION_NAME = "new_table"

astra_http_client = create_client(astra_database_id=ASTRA_DB_ID,
  astra_database_region=ASTRA_DB_REGION,
  astra_application_token=ASTRA_DB_APPLICATION_TOKEN)

consumer = KafkaConsumer(
    'TISENSORTAGDATA',                
    bootstrap_servers= sys.argv[1] + ':9092',  
    group_id="my group",           
    auto_offset_reset='latest',  
    value_deserializer=lambda x: json.dumps(x.decode('utf-8')))

def parse_string_to_dict(input_string):
    dictionary = {}
    
    input_string = input_string[2:-2]
    parts = input_string.split(', ')
    for part in parts:
        key, value = part.split(': ')
        key = key.replace('\\"', '')
        value = value.replace('\\"', '')
        dictionary[key] = value
    
    return dictionary

for message in consumer:
    input_string = message.value
    parsed_dict = parse_string_to_dict(input_string)
    response = astra_http_client.request(
        method=http_methods.POST,
        path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}",
        json_data = parsed_dict)
    print(response)
