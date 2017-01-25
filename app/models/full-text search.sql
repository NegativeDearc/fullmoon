DROP TABLE IF EXISTS [docs];

CREATE VIRTUAL TABLE [docs] USING [fts4](
    uuid, 
    content);

INSERT INTO [docs]
    ([docs])
    VALUES ('optimize');

INSERT INTO [docs]
    ([uuid], 
    [content])
    SELECT [Article].[uuid], 
       [Article].[content]
FROM   [Article];

SELECT [uuid], 
       SNIPPET ([docs], '<b style="color:red";>', '</b>', '...', 1, 10) AS [content]
FROM   [docs]
WHERE  [docs] MATCH '"20170124165204*"';

--DROP TABLE IF EXISTS [docs];
--
--CREATE VIRTUAL TABLE [docs] USING [fts5](
--    uuid, 
--    content);
--
--INSERT INTO [docs]
--    ([docs])
--    VALUES ('optimize');
--
--INSERT INTO [docs]
--    ([uuid], 
--    [content])
--    SELECT [Article].[uuid], 
--       [Article].[content]
--FROM   [Article];
--
--SELECT [uuid], 
--       SNIPPET ([docs], 1, '<b style="color:red";>', '</b>', '...', 15) AS [content]
--FROM   [docs]
--WHERE  [docs] MATCH '"20170124165204*"';
--
--DROP TABLE IF EXISTS [docs];
--
--CREATE VIRTUAL TABLE [docs] USING [fts5](
--    uuid, 
--    content);
--
--INSERT INTO [docs]
--    ([docs])
--    VALUES ('optimize');
--
--INSERT INTO [docs]
--    ([uuid], 
--    [content])
--    SELECT [Article].[uuid], 
--       [Article].[content]
--FROM   [Article];
--
--SELECT [uuid], 
--       HIGHLIGHT ([docs], 1, '<b style="color:red";>', '</b>') AS [content]
--FROM   [docs]
--WHERE  [docs] MATCH '"20170124165204*"';
--
--