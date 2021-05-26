import os, sys, string, inspect
import ctypes
import xml.etree.ElementTree as ET
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
        self.recipeNameTextBox = self.findChild(QtWidgets.QTextEdit, "recipe_name_textedit")
        self.recipeDescriptionTextBox = self.findChild(QtWidgets.QTextEdit, "recipe_description_textedit")
        self.newIngredientTextBox = self.findChild(QtWidgets.QTextEdit, "new_ingredient_textedit")
        self.newIngredientQuantityBox = self.findChild(QtWidgets.QDoubleSpinBox, "new_ingredient_quantity_spinbox")
        self.newIngredientUnitBox = self.findChild(QtWidgets.QComboBox, "new_ingredient_unit_combobox")
        self.ingredientsTableWidget = self.findChild(QtWidgets.QTableWidget, "ingredients_tablewidget")
        self.addIngredientButton = self.findChild(QtWidgets.QPushButton, "add_ingredient_pushbutton")
        self.addIngredientButton.clicked.connect(self.addIngredientToTable)
        self.removeIngredientButton = self.findChild(QtWidgets.QPushButton, "remove_ingredient_pushbutton")
        self.removeIngredientButton.clicked.connect(self.removeSelectedIngredientFromTable)
        self.instructionsListBox = self.findChild(QtWidgets.QListWidget, "instructions_listwidget")
        self.newInstructionTextBox = self.findChild(QtWidgets.QTextEdit, "new_instruction_textedit")
        self.addInstructionButton = self.findChild(QtWidgets.QPushButton, "add_instruction_pushbutton")
        self.addInstructionButton.clicked.connect(self.addInstructionToListBox)
        self.removeInstructionButton = self.findChild(QtWidgets.QPushButton, "remove_instruction_pushbutton")
        self.removeInstructionButton.clicked.connect(self.removeSelectedInstructionsFromListBox)
        self.dlgButtonBox = self.findChild(QtWidgets.QDialogButtonBox, "addRecipeButtonBox")
        self.dlgButtonBox.accepted.connect(self.saveToDB)

    def saveToDB(self):
        name = self.recipeNameTextBox.toPlainText()
        if name == "":
            ctypes.windll.user32.MessageBoxW(0, "Please fill all fields", "ERROR", 0)
            return

        description = self.recipeDescriptionTextBox.toPlainText()
        if description == "":
            ctypes.windll.user32.MessageBoxW(0, "Please fill all fields", "ERROR", 0)
            return

        ingredients_widget = self.ingredientsTableWidget
        if ingredients_widget.rowCount() == 0:
            ctypes.windll.user32.MessageBoxW(0, "You need ingredients for a meal!", "ERROR", 0)
            return

        instructions_widget = self.instructionsListBox
        if instructions_widget.count() == 0:
            ctypes.windll.user32.MessageBoxW(0, "You need instructions to know what to do!", "ERROR", 0)
            return

        ingredients_root = ET.fromstring("<Ingredients></Ingredients>")
        instructions_root = ET.fromstring("<Instructions></Instructions>")
        for row in range(0, ingredients_widget.rowCount()):
            ingredient_name = ingredients_widget.item(row, 0).text()
            ingredient_quantity = ingredients_widget.item(row, 1).text()
            ingredient_unit = ingredients_widget.item(row, 2).text()
            tag = ET.SubElement(ET.Element('Ingredient'), 'Ingredient')
            name_tag = ET.SubElement(ET.Element('Name'), 'Name')
            name_tag.text = ingredient_name
            quantity_tag = ET.SubElement(ET.Element('Quantity'), 'Quantity')
            quantity_tag.text = ingredient_quantity
            unit_tag = ET.SubElement(ET.Element('Unit'), 'Unit')
            unit_tag.text = ingredient_unit
            tag.insert(0, name_tag)
            tag.insert(0, quantity_tag)
            tag.insert(0, unit_tag)
            ingredients_root.insert(1, tag)

        for row in range(0, instructions_widget.count()):
            instruction_text = instructions_widget.item(row).text()
            instruction_tag = ET.SubElement(ET.Element('Instruction'), 'Instruction')
            instruction_tag.text = instruction_text
            instructions_root.insert(1, instruction_tag)

        addRecipe(name, description, ET.tostring(instructions_root).decode('utf-8'), ET.tostring(ingredients_root).decode('utf-8'))

    def addIngredientToTable(self):
        ingredientsTable = self.ingredientsTableWidget
        newIngredientName = self.newIngredientTextBox.toPlainText()
        newIngredientQuantity = self.newIngredientQuantityBox.value()
        newIngredientUnit = self.newIngredientUnitBox.currentText()
        if newIngredientName != "" and newIngredientQuantity != "" and newIngredientUnit != "":
            ingredientsTable.setRowCount(ingredientsTable.rowCount() + 1)
            ingredientsTable.setItem(ingredientsTable.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(newIngredientName))
            ingredientsTable.setItem(ingredientsTable.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(newIngredientQuantity)))
            ingredientsTable.setItem(ingredientsTable.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(newIngredientUnit))

    def removeSelectedIngredientFromTable(self):
        ingredientsTable = self.ingredientsTableWidget
        if ingredientsTable.currentRow() != None:
            currentRow = ingredientsTable.currentRow()
            ingredientsTable.removeRow(currentRow)
        else: ctypes.windll.user32.MessageBoxW(0, "Please select a row to remove", "ERROR", 0)

    def addInstructionToListBox(self):
        instructionList = self.instructionsListBox
        instructionText = self.newInstructionTextBox.toPlainText()
        instructionList.addItem(QtWidgets.QListWidgetItem(instructionText))

    def removeSelectedInstructionsFromListBox(self):
        instructionList = self.instructionsListBox
        if instructionList.currentItem() != None:
            instructionList.takeItem(instructionList.currentRow())

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
        # self.recipesList.itemDoubleClicked.connect(self.cellDoubleClick)
        self.recipesList.itemSelectionChanged.connect(self.cellChange)
        recipes = getAllRecipes()
        for recipe in recipes:
            self.recipesList.setRowCount(self.recipesList.rowCount() + 1)
            self.recipesList.setItem(self.recipesList.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(recipe[1]))
            self.recipesList.setItem(self.recipesList.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(recipe[2]))

        self.show()

    def cellDoubleClick(self, item):
        row = item.row() + 1
        column = item.column() + 1
        # print(f'Row: {row}, Column {column}')

    def cellChange(self):
        print("Test")
        # row = item.row() + 1
        # column = item.column() + 1
        # updateRecipe(self.recipesList.item(item.row(), 0).text(),"Name" if row == 1 else "Description", self.recipesList.item(item.row(), item.column()).text())

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
