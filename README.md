# tensor-trade-py

Simple Python client for the Tensor Trade API.

## Disclaimer

Be aware that this client directly communicates with Tensor. Be sure of your
script before doing any financial operations. Moreover, there is no guarantee
about the reliability of this client.

The developer of this client is not responsible for any errors or issues that
may occur when using this SDK. Use at your own risk.

I encourage you to tests your scripts with cheap cNFT collections first.

## Contributions

Any contribution is welcome, please open your PR for additions and report bug
through Github issues.

## Tips

If you like this client, you can tip me at: wiseCUogbp8QkzrNF6ku8cfZrWkRtbTinYso1KQRH7i


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
price = floor * percentage
const nft = {
  "mint": "nft-mint"
}
client.list_nft(nft["mint"], price) # we assume your keypair owns the NFT.
```

## Functions available

* get\_collection\_infos(slug)
* get\_collection\_floor(slug)
* list\_nft(mint, price) // Price in $SOL
* list\_cnft(mint, price) // Price in $SOL
