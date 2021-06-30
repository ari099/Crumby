from db.db import *
from eel import *

init('web')

@expose
def getRecipes():
    '''
    Getting all relevant recipes

    Obtaining recipes from the database based on ingredients in
    the database

    Returns:
    recipes(list) - Relevant recipes
    '''
    results = query("SELECT Name, Description FROM Recipe")
    return results

start('index.html', size=(650, 612))
