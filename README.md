# Etherlens
EtherLens is a Python library designed to provide comprehensive insights into Blockchain transactions, token balances, and gas balances associated with a specific address. This library offers a range of functionalities, including decoding transactions made by an address, fetching token balances for various ERC-20 tokens, and retrieving gas balances.

### Key Feature
- **Transaction Decoding**: Decode any blockchain **(ETH,BSC,ARB,OP,BASE,POLY)** transaction that contain similar uniswap V2 router functions and universal router like function.It gives insight on token bought,token sold,amount bought,amount sold,hash of the transction
- **Token Balance Fetching**: Fetch token balances associated with a given blockchain address for a wide range of ERC-20 tokens, allowing users to quickly ascertain their token holdings.
- **Gas Balance Retrieval**: Retrieve gas balances associated with an Ethereum address, enabling users to monitor gas usage and ensure efficient management of gas resources.
  
### Caution
⚠ This library has not been audited, and there is no pledge for one !

⚠ Might be of advantage to be familiar with general blockchain concepts and [web3.py](https://github.com/ethereum/web3.py) in particular.

⚠ This project is a work in progress so not all swap transaction are decoded yet.


## Installation
It is recommended to use [Python virtual environments](https://python.readthedocs.io/en/latest/library/venv.html), here is a [tutorial](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) inorder for the dependencies not to conflict with any other Dependencies you might have in your system

This library can be always seen and installed from >>>


```bash
# install the Etherlens from pypi.org
pip install Etherlens
```

---
## Utilization
This Library exposes a class Observe which has hpublic method that can be use to decode address transction,get token address balance,fetch native gas balance and more


## How to decode/get address transaction detail, assuming it swapped on uniswap/sushi or any dapp with similar V2 router contract functions
You can pass in only one address or list of addresses to the method 

  #### Blockchain usage
  During instantiation of the class **Observe** user should specify which blockchain he/she wants eg 'ETH','BSC','BASE','OP','ARB','POLY'
  
```python
form etherlens import Observe

Your_rpc_url = 'https://.......'
Address = ['0x15deac498767a6e997c007ca91df55cbdd8a6198','0xc633843de683ff3e91353412b039b0699fa1615b']
Decode = Observe(Address,'ETH')
print(Decode)
```



