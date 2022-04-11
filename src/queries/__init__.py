import configparser

# CONFIG
import os

from queries.ddl.staging_tables import *
from queries.ddl.oltp_tables import *
from queries.ddl.olap_tables import *
from queries.load import *
from queries.transform import *

config = configparser.ConfigParser()
config.read('dwh.cfg')
dirname = os.path.dirname(__file__)

# TABLE NAMES

main_tables_info = [
    {'table_name': 'staging_trip'},
    {'table_name': 'staging_payment'},
    {'table_name': 'staging_station'},
    {'table_name': 'staging_rider'},
    {'table_name': 'trip'},
    {'table_name': 'station'},
    {'table_name': 'payment'},
    {'table_name': 'rider'},
    {'table_name': 'account'},
    {'table_name': '"dimAccount"'},
    {'table_name': '"dimRider"'},
    {'table_name': '"dimStation"'},
    {'table_name': '"dimDate"'},
    {'table_name': '"factTrip"'},
]

staging_tables_info = [
    {'table_name': 'staging_rider', 'file_name': os.path.join(dirname, '../data/riders.csv')},
    {'table_name': 'staging_station', 'file_name': os.path.join(dirname, '../data/stations.csv')},
    {'table_name': 'staging_payment', 'file_name': os.path.join(dirname, '../data/payments.csv')},
    {'table_name': 'staging_trip', 'file_name': os.path.join(dirname, '../data/trips.csv')}
]


# DROP TABLES

drop_table = """
DROP TABLE IF EXISTS {table_name}
"""

# QUERY LISTS

create_table_queries = [
    create_staging_rider_table,
    create_staging_payment_table,
    create_staging_station_table,
    create_staging_trip_table,
    create_account_table,
    create_rider_table,
    create_payment_table,
    create_station_table,
    create_trip_table,
    create_dim_account_table,
    create_dim_rider_table,
    create_dim_date_table,
    create_dim_station_table,
    create_fact_trip_table
]
drop_table_queries = [drop_table.format(**main_table) for main_table in main_tables_info]
copy_table_queries = [copy_query.format(**staging_table) for staging_table in staging_tables_info]
insert_table_queries = [
    insert_account_table,
    insert_rider_table,
    insert_payment_table,
    insert_station_table,
    insert_trip_table,
    insert_dim_account_table,
    insert_dim_rider_table,
    insert_dim_station_table,
    insert_dim_date_table,
    insert_fact_trip_table
]
