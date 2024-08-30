"""
File: workout_planner_llm_based_tool
Description: 
This file defines an AI-powered structured tool for generating personalized workout plans using a Large Language Model (LLM). It includes:

1. A LlmWorkoutPlannerInput class that specifies the required input parameters for creating a workout plan, including fitness level, goals, available equipment, and additional preferences.

2. A create_llm_workout_plan function that generates a detailed, customized workout plan using OpenAI's GPT-4 model. This function:
   - Initializes a ChatOpenAI instance with the GPT-4 model
   - Uses a ChatPromptTemplate to create a detailed prompt for the LLM
   - Generates a comprehensive workout plan based on user inputs
   - Includes introduction, day-by-day breakdown, form cues, progression suggestions, warm-up/cool-down tips, and dietary advice

3. Integration with OpenAI's API, including setup for API key management

4. A StructuredTool object (LlmWorkoutPlannerTool) that wraps the create_llm_workout_plan function, making it compatible with LangChain's tool system

This tool leverages AI to create highly personalized and detailed workout plans, considering various factors such as fitness level, goals, equipment availability, and user preferences. It can be integrated into a larger AI agent system to provide sophisticated fitness recommendations.

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
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Optional, List
import os

# Ensure you have set your OpenAI API key in your environment variables
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"
import os
import openai

with open('../../../apikeys/api_openai_aimakerspace.key', 'r') as file:
    api_key = file.read().strip()

openai.api_key = api_key
os.environ["OPENAI_API_KEY"] = openai.api_key

class LlmWorkoutPlannerInput(BaseModel):
    fitness_level: str = Field(..., description="The user's fitness level (beginner, intermediate, advanced)")
    goal: str = Field(..., description="The user's fitness goal (e.g., weight loss, muscle gain, endurance)")
    days_per_week: int = Field(..., description="Number of workout days per week")
    duration: Optional[int] = Field(None, description="Desired workout duration in minutes (optional)")
    equipment: str = Field(..., description="Available equipment (full gym, basic dumbbells, no equipment)")
    body_weight_only: bool = Field(False, description="Whether to use only body weight exercises")
    additional_info: Optional[str] = Field(None, description="Any additional information or preferences")

def create_llm_workout_plan(
    fitness_level: str,
    goal: str,
    days_per_week: int,
    equipment: str,
    body_weight_only: bool,
    duration: Optional[int] = None,
    additional_info: Optional[str] = None
) -> str:
    # Initialize the LLM
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    # Create a prompt template
    prompt = ChatPromptTemplate.from_template("""
    You are an expert personal trainer. Create a detailed workout plan based on the following information:

    Fitness Level: {fitness_level}
    Goal: {goal}
    Days per Week: {days_per_week}
    Equipment: {equipment}
    Body Weight Only: {body_weight_only}
    Duration per Session: {duration} minutes
    Additional Information: {additional_info}

    Please create a workout plan that includes:
    1. A brief introduction explaining the plan's focus and how it aligns with the user's goals.
    2. A day-by-day breakdown of exercises, including sets, reps, and rest periods.
    3. Proper form cues for key exercises.
    4. Progression suggestions for the coming weeks.
    5. Tips for warm-up and cool-down routines.
    6. Any dietary advice that complements the workout plan.

    Ensure the plan is appropriately challenging for the specified fitness level and uses available equipment effectively.
    If body weight only is specified, focus exclusively on calisthenics and bodyweight exercises.
    """)

    # Format the prompt with user inputs
    formatted_prompt = prompt.format(
        fitness_level=fitness_level,
        goal=goal,
        days_per_week=days_per_week,
        equipment=equipment,
        body_weight_only=body_weight_only,
        duration=duration or "unspecified",
        additional_info=additional_info or "None provided"
    )

    # Generate the workout plan using the LLM
    response = llm.invoke(formatted_prompt)

    return response.content

LlmWorkoutPlannerTool = StructuredTool.from_function(
    func=create_llm_workout_plan,
    name="LlmWorkoutPlanner",
    description="Creates a personalized workout plan using AI, based on fitness level, goals, schedule, available equipment, and preferences.",
    args_schema=LlmWorkoutPlannerInput
)