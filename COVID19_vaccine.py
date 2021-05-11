import pymssql

class COVID19Vaccine:
    def __init__(self, cursor, init_vaccines):
        vaccine_names = list(init_vaccines.keys())
        vaccine_inv = list(init_vaccines.values())
        try:
            for i in range(len(vaccine_names)):
                self.sqltext = "INSERT INTO Vaccines (Name, inventory, reserved) VALUES (%s, %s, %s)"
                cursor.execute(self.sqltext, ((vaccine_names[i]), (str(vaccine_inv[i])), (0)))
                cursor.connection.commit()
        except pymssql.Error as db_err:
          print("Database Programming Error in SQL Query processing for Vaccines! ")
          print("Exception code: " + str(db_err.args[0]))
          if len(db_err.args) > 1:
              print("Exception message: " + db_err.args[1])
          print("SQL text that resulted in an Error: " + self.sqltext)

    def AddDoses(cursor, vaccineid, new_inventory):
        try:
            sqltext = "SELECT inventory FROM Vaccines WHERE vaccineid=%s"
            cursor.execute(sqltext, (vaccineid))
            row = cursor.fetchone()
            current_inventory = row['inventory']
            sqltext = "UPDATE Vaccines SET inventory=%s WHERE vaccineid=%s"
            cursor.execute(sqltext, ((current_inventory + new_inventory), (vaccineid)))
            cursor.connection.commit()
            print("Successfully added %s doses to vaccineid %s", new_inventory, vaccineid)
        except pymssql.Error as db_err:
            print("ERROR: Could not add new doses. Pymssql error: " + db_err.args[1])
        return None

    def ReserveDoeses():
        return None
