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

CREATE EXTERNAL TABLE [station] (
	[station_id] NVARCHAR(4000),
	[name] NVARCHAR(4000),
	[latitude] FLOAT,
	[longitude] FLOAT
	)
	WITH (
	LOCATION = 'publicstation.txt',
	DATA_SOURCE = [divvyfs_divvy_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDelimitedTextFormat]
	)
GO


SELECT TOP 100 * FROM [dbo].[station]
GO