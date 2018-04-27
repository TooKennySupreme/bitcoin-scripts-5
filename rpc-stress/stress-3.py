import smtplib
import requests
import time
import threading
import sys

# BITCOIN RPC CONFIGURATION
RPC_ADDRESS = "http://127.0.0.1:18332"
RPC_USER = "bitcoin"
RPC_PASSWORD = "password"

# SPAMMER THREADS
THREADS_COUNT = 300

# RPC FUNCTIONS
def send_curl(payload):
  headers = {'content-type': 'text/plain;'}
  return requests.post(RPC_ADDRESS, data=payload, headers=headers, auth=(RPC_USER, RPC_PASSWORD))

def get_info():
  payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
  return send_curl(payload)

def get_block_hash(height):
  payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [' + str(
      height) + '] }'
  return send_curl(payload)

def get_block(hash):
  payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["' + str(
      hash) + '"] }'
  return send_curl(payload)

# INIC FUNCTIONS
def inic_globals():
  global ERROR_1
  global ERROR_2
  global START_TIME
  ERROR_1 = 0
  ERROR_2 = 0
  START_TIME = time.time()

def request_all_blockchain(thread_number):
  #print ("Starting thread: " + str(thread_number) + ".")
  global ERROR_1
  global ERROR_2
  global START_TIME

  #start_time = time.time()
  i = 1
  
  while (i <= 5):
    try:
      block = get_block("000000005bce3341f5b21af5599cd40fbdd2b461ef2b9b5de72a912204868c78")
      if (block.status_code == requests.codes.ok):
        block = block.json()
        if (block['error'] == None):
          #print("Block: " + str(block['result']['height']) + ", on thread: " + str(thread_number))
          i=i+1
        else:
          ERROR_2 = ERROR_2 + 1
          print ERROR_2
      else:
        ERROR_2 = ERROR_2 + 1
        print ERROR_2
    except:
      #print "Unexpected error:", sys.exc_info()[0]
      ERROR_1 = ERROR_1 + 1
      time.sleep(1)

  total_time = time.time() - START_TIME

  print ('Thread ' + str(thread_number) + '. Time: ' + str(total_time) + '. Error_1:' + str(ERROR_1) + '.' + '. Error_2:' + str(ERROR_2) + ".")
  return 

# MAIN
if __name__ == '__main__':
  inic_globals()
  threads = list()
  for i in range(THREADS_COUNT):
    t = threading.Thread(target=request_all_blockchain, args=(i,))
    threads.append(t)
    t.start()
