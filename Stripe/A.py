from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from app import *

app = Flask(__name__)

# Configure Flask-PyMongo
app.config['MONGO_URI'] = 'mongodb://localhost:5000/sobhansanati?directConnection=true'
mongo = PyMongo(app)

@app.route('/')
def index():
    # Access the MongoDB collection
    collection = mongo.db.my_collection

    # Insert sample data
    data = {handel_stripe_event}
    collection.insert_one(data)

    return 'Data inserted successfully!'

@app.route('/check_data')
def check_data():
    # Access the MongoDB collection
    collection = mongo.db.my_collection

    # Retrieve data from MongoDB
    data = collection.find_one({'name': 'John'})

    if data:
        return f"Found data: {data}"
    else:
        return "Data not found!"

if __name__ == '__main__':
    app.run(debug=True)
