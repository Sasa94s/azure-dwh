CREATE TABLE [dbo].[factTrip] (
    trip_id NVARCHAR(100),
    account_key INT,
    rider_key INT,
    station_key INT,
    rideable_type NVARCHAR,
    started_at DATETIME2,
    ended_at DATETIME2,
    rider_age_on_trip INT
)
GO

INSERT INTO [dbo].[factTrip] (
    trip_id,
    account_key,
    rider_key,
    station_key,
    rideable_type,
    started_at,
    ended_at,
    rider_age_on_trip
)
SELECT t.trip_id,
       sub.account_key,
       sub.rider_key,
       ds.station_key,
       t.rideable_type,
       t.start_at,
       t.ended_at,
       sub.rider_age_on_trip
FROM (SELECT DISTINCT da.account_key,
                      dr.rider_key,
                      DATEDIFF(year, dr.birthday, GETDATE()) AS rider_age_on_trip
      FROM rider AS r
               JOIN account AS a ON a.account_number = r.account_number
               JOIN "dimRider" dr ON dr.rider_key = r.rider_id
               JOIN "dimAccount" da ON da.account_key = a.account_number) AS sub
         JOIN trip AS t ON sub.rider_key = t.rider_id
         JOIN "dimStation" AS ds ON ds.from_station = t.start_station_id AND
                                    ds.to_station = t.end_station_id
GO


SELECT TOP 100 * FROM [dbo].[factTrip]
GO

