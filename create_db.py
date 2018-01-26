from sqlalchemy import *


def create_db(symbol1, symbol2):
    '''
    create_db():
    creates the database for the given pair (symbol1/symbol2)
    '''

    db_uri = 'sqlite:///{}_{}.sqlite'.format(symbol1, symbol2)
    engine = create_engine(db_uri, echo = False)

    metadata = MetaData(engine)

    db_session = Table(db_uri, metadata,
                Column('date', DateTime, primary_key = True),
                Column('open', Float),
                Column('high', Float),
                Column('low', Float),
                Column('close', Float),
                Column('volume', Float),)

    db_session.create()

