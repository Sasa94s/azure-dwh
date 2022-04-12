IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseDelimitedTextFormat')
	CREATE EXTERNAL FILE FORMAT [SynapseDelimitedTextFormat]
	WITH ( FORMAT_TYPE = DELIMITEDTEXT ,
	       FORMAT_OPTIONS (
			 FIELD_TERMINATOR = ',',
			 USE_TYPE_DEFAULT = FALSE
			))
GO

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'divvyfs_divvy_dfs_core_windows_net')
	CREATE EXTERNAL DATA SOURCE [divvyfs_divvy_dfs_core_windows_net]
	WITH (
		LOCATION = 'abfss://divvyfs@divvy.dfs.core.windows.net',
		TYPE = HADOOP
	)
GO

CREATE EXTERNAL TABLE [trip] (
	[trip_id] NVARCHAR(4000),
	[rideable_type] NVARCHAR(4000),
	[start_at] DATETIME2,
	[ended_at] DATETIME2,
	[start_station_id] NVARCHAR(4000),
	[end_station_id] NVARCHAR(4000),
	[rider_id] BIGINT
	)
	WITH (
	LOCATION = 'publictrip.txt',
	DATA_SOURCE = [divvyfs_divvy_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDelimitedTextFormat]
	)
GO


SELECT TOP 100 * FROM [dbo].[trip]
GO