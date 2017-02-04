SELECT STRFTIME ("%Y%m", [Article].[create_date]) || "(" || COUNT (*) || ")" AS [archive]
FROM   [Article]
WHERE  [Article].[author] = :a
       AND [Article].[status] = "PUBLISHED"
GROUP  BY STRFTIME ("%Y%m", [Article].[create_date])
ORDER  BY [Article].[create_date];

