import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'boomDID_pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))


async def nymdid():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        # 2.
        print_log('\n2. Open pool ledger and get handle from libindy\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)

        print_log('\n4. Open wallet and get handle from libindy\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        # 9.
        print_log('\n9. Generating and storing DID and verkey representing a Client '
                  'that wants to obtain Trust Anchor Verkey\n')
        client_did, client_verkey = await did.create_and_store_my_did(wallet_handle, "{}")
        print_log('Client DID: ', client_did)
        print_log('Client Verkey: ', client_verkey)

        # 10.
        print_log('\n10. Building the GET_NYM request to query trust anchor verkey\n')
        get_nym_request = await ledger.build_get_nym_request(submitter_did=client_did,
                                                             target_did=trust_anchor_did)
        print_log('GET_NYM request: ')
        pprint.pprint(json.loads(get_nym_request))

        # 11.
        print_log('\n11. Sending the Get NYM request to the ledger\n')
        get_nym_response_json = await ledger.submit_request(pool_handle=pool_handle,
                                                           request_json=get_nym_request)
        get_nym_response = json.loads(get_nym_response_json)
        print_log('GET_NYM response: ')
        pprint.pprint(get_nym_response)

        # 12.
        print_log('\n12. Comparing Trust Anchor verkey as written by Steward and as retrieved in GET_NYM '
                  'response submitted by Client\n')
        print_log('Written by Steward: ', trust_anchor_verkey)
        verkey_from_ledger = json.loads(get_nym_response['result']['data'])['verkey']
        print_log('Queried from ledger: ', verkey_from_ledger)
        print_log('Matching: ', verkey_from_ledger == trust_anchor_verkey)
        # 13.
        print_log('\n13. Closing wallet and pool\n')
        await wallet.close_wallet(wallet_handle)
        await pool.close_pool_ledger(pool_handle)
        return("your nym request is done:)")
    except IndyError as e:
        print('Error occurred: %s' % e)
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nymdid())
    loop.close()


if __name__ == '__main__':
    main()
