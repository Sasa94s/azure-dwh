CREATE TABLE [dbo].[factPayment] (
    payment_date_key INT,
    account_key INT,
    rider_key INT,
    payment_amount MONEY
)
GO

INSERT INTO [dbo].[factPayment] (
    payment_date_key,
    account_key,
    rider_key,
    payment_amount
)
SELECT dd.date_key   AS payment_date_key,
       da.account_key,
       dr.rider_key,
       SUM(p.amount) AS payment_amount
FROM rider AS r
         JOIN account AS a ON a.account_number = r.account_number
         JOIN "dimRider" dr ON dr.rider_key = r.rider_id
         JOIN "dimAccount" da ON da.account_key = a.account_number
         JOIN payment AS p ON p.account_number = a.account_number
         JOIN "dimDate" dd on p.date = dd.date
GROUP BY dd.date_key, da.account_key, dr.rider_key
GO


SELECT TOP 100 * FROM [dbo].[factPayment]
GO

