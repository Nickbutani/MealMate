# MealMate

MealMate is a web application built with Flask that helps users generate recipes and plan their meals. It utilizes two APIs to provide a seamless experience.

## API Key

To use the application, you will need to obtain API keys from the following services:

- Recipe Generator API: [Edamam](https://api.edamam.com/api/recipes/v2)
- Meal Planner API: [Spoonacular](https://api.spoonacular.com/mealplanner/generate)

Once you have obtained the API keys, you can proceed with the setup.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/MealMate.git
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set the API keys as environment variables:

    ```bash
    export RECIPE_API_KEY=your_recipe_api_key
    export MEAL_PLANNER_API_KEY=your_meal_planner_api_key
    ```

5. Run the application:

    ```bash
    flask run
    ```

6. Open your browser and navigate to `http://localhost:5000` to access MealMate.

## Usage

Upon accessing the application, you will be able to generate recipes based on your preferences and dietary restrictions. Additionally, you can plan your meals for the week or days using the meal planner feature.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## Deployed

The application is deployed and can be accessed at [https://mealmate-447u.onrender.com](https://mealmate-447u.onrender.com).
