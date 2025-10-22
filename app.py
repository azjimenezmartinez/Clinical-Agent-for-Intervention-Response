from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

# Using Flask app for my server application side 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# MongoDB 
client = MongoClient('localhost', 27017)
db = client.flask_database
patients = db.patients

# Routes 
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form inputs
        name = request.form.get("name")
        bandwidth = request.form.get("bandwidth")
        symptoms = request.form.get("symptoms")
        pain_level = request.form.get("pain_level")

        # Can handle image uploads if high bandwidth
        image_filename = None
        if bandwidth == "high" and "photo" in request.files:
            photo = request.files["photo"]
            if photo.filename != "":
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image_filename = filename

        # Generating a simple AIish response for now [*** Come back to this ***]
        response = generate_ai_response(symptoms, pain_level)

        # Save to MongoDB
        patient_entry = {
            "name": name, # Do I need this? Should I collect?
            "bandwidth": bandwidth,
            "symptoms": symptoms,
            "pain_level": pain_level,
            "photo": image_filename,
            "response": response
        }
        patients.insert_one(patient_entry)

        return render_template("response.html", name=name, response=response, bandwidth=bandwidth)

    return render_template("index.html")


# Simple AIish Response Generator [*** Come back to this ***]
def generate_ai_response(symptoms, pain_level):
    symptoms = symptoms.lower()
    if "fever" in symptoms and "cough" in symptoms:
        return "Possible viral infection. Recommend hydration, rest, and monitoring for 48 hours."
    elif "pain" in symptoms or int(pain_level) > 7:
        return "High pain detected. Recommend escalation to specialist care."
    elif "headache" in symptoms:
        return "Suggest over-the-counter pain relief and hydration. Escalate if persists."
    else:
        return "Symptoms unclear. Recommend further observation and symptom tracking."


if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)



