import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks
from pathlib import Path



app = FastAPI()
templates = Jinja2Templates(directory="templates")



# Load environment variables from .env file
load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",  
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True"  
)

# Google Gemini API Config
GOOGLE_GEMINI_URL = os.getenv("GOOGLE_GEMINI_URL")
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")  

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

def get_gemini_recommendation(sex, age, height, weight, fitness_goal, fitness_type, health):
    prompt = f"""
    I am {sex}, {age} years old, with a height of {height}m and weight of {weight}kg.
    My fitness goal is {fitness_goal}, and I prefer {fitness_type} workouts.
    I have {health}.
    
    Please provide a **detailed 7-day workout plan** including:
    1️⃣ **Workout Routine** (For each day of the week, include specific exercises, repetitions, and sets).
    2️⃣ **Required Equipment** (List any necessary gym equipment).
    3️⃣ **Diet Plan** (Meal suggestions for **each day**).
    4️⃣ **Additional Recommendations** (Recovery tips, supplements, sleep schedule, and injury prevention).
    
    Please return the response in the following format:

    **Workout Routine**
    - **Monday**: [List of exercises]
    - **Tuesday**: [List of exercises]
    - **Wednesday**: [List of exercises]
    - **Thursday**: [List of exercises]
    - **Friday**: [List of exercises]
    - **Saturday**: [List of exercises]
    - **Sunday**: [List of exercises]

    **Required Equipment**
    - [List of equipment needed]

    **Diet Plan**
    - **Monday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
    - **Tuesday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
    - **Wednesday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
    - **Thursday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
    - **Friday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
    - **Saturday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
    - **Sunday**: Breakfast - [Meal], Lunch - [Meal], Dinner - [Meal]
     
    **Additional Recommendations**
    - Recovery tips: [Tips]
    - Supplements: [Recommendations]
    - Sleep schedule: [Hours per night]
    - Injury prevention: [Precautions]
    """

    headers = {"Content-Type": "application/json"}
    params = {"key": GOOGLE_GEMINI_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = httpx.post(GOOGLE_GEMINI_URL, headers=headers, params=params, json=data, timeout=60.0)
        response.raise_for_status()
        response_data = response.json()

        
        print("🔍 Full Gemini API Response:", response_data)

        if "candidates" not in response_data:
            return {"workout": "API Error: No response from Gemini", "equipment": "", "diet": "", "recommendation": ""}

        gemini_text = response_data["candidates"][0]["content"]["parts"][0]["text"]

        
        sections = {
            "workout": " workout available.",
            "equipment": " equipment specified.",
            "diet": "diet plan provided.",
            "recommendation": " additional recommendations."
        }

        lines = gemini_text.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if "**Workout Routine**" in line:
                current_section = "workout"
            elif "**Required Equipment**" in line:
                current_section = "equipment"
            elif "**Diet Plan**" in line:
                current_section = "diet"
            elif "**Additional Recommendations**" in line:
                current_section = "recommendation"
            elif current_section and line:
                sections[current_section] += "\n" + line

        return sections

    except Exception as e:
        print("❌ Error Occurred:", e)
        return {"workout": "API Error", "equipment": "", "diet": "", "recommendation": str(e)}



@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})



def generate_pdf(recommendations):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)

    text.textLine("🏋️‍♂️ Your Personalized Fitness Plan 🏋️‍♀️\n")
    text.textLine("-" * 50)

    text.textLine("\n📌 Workout Routine:")
    text.textLines(recommendations.get("workout", "No workout available."))

    text.textLine("\n🛠 Required Equipment:")
    text.textLines(recommendations.get("equipment", "No equipment specified."))

    text.textLine("\n🍽 Diet Plan:")
    text.textLines(recommendations.get("diet", "No diet plan provided."))

    text.textLine("\n📢 Additional Recommendations:")
    text.textLines(recommendations.get("recommendation", "No additional recommendations."))

    c.drawText(text)
    c.save()
    buffer.seek(0)
    return buffer

async def send_email_with_pdf(user_email, recommendations):
   
    pdf_buffer = generate_pdf(recommendations)
    temp_pdf_path = "temp_fitness_plan.pdf"

    with open(temp_pdf_path, "wb") as f:
        f.write(pdf_buffer.read())  

    message = MessageSchema(
        subject="Your Personalized Fitness Plan",
        recipients=[user_email], 
        body="Please find your personalized fitness plan attached.",
        subtype="html",
        attachments=[temp_pdf_path]  
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    
    os.remove(temp_pdf_path)

@app.post("/recommend/", response_class=HTMLResponse)
async def recommend_workout(
    request: Request,
    background_tasks: BackgroundTasks, 
    sex: str = Form(...),
    age: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    fitness_goal: str = Form(...),
    fitness_type: str = Form(...),
    health: str = Form(...),
    
    email: str = Form(...)  
):
    bmi, level = calculate_bmi(height, weight)
    
    # Fetch fitness recommendations
    recommendations = get_gemini_recommendation(sex, age, height, weight, fitness_goal, fitness_type,health)
    
    # Background email task
    background_tasks.add_task(send_email_with_pdf, email, recommendations)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "bmi": f"{bmi:.2f}",
        "bmi_level": level,
        "workout": recommendations.get("workout", "No workout available."),
        "equipment": recommendations.get("equipment", "No equipment specified."),
        "diet": recommendations.get("diet", "No diet plan provided."),
        "recommendation": recommendations.get("recommendation", "No additional recommendations.")
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 