from db import database
import private, queries

handler = database(private.HOST, "admin", private.PASSWORD, "cp363")

handler.viewTables(output=False)

handler.exit()
