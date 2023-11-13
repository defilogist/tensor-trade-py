import requests
import uuid


def to_solami(price):
    return price * 1_000_000_000


def from_solami(price):
    return float(price) / 1_000_000_000


class TensorClient:
    def __init__(self, api_key):
        self.init_client(api_key)

    def init_client(self, api_key):
        self.session = requests.session()
        self.api_key = api_key
        self.session.headers = {
            'Content-Type': 'application/json',
            'X-TENSOR-API-KEY': api_key
        }

    def send_query(self, query, variables):
        resp = self.session.post(
            "https://api.tensor.so/graphql/",
            json={
                "query": query,
                "variables": variables
            }
        )
        return resp.json().get("data", {})

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
        return from_solami(data["statsV2"]["buyNowPrice"])

    def list_nft(mint, walletAddress, price):
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
        variables = {
            "mint": mint,
            "owner": walletAddress,
            "price": '' + toSolami(price)
        }
        tx = self.send_query(query, variables)
        return tx["tcompListTx"]["txs"]
