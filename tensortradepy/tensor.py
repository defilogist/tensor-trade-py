import base58
import requests
import uuid

from .solana import (
    create_client,
    from_solami,
    to_solami,
    get_keypair_from_base58_secret_key,
    run_solana_transaction,
    run_solana_versioned_transaction
)

from .helpers import (
    build_tensor_query
)


class TensorClient:

    def __init__(
        self,
        api_key,
        private_key=None,
        network="devnet",
    ):
        """
        The constructor sets up the client. It allows you to set your Tensor
        Trade API key, your wallet private key to perform operations and the
        Solana network where transactions are set.

        Args:
            api_key (str): The Tensor Trade API authentication key.
            private_key (str): Your wallet private key.
            network (str): The Solana network to use.
        """
        self.init_client(api_key)
        self.init_solana_client(private_key, network)

    def init_client(self, api_key: str):
        self.session = requests.session()
        self.api_key = api_key
        self.session.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'tensortradepy',
            'X-TENSOR-API-KEY': api_key
        }

    def init_solana_client(self, private_key, network):
        """
        """
        self.keypair = None
        if private_key is not None:
            self.keypair = get_keypair_from_base58_secret_key(private_key)
        url = f"https://api.{network}.solana.com"
        if network.startswith("http"):
            url = network
        self.solana_client = create_client(url)

    def send_query(self, query, variables):
        """
        """
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

    def extract_transaction(self, data, name):
        return data[name]["txs"][0]["tx"]["data"]

    def extract_versioned_transaction(self, data, name):
        return data[name]["txs"][0]["txV0"]["data"]

    def execute_query(self, query, variables, name):
        data = self.send_query(query, variables)
        if data[name]["txs"][0].get("txV0", None) is not None:
            transaction = self.extract_versioned_transaction(data, name)
            return run_solana_versioned_transaction(
                self.solana_client,
                self.keypair,
                transaction
            )
        else:
            transaction = self.extract_transaction(data, name)
            return run_solana_transaction(
                self.solana_client,
                self.keypair,
                transaction
            )

    def get_collection_infos(self, slug: str):
        """
        Retrieve the main information about a collection including buyNowPrice,
        sellNowPrice and the number of listed elements.

        Args:
            slug (str): the collection slug (ID)

        Returns:
            (dict): ex: { "buyNowPrice": 10, "sellNowPrice": 10, "numListed": 100 }
        """
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
        """
        Retrieve the lowest price of the item listed for the given collection.

        Args:
            slug (str): the collection slug (ID)

        Returns:
            (float): The floor price (buyNow).
        """
        data = self.get_collection_infos(slug)
        if data is None:
            raise Exception("The collection %s is not listed." % slug)
        return from_solami(data["statsV2"]["buyNowPrice"])

    def list_cnft(self, mint, price, wallet_address=None):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TcompListTx",
            "tcompListTx",
            [
                ("mint", "String"),
                ("owner", "String"),
                ("price", "Decimal"),
            ]
        )
        variables = {
            "mint": mint,
            "owner": wallet_address,
            "price": str(to_solami(price))
        }
        return self.execute_query(query, variables, "tcompListTx")

    def edit_cnft_listing(self, mint, price, wallet_address=None):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TcompEditTx",
            "tcompEditTx",
            [
                ("mint", "String"),
                ("owner", "String"),
                ("price", "Decimal"),
            ]
        )
        variables = {
            "mint": mint,
            "owner": wallet_address,
            "price": str(to_solami(price))
        }
        return self.execute_query(query, variables, "tcompEditTx")

    def delist_cnft(self, mint, wallet_address=None):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TcompDelistTx",
            "tcompDelistTx",
            [
                ("mint", "String"),
                ("owner", "String"),
            ]
        )
        variables = {
            "mint": mint,
            "owner": wallet_address,
        }
        return self.execute_query(query, variables, "tcompDelistTx")

    def list_nft(self, mint, price, wallet_address=None):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TswapListNftTx",
            "tswapListNftTx",
            [
                ("mint", "String"),
                ("owner", "String"),
                ("price", "Decimal"),
            ]
        )
        variables = {
            "mint": mint,
            "owner": wallet_address,
            "price": str(to_solami(price))
        }
        return self.execute_query(query, variables, "tswapListNftTx")

    def edit_nft_listing(self, mint, price, wallet_address=None):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TswapEditSingleListing",
            "tswapEditSingleListingTx",
            [
                ("mint", "String"),
                ("owner", "String"),
                ("price", "Decimal"),
            ]
        )
        variables = {
            "mint": mint,
            "owner": wallet_address,
            "price": str(to_solami(price))
        }
        return self.execute_query(query, variables, "tswapEditSingleListingTx")

    def delist_nft(self, mint, wallet_address=None):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TswapDelistNftTx",
            "tswapDelistNftTx",
            [
                ("mint", "String"),
                ("owner", "String"),
            ]
        )
        variables = {
            "mint": mint,
            "owner": wallet_address,
        }
        return self.execute_query(query, variables, "TswapDelistNftTx")


    def set_cnft_collection_bid(
        self,
        slug,
        price,
        quantity,
        wallet_address=None
    ):
        """
        """
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TcompBidTxForCollection",
            "tcompBidTx",
            [
                ("owner", "String"),
                ("price", "Decimal"),
                ("quantity", "Float"),
                ("slug", "String")
            ],
            {
                "txs": {
                    "lastValidBlockHeight": None,
                    "tx": None,
                    "txV0": None
                }
            }
        )
        variables = {
          "owner": wallet_address,
          "price": str(to_solami(price)),
          "quantity": quantity,
          "slug": slug,
        }
        data = self.execute_query(query, variables, "tcompBidTx")
        return data

    def edit_cnft_collection_bid(
        self,
        bid_address,
        price,
        quantity
    ):
        """
        """
        query = build_tensor_query(
            "TcompEditBidTx",
            "tcompEditBidTx",
            [
                ("bidStateAddress", "String"),
                ("price", "Decimal"),
                ("quantity", "Float")
            ]
        )
        variables = {
          "bidStateAddress": bid_address,
          "price": str(to_solami(price)),
          "quantity": quantity,
        }
        return self.execute_query(query, variables, "tcompEditBidTx")

    def cancel_cnft_collection_bid(
        self,
        bid_address
    ):
        """
        """
        query = build_tensor_query(
            "TcompCancelCollBidTx",
            "tcompCancelCollBidTx",
            [
                ("bidStateAddress", "String"),
            ]
        )
        variables = {
          "bidStateAddress": bid_address,
        }
        return self.execute_query(query, variables, "tcompCancelCollBidTx")

    def set_nft_collection_bid(
        self,
        slug,
        price,
        quantity,
        wallet_address=None
    ):
        """
        """
        self.set_cnft_collection_bid(
            slug,
            price,
            wallet_address=wallet_address
        )

    def edit_nft_collection_bid(
        self,
        bid_address,
        price,
        quantity
    ):
        """
        """
        self.edit(
            bid_address,
            price,
            quantity
        )

    def cancel_nft_collection_bid(
        self,
        bid_address
    ):
        """
        """
        self.cancel_cnft_collection_bid(
            bid_address
        )

    def buy_nft(
        self,
        seller,
        mint,
        price,
        wallet_address=None
    ):
        if wallet_address is None:
            wallet_address = str(self.keypair.pubkey())

        query = build_tensor_query(
            "TswapBuySingleListingTx",
            "tswapBuySingleListingTx",
            [
                ("buyer", "String"),
                ("maxPrice", "Decimal"),
                ("mint", "String"),
                ("owner", "String")
            ]
        )
        variables = {
          "owner": seller,
          "maxPrice": str(to_solami(price)),
          "mint": mint,
          "buyer": wallet_address,
        }
        print(variables)
        return self.execute_query(query, variables, "tswapBuySingleListingTx")
