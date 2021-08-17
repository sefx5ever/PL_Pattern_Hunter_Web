from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from django.core.serializers.json import DjangoJSONEncoder
from API.Channel_Doc.web_scrapy import PatternHunterScrapy
from datetime import datetime as dt
from .Channel_Doc.module import PatternHunterModel
from .models import Account, SymbolHistoryData, ResearcherModel
import json

class WSDataShare(WebsocketConsumer):
    def connect(self):
        self.accept()
        # self.send(json.dumps('Welcome to Pattern Hunter!'))
    
    def receive(self,text_data=None,bytes_data=None):
        text_data_json = json.loads(text_data)
        if  (('account' in text_data_json) and ({'user','password'} <= text_data_json.keys()) and \
            (self.__is_account_active(text_data_json['account']['user']),text_data_json['account']['password'])) or \
            (self.__is_authenticate(text_data_json['hash_value'])):
            scrapy = ModelQuery()
            data = scrapy.query_data(text_data_json)
            stop_date = self.run_pred_model(data)
            print(stop_date)
            print('finish')
        else:
            self.close()

    def run_pred_model(self,result_data):
        pred_model = PatternHunterModel()
        len_ = len(result_data)
        data_to_send = []
        for no in range(len_):
            if (len(data_to_send)%50 == 0):
                self.__send(data_to_send)
                data_to_send = []
            if (no+10 < len_):
                input_data = self.__convert_data_10(result_data[no:no+10])
                gasf = pred_model.reshape_to_gasf(input_data)
                result_predict = pred_model.predict(gasf)
                result_data[no].predict = result_predict[0]
                print(result_predict[0])
                data_to_send.append(
                    self.convert_data(result_data[no])
                )
            else:
                self.__send(data_to_send)
                return result_data[no].datetime

    def convert_data(self,data):
        return {
            'date' : data.datetime, 'open' : data.open_price,
            'low' : data.low_price, 'high' : data.high_price,
            'close': data.close_price, 'volume' : data.volume,
            'predict' : data.predict
        }

    def __send(self,data):
        self.send(json.dumps(data,cls=DjangoJSONEncoder,default=str))

    def __convert_data_10(self,data):
        temp = []
        for each in data:
            temp.append([
                each.open_price,each.low_price,
                each.high_price,each.close_price
            ])
        return temp

    def __is_account_active(self,user:str,password:str):
        return authenticate(user=user,password=password)

    def __is_authenticate(self,hash_value:str):
        return True if Account.objects.filter(hash_value=hash_value) else False

    def __get_hash(self,user:str):
        return Account.objects.filter(user=user)[0].hash

class ModelQuery:
    def query_data(self,symbol):
        if ({'user','symbol','kline_size','start_date','end_date'} <= symbol.keys()):
            result_researcher = self.__is_researcher_exist(symbol['user'])
            result_data = self.__is_data_exist(
                symbol['symbol'],symbol['kline_size'],
                symbol['start_date'],symbol['end_date']
            )
            if result_researcher and result_data:
                return result_data
        return False


    def __get_symbol_data(self,symbol,kline_size,start_date,end_date):
        return list(SymbolHistoryData.objects.filter(
            symbol=symbol,kline_size=kline_size,
            datetime__range=(start_date,end_date)
        ).order_by('datetime'))

    def __is_researcher_exist(self,user):
        account = Account.objects.filter(user=user)
        return True if account[0].role else False

    def __is_data_exist(self,symbol,kline_size,start_date,end_date):
        share_data = self.__get_symbol_data(symbol,kline_size,start_date,end_date)
        web_scrapy = PatternHunterScrapy()
        start_date = self.__convert_to_datetime(start_date)
        end_date = self.__convert_to_datetime(end_date)
        minutes = (end_date-start_date).total_seconds()/60
        expect_data_len = int(minutes/web_scrapy.BINSIZES[kline_size])
        if (isinstance(share_data,list)) and (len(share_data) >= expect_data_len):
            return share_data
        else:
            return self.__scrape_symbol_data(
                web_scrapy,share_data,symbol,kline_size,
                start_date,end_date
            )

    def __scrape_symbol_data(self,web_scrapy,share_data,symbol,kline_size,start_date,end_date):
        if share_data:
            obj_start_date = self.__convert_to_datetime(share_data[0].datetime)
            obj_end_date = self.__convert_to_datetime(share_data[-1].datetime)
            partition_start_date,partition_end_date = self.__get_scrape_data_dt(
                start_date,end_date,obj_start_date,obj_end_date
            )
        else:
            partition_start_date = start_date
            partition_end_date = end_date
        web_scrapy.get_all_binance(symbol,kline_size,partition_start_date,partition_end_date)
        return self.__get_symbol_data(symbol,kline_size,start_date,end_date)

    def __convert_to_datetime(self,dt_text):
        return dt.strptime(str(dt_text)[:19],"%Y-%m-%d %H:%M:%S")

    def __get_scrape_data_dt(self,start_date,end_date,obj_start,obj_end):
        if (start_date >= obj_start):
            return obj_end,end_date
        else:
            return start_date,obj_start