"""
Creates a new SQLite DataBase if it does not exist.

Usage:
    initialize_db <config_uri>
"""

import os
import sys

from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from geruapp.models import Base, DBSession, PageRequests

def usage(argv):
    """
    Print the command usage and exit
    """

    cmd = os.path.basename(argv[0])
    print('usage: {} <config_uri>'.format(cmd))
    print('example: {} development.ini'.format(cmd))
    sys.exit(1)

def main(argv = sys.argv):
    """Create the database if configuration is found"""

    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]

    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    DBSession.commit()
    
