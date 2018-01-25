def create_date_list(start, end):
    '''
    create_date_list(start, end):
    returns a list of dates from start to end with format 'YYYYMMDD' and type string.
    
    parameters:
    start -> Starting date with format 'YYYY-MM-DD' (string).
    end   -> Ending date with format 'YYYY-MM-DD' (string).
    '''
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    step = datetime.timedelta(days = 1)
    date_list = list()
    while start <= end:
        date_list.append(str(start.date()).replace('-', ''))
        start += step
        
    return date_list


def create_url_list(symbol1, symbol2, start, end):
    '''
    create_url_list(symbol1, symbol2, start, end):
    returns a list of urls from start to end date of the symbol1/symbol2 transaction.

    parameters:
    symbol1 -> Cryptocurrency acronym (string).
    symbol2 -> Currency acronym (string).
    start   -> Starting date with format 'YYYY-MM-DD' (string).
    end     -> Ending date with format 'YYYY-MM-DD' (string).
    '''

    date_list = create_date_list(start, end)
    url_list = list()
    for date in date_list:
        url = 'http://cex.io/api/ohlcv/hd/{}/{}/{}'.format(date, symbol1, symbol2)
        url_list.append(url)

    return url_list


def get_ohlcv(symbol1, symbol2, start, end, data_rate):
    '''
    get_ohlcv(symbol1, symbol2, start, end, data_rate):
    returns a string with all read fetched data from cex.io for the given pair symbol1/symbol2 between
    the starting and ending dates and with data rate (1m, 1h or 1d).

    Function has a one second sleep to avoid exploding rate limit of exchange (cex.io).
    Cex rate limit is 600 requests per 10 minutes.

    parameters:
    symbol1   -> Cryptocurrency acronym (string).
    symbol2   -> Currency acronym (string).
    start     -> Starting date with format 'YYYY-MM-DD' (string).
    end       -> Ending date with format 'YYYY-MM-DD' (string).
    data_rate -> Data rate, cex.io gives the following options: 'data1m', 'data1h' or 'data1d'.
    '''

    url_list = create_url_list(symbol1, symbol2, start, end)
    # time_sleep: guarantees that no more than 60 request are done per second.
    time_sleep = (len(url_list) / 60) + 0.01
    print('Number of urls = {}'.format(len(url_list)))
    print('Time sleep = {}'.format(time_sleep))
    count_input = 0
    data_ohlcv_list = []
    for url in url_list:
        print('Reading {} -----'.format(url))
        ohlcv = eval(requests.get(url).json()[data_rate])
        data_ohlcv_list.append(ohlcv)
        print('Fetch input data size {}'.format(len(ohlcv)))
        count_input += len(ohlcv)
        print('Finished -----')
        time.sleep(time_sleep)

    print('Total number of inputs {}'.format(count_input))
    return str([item for sublist in data_ohlcv_list for item in sublist])
