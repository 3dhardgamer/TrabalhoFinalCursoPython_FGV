from capturer import Capturer
import os
import datetime
from sqlalchemy import create_engine, MetaData, Table, select

database = 'ohlcv_db.sqlite'


def create_table(pair, start, end):
    capt = Capturer(pair)
    capt.get_ohlcv(start, end)
    print('Table {} is done!\n\n'.format(pair))


def validate_date(moment):
    while True:
        try:
            date = input('Please enter {} date (YYYY-MM-DD): '.format(moment))
            datetime.datetime.strptime(date, '%Y-%m-%d')

        except ValueError:
            print('Incorrect date format, it should be YYYY-MM-DD.')
            continue

        else:
            break
    return date


def ask_dates():
    start_date = validate_date('starting')
    end_date = validate_date('ending')
    if datetime.datetime.strptime(start_date, '%Y-%m-%d') > datetime.datetime.strptime(end_date, '%Y-%m-%d'):
        print('\nEnding date is lower than starting date... contradiction! Ending date should be bigger than starting date.\n')
        end_date = validate_date('ending')

    return [start_date, end_date]


markets = ['BTC/EUR', 'BTC/USD', 'ETH/EUR', 'ETH/USD', 'ZEC/EUR', 'ZEC/USD']

if os.path.isfile(database) == True:
    print('The database already exists!\n')
    engine = create_engine('sqlite:///{}'.format(database))
    metadata = MetaData()
    connection = engine.connect()
    print('The following tables are present: ')
    for table in engine.table_names():
        ohlcv = Table(table, metadata, autoload = True, autoload_with = engine)
        stmt = select([ohlcv])
        ohlcv_data = connection.execute(stmt).fetchall()
        print('{}'.format(table))
        print('start date: {}'.format(ohlcv_data[0][0]))
        print('end date: {}\n'.format(ohlcv_data[-1][0]))

    overwrite = input('Do you want to overwrite the database? ["y" - yes; "n" - no] ')
    if overwrite == 'y':
        print('\nOverwriting the database...\n')
        os.remove(database)

        dates = ask_dates()
        print('\nThis might take a while... please be patient.\n')
        for pair in markets:
            create_table(pair, dates[0], dates[1])

    else:
        print('\nSo proceed to the next section. Thanks! ;)\n')

else:
    print('\nDatabase does not exist yet.\n')
    dates = ask_dates()

    print('\nCreating database...')
    print('This might take a while... please be patient.\n')
    for pair in markets:
        create_table(pair, dates[0], dates[1])


