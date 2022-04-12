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

CREATE EXTERNAL TABLE account (
	[account_number] BIGINT,
	[account_start_date] DATETIME2,
	[account_end_date] DATETIME2,
	[is_member] BIT
	)
	WITH (
	LOCATION = 'publicaccount.txt',
	DATA_SOURCE = [divvyfs_divvy_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDelimitedTextFormat]
	)
GO


SELECT TOP 100 * FROM [dbo].[account]
GO