/* To prevent any potential data loss issues, you should review this script in detail before running it outside the context of the database designer.*/
BEGIN TRANSACTION
SET QUOTED_IDENTIFIER ON
SET ARITHABORT ON
SET NUMERIC_ROUNDABORT OFF
SET CONCAT_NULL_YIELDS_NULL ON
SET ANSI_NULLS ON
SET ANSI_PADDING ON
SET ANSI_WARNINGS ON
COMMIT
BEGIN TRANSACTION
GO
CREATE TABLE dbo.invTypes
	(
	typeID bigint NOT NULL,
	groupID bigint NOT NULL,
	typeName varchar(100) NULL,
	description varchar(3000) NULL,
	mass float(53) NULL,
	volume float(53) NULL,
	capacity float(53) NULL,
	portionSize bigint NULL,
	raceID int NULL,
	basePrice decimal(19, 4) NULL,
	published tinyint NULL,
	marketGroupID bigint NULL,
	iconID bigint NULL,
	soundID bigint NULL
	)  ON [PRIMARY]
GO
ALTER TABLE dbo.invTypes ADD CONSTRAINT
	PK_invTypes PRIMARY KEY CLUSTERED 
	(
	typeID
	) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]

GO
CREATE NONCLUSTERED INDEX IX_invTypes_group ON dbo.invTypes
	(
	groupID
	) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE dbo.invTypes SET (LOCK_ESCALATION = TABLE)
GO
COMMIT
