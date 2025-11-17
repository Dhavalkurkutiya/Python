# AI Diet Plan Generator

A personalized diet plan generator with Flask backend and modern web frontend.

## Features

- 🎯 Personalized meal plans based on your profile
- 📊 BMI calculation and health assessment
- 🥗 Multiple cuisine options (Indian, Chinese, Japanese, Mediterranean, etc.)
- 💪 Nutritional targets (BMR, TDEE, macros)
- 💡 Health suggestions and recommendations
- 🍽️ Flexible meal plans (2-5 meals per day)
- 🌱 Diet type filters (Vegetarian, Vegan, Non-Vegetarian)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Flask Backend

```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

### 3. Open the Frontend

Simply open `index.html` in your web browser, or use a local server:

```bash
# Using Python's built-in server
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

## Usage

1. Fill in your personal information:
   - Age, Gender, Height, Weight
   - Activity Level
   - Diet Type (Vegetarian/Vegan/Non-Vegetarian/Any)
   - Goal (Lose/Maintain/Gain weight)
   - Cuisine Preference
   - Meals per day

2. Click "Generate Meal Plan" to get your personalized diet plan

3. Click "Health Assessment" for detailed health analysis

## API Endpoints

### POST /api/generate-plan
Generate a complete meal plan with health assessment

**Request Body:**
```json
{
  "age": 25,
  "gender": "male",
  "height": 170,
  "weight": 65,
  "activity_level": "medium",
  "diet_type": "any",
  "goal": "maintain",
  "cuisine": "any",
  "meals_per_day": 3
}
```

### POST /api/health-assessment
Get health assessment only

**Request Body:**
```json
{
  "age": 25,
  "gender": "male",
  "height": 170,
  "weight": 65,
  "activity_level": "medium"
}
```

### GET /api/cuisines
Get list of available cuisines

## Technologies Used

- **Backend:** Flask, Pandas, NumPy
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **API:** RESTful API with JSON responses

## Project Structure

```
.
├── app.py              # Flask backend API
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── main.py            # Original Jupyter notebook code
```

## Notes

- The backend must be running for the frontend to work
- Make sure CORS is enabled (already configured in app.py)
- Default port for Flask: 5000
- The frontend can be served from any web server or opened directly
