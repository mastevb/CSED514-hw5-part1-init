import os
import pymssql
from sql_connection_manager import SqlConnectionManager
import unittest
from COVID19_vaccine import COVID19Vaccine as covid
from enums import *
from utils import *

# NOTE: RUN THE TESTS AFTER DROPPING ALL TABLES AND PROCEDURES. TESTS EXECUTE STORED PROCEDURE AND DROP TABLES AUTOMATICALLY.
# PLEASE COMMENT OUT THE 'EXECUTE InitDataModel' IN OUR SQL FILE AS WELL. dbcursor EXECUTES THE PROCEDURE.

class TestCOVID19_vaccine(unittest.TestCase):

    def setUp(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            dbcursor = sqlClient.cursor(as_dict=True)

            with open('hw5_week1_sql.sql') as f: 
              sql = f.read() # Don't do that with untrusted inputs
              dbcursor.execute(sql)
              dbcursor.connection.commit()

            dbcursor.callproc('InitDataModel')

            vaccines = {'Moderna': {'inventory': 100, 'shotsnecessary': 2}, 'Pfizer': {'inventory': 100, 'shotsnecessary': 2}, 'JohnsonJohnson': {'inventory': 100, 'shotsnecessary': 1}}
            vaccinedb = covid(dbcursor, vaccines)

            self.sqltext = "INSERT INTO Caregivers(CaregiverName) VALUES ('Preston'); INSERT INTO Patients(Name, dob, gender, sideeffects) VALUES ('Andreia', '10-11-2000', 'Female', 'No side effects'); INSERT INTO VaccineAppointment(PatientId, firstshot, VaccineId) VALUES (1, 1, 1); INSERT INTO CareGiverSchedule(CaregiverId, WorkDay, SlotHour, SlotMinute, SlotStatus, VaccineAppointmentId) VALUES (1, '12-12-2021', 12, 15, 0, 1);"
            dbcursor.execute(self.sqltext)
            dbcursor.connection.commit()
            dbcursor.close()
    
    def tearDown(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
            
            self.sqltext = "DROP TABLE CareGiverSchedule; DROP TABLE AppointmentStatusCodes; DROP TABLE Caregivers; DROP TABLE VaccineAppointment; DROP TABLE Patients; DROP TABLE Vaccines; DROP PROCEDURE InitDataModel; "   
            dbcursor = sqlClient.cursor(as_dict=True)
            dbcursor.execute(self.sqltext)
            dbcursor.connection.commit()

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

    def test_AddNegativeDoses(self):
      doses_to_add = -1
      with self.assertRaises(Exception) as context:
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
          dbcursor = sqlClient.cursor(as_dict=True)
          covid.AddDoses(dbcursor, 1, doses_to_add)
          self.assertTrue('New inventory must be greater than zero.' in context.exception)
        

    def test_ReserveDoses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                   DBname=os.getenv("DBName"),
                                   UserId=os.getenv("UserID"),
                                   Password=os.getenv("Password")) as sqlClient:
            dbcursor = sqlClient.cursor(as_dict=True)
            # Initial data
            self.sqltext = "SELECT inventory, reserved, shotsnecessary FROM Vaccines WHERE vaccineid=1"
            dbcursor.execute(self.sqltext)
            rows = dbcursor.fetchone()
            current_inventory = rows['inventory']
            current_reserved = rows['reserved']
            shots_necessary= rows['shotsnecessary']
            # Expected Results 
            test_inventory = current_inventory - shots_necessary
            test_reserved = current_reserved + shots_necessary
            # Reserving Doses
            covid.ReserveDoses(dbcursor, 1)
            self.sqltext = "SELECT inventory, reserved FROM Vaccines WHERE vaccineid=1"
            dbcursor.execute(self.sqltext)
            rows = dbcursor.fetchone()
            # Actual Results
            updated_inventory = rows['inventory']
            updated_reserved = rows['reserved']
        # Test
        self.assertEqual(test_inventory, updated_inventory)
        self.assertEqual(test_reserved, updated_reserved)

    def test_ReserveDosesLowInventory(self):
      with self.assertRaises(Exception) as context:
        with SqlConnectionManager(Server=os.getenv("Server"),
                                   DBname=os.getenv("DBName"),
                                   UserId=os.getenv("UserID"),
                                   Password=os.getenv("Password")) as sqlClient:
            dbcursor = sqlClient.cursor(as_dict=True)
            # Setting inventory to zero
            sqltext = "UPDATE Vaccines SET inventory=%s WHERE vaccineid=1"
            dbcursor.execute(sqltext, (str(0)))
            dbcursor.connection.commit()
            covid.ReserveDoses(dbcursor, 1)
            self.assertTrue('Not enough vaccines. Please try a different vaccine or another vaccine!' in context.exception)


if __name__ == '__main__':
    unittest.main()
