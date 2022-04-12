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

CREATE EXTERNAL TABLE [rider] (
	[rider_id] BIGINT,
	[first] NVARCHAR(4000),
	[last] NVARCHAR(4000),
	[address] NVARCHAR(4000),
	[birthday] DATETIME2,
	[account_number] BIGINT
	)
	WITH (
	LOCATION = 'publicrider.txt',
	DATA_SOURCE = [divvyfs_divvy_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDelimitedTextFormat]
	)
GO


SELECT TOP 100 * FROM [dbo].[rider]
GO