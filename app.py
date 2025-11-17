from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Recipe dataset
recipes_data = [
    # INDIAN CUISINE
    ["Masala Dosa", 350, 8, 10, 58, "vegan", "rice,lentils,potato,spices", 25, "breakfast,indian"],
    ["Idli with Sambar", 280, 10, 6, 48, "vegan", "rice,lentils,vegetables,spices", 20, "breakfast,indian"],
    ["Poha", 320, 8, 8, 55, "vegan", "flattened rice,peanuts,turmeric,vegetables", 15, "breakfast,indian,quick"],
    ["Upma", 300, 9, 7, 52, "vegan", "semolina,vegetables,mustard seeds,curry leaves", 15, "breakfast,indian,quick"],
    ["Paratha with Yogurt", 380, 12, 15, 48, "vegetarian", "wheat flour,ghee,yogurt,pickle", 20, "breakfast,indian"],
    ["Palak Paneer with Roti", 520, 22, 28, 45, "vegetarian", "spinach,paneer,roti,spices", 25, "lunch,dinner,indian"],
    ["Dal Tadka with Rice", 480, 18, 12, 75, "vegan", "lentils,rice,ghee,spices", 30, "lunch,dinner,indian"],
    ["Chole Bhature", 620, 16, 22, 85, "vegan", "chickpeas,flour,spices,oil", 35, "lunch,indian"],
    ["Rajma Chawal", 520, 18, 10, 88, "vegan", "kidney beans,rice,tomato,spices", 30, "lunch,dinner,indian"],
    ["Vegetable Biryani", 550, 14, 16, 85, "vegetarian", "basmati rice,vegetables,spices,ghee", 40, "lunch,dinner,indian"],
    ["Chicken Curry with Rice", 620, 42, 22, 58, "non-vegetarian", "chicken,rice,curry spices,coconut milk", 30, "lunch,dinner,indian"],
    ["Fish Curry", 420, 38, 18, 22, "non-vegetarian", "fish,coconut milk,curry leaves,spices", 25, "dinner,indian"],
    ["Paneer Bhurji with Roti", 540, 24, 30, 40, "vegetarian", "paneer,tomato,onion,spices", 20, "dinner,indian"],
    ["Chickpea Curry", 480, 18, 16, 65, "vegan", "chickpeas,tomato,onion,spices", 28, "lunch,dinner,indian"],
    ["Samosa", 320, 6, 16, 40, "vegan", "potato,peas,flour,spices", 30, "snack,indian"],
    
    # CHINESE CUISINE
    ["Vegetable Fried Rice", 420, 12, 14, 62, "vegan", "rice,mixed vegetables,soy sauce,sesame oil", 15, "lunch,dinner,chinese,quick"],
    ["Chicken Fried Rice", 540, 32, 18, 58, "non-vegetarian", "chicken,rice,egg,vegetables,soy sauce", 20, "lunch,dinner,chinese"],
    ["Tofu Stir Fry", 380, 22, 16, 38, "vegan", "tofu,bok choy,ginger,soy sauce", 18, "lunch,dinner,chinese,quick"],
    ["Kung Pao Chicken", 480, 36, 22, 32, "non-vegetarian", "chicken,peanuts,vegetables,chili", 20, "dinner,chinese"],
    ["Mapo Tofu", 420, 20, 24, 28, "vegan", "tofu,sichuan pepper,fermented beans,scallions", 20, "dinner,chinese"],
    ["Egg Drop Soup", 120, 10, 5, 8, "vegetarian", "egg,chicken broth,cornstarch,scallions", 10, "snack,soup,chinese,quick"],
    ["Spring Rolls", 280, 8, 12, 36, "vegan", "rice paper,vegetables,vermicelli,soy sauce", 15, "snack,chinese"],
    
    # JAPANESE CUISINE
    ["Miso Soup", 120, 8, 4, 12, "vegan", "miso paste,tofu,seaweed,scallion", 10, "snack,soup,japanese,quick"],
    ["Chicken Teriyaki Bowl", 580, 38, 18, 62, "non-vegetarian", "chicken,rice,teriyaki sauce,vegetables", 25, "lunch,dinner,japanese"],
    ["Salmon Sushi Bowl", 520, 36, 20, 48, "non-vegetarian", "salmon,sushi rice,avocado,seaweed", 20, "lunch,dinner,japanese"],
    ["Tofu Teriyaki", 380, 24, 16, 38, "vegan", "tofu,teriyaki sauce,sesame seeds,vegetables", 18, "lunch,dinner,japanese"],
    ["Vegetable Tempura", 320, 8, 15, 38, "vegetarian", "mixed vegetables,tempura batter,dipping sauce", 20, "lunch,snack,japanese"],
    ["Edamame", 180, 16, 8, 14, "vegan", "soybeans,sea salt", 5, "snack,japanese,quick"],
    
    # MEDITERRANEAN
    ["Hummus with Veggies", 220, 8, 12, 22, "vegan", "chickpeas,tahini,carrot,cucumber", 5, "snack,mediterranean,quick"],
    ["Greek Salad", 280, 8, 18, 18, "vegetarian", "feta,cucumber,tomato,olives,olive oil", 10, "lunch,salad,mediterranean,quick"],
    ["Falafel Wrap", 480, 16, 20, 58, "vegan", "falafel,pita,tahini,vegetables", 15, "lunch,mediterranean"],
    ["Grilled Chicken Shawarma", 520, 42, 22, 38, "non-vegetarian", "chicken,pita,tahini,vegetables", 25, "lunch,dinner,mediterranean"],
    ["Tabbouleh", 180, 6, 8, 24, "vegan", "bulgur wheat,parsley,tomato,lemon,olive oil", 15, "snack,salad,mediterranean"],
    ["Shakshuka", 320, 18, 20, 18, "vegetarian", "eggs,tomato,peppers,cumin,paprika", 20, "breakfast,mediterranean"],
    
    # ITALIAN CUISINE
    ["Margherita Pizza", 520, 20, 18, 62, "vegetarian", "dough,mozzarella,tomato,basil", 25, "lunch,dinner,italian"],
    ["Pasta Primavera", 480, 16, 14, 72, "vegetarian", "pasta,vegetables,olive oil,parmesan", 20, "lunch,dinner,italian"],
    ["Chicken Alfredo Pasta", 780, 42, 32, 72, "non-vegetarian", "chicken,pasta,cream,parmesan", 25, "dinner,italian"],
    ["Caprese Salad", 240, 12, 16, 12, "vegetarian", "mozzarella,tomato,basil,olive oil", 5, "lunch,salad,italian,quick"],
    ["Veggie Lasagna", 580, 26, 24, 62, "vegetarian", "pasta,ricotta,spinach,tomato sauce", 35, "dinner,italian"],
    ["Minestrone Soup", 220, 10, 6, 32, "vegan", "vegetables,beans,pasta,tomato", 25, "lunch,soup,italian"],
    
    # MEXICAN CUISINE
    ["Black Bean Tacos", 520, 20, 16, 68, "vegan", "black beans,corn tortilla,avocado,salsa", 20, "lunch,dinner,mexican"],
    ["Chicken Burrito Bowl", 620, 38, 22, 62, "non-vegetarian", "chicken,rice,beans,cheese,guacamole", 20, "lunch,dinner,mexican"],
    ["Vegetarian Enchiladas", 540, 22, 20, 58, "vegetarian", "tortilla,cheese,beans,enchilada sauce", 30, "dinner,mexican"],
    ["Cheese Quesadilla", 480, 20, 24, 42, "vegetarian", "tortilla,cheese,peppers,salsa", 12, "lunch,mexican,quick"],
    ["Guacamole with Chips", 320, 6, 22, 28, "vegan", "avocado,lime,cilantro,tortilla chips", 8, "snack,mexican,quick"],
    
    # THAI CUISINE
    ["Pad Thai", 580, 20, 18, 78, "non-vegetarian", "rice noodles,shrimp,egg,tamarind,peanuts", 25, "lunch,dinner,thai"],
    ["Green Curry with Rice", 520, 16, 24, 62, "vegan", "vegetables,coconut milk,green curry paste,rice", 25, "dinner,thai"],
    ["Tom Yum Soup", 180, 12, 6, 18, "non-vegetarian", "shrimp,lemongrass,lime,mushrooms", 20, "snack,soup,thai"],
    ["Thai Basil Chicken", 480, 36, 20, 38, "non-vegetarian", "chicken,basil,chili,soy sauce", 18, "dinner,thai,quick"],
    
    # AMERICAN/WESTERN
    ["Oatmeal with Banana", 350, 10, 5, 60, "vegetarian", "oats,banana,milk,honey", 10, "breakfast,american,quick"],
    ["Greek Yogurt Parfait", 320, 18, 8, 42, "vegetarian", "greek yogurt,granola,berries,honey", 5, "breakfast,american,quick"],
    ["Egg Omelette with Veggies", 300, 18, 20, 8, "non-vegetarian", "eggs,peppers,onion,tomato", 10, "breakfast,american,quick"],
    ["Avocado Toast", 380, 12, 18, 42, "vegan", "whole wheat bread,avocado,tomato,seeds", 8, "breakfast,american,quick"],
    ["Protein Pancakes", 420, 24, 12, 48, "vegetarian", "oats,egg,banana,protein powder", 15, "breakfast,american"],
    ["Grilled Chicken Breast", 380, 45, 12, 5, "non-vegetarian", "chicken breast,herbs,olive oil", 20, "lunch,dinner,american"],
    ["Turkey Wrap", 450, 30, 16, 40, "non-vegetarian", "turkey,tortilla,lettuce,hummus", 10, "lunch,american,quick"],
    ["Chicken Salad", 420, 35, 15, 25, "non-vegetarian", "chicken,lettuce,tomato,olive oil", 15, "lunch,salad,american"],
    ["Salmon with Quinoa", 540, 38, 24, 42, "non-vegetarian", "salmon,quinoa,asparagus,lemon", 25, "dinner,american"],
    ["Veg Sandwich", 290, 9, 12, 36, "vegetarian", "bread,lettuce,cucumber,tomato", 8, "snack,american,quick"],
    ["Cottage Cheese Bowl", 280, 28, 8, 18, "vegetarian", "cottage cheese,berries,honey", 5, "snack,american,quick"],
    ["Mixed Nuts", 320, 10, 28, 12, "vegan", "almonds,cashews,walnuts", 1, "snack,american,quick"],
    ["Apple with Peanut Butter", 280, 8, 16, 32, "vegan", "apple,peanut butter", 2, "snack,american,quick"],
    ["Protein Shake", 280, 25, 6, 28, "vegetarian", "whey protein,banana,almond milk", 3, "snack,drink,american,quick"],
    
    # KOREAN CUISINE
    ["Bibimbap", 580, 24, 18, 78, "non-vegetarian", "rice,vegetables,egg,gochujang,beef", 25, "lunch,dinner,korean"],
    ["Kimchi Fried Rice", 420, 16, 14, 58, "vegan", "rice,kimchi,vegetables,sesame oil", 15, "lunch,dinner,korean,quick"],
    ["Korean BBQ Tofu", 380, 22, 18, 32, "vegan", "tofu,gochujang,sesame,vegetables", 20, "dinner,korean"],
    
    # UNIVERSAL
    ["Buddha Bowl", 550, 18, 22, 68, "vegan", "quinoa,chickpeas,avocado,kale,tahini", 25, "lunch,dinner"],
    ["Quinoa Chickpea Salad", 520, 20, 18, 60, "vegan", "quinoa,chickpeas,tomato,cucumber,olive oil", 20, "lunch,salad"],
    ["Lentil Soup", 380, 22, 9, 45, "vegan", "lentils,carrot,onion,spices", 20, "lunch,soup"],
    ["Scrambled Tofu", 290, 16, 14, 25, "vegan", "tofu,turmeric,spinach,onion", 12, "breakfast"],
]

columns = ["name", "calories", "protein", "fat", "carbs", "diet_type", "ingredients", "prep_time", "tags"]
recipes_df = pd.DataFrame(recipes_data, columns=columns)

def calculate_nutrition_targets(weight, height, age, gender, activity_level, goal="maintain"):
    """Calculate BMR, TDEE, and macro targets"""
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {"low": 1.2, "medium": 1.55, "high": 1.9}
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)

    goal_adjustments = {"lose": -500, "maintain": 0, "gain": 300}
    target_calories = tdee + goal_adjustments.get(goal, 0)

    protein_target = weight * 2.0
    fat_target = (target_calories * 0.25) / 9
    carbs_target = (target_calories - (protein_target * 4) - (fat_target * 9)) / 4

    return {
        "calories": round(target_calories),
        "protein": round(protein_target),
        "fat": round(fat_target),
        "carbs": round(carbs_target),
        "bmr": round(bmr),
        "tdee": round(tdee)
    }

def assess_health_status(weight, height, age, gender, activity_level):
    """Calculate BMI and health status"""
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
        bmi_risk = "May lead to weakened immunity and nutrient deficiencies"
    elif 18.5 <= bmi < 25:
        bmi_status = "Normal"
        bmi_risk = "Healthy weight range"
    elif 25 <= bmi < 30:
        bmi_status = "Overweight"
        bmi_risk = "Increased risk of heart disease and diabetes"
    else:
        bmi_status = "Obese"
        bmi_risk = "High risk - consider medical consultation"

    ideal_weight_min = 18.5 * (height_m ** 2)
    ideal_weight_max = 24.9 * (height_m ** 2)

    return {
        "bmi": round(bmi, 1),
        "bmi_status": bmi_status,
        "bmi_risk": bmi_risk,
        "ideal_weight_range": [round(ideal_weight_min, 1), round(ideal_weight_max, 1)]
    }

def optimize_meal_plan(user_input, recipes_df):
    """Generate optimized meal plan"""
    targets = calculate_nutrition_targets(
        user_input["weight"], user_input["height"], user_input["age"],
        user_input["gender"], user_input["activity_level"], user_input.get("goal", "maintain")
    )

    meals_per_day = user_input.get("meals_per_day", 3)

    # Filter by diet type
    if user_input["diet_type"] != "any":
        allowed = recipes_df[recipes_df["diet_type"] == user_input["diet_type"]].copy()
    else:
        allowed = recipes_df.copy()

    # Filter by cuisine
    if user_input.get("cuisine", "any") != "any":
        cuisine_filter = user_input["cuisine"]
        allowed = allowed[allowed["tags"].str.contains(cuisine_filter, case=False, na=False)]

    if len(allowed) < meals_per_day:
        return {"error": "Not enough recipes for selected filters"}

    # Categorize meals
    breakfast = allowed[allowed["tags"].str.contains("breakfast")]
    lunch = allowed[allowed["tags"].str.contains("lunch")]
    dinner = allowed[allowed["tags"].str.contains("dinner")]
    snacks = allowed[allowed["tags"].str.contains("snack")]

    # Build meal plan
    selected_meals = []

    if meals_per_day == 2:
        if len(breakfast) > 0 and len(dinner) > 0:
            selected_meals.append(breakfast.sample(1).iloc[0].to_dict())
            selected_meals.append(dinner.sample(1).iloc[0].to_dict())
    elif meals_per_day == 3:
        if len(breakfast) > 0 and len(lunch) > 0 and len(dinner) > 0:
            selected_meals.append(breakfast.sample(1).iloc[0].to_dict())
            selected_meals.append(lunch.sample(1).iloc[0].to_dict())
            selected_meals.append(dinner.sample(1).iloc[0].to_dict())
    elif meals_per_day == 4:
        if len(breakfast) > 0 and len(lunch) > 0 and len(dinner) > 0 and len(snacks) > 0:
            selected_meals.append(breakfast.sample(1).iloc[0].to_dict())
            selected_meals.append(lunch.sample(1).iloc[0].to_dict())
            selected_meals.append(snacks.sample(1).iloc[0].to_dict())
            selected_meals.append(dinner.sample(1).iloc[0].to_dict())
    else:  # 5 meals
        if len(breakfast) > 0 and len(lunch) > 0 and len(dinner) > 0 and len(snacks) >= 2:
            selected_meals.append(breakfast.sample(1).iloc[0].to_dict())
            selected_meals.append(snacks.sample(1).iloc[0].to_dict())
            selected_meals.append(lunch.sample(1).iloc[0].to_dict())
            snack2 = snacks[~snacks["name"].isin([selected_meals[1]["name"]])]
            selected_meals.append((snack2.sample(1).iloc[0] if len(snack2) > 0 else snacks.sample(1).iloc[0]).to_dict())
            selected_meals.append(dinner.sample(1).iloc[0].to_dict())

    # Calculate totals
    total_cal = sum(m["calories"] for m in selected_meals)
    total_protein = sum(m["protein"] for m in selected_meals)
    total_fat = sum(m["fat"] for m in selected_meals)
    total_carbs = sum(m["carbs"] for m in selected_meals)

    cal_accuracy = 100 - abs((total_cal - targets["calories"]) / targets["calories"] * 100)
    protein_accuracy = 100 - abs((total_protein - targets["protein"]) / targets["protein"] * 100)

    return {
        "targets": targets,
        "meals_per_day": meals_per_day,
        "totals": {
            "calories": total_cal,
            "protein": total_protein,
            "fat": total_fat,
            "carbs": total_carbs
        },
        "accuracy": {
            "calories": round(max(0, cal_accuracy), 1),
            "protein": round(max(0, protein_accuracy), 1)
        },
        "meals": selected_meals
    }

def generate_exercise_plan(user_data, health_status):
    """Generate personalized exercise recommendations"""
    exercises = {
        "cardio": [],
        "strength": [],
        "flexibility": [],
        "weekly_schedule": []
    }

    bmi = health_status["bmi"]
    goal = user_data.get("goal", "maintain")
    activity = user_data["activity_level"]

    # Cardio recommendations based on BMI and goal
    if bmi < 18.5:  # Underweight
        exercises["cardio"] = [
            "🚶 Light walking: 20-30 min, 3x/week",
            "🚴 Stationary cycling: 15-20 min, 2x/week (low intensity)",
            "🏊 Swimming: 20 min, 2x/week (builds muscle without high impact)"
        ]
    elif bmi >= 30:  # Obese
        exercises["cardio"] = [
            "🚶 Walking: 30-45 min, 5-6x/week (low impact, joint-friendly)",
            "🚴 Cycling: 20-30 min, 3x/week",
            "💧 Water aerobics: 30 min, 2x/week (excellent for joints)",
            "🏋️ Elliptical: 20-25 min, 2-3x/week (low impact)"
        ]
    elif bmi >= 25:  # Overweight
        exercises["cardio"] = [
            "🏃 Brisk walking/jogging: 30-45 min, 4-5x/week",
            "🚴 Cycling: 30-40 min, 3x/week",
            "🏊 Swimming: 30 min, 2x/week",
            "⛰️ Stair climbing: 15-20 min, 2x/week"
        ]
    else:  # Normal weight
        exercises["cardio"] = [
            "🏃 Running: 30-40 min, 3-4x/week",
            "🚴 HIIT cycling: 20-30 min, 2x/week",
            "🏊 Swimming: 30-45 min, 2x/week",
            "🎾 Sports (tennis, basketball): 45-60 min, 2x/week"
        ]

    # Strength training based on goal
    if goal == "gain" or bmi < 18.5:
        exercises["strength"] = [
            "🏋️ Compound lifts: Squats, Deadlifts, Bench Press (3 sets × 8-12 reps)",
            "💪 Upper body: Pull-ups, Rows, Shoulder Press (3 sets × 8-12 reps)",
            "🦵 Lower body: Lunges, Leg Press, Calf Raises (3 sets × 10-15 reps)",
            "💪 Core: Planks (3 × 30-60 sec), Ab wheel rollouts",
            "📅 Frequency: 4-5 days/week, progressive overload",
            "⏱️ Rest: 60-90 seconds between sets"
        ]
    elif goal == "lose":
        exercises["strength"] = [
            "🏋️ Circuit training: 3 sets × 12-15 reps (minimal rest)",
            "💪 Bodyweight: Push-ups, Squats, Lunges, Burpees",
            "🏋️ Resistance bands: Full body workout",
            "💪 Core circuit: Planks, Mountain climbers, Bicycle crunches",
            "📅 Frequency: 3-4 days/week",
            "⏱️ Rest: 30-45 seconds between exercises"
        ]
    else:  # Maintain
        exercises["strength"] = [
            "🏋️ Full body workout: 3 sets × 10-12 reps",
            "💪 Upper: Bench press, Rows, Overhead press",
            "🦵 Lower: Squats, Deadlifts, Leg curls",
            "💪 Core: Weighted planks, Cable rotations",
            "📅 Frequency: 3 days/week",
            "⏱️ Rest: 45-60 seconds between sets"
        ]

    # Flexibility and recovery
    exercises["flexibility"] = [
        "🧘 Yoga: 20-30 min, 2-3x/week (improves flexibility & reduces stress)",
        "🤸 Dynamic stretching: 10 min before workouts",
        "🧘 Static stretching: 10-15 min after workouts",
        "🎯 Foam rolling: 10 min, 3-4x/week (muscle recovery)",
        "🧘 Meditation: 10-15 min daily (mental health)"
    ]

    # Weekly schedule template
    if activity == "low":
        exercises["weekly_schedule"] = [
            "Monday: 30 min walk + 10 min stretching",
            "Tuesday: Rest or light yoga",
            "Wednesday: 20 min bodyweight exercises + 30 min walk",
            "Thursday: Rest or 20 min yoga",
            "Friday: 30 min walk + 10 min core work",
            "Saturday: 30-45 min outdoor activity (cycling, hiking)",
            "Sunday: Rest day"
        ]
    elif activity == "medium":
        exercises["weekly_schedule"] = [
            "Monday: 30 min cardio + 20 min upper body strength",
            "Tuesday: 30 min yoga or active recovery",
            "Wednesday: 30 min HIIT + 15 min core",
            "Thursday: 30 min cardio + 20 min lower body strength",
            "Friday: Rest or light activity",
            "Saturday: 45 min full body workout or sports",
            "Sunday: 30 min yoga + stretching"
        ]
    else:  # High activity
        exercises["weekly_schedule"] = [
            "Monday: 40 min cardio + 30 min upper body strength",
            "Tuesday: 30 min HIIT + 20 min core",
            "Wednesday: 40 min cardio + 30 min lower body strength",
            "Thursday: Active recovery (yoga, swimming)",
            "Friday: 40 min cardio + 30 min full body circuit",
            "Saturday: 60 min intense workout or sports",
            "Sunday: 30 min yoga + foam rolling"
        ]

    return exercises

def generate_health_suggestions(user_data, health_status, plan):
    """Generate personalized health suggestions"""
    suggestions = []

    # BMI-based suggestions
    if health_status["bmi"] < 18.5:
        suggestions.extend([
            "🎯 Focus on calorie-dense, nutrient-rich foods",
            "💪 Include strength training 3-4x per week to build muscle mass",
            "🥜 Add healthy fats: nuts, avocados, olive oil",
            "🍽️ Eat 5-6 smaller meals throughout the day",
            "💊 Consider a multivitamin supplement (consult doctor)"
        ])
    elif health_status["bmi"] >= 25:
        suggestions.extend([
            "🏃 Increase physical activity to 45-60 min daily",
            "🥗 Focus on high-fiber, low-calorie vegetables",
            "💧 Drink 8-10 glasses of water daily",
            "🍬 Reduce sugar and processed foods",
            "📊 Track your calories and maintain a 300-500 deficit"
        ])
    else:
        suggestions.extend([
            "✅ Maintain your current healthy weight",
            "🏋️ Continue regular exercise routine",
            "🥗 Focus on balanced nutrition"
        ])

    # Activity level suggestions
    if user_data["activity_level"] == "low":
        suggestions.append("🚶 Start with 30 min daily walks and gradually increase")
        suggestions.append("🧘 Try yoga or stretching for flexibility")
    elif user_data["activity_level"] == "medium":
        suggestions.append("💪 Add 2-3 strength training sessions per week")
    else:
        suggestions.append("⚡ Ensure adequate rest and recovery days")
        suggestions.append("🥤 Stay well-hydrated during intense workouts")

    # Goal-specific suggestions
    goal = user_data.get("goal", "maintain")
    if goal == "lose":
        suggestions.extend([
            "📉 Aim for 0.5-1kg weight loss per week (safe rate)",
            "🍽️ Use smaller plates to control portion sizes",
            "😴 Get 7-8 hours of quality sleep",
            "📝 Keep a food journal to track progress"
        ])
    elif goal == "gain":
        suggestions.extend([
            "📈 Aim for 0.25-0.5kg weight gain per week",
            "🥩 Prioritize protein (aim for 2g per kg body weight)",
            "🏋️ Focus on progressive overload in strength training",
            "🍚 Don't skip meals, especially post-workout"
        ])

    # Protein adequacy check
    protein_ratio = plan["totals"]["protein"] / user_data["weight"]
    if protein_ratio < 1.2:
        suggestions.append("⚠️ Increase protein intake - current level may be insufficient")

    # General wellness tips
    suggestions.extend([
        "🧘 Practice stress management (meditation, deep breathing)",
        "🥦 Eat a variety of colorful vegetables daily",
        "☀️ Get 15-20 min of sunlight daily for vitamin D"
    ])

    return suggestions

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """Generate meal plan endpoint"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['age', 'gender', 'height', 'weight', 'activity_level', 'diet_type', 'goal', 'meals_per_day']
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Generate health assessment
        health_status = assess_health_status(
            data["weight"], data["height"], data["age"], 
            data["gender"], data["activity_level"]
        )
        
        # Generate meal plan
        plan = optimize_meal_plan(data, recipes_df)
        
        if "error" in plan:
            return jsonify(plan), 400
        
        # Generate suggestions
        suggestions = generate_health_suggestions(data, health_status, plan)
        
        return jsonify({
            "health_status": health_status,
            "plan": plan,
            "suggestions": suggestions
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health-assessment', methods=['POST'])
def health_assessment():
    """Health assessment endpoint"""
    try:
        data = request.json
        health_status = assess_health_status(
            data["weight"], data["height"], data["age"],
            data["gender"], data["activity_level"]
        )
        return jsonify(health_status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/exercise-plan', methods=['POST'])
def exercise_plan():
    """Generate exercise plan endpoint"""
    try:
        data = request.json
        
        # Generate health assessment
        health_status = assess_health_status(
            data["weight"], data["height"], data["age"],
            data["gender"], data["activity_level"]
        )
        
        # Generate exercise plan
        exercises = generate_exercise_plan(data, health_status)
        
        # Generate exercise tips
        tips = [
            "⏰ Consistency is key - schedule workouts like appointments",
            "📈 Track your progress - note weights, reps, and how you feel",
            "💧 Stay hydrated - drink water before, during, and after workouts",
            "🍽️ Fuel properly - eat protein + carbs within 2 hours post-workout",
            "😴 Prioritize recovery - muscles grow during rest, not during workout",
            "🎵 Make it fun - listen to music or workout with friends",
            "📱 Use fitness apps to track progress and stay motivated",
            "⚠️ Listen to your body - rest if you feel pain or excessive fatigue",
            "🎯 Set SMART goals - Specific, Measurable, Achievable, Relevant, Time-bound",
            "👥 Consider a personal trainer for proper form and motivation"
        ]
        
        # Goal-specific advice
        goal_advice = []
        if data.get("goal") == "lose":
            goal_advice = [
                "🔥 Focus on burning calories through cardio and HIIT",
                "💪 Maintain muscle mass with strength training 3x/week",
                "⏱️ Create a calorie deficit: exercise + diet combined",
                "📊 Aim for 150-300 minutes of moderate cardio per week",
                f"🎯 Target heart rate: 60-75% of max ({220 - data['age']} bpm max)"
            ]
        elif data.get("goal") == "gain":
            goal_advice = [
                "🏋️ Prioritize strength training with progressive overload",
                "💪 Focus on compound movements for maximum muscle gain",
                "🍽️ Eat in calorie surplus, especially post-workout",
                "⏱️ Limit cardio to 2-3x/week to preserve calories",
                "😴 Get 8-9 hours of sleep for optimal muscle recovery"
            ]
        else:
            goal_advice = [
                "⚖️ Balance cardio and strength training equally",
                "🎯 Maintain current fitness level with consistency",
                "💪 Challenge yourself progressively to avoid plateaus",
                "🧘 Focus on overall wellness and injury prevention",
                "🏃 Mix up your routine to keep it interesting"
            ]
        
        return jsonify({
            "health_status": health_status,
            "exercises": exercises,
            "tips": tips,
            "goal_advice": goal_advice
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cuisines', methods=['GET'])
def get_cuisines():
    """Get available cuisines"""
    cuisines = ['any', 'indian', 'chinese', 'japanese', 'mediterranean', 
                'italian', 'mexican', 'thai', 'american', 'korean']
    return jsonify(cuisines)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
