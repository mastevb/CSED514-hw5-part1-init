INSERT INTO Vaccines(VaccineName, VaccineSupplier, AvailableDoses, ReservedDoses, TotalDoses, DosesPerPatient, DaysBetweenDosesLower, DaysBetweenDosesUpper) values ('Moderna', 'Moderna', 100, 0, 100, 2, 21, 42);
INSERT INTO Vaccines(VaccineName, VaccineSupplier, AvailableDoses, ReservedDoses, TotalDoses, DosesPerPatient, DaysBetweenDosesLower, DaysBetweenDosesUpper) values ('Pfizer', 'Pfizer', 100, 0, 100, 2, 21, 42);
INSERT INTO Vaccines(VaccineName, VaccineSupplier, AvailableDoses, ReservedDoses, TotalDoses, DosesPerPatient, DaysBetweenDosesLower, DaysBetweenDosesUpper) values ('JohnsonJohnson', 'JJ', 100, 0, 100, 1, 21, 42);
INSERT INTO Caregivers(CaregiverName) VALUES ('Preston');
INSERT INTO CareGiverSchedule(CaregiverId, WorkDay, SlotHour, SlotMinute, SlotStatus, VaccineAppointmentId, SlotTime) VALUES (1, '12-12-2021', 12, 15, 0, 1, '12:05:00');
INSERT INTO Patients(PatientName, VaccineStatus) VALUES ('Andreia', 0);
INSERT INTO VaccineAppointments( PatientId, DoseNumber, SlotStatus, VaccineName) VALUES( 1, 1, 1, 'Pfizer')