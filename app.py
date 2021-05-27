from db.db import *
from eel import *

init('web')

@expose
def getRecipes():
    results = query("SELECT Name, Description FROM Recipe")
    return results

start('index.html', size=(650, 612))
