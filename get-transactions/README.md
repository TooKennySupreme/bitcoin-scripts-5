# Get the transactions from the last N blocks

# Requirements:

* Python
* bitcoinrpc `pip install bitcoinrpc`
* sqlite3 `pip install sqlite3`
* A bitcoin node with rpc support

# To run the script:

Configurate your rpc credentials, ip:port and blocks to be requested to the bitcoin node (`blockcount`)

```
python script.py
```
A txns.db will be created with the hash, size, output count and input count of each transaction.

# Request data

## Requirements
* SQLite3 (`apt-get install sqlite3`)

## Sqlite:
```
sqlite3 txns.db
select count (*) as TX_COUNT, avg(inputs) as INPUTSxTXN, (1.0*sum(inputs)/sum(size)) as INPUTSxSIZE, avg(outputs) as OUTPUTSxTXN, (1.0*sum(outputs)/sum(size)) as OUTPUTSxSIZE, avg(size) as AVG_TX_SIZE, sum(size) as TOTAL_SIZE from txns;
```

## Result:
```
305899|2.51470583427863|0.00494204837531459|2.80540962866829|0.00551335663538123|508.83877358213|155653272
```