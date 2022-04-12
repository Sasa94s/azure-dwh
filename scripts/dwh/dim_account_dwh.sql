CREATE TABLE [dbo].[dimAccount] (
	[account_key] BIGINT,
	[account_start_date] DATETIME2,
	[account_end_date] DATETIME2,
	[is_member] BIT
)
GO

INSERT INTO [dbo].[dimAccount] (
    account_key,
    account_start_date,
    account_end_date,
    is_member
)
SELECT a.account_number AS account_key,
       a.account_start_date AS start_date,
       a.account_end_date AS end_date,
       a.is_member
FROM [dbo].[account] AS a
GO


SELECT TOP 100 * FROM [dbo].[dimAccount]
GO