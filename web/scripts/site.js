/**
 * Method for filling the HTML5 Recipes table with the recipes
 * that can be made with the ingredients specified....
 */
function fillRecipesTable(recipes) {
  let recipeList = document.getElementById("recipeList");
  for(let i = 0; i < recipes.length; i++) {
    let row = recipeList.insertRow(-1);
    let nameCell = row.insertCell(0);
    let descriptionCell = row.insertCell(1);
    nameCell.innerHTML = recipes[i][0];
    descriptionCell.innerHTML = recipes[i][1];
  }
}

window.onload = () => eel.getRecipes()(fillRecipesTable);
