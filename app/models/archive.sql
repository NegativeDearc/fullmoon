SELECT STRFTIME ("%Y%m", [Article].[create_date]) || "(" || 
       COUNT (STRFTIME ("%Y%m", [Article].[create_date])) || ")" AS [archive]
FROM   [Article]
WHERE  [Article].[author] = "scc"
       AND [Article].[status] = "PUBLISHED";
