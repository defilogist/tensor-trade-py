# DEPRECATED: Tensor has new API. Update in progress

# (unofficial) Python Client for Tensor Trade

This library is a simple Python client for the Tensor Trade API. It's aimed is 
to make your bot trading simpler.


## Disclaimer

Be aware that this client directly communicates with Tensor. Be sure of your
script before doing any financial operations. Moreover, there is no guarantee
about the reliability of this client. I encourage you to tests your scripts
with cheap cNFT collections first. 

The developer of this client is not responsible for any errors or issues that
may occur when using this SDK. Use at your own risk.

## Tips

If you like this client, you can tip me at: thewisetrade.sol or buy 
[the logo NFT](https://exchange.art/editions/9rukfGYfTxpmiRFrGvhSSCASsqhgsWGundBHNQB2vKPy).

## Install

Install the library with:

```
pip install tensortradepy
```


Development version:

```
pip install git+https://github.com/defilogist/tensor-trade-py
```

## Usage example

``` python
import os
from tensortradepy import TensorClient

client = TensorClient(
    os.getenv("TENSOR_API_KEY"),
    os.getenv("WALLET_PRIVATE_KEY"),
    "mainnet-beta"
)

floor = client.get_collection_floor("theheist")
price = floor * 0.99
nft_mint = "nft-mint"
client.list_nft(nft_mint, price) # we assume your keypair owns the NFT.
```

## Documenation

A [full documentation](https://tensortradepy.thewise.trade/) is available.

## Functions available

* get\_collection\_infos(slug)
* get\_collection\_floor(slug)
* list\_nft(mint, price) // Price in $SOL
* list\_cnft(mint, price) // Price in $SOL
* delist\_cnft(mint)
* edit\_cnft\_listing(mint, price) // Price in $SOL
* set\_cnft\_collection\_bid(slug, price, quantity)
* edit\_cnft\_collection\_bid(slug, price, quantity)
* cancel\_cnft\_collection\_bid(slug, price, quantity)
* buy\_nft\_(seller, mint\_address, price)
* buy\_cnft\_(seller, mint\_address, price)

## Contributions

Any contribution is welcome, please open your PR for additions and report bug
through Github issues.

## About

This client is developed by [thewise.trade](https://thewise.trade).
