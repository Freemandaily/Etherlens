from h11 import Data
from uniswap_universal_router_decoder import RouterCodec
from web3 import *

uni_comman_value = ['0b08','080c','000c','0a080c','0a000c','0a00','0b00','0b0800','0a08','0a010c','0a090c','0b090c','0b080c','0b000c','Ob09','0a09']  #REFER TO command module for clear understanding of this commands
codec = RouterCodec()

class Decoder_input:
    def process_trade(self,input_data,hash):

        codec = RouterCodec()
        decoded_input = codec.decode.function_input(input_data)
        main_input = decoded_input[1]
        command = main_input['commands'].hex()
        #print(command)

        if command == uni_comman_value[0] or command == uni_comman_value[7] or command == uni_comman_value[11] or command == uni_comman_value[12] or command == uni_comman_value[14]:                       
            swapinfo = self.WRAP_ETH_AND_V2_SWAP_EXACT_IN_OUT(main_input)
            
            return swapinfo 
        elif command == uni_comman_value[1]:
            swapinfo = self.V2_SWAP_EXACT_IN_AND_UNWRAP_WETH(main_input)
            return swapinfo
        elif command == uni_comman_value[2]:
            swapinfo = self.V3_SWAP_EXACT_IN_AND_UNWRAP_WETH(main_input)
            return swapinfo 
        elif command == uni_comman_value[3] or command == uni_comman_value[8] or command == uni_comman_value[10] or command == uni_comman_value[15]:
            swapinfo = self.PERMIT2_PERMIT_V2(main_input)
            return swapinfo
        elif command == uni_comman_value[4] or command == uni_comman_value[5] or command == uni_comman_value[9]:
            swapinfo = self.PERMIT2_PERMIT_V3(main_input)
            return swapinfo
        elif command == uni_comman_value[6] or command == uni_comman_value[13]:
            swapinfo = self.WRAP_ETH_AND_V3_SWAP_EXACT_IN_OUT(main_input)
            return swapinfo


        
    def WRAP_ETH_AND_V2_SWAP_EXACT_IN_OUT(self,main_input):
        try:#0b08 for v2 buying
            data = {}
            input_swap_path = main_input['inputs'][1][1]['path']
            data['amountIn'] = main_input['inputs'][1][1]['amountIn']
            data['aountOut'] = main_input['inputs'][1][1]['amountOutMin']
            data['tokenIn'] = input_swap_path [0]
            data['tokenOut'] = input_swap_path [-1]
            return data
        except: #0b090c
            data = {}
            data['amountIn'] = main_input['inputs'][1][1]["amountInMax"]
            data['aountOut'] = main_input['inputs'][1][1]['amountOut']
            data['tokenIn'] = input_swap_path [0]
            data['tokenOut'] = input_swap_path [-1]
            return data
        
        



    def WRAP_ETH_AND_V3_SWAP_EXACT_IN_OUT(self,main_input):
        input_swap_path = main_input['inputs'][1][1]['path']
        fun_name = 'V3_SWAP_EXACT_IN'
        decoded_swap_path = codec.decode.v3_path(fun_name,input_swap_path)
        #print(decoded_swap_path)
        try:
            data = {}
            data['amountIn'] = main_input['inputs'][1][1]['amountIn']
            data['aountOut'] = main_input['inputs'][1][1]['amountOutMin']
            data['tokenIn'] = decoded_swap_path [0]
            Data()['tokenOut'] = decoded_swap_path [-1]
        except:
            data = {}
            data['amountIn'] = main_input['inputs'][1][1]["amountInMax"]
            data['aountOut'] = main_input['inputs'][1][1]['amountOut']
            data['tokenIn'] = decoded_swap_path [-1]
            data['tokenOut'] = decoded_swap_path [0]
        return data


    def V2_SWAP_EXACT_IN_AND_UNWRAP_WETH(self,main_input):
        data = {}
        input_swap_path =main_input['inputs'][0][1]['path']
        data['amountIn'] = main_input['inputs'][0][1]['amountIn']
        data['aountOut'] = main_input['inputs'][0][1]['amountOutMin']
        data['tokenIn'] = input_swap_path [0]
        data['tokenOut'] = input_swap_path [-1]
        return data

    def V3_SWAP_EXACT_IN_AND_UNWRAP_WETH(self,main_input):
        data = {}
        input_swap_path =main_input['inputs'][0][1]['path']
        fun_name = 'V3_SWAP_EXACT_IN'
        decoded_swap_path = codec.decode.v3_path(fun_name,input_swap_path)
        data['amountIn'] = main_input['inputs'][0][1]['amountIn']
        data['aountOut'] = main_input['inputs'][0][1]['amountOutMin']
        data['tokenIn'] = decoded_swap_path [0]
        data['tokenOut'] = decoded_swap_path [-1]
        return data

    def PERMIT2_PERMIT_V2(self,main_input):
        input_swap_path =main_input['inputs'][1][1]['path']
        try:
            data = {}
            data['amountIn'] = main_input['inputs'][1][1]["amountIn"]
            data['aountOut'] = main_input['inputs'][1][1]['amountOutMin']
            data['tokenIn'] = input_swap_path [0]
            data['tokenOut'] = input_swap_path [-1]
            return data
        except:
            data['amountIn'] = main_input['inputs'][1][1]["amountInMax"]
            data['aountOut'] = main_input['inputs'][1][1]['amountOut']
            data['tokenIn'] = input_swap_path [-1]
            data['tokenOut'] = input_swap_path [0]
            return data

        

    def PERMIT2_PERMIT_V3(self,main_input):
        input_swap_path =main_input['inputs'][1][1]['path']
        fun_name = 'V3_SWAP_EXACT_IN'
        decoded_swap_path = codec.decode.v3_path(fun_name,input_swap_path)
        try:
            data = {}
            data['amountIn'] = main_input['inputs'][1][1]["amountIn"]
            data['aountOut'] = main_input['inputs'][1][1]['amountOutMin']
            data['tokenIn'] = decoded_swap_path [0]
            data['tokenOut'] = decoded_swap_path [-1]
            return data
        except:
            data = {}
            data['amountIn'] = main_input['inputs'][1][1]["amountInMax"]
            data['aountOut'] = main_input['inputs'][1][1]['amountOut']
            data['tokenIn'] = decoded_swap_path [-1]
            data['tokenOut'] = decoded_swap_path [0]
            return data
        