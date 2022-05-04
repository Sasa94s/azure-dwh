CREATE TABLE [dbo].[factTrip] (
    trip_id NVARCHAR(100),
    account_key INT,
    rider_key INT,
    station_key INT,
    rideable_type NVARCHAR,
    started_at DATETIME2,
    ended_at DATETIME2,
    trip_start_date_key INT,
    trip_end_date_key INT,
    trip_duration INT,
    rider_age_on_trip INT
)
GO

INSERT INTO [dbo].[factTrip] (
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
       DATEDIFF(minute, t.start_at, t.ended_at) AS trip_duration,
       sub.rider_age_on_trip
FROM (SELECT DISTINCT da.account_key,
                      dr.rider_key,
                      (0 + CONVERT(VARCHAR(8), SYSDATETIME(), 112) - CONVERT(VARCHAR(8), dr.birthday, 112)) / 10000 AS rider_age_on_trip
      FROM rider AS r
               JOIN account AS a ON a.account_number = r.account_number
               JOIN "dimRider" dr ON dr.rider_key = r.rider_id
               JOIN "dimAccount" da ON da.account_key = a.account_number) AS sub
         JOIN trip AS t ON sub.rider_key = t.rider_id
         JOIN "dimStation" AS ds ON ds.from_station = t.start_station_id AND
                                    ds.to_station = t.end_station_id
         JOIN "dimDate" dds ON dds.date = t.start_at
         JOIN "dimDate" dde ON dde.date = t.ended_at
GO


SELECT TOP 100 * FROM [dbo].[factTrip]
GO

