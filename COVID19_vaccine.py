import pymssql

class COVID19Vaccine:
    def __init__(self, cursor, init_vaccines):
        vaccine_names = list(init_vaccines.keys())
        vaccine_inv = list(init_vaccines.values())
        try:
            for i in range(len(vaccine_names)):
                print(type(vaccine_names[i]))
                print(type(vaccine_inv[i]))
                self.sqltext = "INSERT INTO Vaccines (Name, inventory, reserved) VALUES (%s, %s, %s)"
                print(type(self.sqltext))
                cursor.execute(self.sqltext, ((vaccine_names[i]), (str(vaccine_inv[i])), (0)))
                cursor.connection.commit()
        except pymssql.Error as db_err:
          print("Database Programming Error in SQL Query processing for Vaccines! ")
          print("Exception code: " + str(db_err.args[0]))
          if len(db_err.args) > 1:
              print("Exception message: " + db_err.args[1])
          print("SQL text that resulted in an Error: " + self.sqltext)

    def AddDoses(self, cursor, name, inventory):
        return None

    def ReserveDoeses():
        return None
