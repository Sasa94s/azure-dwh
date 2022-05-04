create_dim_account_table = """
CREATE TABLE "dimAccount" (
    account_key INTEGER PRIMARY KEY,
    account_type VARCHAR(50),
    start_date DATE,
    end_date DATE
)
"""

create_dim_rider_table = """
CREATE TABLE "dimRider" (
    rider_key INTEGER PRIMARY KEY,
    address VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birthday DATE
)
"""

create_dim_station_table = """
CREATE TABLE "dimStation" (
    station_key SERIAL PRIMARY KEY,
    from_station VARCHAR(50),
    from_station_name VARCHAR(75),
    from_station_latitude FLOAT, 
    from_station_longitude FLOAT,
    to_station VARCHAR(50),
    to_station_name VARCHAR(75),
    to_station_latitude FLOAT, 
    to_station_longitude FLOAT
)
"""

create_dim_date_table = """
CREATE TABLE "dimDate" (
    date_key SERIAL PRIMARY KEY,
    "date"  DATE,
    day_number_of_week INTEGER,
    "month" INTEGER,
    quarter INTEGER,
    "year" INTEGER,
    day_number_of_month INTEGER,
    day_number_of_year INTEGER,
    week_number_of_year INTEGER
)
"""

create_fact_trip_table = """
CREATE TABLE "factTrip" (
    trip_id VARCHAR(50),
    account_key INTEGER,
    rider_key INTEGER,
    station_key INTEGER,
    rideable_type VARCHAR(75),
    trip_start_date_key INTEGER,
    trip_end_date_key INTEGER,
    trip_duration INTEGER,
    rider_age_on_trip INTEGER,
    PRIMARY KEY(trip_id, account_key, rider_key, station_key)
)
"""

create_fact_payment_table = """
CREATE TABLE "factPayment" (
    payment_date_key INTEGER,
    account_key INTEGER,
    rider_key INTEGER,
    payment_amount MONEY,
    PRIMARY KEY(payment_date_key, account_key, rider_key)
)
"""
