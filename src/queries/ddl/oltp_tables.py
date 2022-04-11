create_account_table = """
CREATE TABLE account (
    account_number INTEGER PRIMARY KEY, 
    account_start_date DATE, 
    account_end_date DATE, 
    is_member BOOLEAN
)
"""

create_rider_table = """
CREATE TABLE rider (
    rider_id INTEGER PRIMARY KEY, 
    "first" VARCHAR(50), 
    "last" VARCHAR(50), 
    address VARCHAR(100), 
    birthday DATE,
    account_number INTEGER REFERENCES account (account_number)
)
"""

create_payment_table = """
CREATE TABLE payment (
    payment_id INTEGER PRIMARY KEY, 
    "date" DATE, 
    amount MONEY, 
    account_number INTEGER REFERENCES account (account_number)
)
"""

create_station_table = """
CREATE TABLE station (
    station_id VARCHAR(50) PRIMARY KEY, 
    "name" VARCHAR(75), 
    latitude FLOAT, 
    longitude FLOAT
)
"""

create_trip_table = """
CREATE TABLE trip (
    trip_id VARCHAR(50) PRIMARY KEY, 
    rideable_type VARCHAR(75), 
    start_at TIMESTAMP, 
    ended_at TIMESTAMP, 
    start_station_id VARCHAR(50), 
    end_station_id VARCHAR(50), 
    rider_id INTEGER REFERENCES rider (rider_id)
)
"""
