# FTX-Trader

## What It Is

Webhook TradingView Alert order execution for FTX Leveraged Contracts

## How To Use

Create a new screen session > screen -S FTX-Trader

Enter your api key and api secret on lines 19 and 20 of ftx_webhook_functions.py

Run the following one-liner, replacing <YOUR_NGROK_AUTHTOKEN> with your token

sudo apt update && sudo apt upgrade -y && sudo apt install unzip -y && sudo apt install python3.7 -y && sudo apt-get install python3-pip -y && sudo apt-get install python3-venv -y && git clone https://github.com/zalzibab/ftx_trader.git && cd ftx_trader && python3 -m venv env && source env/bin/activate && python -m pip install -r requirements.txt && wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip && unzip ngrok-stable-linux-amd64.zip && ./ngrok authtoken <YOUR_NGROK_AUTHTOKEN> && ./ngrok http 5000

Enter Tradingview Alerts Message in the Following Format

Example to long SUSHI-PERP: '{'contract': 'SUSHI-PERP', 'side': 'buy'}'

Example to short BTC-PERP: '{'contract': 'BTC-PERP', 'side': 'sell'}'

Example to execute stop order on UNI-PERP: '{'contract': 'UNI-PERP', 'side': 'stop'}'

You can also use subaccounts by adding the 'subaccount' dictionary key to your TV Alert Msg
Example to long SOL-PERP on 'UpOnly' Subaccount: '{'contract': 'SOL-PERP', 'side': 'buy', 'subaccount': 'UpOnly'}'

Input the http address from your ngrok tunnel to the webhook alert section of
the Tradingview Alert, and add /webhook to the end

Create a new screen within active session

source env/bin/activate && python ftx_webhook_app.py

Detach from screen session
