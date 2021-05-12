-- Given CREATE TABLE statements to start your database
CREATE PROCEDURE InitDataModel AS
	DECLARE @SQLString0 NVARCHAR(MAX)
	SET @SQLString0 = 'Create Table Caregivers(
		CaregiverId int IDENTITY PRIMARY KEY,
		CaregiverName varchar(50)
		);'
	EXEC (@SQLString0)

	DECLARE @SQLString1 NVARCHAR(MAX)
	SET @SQLString1 ='Create Table AppointmentStatusCodes(
		StatusCodeId int PRIMARY KEY,
		StatusCode   varchar(30)
	);'
	EXEC (@SQLString1)

	DECLARE @SQLString2 NVARCHAR(MAX)
	SET @SQLString2 = 'Create Table Patients(
		PatientId int IDENTITY PRIMARY KEY,
		Name varchar(50),
		dob DATE,
		gender varchar(30),
		sideeffects varchar(200)
	);'
	EXEC (@SQLString2)

	DECLARE @SQLString3 NVARCHAR(MAX)
	SET @SQLString3 = 'Create Table Vaccines(
		VaccineId int IDENTITY PRIMARY KEY,
		Name varchar(60),
		inventory int DEFAULT 0 NOT NULL,
		reserved int DEFAULT 0 NOT NULL,
		shotsnecessary int DEFAULT 1 NOT NULL
	);'
	EXEC (@SQLString3)	
	
	DECLARE @SQLString4 NVARCHAR(MAX)
	SET @SQLString4 = 'INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode) VALUES (0, ''Open'');
	INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode) VALUES (1, ''OnHold'');
	INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode) VALUES (2, ''Scheduled'');
	INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode) VALUES (3, ''Completed'');
	INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode) VALUES (4, ''Missed'');'
	EXEC (@SQLString4)

	DECLARE @SQLString5 NVARCHAR(MAX)
	SET @SQLString5 = 'Create Table CareGiverSchedule(
		CaregiverSlotSchedulingId int Identity PRIMARY KEY, 
		CaregiverId int DEFAULT 0 NOT NULL
			CONSTRAINT FK_CareGiverScheduleCaregiverId FOREIGN KEY (CaregiverId)
				REFERENCES Caregivers(CaregiverId),
		WorkDay date,
		SlotTime time,
		SlotHour int DEFAULT 0 NOT NULL,
		SlotMinute int DEFAULT 0 NOT NULL,
		SlotStatus int  DEFAULT 0 NOT NULL
			CONSTRAINT FK_CaregiverStatusCode FOREIGN KEY (SlotStatus) 
				REFERENCES AppointmentStatusCodes(StatusCodeId),
		VaccineAppointmentId int DEFAULT 0 NOT NULL);'
	EXEC (@SQLString5)

	DECLARE @SQLString6 NVARCHAR(MAX)
	SET @SQLString6 = 'Create Table VaccineAppointment(
		VaccineAppointmentId int IDENTITY PRIMARY KEY,
		PatientId int NOT NULL
			CONSTRAINT FK_PatientId FOREIGN KEY (PatientId)
				REFERENCES Patients(PatientId),
		firstshot bit,
		VaccineId int NOT NULL
			CONSTRAINT FK_VaccineId FOREIGN KEY (VaccineId)
				REFERENCES Vaccines(VaccineId));'
	EXEC (@SQLString6)
	GO

EXECUTE InitDataModel;

-- Additional helper code for your use if needed

-- --- Drop commands to restructure the DB
-- Drop Table CareGiverSchedule
-- Drop Table AppointmentStatusCodes
-- Drop Table Caregivers
-- Drop Table VaccineAppointment
-- Drop Table Patients
-- Drop Table Vaccines 
-- Drop Procedure InitDataModel
-- Go

-- --- Commands to clear the active database Tables for unit testing
-- Truncate Table CareGiverSchedule
-- DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)
-- Delete From Caregivers
-- DBCC CHECKIDENT ('Caregivers', RESEED, 0)
-- GO
