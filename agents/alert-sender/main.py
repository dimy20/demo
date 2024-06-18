#! venv/bin/python3

import requests
import json
import time

import splunklib.client as client
import splunklib.results as results

HOSTNAME = "vigilant-ai-api"
ENDPOINT = f"http://{HOSTNAME}:80/api/alert"
ALERT_FILENAME = "fake_alert.txt"

# Splunk configuration
SPLUNK_HOST = "127.0.0.1"
SPLUNK_PORT = 8089
SPLUNK_USERNAME = 'admin'
SPLUNK_PASSWORD = "D1myCs89?02"
SPLUNK_APP = 'search'


from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook")
async def receive_alert(request: Request):
    alert_data = await request.json()
    print("Received alert:")
    print(json.dumps(alert_data, indent=4))
    # Process the alert here (e.g., log it, take an action, etc.)
    return {"message": "Alert received"}

#def search_splunk(query):
#    job = service.jobs.create(query)
#    while not job.is_ready():
#        time.sleep(1)
#
#    # Wait for the job to complete
#    while not job['isDone'] == '1':
#        time.sleep(2)
#
#    # Get results
#    result_stream = job.results(output_mode='json')
#    return results.JSONResultsReader(result_stream)
#
#
#if __name__ == '__main__':
#    service = client.connect(
#        host=SPLUNK_HOST,
#        port=SPLUNK_PORT,
#        username=SPLUNK_USERNAME,
#        password=SPLUNK_PASSWORD,
#        app=SPLUNK_APP
#    )
#    query = 'search index=fake_brute_force sourcetype="fake_brute_force" | stats count by ip, username | where count > 3'
#
#    while True:
#        print('Checking for new alerts...')
#        alerts = search_splunk(query)
#        a = [alert for alert in alerts][0]
#        print(a)
#        #print(type(alerts))
#        #print(f"Alert: \n{alerts[0]}")
#
#        #for alert in alerts:
#        #    print(alert)
#        #    # Process the alert here (e.g., log it, take an action, etc.)
#
#        # Wait for a while before checking again
#        time.sleep(60)
#

#def send_fake_alert():
#    with open(ALERT_FILENAME, "r") as f:
#        content = f.read()
#
#    time.sleep(5)
#
#    print("sending fake alert...")
#
#    res = requests.post(
#        ENDPOINT,
#        headers={"Content-Type" : "application/json"},
#        data=json.dumps({
#                "content" : json.dumps(content),
#                "user" : "enzowstm@gmail.com",
#        })
#    )
#
#    if res.status_code == 200:
#        print(json.loads(res.content))
#    else:
#        print(f"Error {res.status_code}")
