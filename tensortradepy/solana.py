from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction


def create_client(url):
    return Client(url)


def to_solami(price):
    return price * 1_000_000_000


def from_solami(price):
    return float(price) / 1_000_000_000


def get_keypair_from_base58_secret_key(private_key_base58):
    return Keypair.from_base58_string(private_key_base58)


def run_solana_transaction(client, sender_key_pair, transaction_buffer):
    transaction = Transaction.deserialize(bytes(transaction_buffer))
    transaction.sign(sender_key_pair)
    response = None
    try:
        response = client.send_transaction(transaction, sender_key_pair)
    except Exception as e:
        print("An error occurred:", e)
    return response


