CREATE TABLE [dbo].[dimDate] (
    date_key BIGINT,
    [date]  DATETIME2,
    day_number_of_week INT,
    [month] INT,
    quarter INT,
    [year] INT,
    day_number_of_month INT,
    day_number_of_year INT,
    week_number_of_year INT
)
GO

INSERT INTO "dimDate" (
    date_key,
    [date],
    day_number_of_week,
    [month],
    quarter,
    [year],
    day_number_of_month,
    day_number_of_year,
    week_number_of_year
)
SELECT DISTINCT ROW_NUMBER() OVER(ORDER BY p.[date]),
                p.[date],
                DATEPART(weekday, p.[date]) AS day_number_of_week,
                DATEPART(month, p.[date]) AS "month",
                DATEPART(quarter, p.[date]) AS quarter,
                DATEPART(year, p.[date]) AS "year",
                DATEPART(day, p.[date]) AS day_number_of_month,
                DATEPART(dayofyear, p.[date]) AS day_number_of_year,
                DATEPART(iso_week, p.[date]) AS week_number_of_year
FROM payment AS p
JOIN account AS a ON p.account_number = a.account_number
JOIN rider AS r ON a.account_number = r.account_number
JOIN trip AS t ON r.rider_id = t.rider_id
GROUP BY p."date"
UNION ALL
SELECT DISTINCT ROW_NUMBER() OVER(ORDER BY t.[start_at]),
                t.[start_at],
                DATEPART(weekday, t.[start_at]) AS day_number_of_week,
                DATEPART(month, t.[start_at]) AS "month",
                DATEPART(quarter, t.[start_at]) AS quarter,
                DATEPART(year, t.[start_at]) AS "year",
                DATEPART(day, t.[start_at]) AS day_number_of_month,
                DATEPART(dayofyear, t.[start_at]) AS day_number_of_year,
                DATEPART(iso_week, t.[start_at]) AS week_number_of_year
FROM trip AS t
GROUP BY t.[start_at]
UNION ALL
SELECT DISTINCT ROW_NUMBER() OVER(ORDER BY t.[ended_at]),
                t.[ended_at],
                DATEPART(weekday, t.[ended_at]) AS day_number_of_week,
                DATEPART(month, t.[ended_at]) AS "month",
                DATEPART(quarter, t.[ended_at]) AS quarter,
                DATEPART(year, t.[ended_at]) AS "year",
                DATEPART(day, t.[ended_at]) AS day_number_of_month,
                DATEPART(dayofyear, t.[ended_at]) AS day_number_of_year,
                DATEPART(iso_week, t.[ended_at]) AS week_number_of_year
FROM trip AS t
GROUP BY t.[ended_at]
GO


SELECT TOP 100 * FROM [dbo].[dimDate]
GO

