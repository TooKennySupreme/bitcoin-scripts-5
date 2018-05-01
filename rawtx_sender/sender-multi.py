import smtplib
import requests
import time
import threading
import sys
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# RAW DATA CONFIGURATION
rawdatafile="./rawdata.txt"
# Read the file
with open(rawdatafile) as f:
    txns = f.readlines()
# Strip the lines
txns = [x.strip() for x in txns]


rpc_user="user"
rpc_password="pass"
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:28332"%(rpc_user, rpc_password))


# foreach tx in txns sendrawtransaction
commands = [ [ "sendrawtransaction", tx] for tx in txns ]

time0 = time.time()
result = rpc_connection.batch_(commands)
time1 = time.time() - time0

for res in result:
    print (str(res))

print (time1)