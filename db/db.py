import sqlite3
import ctypes
import xml.etree.ElementTree as ET
from PyQt5 import QtWidgets

def query(sql):
   """
   Query the Database

   Execute a query on the Crummy SQLite database

   Parameters:
   sql (string): SQL query text

   Returns:
   list: Query Results
   """
   # Connect to 'finesse.db'
   db = sqlite3.connect('.\\crummy.db')

   # Create database cursor for query execution....
   cursor = db.cursor()
   try:
      # Execute SQL Query....
      cursor.execute(sql)

      # Getting the SQL query results....
      results = cursor.fetchall()

      # Commit any new changes to the database....
      db.commit()

      # Return the results to function caller
      return results
   except sqlite3.Error as error:
      # Return any errors returned from the query....
      # app = QtWidgets.QApplication([])
      # error_dialog = QtWidgets.QErrorMessage()
      # error_dialog.showMessage("ERROR! {}".format(error.args[0]))
      # app.exec_()
      ctypes.windll.user32.MessageBoxW(0, "ERROR! {}".format(error.args[0]), "ERROR", 0)
      return []
