import os
import pymssql
from sql_connection_manager import SqlConnectionManager
import unittest
from COVID19_vaccine import COVID19Vaccine as covid
from enums import *
from utils import *

class TestCOVID19_vaccine(unittest.TestCase):

    def setUp(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
              clear_tables(sqlClient)
              self.sqltext = "INSERT INTO Caregivers(CaregiverName) VALUES ('Preston'); INSERT INTO Patients(Name, dob, gender, sideeffects) VALUES ('Andreia', '10-11-2000', 'Female', 'No side effects'); INSERT INTO VaccineAppointment (PatientId, firstshot, VaccineId) VALUES (1, 1, 1); INSERT INTO CareGiverSchedule(CaregiverId, WorkDay, SlotHour, SlotMinute, SlotStatus, VaccineAppointmentId) VALUES (1, '12-12-2021', 12, 15, 0, 2);"
              dbcursor = sqlClient.cursor(as_dict=True)
              dbcursor.execute(self.sqltext)
              dbcursor.connection.commit()
              vaccines = {'Moderna': {'inventory': 100, 'shotsnecessary': 2}, 'Pfizer': {'inventory': 100, 'shotsnecessary': 2}, 'JohnsonJohnson': {'inventory': 100, 'shotsnecessary': 1}}
              vaccinedb = covid(dbcursor, vaccines)

    def test_AddDoses(self):
        test_value = 0
        updated_inventory = 0
        doses_to_add = 30
        with SqlConnectionManager(Server=os.getenv("Server"),
                                   DBname=os.getenv("DBName"),
                                   UserId=os.getenv("UserID"),
                                   Password=os.getenv("Password")) as sqlClient:
            dbcursor = sqlClient.cursor(as_dict=True)
            self.sqltext = "SELECT inventory FROM Vaccines WHERE vaccineid=1"
            dbcursor.execute(self.sqltext)
            rows = dbcursor.fetchone()
            current_inventory = rows['inventory']
            test_value = current_inventory + doses_to_add
            covid.AddDoses(dbcursor, 1, doses_to_add)
            self.sqltext = "SELECT inventory FROM Vaccines WHERE vaccineid=1"
            dbcursor.execute(self.sqltext)
            rows = dbcursor.fetchone()
            updated_inventory = rows['inventory']
        self.assertEqual(test_value, updated_inventory)

if __name__ == '__main__':
    unittest.main()
