from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient 

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["cair_db"]
patients_collection = db["patients"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/patients")
def patients():
    patients = list(patients_collection.find())
    return render_template("patients.html", patients=patients)

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        symptoms = request.form["symptoms"]

        patient = {
            "name": name,
            "age": age,
            "symptoms": symptoms,
            "recommendation": "will use AI"  
        }
        patients_collection.insert_one(patient)
        return redirect(url_for("patients"))
    
    return render_template("add_patient.html")

if __name__ == "__main__":
    app.run(debug=True)