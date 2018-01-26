import pandas as pd
import sqlalchemy
import pytz


def upload_to_db(symbol1, symbol2):
    db_uri = 'sqlite:///{}_{}.sqlite'.format(symbol1, symbol2)
