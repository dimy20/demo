#! venv/bin/python3

import time
import splunklib.client as client
import splunklib.results as results
from datetime import datetime

# Splunk configuration
SPLUNK_HOST = 'localhost'
SPLUNK_PORT = 8089
SPLUNK_USERNAME = 'admin'
SPLUNK_PASSWORD = 'D1myCs89?02'
SPLUNK_INDEX = 'fake_log'
SPLUNK_SOURCE = 'fake_log'

# Connect to Splunk
service = client.connect(
    host=SPLUNK_HOST,
    port=SPLUNK_PORT,
    username=SPLUNK_USERNAME,
    password=SPLUNK_PASSWORD
)

def generate_log_entry():
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    log_entry = f'{timestamp},host1,authentication,failed,username=user1,ip=192.168.1.10\n'
    return log_entry

def send_log_entry():
    index = service.indexes[SPLUNK_INDEX]
    log_entry = generate_log_entry()
    index.submit(log_entry, sourcetype=SPLUNK_SOURCE)

if __name__ == "__main__":
    #while True:
    send_log_entry()
    print("Sent alert!")
    #time.sleep(10)  # Adjust the frequency as needed
