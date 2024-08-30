"""
File: workout_planner_tool
Description: 
This file defines a structured tool for generating personalized workout plans. It includes:

1. A WorkoutPlannerInput class that specifies the required input parameters for creating a workout plan, such as fitness level, goals, and available equipment.

2. A create_workout_plan function that generates a customized workout plan based on the input parameters. This function:
   - Handles different fitness levels (beginner, intermediate, advanced)
   - Accommodates various equipment scenarios (full gym, basic dumbbells, no equipment)
   - Supports body weight only workouts
   - Creates progressive plans where higher fitness levels incorporate exercises from lower levels
   - Randomly selects exercises for each workout day to provide variety
   - Adjusts rep ranges based on the user's fitness goals

3. A predefined set of exercises for different fitness levels and equipment types

4. Logic to validate input parameters and handle potential errors

5. A StructuredTool object (WorkoutPlannerTool) that wraps the create_workout_plan function, making it compatible with LangChain's tool system

This tool can be integrated into a larger AI agent system to provide tailored workout recommendations based on user inputs.

Author: Juan Olano
Date created: 8/30/2024
Last modified: 8/30/2024

This file is part of the Workout Planner Agent project.

License: MIT License

Copyright (c) {current_year} {your_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, List
import random

class WorkoutPlannerInput(BaseModel):
    fitness_level: str = Field(..., description="The user's fitness level (beginner, intermediate, advanced)")
    goal: str = Field(..., description="The user's fitness goal (e.g., weight loss, muscle gain, endurance)")
    days_per_week: int = Field(..., description="Number of workout days per week")
    duration: Optional[int] = Field(None, description="Desired workout duration in minutes (optional)")
    equipment: str = Field(..., description="Available equipment (full gym, basic dumbbells, no equipment)")
    body_weight_only: bool = Field(False, description="Whether to use only body weight exercises")

def create_workout_plan(
    fitness_level: str,
    goal: str,
    days_per_week: int,
    equipment: str,
    body_weight_only: bool,
    duration: Optional[int] = None
) -> str:
    exercises = {
        "beginner": {
            "full gym": ["Leg press", "Chest press machine", "Treadmill", "Seated cable rows", "Machine shoulder press"],
            "basic dumbbells": ["Dumbbell squats", "Dumbbell bench press", "Dumbbell rows", "Dumbbell lunges", "Dumbbell curls"],
            "no equipment": ["Bodyweight squats", "Push-ups", "Walking lunges", "Plank", "Mountain climbers"]
        },
        "intermediate": {
            "full gym": ["Barbell squats", "Bench press", "Lat pulldowns", "Romanian deadlifts", "Cable face pulls"],
            "basic dumbbells": ["Dumbbell lunges", "Dumbbell overhead press", "Dumbbell deadlifts", "Dumbbell flyes", "Dumbbell renegade rows"],
            "no equipment": ["Jump squats", "Diamond push-ups", "Burpees", "Superman holds", "Mountain climbers"]
        },
        "advanced": {
            "full gym": ["Deadlifts", "Weighted pull-ups", "Barbell rows", "Front squats", "Overhead press"],
            "basic dumbbells": ["Dumbbell clean and press", "Renegade rows", "Bulgarian split squats", "Single-leg Romanian deadlifts", "Dumbbell thrusters"],
            "no equipment": ["Pistol squats", "One-arm push-ups", "Muscle-ups", "Plyometric lunges", "L-sit holds"]
        }
    }

    body_weight_exercises = {
        "beginner": ["Bodyweight squats", "Push-ups", "Lunges", "Plank", "Mountain climbers", "Bird dogs", "Glute bridges"],
        "intermediate": ["Jump squats", "Diamond push-ups", "Burpees", "Spider-man push-ups", "V-ups", "Box jumps", "Flutter kicks"],
        "advanced": ["Pistol squats", "One-arm push-ups", "Plyometric lunges", "Handstand push-ups", "L-sit holds", "Muscle-ups", "Planche progressions"]
    }

    if fitness_level not in exercises:
        return "Invalid fitness level. Please choose beginner, intermediate, or advanced."
    
    if days_per_week < 1 or days_per_week > 7:
        return "Invalid number of days. Please choose between 1 and 7."
    
    if equipment not in ["full gym", "basic dumbbells", "no equipment"]:
        return "Invalid equipment option. Please choose full gym, basic dumbbells, or no equipment."

    workout_plan = f"Workout Plan ({fitness_level} level, {goal} focus, {days_per_week} days/week, "
    workout_plan += f"{'body weight only' if body_weight_only else equipment}):\n\n"

    if body_weight_only:
        if fitness_level == "beginner":
            exercise_pool = body_weight_exercises["beginner"]
        elif fitness_level == "intermediate":
            exercise_pool = body_weight_exercises["beginner"] + body_weight_exercises["intermediate"]
        else:  # advanced
            exercise_pool = body_weight_exercises["beginner"] + body_weight_exercises["intermediate"] + body_weight_exercises["advanced"]
    else:
        if fitness_level == "beginner":
            exercise_pool = exercises["beginner"][equipment]
        elif fitness_level == "intermediate":
            exercise_pool = exercises["beginner"][equipment] + exercises["intermediate"][equipment]
        else:  # advanced
            exercise_pool = exercises["beginner"][equipment] + exercises["intermediate"][equipment] + exercises["advanced"][equipment]

    for day in range(1, days_per_week + 1):
        workout_plan += f"Day {day}:\n"
        daily_exercises = random.sample(exercise_pool, min(5, len(exercise_pool)))
        for exercise in daily_exercises:
            reps = "10-15 reps" if "weight" in goal.lower() or "muscle" in goal.lower() else "30-60 seconds"
            workout_plan += f"- {exercise}: 3 sets of {reps}\n"
        workout_plan += "- Cool-down: 5-10 minutes of light stretching\n\n"
    
    if duration:
        workout_plan += f"Aim to complete each workout session in about {duration} minutes.\n"
    
    return workout_plan

WorkoutPlannerTool = StructuredTool.from_function(
    func=create_workout_plan,
    name="WorkoutPlanner",
    description="Creates a personalized workout plan based on fitness level, goals, schedule, available equipment, and preference for body weight exercises.",
    args_schema=WorkoutPlannerInput
)