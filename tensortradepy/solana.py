from solana.blockhash import BlockhashCache
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.hash import Hash
from solders.instruction import Instruction
from solders.message import to_bytes_versioned, Message, MessageV0
from solders.transaction import VersionedTransaction

from .exceptions import TransactionFailedException


def create_client(url):
    return Client(url)


def to_solami(price):
    return int(price * 1_000_000_000)


def from_solami(price):
    return float(price) / 1_000_000_000


def get_keypair_from_base58_secret_key(private_key_base58):
    return Keypair.from_base58_string(private_key_base58)


def run_solana_transaction(client, sender_key_pair, transaction_buffer):
    transaction = Transaction.deserialize(bytes(transaction_buffer))
    signature = transaction.sign(sender_key_pair)
    response = None
    try:
        response = client.send_transaction(transaction, sender_key_pair)
    except Exception as e:
        raise TransactionFailedException(e)
    return response


def run_solana_versioned_transaction(client, sender_key_pair, transaction_buffer):
    block = client.get_latest_blockhash().value
    transaction = VersionedTransaction.from_bytes(bytes(transaction_buffer))
    new_msg = MessageV0(
        transaction.message.header,
        transaction.message.account_keys,
        block.blockhash,
        transaction.message.instructions,
        []
    )
    signature = sender_key_pair.sign_message(to_bytes_versioned(new_msg))
    signed_tx = VersionedTransaction.populate(new_msg, [signature])
    response = None
    try:
        response = client.send_transaction(
            signed_tx
        )
    except Exception as e:
        print("An error occurred:", e)
    return response
