CREATE TABLE [dbo].[dimStation] (
    station_key BIGINT,
    from_station NVARCHAR(4000),
    from_station_name NVARCHAR(4000),
    from_station_latitude FLOAT,
    from_station_longitude FLOAT,
    to_station NVARCHAR(4000),
    to_station_name NVARCHAR(4000),
    to_station_latitude FLOAT,
    to_station_longitude FLOAT
)
GO

DECLARE @MaxStationKey int
SET @MaxStationKey = (SELECT ISNULL(MAX(station_key),0)+1 FROM [dbo].[dimStation])
GO

INSERT INTO [dbo].[dimStation] (
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
SELECT DISTINCT ROW_NUMBER() OVER (ORDER BY ss.station_id, es.station_id),
                ss.station_id AS from_station,
                ss."name" AS from_station_name,
                ss.latitude AS from_station_latitude,
                ss.longitude AS from_station_longitude,
                es.station_id AS to_station,
                es."name" AS to_station_name,
                es.latitude AS to_station_latitude,
                es.longitude AS to_station_longitude
FROM [dbo].[trip] AS t
JOIN [dbo].[station] AS ss ON t.start_station_id = ss.station_id
JOIN [dbo].[station] AS es ON t.end_station_id = es.station_id
GO

SELECT TOP 100 * FROM [dbo].[dimStation]
GO