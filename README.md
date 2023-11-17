# tensor-trade-py

Simple Python client for the Tensor Trade API.

## Disclaimer

Be aware that this client directly communicates with Tensor. Be sure of your
script before doing any financial operations. Moreover, there is no guarantee
about the reliability of this client.

The developer of this client is not responsible for any errors or issues that
may occur when using this SDK. Use at your own risk.

I encourage you to tests your scripts with cheap cNFT collections first.


## Install

```
pip install git+https://github.com/defilogist/tensor-trade-py
```

## Usage example

```python
import os
from tensortradepy import TensorClient

client = TensorClient(
    os.getenv("TENSOR_API_KEY"),
    os.getenv("WALLET_PRIVATE_KEY"),
    "mainnet-beta"
)
floor = client.get_collection_floor("theheist")
const percentage = 0.99
const nft = {
  "mint": "nft-mint",
  "wallet_address": "wallet-address"
}
client.list_nft(nft["mint"], nft["walletAddress"], floor * percentage)
```

## Functions available

* get\_collection\_infos(slug)
* get\_collection\_floor(slug)
* list\_nft(mint, price) // Price in $SOL
* list\_cnft(mint, price) // Price in $SOL
