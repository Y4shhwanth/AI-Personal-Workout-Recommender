from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import joblib
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("workout_recommender.keras")
vectorizer = joblib.load("vectorizer.pkl")
exercise_encoder = joblib.load("exercise_encoder.pkl")
df = joblib.load("dataframe.pkl")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class UserInput(BaseModel):
    sex: str
    age: int
    height: float
    weight: float
    fitness_goal: str
    fitness_type: str
    hypertension: str
    diabetes: str

def calculate_bmi(height, weight):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        return bmi, 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return bmi, 'Normal weight'
    elif 25 <= bmi < 29.9:
        return bmi, 'Overweight'
    else:
        return bmi, 'Obese'

@app.post("/recommend/", response_class=HTMLResponse)
def recommend_workout(request: Request,
    sex: str = Form(...),
    age: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    fitness_goal: str = Form(...),
    fitness_type: str = Form(...),
    hypertension: str = Form(...),
    diabetes: str = Form(...)):
    
    bmi, level = calculate_bmi(height, weight)
    processed_input = f"{sex} {age} {bmi:.2f} {level} {fitness_goal} {fitness_type} {hypertension} {diabetes}"
    input_vector = vectorizer([processed_input])
    prediction = model.predict(input_vector)
    predicted_label = list(exercise_encoder.keys())[tf.argmax(prediction).numpy()[0]]
    predicted_equipment = df[df['Exercises'] == predicted_label]['Equipment'].values[0]
    predicted_diet = df[df['Exercises'] == predicted_label]['Diet'].values[0]
    predicted_recommendation = df[df['Exercises'] == predicted_label]['Recommendation'].values[0]
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "workout": predicted_label,
        "equipment": predicted_equipment,
        "diet": predicted_diet,
        "recommendation": predicted_recommendation
    })

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
