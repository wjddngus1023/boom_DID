import asyncio
import json
import pprint

from indy import pool,ledger,wallet,did,anoncreds
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

import write_did_and_query_verkey as fn1
import rotate_key as fn2
import save_schema_and_cred_def as fn3
import negotiate_proof as fn4
import issue_credential as fn5
import send_secure_msg as fn6

from flask import Flask

pool_name = 'BoomLedgerPool'
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

@app.route("/writedid")
async def func1():
	a = await fn1.write_nym_and_query_verkey()
	print(a)
	return a

@app.route("/rotatekey")
async def func2():
	await fn2.rotate_key_on_the_ledger()
	return "<h1>rotate_key</h1>"

@app.route("/saveschema")
async def func3():
	await fn3.write_schema_and_cred_def()
	return "<h1>save schema</h1>"

@app.route("/negotiate")
async def func4():
	await fn4.proof_negotiation()
	return "<h1>negotiate<h1>"

@app.route("/issuecredential")
async def func5():
	await fn5.issue_credential()
	return "<h1>issue credential<h1>"

@app.route("/sendmessage")
def func6():
	return "<h1>send message<h1>"



host_addr = "127.0.0.1"
port_num = "8080"

if __name__ == "__main__":
	app.run(host=host_addr,port=port_num)


