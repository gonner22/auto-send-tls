"""
Telestai Wallet Manager Script
Developed by the Telestai Dev Team in 2025

This script provides a command-line interface for managing a Telestai wallet. 
It allows users to check their balance, list UTXOs, consolidate UTXOs, and 
automatically generate small transactions for testing purposes.
"""

import json
import subprocess
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configuration
MIN_CONF = int(os.getenv("MIN_CONF", 1))  # The minimum number of confirmations before payments are included. Default to 1 if not set
MAX_UTXOS = int(os.getenv("MAX_UTXOS", 500))  # The max number of UTXOs to consolidate. Default to 500 if not set
CONSOLIDATION_THRESHOLD = int(os.getenv("CONSOLIDATION_THRESHOLD", 118))  # The threshold for consolidation. Default to 118 if not set
WALLET_ADDRESS_INDEX = int(os.getenv("WALLET_ADDRESS_INDEX", 0))  # Wallet address index. Default to 0 if not set

# Configure logging for consolidation
consolidation_logger = logging.getLogger('consolidation')
consolidation_handler = logging.FileHandler('consolidation.log')
consolidation_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consolidation_handler.setFormatter(consolidation_formatter)
consolidation_logger.addHandler(consolidation_handler)
consolidation_logger.setLevel(logging.INFO)

# Configure logging for split
split_logger = logging.getLogger('split')
split_handler = logging.FileHandler('split.log')
split_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
split_handler.setFormatter(split_formatter)
split_logger.addHandler(split_handler)
split_logger.setLevel(logging.INFO)

def run_cli_command(command):
    """Executes a command using the telestai-cli and returns the output."""
    try:
        result = subprocess.run(["telestai-cli"] + command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error processing command output: {e.stdout.strip()}\n❌ {e.stderr.strip()}")
        return None

def get_balance():
    """Fetches and displays the wallet balance."""
    balance = run_cli_command(["getbalance"])
    if balance is not None:
        print(f"💰 Balance: {balance} TLS")
    else:
        print("❌ Failed to fetch balance.")

def list_utxos():
    """Lists all unspent transaction outputs (UTXOs)."""
    utxos_json = run_cli_command(["listunspent"])
    if not utxos_json:
        print("❌ No available UTXOs.")
        return []

    utxos = json.loads(utxos_json)
    if not utxos:
        print("❌ No UTXOs available.")
        return []

    return utxos

def display_utxos(utxos):
    """Displays the details of each UTXO."""
    print("🔍 UTXOs:")
    for index, utxo in enumerate(utxos, start=1):
        print(f"{index}. TXID: {utxo['txid']}, VOUT: {utxo['vout']}, Address: {utxo['address']}, Amount: {utxo['amount']} TLS, Confirmations: {utxo['confirmations']}")

def consolidate_utxos():
    """Consolidates UTXOs below the specified threshold into a single transaction."""
    utxos_json = run_cli_command(["listunspent", str(MIN_CONF)])
    if not utxos_json:
        print("No UTXOs available for consolidation.")
        return

    utxos = json.loads(utxos_json)

    # Check if there is only one UTXO
    if len(utxos) <= 1:
        print("Cannot consolidate because there is only one UTXO available.")
        return

    # Filter UTXOs below the consolidation threshold
    selected_utxos = [utxo for utxo in utxos if utxo["amount"] < CONSOLIDATION_THRESHOLD]
    if not selected_utxos:
        print("No UTXOs below the threshold for consolidation.")
        return

    # Limit to the first MAX_UTXOS UTXOs
    selected_utxos = selected_utxos[:MAX_UTXOS]
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]} for utxo in selected_utxos]
    total_amount = sum(utxo["amount"] for utxo in selected_utxos)

    # Calculate final amount after fees
    amount_to_send = total_amount
    destination_address = get_wallet_address()
    if not destination_address:
        print("Failed to get a destination address.")
        return

    try:
        # Create a raw transaction
        raw_tx = run_cli_command(["createrawtransaction", json.dumps(inputs), json.dumps({destination_address: round(amount_to_send, 8)})])
        if raw_tx:
            # Fund the transaction to adjust for fees
            funded_tx_json = run_cli_command([
                "fundrawtransaction", raw_tx,
                json.dumps({
                    "changeAddress": destination_address,
                    "changePosition": 1,
                    "subtractFeeFromOutputs": [0]
                })
            ])
            funded_tx = json.loads(funded_tx_json)
            funded_raw_tx = funded_tx["hex"]
            estimated_fee = funded_tx["fee"]
            amount_to_send = total_amount - estimated_fee

            # Display summary before sending
            print("\nConsolidation Summary:")
            print(f"Total UTXOs: {len(selected_utxos)}")
            print(f"Total Amount: {total_amount:.8f} TLS")
            print(f"Transaction Fee: {estimated_fee:.8f} TLS")
            print(f"Amount to be sent: {amount_to_send:.8f} TLS")
            confirm = input("Do you want to proceed? (yes/no): ").strip().lower()
            if confirm not in {"yes", "y"}:
                print("Consolidation cancelled.")
                return

            # Sign the transaction
            signed_tx_json = run_cli_command(["signrawtransaction", funded_raw_tx])
            signed_tx = json.loads(signed_tx_json)
            if signed_tx.get("complete", False):
                txid = run_cli_command(["sendrawtransaction", signed_tx["hex"]])
                if txid:
                    print(f"Consolidation completed, TXID: {txid}")
                    # Log the transaction details after user confirmation
                    consolidation_logger.info(f"Consolidation Summary: Total UTXOs: {len(selected_utxos)}, Total Amount: {total_amount:.8f} TLS, Transaction Fee: {estimated_fee:.8f} TLS, Amount to be sent: {amount_to_send:.8f} TLS")
                    consolidation_logger.info(f"Consolidation completed, TXID: {txid}")
    except Exception as e:
        print(f"❌ Failed to consolidate UTXOs: {e}")
        consolidation_logger.error(f"Failed to consolidate UTXOs: {e}")

def get_wallet_address():
    """Retrieves the wallet address based on the configured index."""
    addresses_json = run_cli_command(["listreceivedbyaddress", "0", "false"])
    if addresses_json:
        addresses = json.loads(addresses_json)

        if WALLET_ADDRESS_INDEX < len(addresses):
            return addresses[WALLET_ADDRESS_INDEX]["address"]
        else:
            print(f"❌ Wallet Address Index {WALLET_ADDRESS_INDEX} does not exist.")
            print("Please run 'telestai-cli listreceivedbyaddress 0 false' to see available addresses.")
            print("The index is 0 based, so the first address is 0, the second is 1, etc.")
            print("After get the index, you can change the WALLET_ADDRESS_INDEX in the .env file.")
            return None

def auto_generate_spents():
    """Automatically generates small transactions for testing purposes."""
    utxos = list_utxos()
    if not utxos:
        print("❌ No UTXOs available.")
        return

    display_utxos(utxos)

    change_address = get_wallet_address()
    if not change_address:
        print("❌ Failed to get a change address.")
        return

    for utxo in utxos:
        if utxo["amount"] > 0.01:
            # Create a raw transaction
            try:
                raw_tx = run_cli_command(["createrawtransaction", json.dumps([{"txid": utxo["txid"], "vout": utxo["vout"]}]), json.dumps({change_address: 0.01})])
                if raw_tx:
                    # Fund the transaction to adjust for fees
                    funded_tx_json = run_cli_command([
                        "fundrawtransaction", raw_tx,
                        json.dumps({
                            "changeAddress": change_address,
                            "changePosition": 1,
                            "subtractFeeFromOutputs": []
                        })
                    ])
                    funded_tx = json.loads(funded_tx_json)
                    funded_raw_tx = funded_tx["hex"]
                    estimated_fee = funded_tx["fee"]

                    # Calculate change amount
                    total_amount = utxo["amount"]
                    change_amount = total_amount - 0.01 - estimated_fee

                    # Display transaction details
                    print("\nTransaction Details:")
                    print(f"Amount to Send: 0.01 TLS")
                    print(f"Destination Address: {change_address}")
                    print(f"Transaction Fee: {estimated_fee:.8f} TLS")
                    print(f"Change Amount: {change_amount:.8f} TLS")
                    confirm = input("Do you want to proceed with this transaction? (yes/no): ").strip().lower()
                    if confirm not in {"yes", "y"}:
                        print("Transaction cancelled.")
                        continue

                    # Sign the transaction
                    signed_tx_json = run_cli_command(["signrawtransaction", funded_raw_tx])
                    signed_tx = json.loads(signed_tx_json)
                    if signed_tx.get("complete", False):
                        txid = run_cli_command(["sendrawtransaction", signed_tx["hex"]])
                        if txid:
                            print(f"✅ Transaction sent! TXID: {txid}")
                            # Log the transaction details after user confirmation
                            split_logger.info(f"Transaction Details: Amount to Send: 0.01 TLS, Destination Address: {change_address}, Transaction Fee: {estimated_fee:.8f} TLS, Change Amount: {change_amount:.8f} TLS")
                            split_logger.info(f"Transaction sent! TXID: {txid}")

            except Exception as e:
                print(f"❌ Failed to create raw transaction: {e}")
                split_logger.error(f"Failed to create raw transaction: {e}")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\n===== Telestai Wallet Manager =====")
        print("1. Check Balance")
        print("2. List UTXOs")
        print(f"3. Consolidate UTXOs (max {MAX_UTXOS}, <{CONSOLIDATION_THRESHOLD} TLS)")
        print("4. Auto Generate Spents (for testing with predefine amount 0.01 TLS)")
        print("5. Exit")
        option = input("Select an option: ").strip()

        if option == "1":
            get_balance()
        elif option == "2":
            utxos = list_utxos()
            if utxos:
                display_utxos(utxos)
        elif option == "3":
            consolidate_utxos()
        elif option == "4":
            auto_generate_spents()
        elif option == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
