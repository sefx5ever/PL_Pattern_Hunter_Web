import pandas as pd
import environ, asyncio
from binance.client import Client
from channels.db import database_sync_to_async
from ..models import SymbolHistoryData

class PatternHunterScrapy:
    def __init__(self):
        env = environ.Env()
        environ.Env.read_env('../../Web_Pattern_Hunter/.env')
        binance_api_key = env('BINANCE_API_KEY')    
        binance_api_secret = env('BINANCE_API_SECRET') 

        ### CONSTANTS
        self.BINSIZES = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
        self.BATCH_SIZE = 750
        self.BINANCE_CLIENT = Client(api_key=binance_api_key, api_secret=binance_api_secret)

    def get_binance_latest_datetime(self,symbol,kline_size):
        return pd.to_datetime(self.BINANCE_CLIENT.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')

    def get_db_latest_datetime(self,symbol,kline_size):
        share_data = SymbolHistoryData.objects.filter(symbol=symbol,kline_size=kline_size)
        return share_data[-1]['datetime']

    def get_all_binance(self,symbol,kline_size,start_date,end_date):
        try:
            new_time = end_date or self.get_binance_latest_datetime(symbol,kline_size)
            old_time = start_date or self.get_db_latest_datetime(symbol,kline_size)
            klines = self.BINANCE_CLIENT.get_historical_klines(symbol, kline_size, old_time.strftime("%Y-%m-%d %H:%M:%S"), new_time.strftime("%Y-%m-%d %H:%M:%S"))
            data = pd.DataFrame(klines, columns = ['timestamp','open','high','low','close','volume','close_time','quote_av','trades','tb_base_av','tb_quote_av','ignore'])
            data = data[['timestamp','open','high','low','close','volume']]
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            result_save = self.__save_data_to_db(symbol,kline_size,data)
            return True if result_save else False
        except Exception as err:
            # raise ValueError(str(err))
            print(err,symbol,kline_size,start_date,end_date)

    def __save_data_to_db(self,symbol,kline_size,data):
        batch_list = []
        rows = data.values.tolist()
        for no,row in enumerate(rows):
            batch_list.append(
                SymbolHistoryData(
                    symbol = symbol,
                    open_price = row[1],
                    high_price = row[2],
                    low_price = row[3],
                    close_price = row[4],
                    volume = row[5],
                    kline_size = kline_size,
                    datetime = row[0]
                )
            )
            print(f'Fetching {symbol} data to database in ... {no+1}/{len(rows)}')
        return self.__save(batch_list)
        
    def __save(self,batch_list):
        database_sync_to_async(SymbolHistoryData.objects.bulk_create(batch_list,ignore_conflicts=True))()
        return True

