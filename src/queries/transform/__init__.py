insert_dim_rider_table = """
INSERT INTO "dimRider" (
    rider_key,
    address,
    first_name,
    last_name,
    birthday
)
SELECT rider_id AS rider_key,
       address,
       "first" AS first_name,
       "last" AS last_name,
       birthday
FROM rider
"""

insert_dim_account_table = """
INSERT INTO "dimAccount" (
    account_key,
    account_type,
    start_date,
    end_date
)
SELECT account_number AS account_key,
       CASE WHEN is_member THEN 'MEMBER' ELSE 'CASUAL' END AS account_type,
       account_start_date AS start_date,
       account_end_date AS end_date
FROM account
"""

insert_dim_station_table = """
INSERT INTO "dimStation" (
    from_station,
    from_station_name,
    from_station_latitude,
    from_station_longitude,
    to_station,
    to_station_name,
    to_station_latitude,
    to_station_longitude
)
SELECT DISTINCT ss.station_id AS from_station,
                ss."name" AS from_station_name,
                ss.latitude AS from_station_latitude,
                ss.longitude AS from_station_longitude,
                es.station_id AS to_station,
                es."name" AS to_station_name,
                es.latitude AS to_station_latitude,
                es.longitude AS to_station_longitude
FROM trip AS t
JOIN station AS ss ON t.start_station_id = ss.station_id
JOIN station AS es ON t.end_station_id = es.station_id
"""

insert_dim_date_table = """
INSERT INTO "dimDate" (
    "date",
    day_number_of_week,
    "month",
    quarter,
    "year",
    day_number_of_month,
    day_number_of_year,
    week_number_of_year
)
SELECT DISTINCT p."date",
                EXTRACT(ISODOW FROM p."date") AS day_number_of_week,
                EXTRACT(MONTH FROM p."date") AS "month",
                EXTRACT(QUARTER FROM p."date") AS quarter,
                EXTRACT(YEAR FROM p."date") AS "year",
                EXTRACT(DAY FROM p."date") AS day_number_of_month,
                EXTRACT(DOY FROM p."date") AS day_number_of_year,
                EXTRACT(ISOYEAR FROM p."date") AS week_number_of_year
FROM payment AS p
JOIN account AS a ON p.account_number = a.account_number
JOIN rider AS r ON a.account_number = r.account_number
JOIN trip AS t ON r.rider_id = t.rider_id
GROUP BY p."date"
UNION ALL
SELECT DISTINCT t.start_at,
                EXTRACT(ISODOW FROM t.start_at) AS day_number_of_week,
                EXTRACT(MONTH FROM t.start_at) AS "month",
                EXTRACT(QUARTER FROM t.start_at) AS quarter,
                EXTRACT(YEAR FROM t.start_at) AS "year",
                EXTRACT(DAY FROM t.start_at) AS day_number_of_month,
                EXTRACT(DOY FROM t.start_at) AS day_number_of_year,
                EXTRACT(ISOYEAR FROM t.start_at) AS week_number_of_year
FROM trip AS t
GROUP BY t.start_at
UNION ALL
SELECT DISTINCT t.ended_at,
                EXTRACT(ISODOW FROM t.ended_at) AS day_number_of_week,
                EXTRACT(MONTH FROM t.ended_at) AS "month",
                EXTRACT(QUARTER FROM t.ended_at) AS quarter,
                EXTRACT(YEAR FROM t.ended_at) AS "year",
                EXTRACT(DAY FROM t.ended_at) AS day_number_of_month,
                EXTRACT(DOY FROM t.ended_at) AS day_number_of_year,
                EXTRACT(ISOYEAR FROM t.ended_at) AS week_number_of_year
FROM trip AS t
GROUP BY t.ended_at
"""

insert_fact_trip_table = """
INSERT INTO "factTrip" (
    trip_id,
    account_key,
    rider_key,
    station_key,
    rideable_type,
    trip_start_date_key,
    trip_end_date_key,
    trip_duration,
    rider_age_on_trip
)
SELECT t.trip_id,
       sub.account_key,
       sub.rider_key,
       ds.station_key,
       t.rideable_type,
       dds.date_key AS trip_start_date_key,
       dde.date_key AS trip_end_date_key,
       EXTRACT(MINUTE FROM AGE(t.ended_at, t.start_at)) AS trip_duration,
       sub.rider_age_on_trip
FROM (SELECT DISTINCT da.account_key,
                      dr.rider_key,
                      EXTRACT(YEAR FROM AGE(NOW(), dr.birthday)) AS rider_age_on_trip
      FROM rider AS r
               JOIN account AS a ON a.account_number = r.account_number
               JOIN "dimRider" dr ON dr.rider_key = r.rider_id
               JOIN "dimAccount" da ON da.account_key = a.account_number) AS sub
         JOIN trip AS t ON sub.rider_key = t.rider_id
         JOIN "dimStation" AS ds ON ds.from_station = t.start_station_id AND
                                    ds.to_station = t.end_station_id
         JOIN "dimDate" dds ON dds.date = t.start_at
         JOIN "dimDate" dde ON dde.date = t.ended_at
"""

insert_fact_payment_table = """
INSERT INTO "factPayment" (
    payment_date_key,
    account_key,
    rider_key,
    payment_amount
)
SELECT dd.date_key   AS payment_date_key,
       da.account_key,
       dr.rider_key,
       SUM(p.amount) AS payment_amount
FROM rider AS r
         JOIN account AS a ON a.account_number = r.account_number
         JOIN "dimRider" dr ON dr.rider_key = r.rider_id
         JOIN "dimAccount" da ON da.account_key = a.account_number
         JOIN payment AS p ON p.account_number = a.account_number
         JOIN "dimDate" dd on p.date = dd.date
GROUP BY dd.date_key, da.account_key, dr.rider_key
"""