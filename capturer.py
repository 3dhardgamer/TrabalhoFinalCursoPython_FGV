import pandas as pd
import datetime
import requests
import json
import pytz
import time
from sqlalchemy import create_engine


class Capturer:

    def __init__(self, pair, exchange = 'cex'):
        '''
        symbol1   -> Cryptocurrency acronym (string).
        symbol2   -> Currency acronym (string).
        '''
        self.exchange = exchange
        self.pair = pair
        self.symbol1 = self.pair.split('/')[0].upper()
        self.symbol2 = self.pair.split('/')[1].upper()
        self.conn = create_engine('sqlite:///{}_{}.sqlite'.format(self.symbol1, self.symbol2))


    def create_date_list(self):
        '''
        create_date_list():
        returns a list of dates from start to end with format 'YYYYMMDD' and type string.
        '''

        step = datetime.timedelta(days = 1)
        date_list = list()
        start = self.start
        while start <= self.end:
            date_list.append(str(start.date()).replace('-', ''))
            start += step

        return date_list


    def create_url_list(self):
        '''
        create_url_list():
        returns a list of urls from start to end date of the symbol1/symbol2 transaction.
        '''

        date_list = self.create_date_list()
        url_list = list()
        for date in date_list:
            url = 'http://cex.io/api/ohlcv/hd/{}/{}/{}'.format(date, self.symbol1, self.symbol2)
            url_list.append(url)

        return url_list


    def get_ohlcv(self, start, end, data_rate = 'data1m'):
        '''
        get_ohlcv(start, end, data_rate):
        returns a string with all read fetched data from cex.io for the given pair symbol1/symbol2 between
        the starting and ending dates and with data rate (1m, 1h or 1d).

        Function has a one second sleep to avoid exploding rate limit of exchange (cex.io).
        Cex rate limit is 600 requests per 10 minutes (1 request per second).

        parameters:
        start     -> Starting date with format 'YYYY-MM-DD' (string).
        end       -> Ending date with format 'YYYY-MM-DD' (string).
        data_rate -> Data rate, cex.io gives the following options: 'data1m', 'data1h' or 'data1d'.
        '''
        self.start = datetime.datetime.strptime(start, '%Y-%m-%d')
        self.end = datetime.datetime.strptime(end, '%Y-%m-%d')
        url_list = self.create_url_list()

        # time_sleep: guarantees that no more than 1 request per second is done.
        time_sleep = 1.1
        print('Number of urls = {}'.format(len(url_list)))
        print('Time sleep = {}'.format(time_sleep))
        count_input = 0
#        data_ohlcv_list = []
        for url in url_list:
            print('Reading {} -----'.format(url))
            ohlcv = eval(requests.get(url).json()[data_rate])
#            data_ohlcv_list.append(ohlcv)
            print('Now upload')
            self.upload_to_db(ohlcv)
            print('Fetch input data size {}'.format(len(ohlcv)))
            count_input += len(ohlcv)

            print('Finished -----')
            time.sleep(time_sleep)

        print('Total number of inputs {}'.format(count_input))
#        return str([item for sublist in data_ohlcv_list for item in sublist])


    def upload_to_db(self, ohlcv):
        self.test = ohlcv

        time_format = '%Y-%m-%d %H:%M:%S'
        date_utc = lambda x: datetime.datetime.fromtimestamp(x, tz = pytz.utc)
        format_date = lambda x: datetime.datetime.replace(date_utc(x), tzinfo = None)

        data = pd.DataFrame(ohlcv, columns = ['date', 'open', 'high', 'low', 'close', 'volume'])
        data['date'] = pd.to_datetime(data['date'].apply(format_date, format = time_format))
        data.set_index('date', inplace = True)
        data.to_sql('{}_{}.sqlite'.format(self.symbol1, self.symbol2), self.conn, if_exists = 'append')
