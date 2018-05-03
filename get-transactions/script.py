# bitcoin-scripts
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import sys
import sqlite3

# Configuration
rpc_user="bitcoin"
rpc_password="password"
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:19332"%(rpc_user, rpc_password))
blockcount=2000
conn = sqlite3.connect('txns.db')

# Database
c = conn.cursor()
c.execute ("DROP TABLE IF EXISTS TXNS;")
c.execute ("CREATE TABLE TXNS(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, HASH TEXT NOT NULL, SIZE INTEGER NOT NULL, OUTPUTS INTEGER NOT NULL, INPUTS INTEGER NOT NULL);")

best_block_hash = rpc_connection.getbestblockhash()
info = rpc_connection.getinfo()
chainheight= int(info["blocks"])
counter=chainheight-blockcount
print "Chain Height:",chainheight
print "Start Height:",counter
while (counter < chainheight):
    blockrange = range(counter,counter+1000)
    commands = [ [ "getblockhash", int(height)] for height in blockrange ]
    block_hashes = rpc_connection.batch_(commands)
    blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
    for block in blocks:
        txns = rpc_connection.batch_([ [ "getrawtransaction", tx, 1 ] for tx in block["tx"] ])
        for rawtx in txns:
                c.execute("INSERT INTO TXNS (HASH, SIZE, OUTPUTS, INPUTS) VALUES (\"" +str(rawtx["txid"]) + "\", " + str(rawtx["size"]) + "," + str(len(rawtx["vout"]))+ ","+ str(len(rawtx["vin"]))+");")
                print "Txn inserted",str(rawtx["txid"])
    if ((counter + 1000) > chainheight):
        counter = counter + (chainheight - counter)
    else:
        counter=counter+1000
    conn.commit()


conn.close()