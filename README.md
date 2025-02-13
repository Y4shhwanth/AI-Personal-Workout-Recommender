# **🏋️ AI-Powered Workout Recommendation Web App**

🚀 **AI-based fitness planner** that provides **personalized workout plans, equipment suggestions, diet recommendations, and fitness tips** based on user input. Built using **FastAPI, TensorFlow, Jinja2, and HTML/CSS**.

---

## **🔹 Features**
✅ **Personalized Workout Plans** – Get AI-generated workout recommendations tailored to your fitness goals.  
✅ **Diet & Equipment Suggestions** – Receive nutrition advice and the necessary gym equipment for your routine.  
✅ **BMI-Based Categorization** – Automatically calculates **BMI** and adjusts recommendations accordingly.  
✅ **Interactive UI** – Sleek, gym-inspired user interface with a modern **black & gold fitness theme**.  
✅ **AI-Driven Predictions** – Uses **TensorFlow & NLP** to process user inputs and generate results.  
✅ **FastAPI Backend** – Lightweight, high-performance API framework for seamless integration.  

---

## **🔧 Tech Stack**
- **Frontend:** HTML, CSS (Styled for a fitness theme)  
- **Backend:** FastAPI (Python)  
- **AI Model:** TensorFlow (Deep Learning)  
- **Data Processing:** Pandas, Joblib  
- **Templating:** Jinja2  

---

## **🚀 Installation & Setup**
1️⃣ **Clone the repository**  
```bash
git clone https://github.com/yourusername/workout-recommender.git
cd workout-recommender
```

2️⃣ **Install dependencies**  
```bash
pip install -r requirements.txt
```

3️⃣ **Run the FastAPI server**  
```bash
uvicorn app:app --reload
```

4️⃣ **Access the UI**  
Open **`http://127.0.0.1:8000/`** in your browser.

---

## **📂 Project Structure**
```
📂 workout-recommender
 ├── 📁 templates        # HTML templates for UI
 │   ├── form.html       # Input form for user details
 │   ├── result.html     # Styled results page
 ├── 📂 static           # CSS, Images (Optional)
 ├── app.py             # FastAPI backend with AI model integration
 ├── workout_recommender.keras  # Pre-trained AI model
 ├── vectorizer.pkl     # NLP vectorizer
 ├── exercise_encoder.pkl  # Label encoder
 ├── dataframe.pkl      # Processed dataset for equipment, diet, and recommendations
 ├── requirements.txt   # Python dependencies
 ├── README.md          # Documentation (You’re reading it!)
```

---

## **🌟 How It Works**
1️⃣ **User enters details** (Age, Height, Weight, Fitness Goal, etc.) on the **form page**.  
2️⃣ **AI model processes input** using **Natural Language Processing (NLP)** and deep learning.  
3️⃣ **System predicts a workout plan** along with **equipment, diet, and tips**.  
4️⃣ **User gets a visually appealing, fitness-themed results page** with suggestions.  

---

## **🛠 Future Enhancements**
🔹 **User Authentication** – Allow users to save their workout history.  
🔹 **Progress Tracking** – Track fitness progress using graphs & analytics.  
🔹 **Real-Time Recommendations** – Improve AI by integrating **live feedback** from users.  

---

## **📜 License**
This project is **open-source** under the **MIT License**. Feel free to use, modify, and contribute!  

---

## **🙌 Contributing**
Want to improve this project? **Fork the repo, make changes, and submit a pull request!** 🚀  

---

## **📞 Contact & Support**
If you have questions or suggestions, feel free to reach out!  
💬 **Email:** yashwanth_22csb63@kgkite.ac.in or yy4972765@gmail.com  
🐙 **GitHub:** [yourusername](https://github.com/Y4shhwanth)  

---

