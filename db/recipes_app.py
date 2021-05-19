import os, sys, string, inspect
import ctypes
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from db import *

# Dialog Boxes
add_recipe = uic.loadUiType("add_recipe_dialog.ui")[0]

# Class Declarations
class CrummyAddRecipe(QtWidgets.QDialog, add_recipe):
    """ Open AddRecipe Dialog Box """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

class Recipes(QtWidgets.QMainWindow):
    """ Recipes App MainWindow """
    def __init__(self):
        super(Recipes, self).__init__()
        uic.loadUi('recipes_app.ui', self)
        # Menu options....
        self.add_recipe = self.findChild(QtWidgets.QAction, 'actionAdd_Recipe')
        self.add_recipe.triggered.connect(self.openAddRecipes)
        self.remove_recipe = self.findChild(QtWidgets.QAction, 'actionRemove_Recipe')
        self.remove_recipe.triggered.connect(self.removeRecipe)

        # Filling up the Recipes QTableWidget....
        self.recipesList = self.findChild(QtWidgets.QTableWidget, 'recipe_list_tablewidget')
        recipes = getAllRecipes()
        for recipe in recipes:
            self.recipesList.setRowCount(self.recipesList.rowCount() + 1)
            self.recipesList.setItem(self.recipesList.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(recipe[1]))
            self.recipesList.setItem(self.recipesList.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(recipe[2]))

        self.show()

    def openAddRecipes(self):
        dlg = CrummyAddRecipe()
        dlg.exec_()
        self.reloadTable()

    def reloadTable(self):
        self.recipesList.setRowCount(0)
        recipes = getAllRecipes()
        for recipe in recipes:
            self.recipesList.setRowCount(self.recipesList.rowCount() + 1)
            self.recipesList.setItem(self.recipesList.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(recipe[1]))
            self.recipesList.setItem(self.recipesList.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(recipe[2]))

    def removeRecipe(self):
        """ Remove selected row from Recipes QTableWidget """
        # Check if any are selected
        if self.recipesList.currentRow() != None:
            # If so, remove the selected item
            currentRow = self.recipesList.currentRow()
            query(f"DELETE FROM Recipe WHERE Name = '{self.recipesList.item(currentRow, 0).text()}'")
            self.recipesList.removeRow(currentRow)
            self.reloadTable()
        else: ctypes.windll.user32.MessageBoxW(0, "Please select a row to remove", "ERROR", 0)

# Main app execution
app = QtWidgets.QApplication(sys.argv)
window = Recipes()
app.exec_()
