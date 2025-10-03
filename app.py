from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient 

app = Flask(__name__)

client = MongoClient('localhost',27017)


#This is a mongodb database 
db = client.flask_database 
#Mongodb database 
patients = db.patients 

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)

