/* 
   INVENTARIO DWH - Tablas / Vistas / Procedimientos
   QUE ES LO QUE TENEMOS DE MOMENTO!!
   */

-- TABLAS (stg/cln/gold)
SELECT
    s.name  AS [schema],
    t.name  AS [object_name],
    'TABLE' AS [object_type]
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE s.name IN ('stg','cln','gold')
ORDER BY s.name, t.name;

-- VISTAS (stg/cln/gold)
SELECT
    s.name AS [schema],
    v.name AS [object_name],
    'VIEW' AS [object_type]
FROM sys.views v
JOIN sys.schemas s ON s.schema_id = v.schema_id
WHERE s.name IN ('stg','cln','gold')
ORDER BY s.name, v.name;

-- PROCEDIMIENTOS (stg/cln/gold/dbo)
SELECT
    s.name  AS [schema],
    p.name  AS [object_name],
    'PROC'  AS [object_type]
FROM sys.procedures p
JOIN sys.schemas s ON s.schema_id = p.schema_id
WHERE s.name IN ('stg','cln','gold','dbo')
ORDER BY s.name, p.name;
