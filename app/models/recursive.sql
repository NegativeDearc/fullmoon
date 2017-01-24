SELECT STRFTIME ("%Y%m", [Article].[create_date]) AS [archive], 
       COUNT (STRFTIME ("%Y%m", [Article].[create_date])) AS [count]
FROM   [Article];