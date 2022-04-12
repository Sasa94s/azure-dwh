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

CREATE EXTERNAL TABLE [payment] (
	[payment_id] BIGINT,
	[date] DATETIME2,
	[amount] MONEY,
	[account_number] BIGINT
	)
	WITH (
	LOCATION = 'publicpayment.txt',
	DATA_SOURCE = [divvyfs_divvy_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDelimitedTextFormat]
	)
GO


SELECT TOP 100 * FROM [dbo].[payment]
GO