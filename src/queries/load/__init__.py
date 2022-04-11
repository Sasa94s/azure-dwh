copy_query = """
COPY {table_name} 
FROM '{file_name}' 
DELIMITER ',' CSV
"""

insert_account_table = """
INSERT INTO account (
    account_number,
    account_start_date,
    account_end_date,
    is_member
)
SELECT ROW_NUMBER() OVER (ORDER BY account_start_date) AS account_number,
       r.account_start_date,
       r.account_end_date,
       r.is_member
FROM (SELECT DISTINCT account_start_date,
                      account_end_date,
                      is_member
      FROM staging_rider
      WHERE rider_id IS NOT NULL) AS r
"""

insert_rider_table = """
INSERT INTO rider (
    rider_id,
    "first",
    "last",
    address,
    birthday,
    account_number
)
SELECT DISTINCT sr.rider_id,
                sr."first",
                sr."last",
                sr.address,
                sr.birthday,
                a.account_number
FROM staging_rider sr
JOIN account a ON sr.account_start_date = a.account_start_date AND 
                  sr.account_end_date = a.account_end_date AND 
                  sr.is_member = a.is_member
WHERE rider_id IS NOT NULL
"""

insert_payment_table = """
INSERT INTO payment (
    payment_id,
    "date",
    amount,
    account_number
)
SELECT DISTINCT sp.payment_id,
                sp."date",
                sp.amount,
                a.account_number
FROM staging_payment sp
JOIN rider r ON sp.rider_id = r.rider_id
JOIN account a ON a.account_number = r.account_number
WHERE sp.payment_id IS NOT NULL AND
      r.rider_id IS NOT NULL AND
      a.account_number IS NOT NULL
"""

insert_station_table = """
INSERT INTO station (
    station_id,
    "name",
    latitude,
    longitude
)
SELECT DISTINCT station_id,
                "name",
                latitude,
                longitude
FROM staging_station
WHERE station_id IS NOT NULL
"""

insert_trip_table = """
INSERT INTO trip (
    trip_id,
    rideable_type,
    start_at,
    ended_at,
    start_station_id,
    end_station_id,
    rider_id
)
SELECT DISTINCT st.trip_id,
                st.rideable_type,
                st.start_at,
                st.ended_at,
                st.start_station_id,
                st.end_station_id,
                st.rider_id
FROM staging_trip st
JOIN rider r ON st.rider_id = r.rider_id 
WHERE st.trip_id IS NOT NULL
"""
