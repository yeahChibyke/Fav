from vyper import compile_code
from web3 import Web3  
from dotenv import load_dotenv
import os
from encrypt_key import KEYSTORE_PATH
import getpass
from eth_account import Account

load_dotenv()
MY_ADDR = os.getenv("MY_ADDR")
# MY_KEY = os.getenv("MY_KEY")
RPC_URL = os.getenv("RPC_URL")

def main():
    print("Reading into vyper contract...")
    with open("fav.vy", "r") as fav_file:
        fav_code = fav_file.read()
        compilation_details = compile_code(fav_code, output_formats = ["bytecode", "abi"])
        print(compilation_details)

    fav3 = Web3(Web3.HTTPProvider(RPC_URL))
    fav_contract = fav3.eth.contract(bytecode = compilation_details["bytecode"], abi = compilation_details["abi"])
    print(fav_contract)

    print("Building the transaction...")
    fav_nonce = fav3.eth.get_transaction_count(MY_ADDR)
    fav_txn = fav_contract.constructor().build_transaction({
        "nonce": fav_nonce,
        "from": MY_ADDR,
        "gasPrice": fav3.eth.gas_price
    })
    print(fav_txn)

    print("Signing transaction...")
    private_key = decrypt_key()
    fav_signed_txn = fav3.eth.account.sign_transaction(fav_txn, private_key = private_key)
    print(fav_signed_txn)

    print("Sending transaction...")
    fav_tx_hash = fav3.eth.send_raw_transaction(fav_signed_txn.raw_transaction)
    print(f"Transaction hash is: {fav_tx_hash}")

    print("Getting transaction receipt...")
    fav_tx_receipt = fav3.eth.wait_for_transaction_receipt(fav_tx_hash)

    print(f"Done!!! Contract deployed to: {fav_tx_receipt.contractAddress}")
    
def decrypt_key() -> str:
    with open (KEYSTORE_PATH, "r") as fp:
        encrypted_account = fp.read()
        password = getpass.getpass("Enter your password: ")
        key = Account.decrypt(encrypted_account, password)
        print("Decrypted key!!!")
        return key


if __name__ == "__main__":
    main()

