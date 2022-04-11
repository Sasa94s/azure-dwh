create_staging_rider_table = """
CREATE TABLE staging_rider (
    rider_id INTEGER PRIMARY KEY, 
    first VARCHAR(50), 
    last VARCHAR(50), 
    address VARCHAR(100), 
    birthday DATE, 
    account_start_date DATE, 
    account_end_date DATE, 
    is_member BOOLEAN
)
"""

create_staging_payment_table = """
CREATE TABLE staging_payment (
    payment_id INTEGER PRIMARY KEY, 
    date DATE, 
    amount MONEY, 
    rider_id INTEGER
)
"""

create_staging_station_table = """
CREATE TABLE staging_station (
    station_id VARCHAR(50) PRIMARY KEY, 
    "name" VARCHAR(75), 
    latitude FLOAT, 
    longitude FLOAT
)
"""

create_staging_trip_table = """
CREATE TABLE staging_trip (
    trip_id VARCHAR(50) PRIMARY KEY, 
    rideable_type VARCHAR(75), 
    start_at TIMESTAMP, 
    ended_at TIMESTAMP, 
    start_station_id VARCHAR(50), 
    end_station_id VARCHAR(50), 
    rider_id INTEGER
)
"""
