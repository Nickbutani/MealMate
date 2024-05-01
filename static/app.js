document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form.form-inline').addEventListener('submit', function(event) {
        event.preventDefault();

        var searchQuery = document.querySelector('input[type="search"]').value;

        var apiUrl = '/search-recipes?q=' + encodeURIComponent(searchQuery);

        axios.get(apiUrl)
            .then(function(response) {
                if (response.status !== 200) {
                    throw new Error('Network response was not ok');
                }
                return response.data;
            })
            .then(function(data) {
                console.log(data);
                displayRecipes(data.hits);
            })
            .catch(function(error) {
                console.error('There was a problem with the fetch operation:', error);
            });
    });
});

function displayRecipes(recipes) {
    var recipeContainer = document.getElementById('recipe-container');
    recipeContainer.innerHTML = '';

    recipes.forEach(function(recipe) {
        var recipeElement = document.createElement('div');
        recipeElement.classList.add('recipe');

        var ingredientsHTML = '<h2>' + recipe.recipe.label + '</h2>';
        ingredientsHTML += '<img src="' + recipe.recipe.image + '" alt="' + recipe.recipe.label + '">';

        // Iterate over each ingredient and format the data
        ingredientsHTML += '<h3>Ingredients:</h3>';
        recipe.recipe.ingredients.forEach(function(ingredient) {
            var ingredientText = '';

            // Check if quantity and measure exist
            if (ingredient.quantity && ingredient.measure) {
                ingredientText += ingredient.quantity + ' ' + ingredient.measure + ' ';
            }

            // Check if food name exists
            if (ingredient.food) {
                ingredientText += ingredient.food;
            }

            // Add the formatted ingredient text to the HTML
            if (ingredientText !== '') {
                ingredientsHTML += '<p>' + ingredientText + '</p>';
            }
        });

        // Add calories, servings, and link information
        ingredientsHTML += '<p>Calories: ' + recipe.recipe.calories + '</p>';
        ingredientsHTML += '<p>Servings: ' + recipe.recipe.yield + '</p>';
        ingredientsHTML += '<p>Link: <a href="' + recipe.recipe.url + '" target="_blank">View Recipe</a></p>';

        recipeElement.innerHTML = ingredientsHTML;
        recipeContainer.appendChild(recipeElement);
    });
}



