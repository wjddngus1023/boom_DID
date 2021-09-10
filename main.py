import asyncio
import json
import pprint

from indy import pool,ledger,wallet,did,anoncreds
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

import createledger as create_ledger
import writedid as write_did
import nymdid as nym_did

from flask import Flask

pool_name = 'boonDID_pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})

def print_log(value_color="", value_noncolor=""):
	HEADER = '\033[92m'
	ENDC = '\033[0m'
	print(HEADER + value_color + ENDC + str(value_noncolor))

app = Flask(__name__)

@app.route("/")
async def main():
	return "<h1>Hello world!</h1>"

@app.route("/createledger")
async def create_Ledger():
	await create_ledger.createledger()
	return "<h1>Create Ledger!</h1>"

@app.route("/writedid")
async def write_DID():
	a = await write_did.writedid()
	print(a)
	return a
@app.route("/nymdid")
async def nym_DID():
    b = await nym_did.nymdid()
    print(b)
    return b
host_addr = "127.0.0.1"
port_num = "8080"

if __name__ == "__main__":
	app.run(host=host_addr,port=port_num)


