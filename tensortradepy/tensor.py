import base58
import requests
import uuid

from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction


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


class TensorClient:

    def __init__(
        self,
        api_key,
        private_key=None,
        network="devnet",
    ):
        self.init_client(api_key)
        self.init_solana_client(private_key, network)

    def init_client(self, api_key):
        self.session = requests.session()
        self.api_key = api_key
        self.session.headers = {
            'Content-Type': 'application/json',
            'X-TENSOR-API-KEY': api_key
        }

    def init_solana_client(self, private_key, network):
        self.keypair = None
        if private_key is not None:
            self.keypair = get_keypair_from_base58_secret_key(private_key)
        url = f"https://api.{network}.solana.com"
        if network.startswith("http"):
            url = network
        self.solana_client = Client(url)

    def send_query(self, query, variables):
        resp = self.session.post(
            "https://api.tensor.so/graphql/",
            json={
                "query": query,
                "variables": variables
            }
        )
        try:
            return resp.json().get("data", {})
        except requests.exceptions.JSONDecodeError:
            if resp.status_code == 403:
                raise Exception("Invalid API Key")
            else:
                raise

    def get_collection_infos(self, slug):
        query = """query CollectionsStats($slug: String!) {
            instrumentTV2(slug: $slug) {
                id
                slug
                firstListDate
                name
                statsV2 {
                    currency
                    buyNowPrice
                    buyNowPriceNetFees
                    sellNowPrice
                    sellNowPriceNetFees
                    numListed
                    numMints
                }
            }
        }
        """
        variables = {"slug": slug}
        data = self.send_query(query, variables)
        return data.get("instrumentTV2", {})

    def get_collection_floor(self, slug):
        data = self.get_collection_infos(slug)
        if data is None:
            raise Exception("The collection %s is not listed." % slug)
        return from_solami(data["statsV2"]["buyNowPrice"])

    def list_cnft(self, mint, price, wallet_address=None):
        query = """query TcompListTx(
            $mint: String!,
            $owner: String!,
            $price: Decimal!
        ) {
            tcompListTx(mint: $mint, owner: $owner, price: $price) {
                txs {
                    lastValidBlockHeight
                    tx
                    txV0
                }
            }
        }"""
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        variables = {
            "mint": mint,
            "owner": wallet_address,
            "price": str(to_solami(price))
        }
        tx = self.send_query(query, variables)
        transaction = tx["tcompListTx"]["txs"][0]["tx"]["data"]
        result = run_solana_transaction(
            self.solana_client,
            self.keypair,
            transaction
        )
        print(f"cNFT listed {mint}")
        return result


    def list_nft(self, mint, price, wallet_address=None):
        query = """query TswapListNftTx(
            $mint: String!,
            $owner: String!,
            $price: Decimal!
        ) {
            tswapListNftTx(mint: $mint, owner: $owner, price: $price) {
                txs {
                    lastValidBlockHeight
                    tx
                    txV0
                }
            }
        }"""
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        variables = {
            "mint": mint,
            "owner": wallet_address,
            "price": str(to_solami(price))
        }
        tx = self.send_query(query, variables)
        transaction = tx["tswapListNftTx"]["txs"][0]["tx"]["data"]
        result = run_solana_transaction(
            self.solana_client,
            self.keypair,
            transaction
        )
        print(f"NFT listed {mint}")
        return result
