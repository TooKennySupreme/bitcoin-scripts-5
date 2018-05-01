import smtplib
import requests
import time
import threading
import sys

# BITCOIN RPC CONFIGURATION
RPC_ADDRESS = "http://127.0.0.1:28332"
RPC_USER = "user"
RPC_PASSWORD = "pass"

# RAW DATA CONFIGURATION
rawdatafile="./rawdata.txt"

# RPC FUNCTIONS
def send_curl(payload):
  headers = {'content-type': 'text/plain;'}
  return requests.post(RPC_ADDRESS, data=payload, headers=headers, auth=(RPC_USER, RPC_PASSWORD))

def get_info():
  payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
  return send_curl(payload)

def send_tx(rawtx):
  payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "sendrawtransaction", "params": ["' + str(rawtx) + '"] }'
  return send_curl(payload)


# Read the file
with open(rawdatafile) as f:
    txns = f.readlines()
# Strip the lines
txns = [x.strip() for x in txns]


time0 = time.time()
# foreach tx in txns sendrawtransaction
result=[]
for tx in txns[:3] :
  result.append(send_tx(tx))

time1 = time.time() - time0

print(result)
print(time1)

