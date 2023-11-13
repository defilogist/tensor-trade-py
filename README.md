# tensor-trade-js

Simple Python client for the Tensor Trade API.

Be aware that this client directly communicates with Tensor. Be sure of your
script before doing any financial operations. Moreover, I don't guarantee
anything about the reliability of this client.

I encourage you to tests your scripts with cheap cNFT collections first.


## Install

```
pip install git+https://github.com/defilogist/tensor-trade-js
```

## Usage example

```python
import os
from tensortradepy import TensorClient

client = TensorClient(os.getenv("TENSOR_API_KEY"))
floor = client.get_collection_floor("theheist")
const percentage = 0.99
const nft = {
  "mint": "nft-mint",
  "wallet_ddress": "wallet-address"
}
client.list_nft(nft.mint, nft.walletAddress, floor * percentage)
```

## Functions available

* get\_collection\_infos(slug)
* get\_collection\_floor(slug)
* list\_nft(mint, walletAddress, price) // Price in $SOL
