-- Given CREATE TABLE statements to start your database
CREATE PROCEDURE InitDataModel AS 
BEGIN
	Create Table Caregivers(
		CaregiverId int IDENTITY PRIMARY KEY,
		CaregiverName varchar(50)
		);

	Create Table AppointmentStatusCodes(
		StatusCodeId int PRIMARY KEY,
		StatusCode   varchar(30)
	);

	Create Table Patients(
		PatientId int IDENTITY PRIMARY KEY,
		Name varchar(50),
		dob DATE,
		gender varchar(30),
		sideeffects varchar(200)
	)

	Create Table Vaccines(
		VaccineId int IDENTITY PRIMARY KEY,
		Name varchar(60),
		inventory int DEFAULT 0 NOT NULL,
		reserved int DEFAULT 0 NOT NULL
	)

	Create Table CareGiverSchedule(
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
		VaccineAppointmentId int DEFAULT 0 NOT NULL);

	Create Table VaccineAppointment(
		VaccineAppointmentId int IDENTITY PRIMARY KEY,
		PatientId int NOT NULL
			CONSTRAINT FK_PatientId FOREIGN KEY (PatientId)
				REFERENCES Patients(PatientId),
		firstshot bit,
		VaccineId int NOT NULL
			CONSTRAINT FK_VaccineId FOREIGN KEY (VaccineId)
				REFERENCES Vaccines(VaccineId)
	)
END

EXEC InitDataModel;
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
