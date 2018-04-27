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
THREADS_COUNT = 1

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
  global LAST_HEIGHT
  info = get_info()
  if (info.status_code == requests.codes.ok):
      LAST_HEIGHT = get_block_hash(info.json()['result']['blocks'])
      return True
  return False

def request_all_blockchain(thread_number):
  print ("Starting thread: " + str(thread_number) + ".")
  global LAST_HEIGHT

  start_time = time.time()
  error_count = 0
  i = 1
  
  # while (i <= 100000):
  while (i <= LAST_HEIGHT):
    try:
      hash_data = get_block_hash(i)
      if (hash_data.status_code == requests.codes.ok):
        hash_data = hash_data.json()
        if (hash_data['error'] == None):
          #print("Requesting hash: " + str(hash_data['result']))
          block = get_block(hash_data['result'])
          if (block.status_code == requests.codes.ok):
            block = block.json()
            if (block['error'] == None):
              print("Block: " + str(i) + ", on thread: " + str(thread_number))
              i=i+1
            else:
              error_count = error_count + 1
          else:
            error_count = error_count + 1
        else:
          error_count = error_count + 1
      else:
        error_count = error_count + 1
    except:
      print "Unexpected error:", sys.exc_info()[0]
      time.sleep(2)
      
  total_time = time.time() - start_time

  print ('Thread ' + str(thread_number) + '. Time: ' + str(total_time) + '. Errors:' + str(error_count) + ".")
  return 

# MAIN
if __name__ == '__main__':
  if (inic_globals()):
    threads = list()
    for i in range(THREADS_COUNT):
      t = threading.Thread(target=request_all_blockchain, args=(i,))
      threads.append(t)
      t.start()