from flask import Flask, render_template, jsonify, redirect, url_for, request
from astrapy.rest import create_client, http_methods
from threading import Thread
import threading
import time
import uuid
import os
import subprocess

ASTRA_DB_ID = "bb4ffbd3-30a3-46f6-9c51-c59c943aa425"  
ASTRA_DB_REGION = "us-east-1"
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:nKXLJoKycTFzdLIyXDJzjWrx:e60b0ca440d563f3b7352304a3bc92c8fe6dcc73d66d52ea13fbb3a514c26172"
ASTRA_DB_KEYSPACE = "keyspace_name"
COLLECTION_NAME = "new_table"


app = Flask(__name__)

responseDict = {}

def poll_cassandra():
    global responseDict
    while True:
        response = astra_http_client.request(
            method=http_methods.GET,
            path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}/rows")
        responseDict = response.get("data")
        time.sleep(5)  

# sensor_processes = []

# def run_virtual_sensor():
#     try:
#         process = subprocess.Popen(['python', 'simulator.py'])
#         print('Virtual sensor started successfully')

#         sensor_processes.append(process)
#     except Exception as e:
#         print(f'Error starting virtual sensor: {str(e)}')

@app.route('/')
def index():
    return render_template('index.html', response=responseDict)

# @app.route('/add_sensor', methods=['POST'])
# def add_sensor():
#     sensor_thread = threading.Thread(target=run_virtual_sensor)
#     sensor_thread.start()
#     return redirect(url_for('index'))

@app.route('/remove_sensor', methods=['POST'])
def remove_sensor():
    global responseDict
    sensor_id = request.form.get('sensor_id')

    if not sensor_id:
        return "Sensor ID is required", 400
    try:
        astra_http_client.request(
            method=http_methods.DELETE,
            path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}/{sensor_id}")
        
        response = astra_http_client.request(
            method=http_methods.GET,
            path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}/rows")
        
        responseDict = response.get("data")
        return redirect(url_for('index'))
    except Exception as e:
        print("Failed to remove sensor: " + str(e))
        return f"Failed to remove sensor: {str(e)}", 500

@app.route('/remove_all', methods=['POST'])
def remove_all():
    global responseDict
    #print("test")
    try:
        copyDict = responseDict.copy()
        for x in copyDict:
            print("Removing:", x["system_id"])
            astra_http_client.request(
                method=http_methods.DELETE,
                path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}/{x['system_id']}")

        # astra_http_client.request(
        #     method=http_methods.DELETE,
        #     path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}/rows")
        
        response = astra_http_client.request(
            method=http_methods.GET,
            path=f"/api/rest/v2/keyspaces/{ASTRA_DB_KEYSPACE}/{COLLECTION_NAME}/rows")
        
        responseDict = response.get("data")
        return redirect(url_for('index'))
    except Exception as e:
        print("Failed to remove all sensors: " + str(e))
        return f"Failed to remove all sensor: {str(e)}", 500

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(responseDict)

if __name__ == '__main__':
    astra_http_client = create_client(astra_database_id=ASTRA_DB_ID,
      astra_database_region=ASTRA_DB_REGION,
      astra_application_token=ASTRA_DB_APPLICATION_TOKEN)
    
 
    poll_thread = Thread(target=poll_cassandra)
    poll_thread.daemon = True 
    poll_thread.start()

    app.run()
