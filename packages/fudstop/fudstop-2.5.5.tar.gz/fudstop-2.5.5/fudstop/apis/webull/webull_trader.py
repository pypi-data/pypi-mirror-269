import os
from dotenv import load_dotenv
load_dotenv()
import httpx
import asyncio
from .trader_models.trader_models import Capital, DT_DAY_DETAIL_LIST, Positions, OpenPositions
account_id = os.environ.get('webull_account_id')




class WebulLTrader:
    def __init__(self):
        self.account_id = account_id


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
        "T_Token": os.environ.get('TRADE_TOKEN')
    }
        

    

    async def get_account_detail(self, account_id:str=account_id):
        """Gets trading summary."""

        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/asset/summary?secAccountId={account_id}"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            capital = data['capital']

            return Capital(capital)
        

    async def profit_loss(self):
        endpoint=f"https://ustrade.webullfinance.com/api/trading/v1/webull/profitloss/account/getProfitlossAccountSummary?secAccountId=12165004&startDate=2024-04-19&endDate=2024-04-23"

        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            return data




    async def positions(self):
        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/asset/summary?secAccountId={account_id}"

        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            pos = data['positions']
            items = [i.get('items') for i in pos]
            items = [item for sublist in items for item in sublist]

            positions = Positions(data['positions'])

            open_positions = OpenPositions(items)

            return open_positions
