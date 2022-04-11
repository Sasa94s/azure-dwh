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
    station_key,
    from_station,
    from_station_name,
    from_station_latitude,
    from_station_longitude,
    to_station,
    to_station_name,
    to_station_latitude,
    to_station_longitude
)
SELECT ROW_NUMBER() OVER (ORDER BY ss.station_id, es.station_id) AS station_key,
       ss.station_id AS from_station,
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
    date_key,
    "date",
    day_number_of_week,
    "month",
    quarter,
    "year",
    day_number_of_month,
    day_number_of_year,
    week_number_of_year
)
SELECT ROW_NUMBER() OVER (ORDER BY p."date") AS date_key,
       p."date",
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
"""

insert_fact_trip_table = """
INSERT INTO "factTrip" (
    trip_id,
    account_key,
    rider_key,
    station_key,
    payment_date_key,
    rideable_type,
    started_at,
    ended_at,
    payment_amount,
    rider_age_on_trip
)
SELECT t.trip_id,
       sub.account_key,
       sub.rider_key,
       ds.station_key,
       sub.payment_date_key,
       t.rideable_type,
       t.start_at,
       t.ended_at,
       sub.payment_amount,
       sub.rider_age_on_trip
FROM (SELECT DISTINCT da.account_key,
                      dr.rider_key,
                      dd.date_key AS payment_date_key,
                      p.amount AS payment_amount,
                      EXTRACT(YEAR FROM AGE(NOW(), dr.birthday)) AS rider_age_on_trip
      FROM rider AS r
      JOIN account AS a ON a.account_number = r.account_number
      JOIN payment AS p ON p.account_number = a.account_number

      JOIN "dimRider" dr ON dr.rider_key = r.rider_id
      JOIN "dimAccount" da ON da.account_key = a.account_number
      JOIN "dimDate" dd on p.date = dd.date) AS sub
JOIN trip AS t ON sub.rider_key = t.rider_id
JOIN "dimStation" AS ds ON ds.from_station = t.start_station_id AND
                           ds.to_station = t.end_station_id
"""