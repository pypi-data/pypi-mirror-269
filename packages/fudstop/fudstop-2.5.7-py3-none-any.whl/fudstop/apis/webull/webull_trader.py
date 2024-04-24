import os
from dotenv import load_dotenv
load_dotenv()
import httpx
import asyncio
from .trader_models.trader_models import Capital, DT_DAY_DETAIL_LIST, Positions, OpenPositions
account_id = os.environ.get('webull_account_id')
from datetime import datetime, timedelta

from .trader_models.trader_models import OptionData

class WebulLTrader:
    def __init__(self):
        self.account_id = account_id
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        self.headers = {
        "Access_token": os.environ.get('ACCESS_TOKEN'),
        "App": "global",

        "App-Group": "broker",
        "Appid": "wb_web_app",
        "Content-Type": "application/json",
        "Device-Type": "Web",
        "Did": os.environ.get('DID'),
        "Hl": "en",
        "Locale": "eng",
        "Os": "web",
        "Osv": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Ph": "Windows Chrome",
        "Platform": "web",
        "Referer": "https://app.webull.com/",
        
    }
        
    async def update_trade_token(self):
        payload = { 'pwd': '5ad14adc3d09d9517fecfb031e3676e9'}
        endpoint = f"https://u1suser.webullfintech.com/api/user/v1/security/login"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint, json=payload, headers=self.headers)
            data = data.json()
            token = data.get('tradeToken')
            
            return token
    

    async def get_account_detail(self, account_id:str=account_id):
        """Gets trading summary."""
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/asset/summary?secAccountId={account_id}"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()
            print(data)
            capital = data['capital']

            return Capital(capital)
        

    async def profit_loss(self):
        endpoint=f"https://ustrade.webullfinance.com/api/trading/v1/webull/profitloss/account/getProfitlossAccountSummary?secAccountId=12165004&startDate=2024-04-19&endDate=2024-04-23"
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            return data


    async def get_option_data(self, option_ids):
        endpoint = f"https://quotes-gw.webullfintech.com/api/quote/option/quotes/queryBatch?derivativeIds={option_ids}"
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            return OptionData(data)


    async def positions(self):
        """RETURNS OPEN POSITIONS AND ACCOMPANYING DATA"""
        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/asset/summary?secAccountId={account_id}"
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            pos = data['positions']
            items = [i.get('items') for i in pos]
            items = [item for sublist in items for item in sublist]

            positions = Positions(data['positions'])

            open_positions = OpenPositions(items)

            option_ids = open_positions.tickerId

            option_ids_str = ','.join(map(str, option_ids))

            option_data = f"https://quotes-gw.webullfintech.com/api/quote/option/quotes/queryBatch?derivativeIds={option_ids_str}"

            async with httpx.AsyncClient() as client:
                data = await client.get(option_data, headers=self.headers)
                data = data.json()
                return open_positions, OptionData(data)






