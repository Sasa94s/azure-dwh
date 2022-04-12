CREATE TABLE [dbo].[dimRider] (
    rider_key BIGINT,
    address NVARCHAR(4000),
    first_name NVARCHAR(4000),
    last_name NVARCHAR(4000),
    birthday DATETIME2
)
GO

INSERT INTO [dbo].[dimRider] (
    rider_key,
    address,
    first_name,
    last_name,
    birthday
)
SELECT r.rider_id AS rider_key,
       r.address,
       r.[first] AS first_name,
       r.[last] AS last_name,
       r.birthday
FROM [dbo].[rider] AS r
GO

SELECT TOP 100 * FROM [dbo].[dimRider]
GO