# Declare dependencies
from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Set up Flask
app = Flask(__name__)

# PyMongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: 
# index.html to Display Data
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

# Scrape Route to Import `scrape_mars.py` Script 
# Call `master_scrape` Function
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_new_news = scrape_mars.master_scrape()
    mars_data.update({}, mars_new_news, upsert=True)
    return redirect("/", code=302)

# Create raw json format data page to review work
@app.route("/scrape-raw")
def scrape_raw():
    mars_news = scrape_mars.master_scrape()
    return jsonify(mars_news)

if __name__ == "__main__":
    app.run(debug=True)
