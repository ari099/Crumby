import os, sys, string, inspect
import ctypes
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from db import *

# Dialog Windows
add_ingredient = uic.loadUiType("add_ingredient_dialog.ui")[0]

class CrummyAddIngredient(QtWidgets.QDialog, add_ingredient):
    """ Open AddIngredient Dialog Box"""
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.ingredientName = self.findChild(QtWidgets.QTextEdit, 'ingredient_name_textedit')
        self.quantity = self.findChild(QtWidgets.QSpinBox, 'quantity_spinbox')
        self.unitOfMeasure = self.findChild(QtWidgets.QComboBox, 'unit_combobox')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        self.buttonBox.accepted.connect(self.addIngredient)

    def addIngredient(self):
        ingredientName = self.ingredientName.toPlainText()
        quantity = self.quantity.value()
        unit = self.unitOfMeasure.currentText()
        if ingredientName != "" and quantity > 0 and unit != "":
            addIngredient(ingredientName, int(quantity), unit)
        else: ctypes.windll.user32.MessageBoxW(0, "Please fill out the whole form", "ERROR", 0)

class Ingredients(QtWidgets.QMainWindow):
    """ Ingredients App MainWindow """
    def __init__(self):
        super(Ingredients, self).__init__()
        uic.loadUi('ingredients_app.ui', self)
        # Menu options....
        self.add_ingredient = self.findChild(QtWidgets.QAction, 'actionAdd_Ingredient')
        self.add_ingredient.triggered.connect(self.openAddIngredients)
        self.remove_ingredient = self.findChild(QtWidgets.QAction, 'actionRemove_Ingredient')
        self.remove_ingredient.triggered.connect(self.removeIngredient)

        # Filling up the Ingredients QTableWidget....
        self.ingredientsList = self.findChild(QtWidgets.QTableWidget, 'ingredients_list')
        ingredients = getAllIngredients()
        for ingredient in ingredients:
            self.ingredientsList.setRowCount(self.ingredientsList.rowCount() + 1)
            self.ingredientsList.setItem(self.ingredientsList.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ingredient[1]))
            self.ingredientsList.setItem(self.ingredientsList.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(ingredient[2])))
            self.ingredientsList.setItem(self.ingredientsList.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(ingredient[3]))

        self.show()

    def openAddIngredients(self):
        dlg = CrummyAddIngredient()
        dlg.exec_()
        self.reloadTable()

    def reloadTable(self):
        self.ingredientsList.setRowCount(0)
        ingredients = getAllIngredients()
        for ingredient in ingredients:
            self.ingredientsList.setRowCount(self.ingredientsList.rowCount() + 1)
            self.ingredientsList.setItem(self.ingredientsList.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ingredient[1]))
            self.ingredientsList.setItem(self.ingredientsList.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(ingredient[2])))
            self.ingredientsList.setItem(self.ingredientsList.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(ingredient[3]))

    def removeIngredient(self):
        """ Remove selected row from Ingredients QTableWidget """
        # Check if any are selected
        if self.ingredientsList.currentRow() != None:
            # If so, remove the selected item
            currentRow = self.ingredientsList.currentRow()
            query(f"DELETE FROM Ingredient WHERE Name = '{self.ingredientsList.item(currentRow, 0).text()}'")
            self.ingredientsList.removeRow(currentRow)

            # Update the Ingredients table in Database
            for index in range(0, self.ingredientsList.rowCount()):
                results = query(f"SELECT Name, Quantity, Unit FROM Ingredient WHERE Name = '{self.ingredientsList.item(index, 0).text()}'")
                if len(results) == 0:
                    addIngredient(self.ingredientsList.item(index, 0).text(),
                        self.ingredientsList.item(index, 1).text(),
                        self.ingredientsList.item(index, 2).text())

        else: ctypes.windll.user32.MessageBoxW(0, "Please select a row to remove", "ERROR", 0)

app = QtWidgets.QApplication(sys.argv)
window = Ingredients()
app.exec_()
