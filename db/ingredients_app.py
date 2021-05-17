import os, sys, string, inspect
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

class Ingredients(QtWidgets.QMainWindow):
    """ Ingredients App MainWindow """
    def __init__(self):
        super(Ingredients, self).__init__()
        uic.loadUi('ingredients_app.ui', self)
        self.add_ingredient = self.findChild(QtWidgets.QAction, 'actionAdd_Ingredient')
        self.add_ingredient.triggered.connect(self.openAddIngredients)
        self.remove_ingredient = self.findChild(QtWidgets.QAction, 'actionRemove_Ingredient')
        self.remove_ingredient.triggered.connect(self.removeIngredient)
        self.show()

    def openAddIngredients(self):
        dlg = CrummyAddIngredient()
        dlg.exec_()

    def removeIngredient(self):
        pass

app = QtWidgets.QApplication(sys.argv)
window = Ingredients()
app.exec_()
