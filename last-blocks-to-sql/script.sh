
#PRECONDITIONS: PYTHON AND SQLITE3 INSTALLED

#NODE PARAMS
#user:pass
user="bitcoin:password"
#ip:port
ip="127.0.0.1:8332"

#BLOCKS UNDER THE LASTBLOCK TO SAVE
firstblock=1174943


########RPC FUNCTIONS########
function getinfo {
#$1 = height
curl --user $user --data-binary "{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"getinfo\", \"params\": [] }" -H 'content-type: application/json;' http://$ip/
}

function getblockhash {
#$1 = height
curl --user $user --data-binary "{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"getblockhash\", \"params\": [$1] }" -H 'content-type: application/json;' http://$ip/
}

function getblock {
#$1 = hash
curl --user $user --data-binary "{\"jsonrpc\": \"1.0\", \"id\":\"curltest\", \"method\": \"getblock\", \"params\": [\"$1\"] }" -H 'content-type: application/json;' http://$ip/
}

function get-getblockhash {
#$1 = height
getblockhash "$1" | \
python -c "import json,sys;
obj=json.load(sys.stdin);
obj=obj['result']
print (obj)
"
}

function get-getinfo {
getinfo | \
python -c "import json,sys;
obj=json.load(sys.stdin);
obj=obj['result']
print (obj['blocks'])
"
}

######DATABASE FUNCTIONS#####

function drop-table {
sqlite3 bitprim.db "DROP TABLE IF EXISTS BLOCKS;"
}

function create-table-blocks-bitcoind {
sqlite3 bitprim.db "CREATE TABLE BLOCKS(
  ID            INTEGER PRIMARY KEY    AUTOINCREMENT NOT NULL,
  HASH          TEXT    NOT NULL,
  HEIGHT        TEXT    NOT NULL,
  TIME          TIMESTAMP    NOT NULL,
  MEDIANTIME    TIMESTAMP    NOT NULL,
  BITS          TEXT    NOT NULL,
  DIFFICULTY    TEXT    NOT NULL,
  CHAINWORK     TEXT    NOT NULL
);"
}

function populate-getblock {
#$1 = hash
getblock "$1" | \
python -c "import json,sys,sqlite3;
obj=json.load(sys.stdin);
obj=obj['result']
conn = sqlite3.connect('bitprim.db')
c = conn.cursor()
hash=obj['hash']
height=obj['height']
time=obj['time']
mediantime=obj['mediantime']
bits=obj['bits']
difficulty=obj['difficulty']
chainwork=obj['chainwork']
c.execute('INSERT INTO BLOCKS (HASH,HEIGHT,TIME,MEDIANTIME,BITS,DIFFICULTY,CHAINWORK) VALUES (?,?,?,?,?,?,?)',(hash,height,time,mediantime,bits,difficulty,chainwork))
conn.commit()
conn.close()
"
}

####MAIN PROGRAM
$(drop-table)
$(create-table-blocks-bitcoind)

lastheight=$(get-getinfo)

for (( i=$firstblock; i < $lastheight; ++i )) do
    hash=$(get-getblockhash $i)
    $(populate-getblock $hash)
done
