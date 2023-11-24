import mysql.connector
# A component that is used to interact with any database

class database:
    
    def __init__(self, host, username, password, name):
        self.host, self.username, self.name = host, username, name
        self.database = mysql.connector.connect( # Establish a connection with the DB
            host=self.host,
            user=self.username,
            password=password,
            database=self.name
        )
        self.cursor = self.database.cursor()  # Create a cursor (thorugh which SQL commands are sent)
        # Should we handle the views in here?
        return

    # Given a fetch type query, this function fetches all the rows and either displays or returns them depending on the bool value of 'output' 
    def fetch(self, query, output=False): 
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if not output:
            for row in rows: print(row)
        return rows if output else None
    
    # Insert (and update) given values into db based on given the sql command and return True or False depending on the success
    def insert(self, sql, values:list):
        success = False
        try:
            self.cursor.execute(sql,values)
            self.database.commit()
        except Exception as e: print("Failed to insert:", e)
        else: success = True
        return success

    def delete(self,sql):
        success = False
        try: 
            self.cursor.execute(sql)
            self.database.commit()
        except Exception as e: print(e)
        else: success=True
        return success

    def viewTables(self, output=False): return self.fetch("SHOW TABLES;", output)

    def viewEntries(self,table:str,output=False):
        return self.fetch(f'SELECT * FROM {self.name}.{table};',output=output)

    def exit(self):
        self.cursor.close()
        self.database.close()
        return
