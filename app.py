from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = mission_to_mars.scrape()
    mars.update({}, data, upsert=True)
    return redirect("http://localhost:5010/", code=302)
if __name__ == "__main__":
    app.run(debug=True, port=5010)