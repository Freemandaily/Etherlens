from re import A
from typing import Optional,Union
from decoder import Decoder_input
from address_abi import *
from web3 import *
import time,os,sys
import requests,json


class Decoder:
    def __init__(self,RPC_URL:str,blockchain:str) -> None:
        self.connect = Web3(Web3.HTTPProvider(RPC_URL))
        self.blockchain = blockchain 
        self.swapContract = self.connect.eth.contract(address=self.connect.to_checksum_address(swap_router),abi=CONTRACT_ABI)
        print(self.connect.is_connected())
        
    def blockchain_api_fetcher(self,address:str):  # ETH BSC OP BASE POLY ARB
        ABB_KEY = 'EVC67MEUGJS31D7VE8R2XIDMCF5EU1WH59' # ARB api.arbiscan.io
        ETH_KEY = '8TSUD2IHRGJ4ITVIAYEXNCAWE1ZV3U9J4I' # ETH api.etherscan.io
        BSC_KEY = 'I39P5W2Q4EXZEE9Z3MYHP7B2MDM2Z1XPSH' #BSC api.bscscan.com
        OP_KEY = '1DPMQMF1S78SKE1NID7NCA8CWQS5SJCAMN' # OP api-optimistic.etherscan.io
        POLY_KEY = 'QQXPMKVXDIXR5MVBRFB6RE9YJQZZUY8FQ2' # api.polygonscan.com
        BASE_KEY = 'CDHWFP4UDZ2JP5CBCE97BSVHVBPUUUNXHC'
        if self.blockchain == 'ETH':
            api_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={ETH_KEY}&page=1&offset=2'
            return api_url
        elif self.blockchain == 'BSC':
            api_url = f'https://api.bscscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={BSC_KEY}&page=1&offset=2'
            return api_url
        elif self.blockchain == 'OP':
            api_url = f'https://api-optimistic.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={OP_KEY}&page=1&offset=2'
            return api_url
        elif self.blockchain == 'BASE':
            api_url = f'https://api.basescan.org/api?module=account&action=txlist&address={address}&sort=desc&apikey={BASE_KEY}&page=1&offset=2'
            return api_url
        elif self.blockchain == 'POLY':
            api_url = f'https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={POLY_KEY}&page=1&offset=2'
            return api_url
        elif self.blockchain == 'ARB':
            api_url = f'https://api.arbiscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={ABB_KEY}&page=1&offset=2'
            return api_url

    def check_balance(self,tokenAddress:str, addresses: list):
        addressBalanceInfo = {}
        tokenContract = self.connect.eth.contract(address=self.connect.to_checksum_address(tokenAddress),abi=BASIC_TOKEN_ABI)
        for address in addresses:
            balance = tokenContract.functions.balanceOf(self.connect.to_checksum_address(address)).call()
            decimal = tokenContract.functions.decimals().call()
            addressBalanceInfo[address] = balance/10**decimal
        return addressBalanceInfo
    
    def native_gas(self,addresses: list):
        balanceInfo = {}
        for address in addresses:
            eth_in_wei = self.connect.eth.get_balance(self.connect.to_checksum_address(address))
            change_to_eth = self.connect.from_wei(eth_in_wei,'ether')
            balanceInfo[address] = float(round(change_to_eth,6))
        return balanceInfo
    
    def TransactionsFetcher(self,address):
        try:
            time.sleep(3)
            tracking_url = self.blockchain_api_fetcher(address)
            response = requests.get(tracking_url)
            data = json.loads(response.text)
            transactions = data.get('result',[])
            return transactions
        except Exception as e:
            time.sleep(3)
            tracking_url = self.blockchain_api_fetcher(address)
            response = requests.get(tracking_url)
            data = json.loads(response.text)
            transactions = data.get('result',[])
            return transactions

    def Swap_v2_01(self,inputData,hash):
        data = {}
        transaction_rec = self.connect.eth.get_transaction_receipt(hash)
        log = transaction_rec.get('logs',[])
        data['ammountIn'] = int(log[0]['data'].hex(),16)
        data['amountOut'] = int(log[2]['data'].hex(),16)
        decode = self.swapContract.decode_function_input(inputData)[1]
        data["tokenIn"] = decode['path'][0]
        data['tokenOut'] = decode['path'][1]
        return data

    def Swap_v2_02(self,inputData,hash):
        data = {}
        transaction_rec = self.connect.eth.get_transaction_receipt(hash)
        log = transaction_rec.get('logs',[])
        data['ammountIn'] = int(log[0]['data'].hex(),16)
        data['amountOut'] = int(log[1]['data'].hex(),16)
        decode = self.swapContract.decode_function_input(inputData)[1]
        data['tokenIn'] = decode['path'][0]
        data['tokenOut'] = decode['path'][1]
        return data

    def Swap_detail(self,inputData,hash):
        processor = Decoder_input()
        hash_detail = {}
        swap_decoder_function = [self.Swap_v2_01,self.Swap_v2_01,processor.process_trade]
        for function in swap_decoder_function:
            try:
                detail = function(inputData,hash)
                hash_detail[f'hash({hash})'] = detail
                return hash_detail
            except Exception as e:
                pass
                #print(f'Cant decode the input due to {e}')

class Observe(Decoder):

    def __init__(self,RPC_URL:str,blockchain:Optional[str]='ETH') -> None:
        super().__init__(RPC_URL,blockchain)
        self.connect = Web3(Web3.HTTPProvider(RPC_URL))
        
    def token_balance(self,tokenAddress:str,address: Union[str, list[str]]):
        if isinstance(address,str):
            address = [address]
            balanceInfo = self.check_balance(tokenAddress,address)
            return balanceInfo[address[0]]
        elif isinstance(address,list):
            balanceInfo = self.check_balance(tokenAddress,address)
            return balanceInfo
        else:
            raise TypeError('Parameter Must Be Either str or list. Invalid Data Type')
    

    def eth_balance(self,address: Union[str, list[str]]):
        if isinstance(address,str):
            address = [address]
            balanceInfo = self.native_gas(address)
            return balanceInfo[address[0]] 
        elif isinstance(address,list):
            balanceInfo = self.native_gas(address)
            return balanceInfo
        else:
            raise TypeError('Parameter Must Be Either str or list. Invalid Data Type')
    

    def monitor(self,address:Union[str,list[str]]):
        monitored_transactions = {}
        if isinstance(address,str):
            address = [address]
        for wallet in address:
            transaction_detail = []
            transactions =  self.TransactionsFetcher(wallet)
            for transaction in transactions:
                hash = transaction['hash']
                inputData = transaction['input']
                hash_detail = self.Swap_detail(inputData,hash)
                if type(hash_detail) == dict:
                    transaction_detail.append(hash_detail)

            if bool(transaction_detail):
                monitored_transactions[f'Address({wallet})'] = transaction_detail

        return monitored_transactions

    def monitor_with_hash(self,hash):
        inputData = self.connect.eth.get_transaction(hash)['input']   
        hash_detail = self.Swap_detail(inputData,hash)
        return hash_detail

