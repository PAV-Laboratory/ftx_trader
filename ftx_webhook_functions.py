#!/usr/bin/env python
# coding: utf-8


def parse_webhook(webhook_data):
    import ast
    data = ast.literal_eval(webhook_data)
    return data



def order_execution(data):
    #Import Libraries
    import math
    import ftx
    import time
    
    #Create Account Connection
    api_key = ''
    api_secret = ''
    try:
        subaccount = data['subaccount']
    except KeyError:
        subaccount = None
    if subaccount:
        client = ftx.FtxClient(api_key=api_key, api_secret=api_secret, subaccount_name=subaccount)
    else:
        client = ftx.FtxClient(api_key=api_key, api_secret=api_secret)
    
    contract = data['contract'].upper()
    signal = data['side'].lower()
    
    #Get Open Position Data
    _open = [x for x in client.get_positions() if x['size'] != 0 and x['future'] == contract]
    if len(_open) != 0:
        _open = _open[0]
        _side = _open['side']
        _size = _open['size']
    else:
        _side = None
        _size = None
    
    #Close Existing Position
    if _side != signal:
        if _side is not None:
            if signal == 'stop':
                if _side == 'buy':
                    stop_signal = 'sell'
                else:
                    stop_signal = 'buy'
                while True:
                    try:
                        client.place_order(market=contract, side=stop_signal, price=0, size=_size)
                    except Exception as e:
                        print(e)
                        time.sleep(0.5)
                    else:
                        msg = f'''
{contract} Position Closed'''
                        print(msg)
                        break
            else:
                while True:
                    try:
                        client.place_order(market=contract, side=signal, price=0, size=_size)
                    except Exception as e:
                        print(e)
                        time.sleep(0.5)
                    else:
                        msg = f'''
{contract} Position Closed'''
                        print(msg)
                        break
        if signal != 'stop':
            #Open New Position
            while True:
                try:
                    _account = client.get_account_info()
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                else:
                    _collateral = _account['freeCollateral']
                    _leverage = _account['leverage']
                    _balance = _collateral*_leverage
                    break
            while True:
                try:
                    price_data = client.get_future(contract)
                    if signal == 'buy':
                        execution_price = price_data['ask']
                    else:
                        execution_price = price_data['bid']
                    new_size = round(_balance/execution_price*0.98/price_data['sizeIncrement'])*price_data['sizeIncrement']
                    client.place_order(market=contract, side=signal, price=0, size=new_size)
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                else:
                    msg = f'''
{contract} Position Opened
{signal} {new_size} Contracts at ${execution_price}'''
                    print(msg)
                    break
    else:
        msg = f'''
Already in {signal} Side of {contract}'''
        print(msg)
    return 'Order Executed'





