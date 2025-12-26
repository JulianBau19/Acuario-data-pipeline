/* 
   Crear schemas del DWH (STG/CLN/GOLD) si no existen!!
   IMPORTANTE:   Ejecutar 1 vez al iniciar el entorno o cuando recreas la BD
  
*/

SET NOCOUNT ON;
GO

-- STG
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'stg')
    EXEC('CREATE SCHEMA stg AUTHORIZATION dbo;');
GO

-- CLN
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'cln')
    EXEC('CREATE SCHEMA cln AUTHORIZATION dbo;');
GO

-- GOLD
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'gold')
    EXEC('CREATE SCHEMA gold AUTHORIZATION dbo;');
GO



---check---

SELECT name
FROM sys.schemas
WHERE name IN ('stg','cln','gold')
ORDER BY name;
