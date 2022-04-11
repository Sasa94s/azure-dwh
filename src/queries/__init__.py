import configparser
import os

from queries.ddl.olap_tables import *
from queries.ddl.oltp_tables import *
from queries.ddl.staging_tables import *
from queries.load import *
from queries.transform import *

config = configparser.ConfigParser()
config.read('dwh.cfg')
dirname = os.path.dirname(__file__)

# TABLES

tables_info = [
    {
        'name': 'staging_rider',
        'create_stmt': create_staging_rider_table,
        'file_name': os.path.join(dirname, '../data/riders.csv'),
    },
    {
        'name': 'staging_payment',
        'create_stmt': create_staging_payment_table,
        'file_name': os.path.join(dirname, '../data/payments.csv'),
    },
    {
        'name': 'staging_station',
        'create_stmt': create_staging_station_table,
        'file_name': os.path.join(dirname, '../data/stations.csv'),
    },
    {
        'name': 'staging_trip',
        'create_stmt': create_staging_trip_table,
        'file_name': os.path.join(dirname, '../data/trips.csv'),
    },
    {
        'name': 'account',
        'create_stmt': create_account_table,
        'insert_stmt': insert_account_table,
    },
    {
        'name': 'rider',
        'create_stmt': create_rider_table,
        'insert_stmt': insert_rider_table,
    },
    {
        'name': 'payment',
        'create_stmt': create_payment_table,
        'insert_stmt': insert_payment_table,
    },
    {
        'name': 'station',
        'create_stmt': create_station_table,
        'insert_stmt': insert_station_table,
    },
    {
        'name': 'trip',
        'create_stmt': create_trip_table,
        'insert_stmt': insert_trip_table,
    },
    {
        'name': '"dimAccount"',
        'create_stmt': create_dim_account_table,
        'insert_stmt': insert_dim_account_table,
    },
    {
        'name': '"dimRider"',
        'create_stmt': create_dim_rider_table,
        'insert_stmt': insert_dim_rider_table,
    },
    {
        'name': '"dimDate"',
        'create_stmt': create_dim_date_table,
        'insert_stmt': insert_dim_station_table,
    },
    {
        'name': '"dimStation"',
        'create_stmt': create_dim_station_table,
        'insert_stmt': insert_dim_date_table,
    },
    {
        'name': '"factTrip"',
        'create_stmt': create_fact_trip_table,
        'insert_stmt': insert_fact_trip_table,
    },
]

# DROP TABLES

drop_table = """
DROP TABLE IF EXISTS {name} CASCADE
"""

# QUERY LISTS

create_table_queries = [(table['name'], 'CREATE', table['create_stmt']) for table in tables_info]
drop_table_queries = [(table['name'], 'DROP', drop_table.format(**table)) for table in tables_info]
copy_table_queries = [(table['name'], 'COPY', copy_query.format(**table)) for table in tables_info if
                      'file_name' in table]
insert_table_queries = [(table['name'], 'INSERT', table['insert_stmt']) for table in tables_info if
                        'insert_stmt' in table]
