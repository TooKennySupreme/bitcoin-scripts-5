from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import sys
rpc_user="bitcoin"
rpc_password="password"
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(rpc_user, rpc_password))
best_block_hash = rpc_connection.getbestblockhash()
counter=0
#ifile = open("missing", "r")
#lines = ifile.read().splitlines()
info = rpc_connection.getinfo()
#chainheight= int(info["blocks"])
chainheight= 100000
print "Chain Height:",chainheight
while (counter < chainheight):
 linerange = range(counter,counter+10000)
 commands = [ [ "getblockhash", int(height)] for height in linerange ]
 block_hashes = rpc_connection.batch_(commands)
 blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
 for block in blocks:
   #a = 1
   print str(block["height"]) + "," + "\"" + str(block["hash"]) + "\"" + "," + str(block["time"]) + "," + str(float(block["difficulty"])) + "," + str(block["size"]) + "," + str(len(block["tx"]))
 if ((counter + 10000) > chainheight):
   #print "before",counter
   counter = counter + (chainheight - counter)
 else:
   counter=counter+10000
