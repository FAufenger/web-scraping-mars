# Declare dependencies
from flask import Flask, 
from flask_pymongo import flask_pymongo
import scrape_mars

# Set up Flask
app = Flask(__name__)

# PyMongo Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_search"
mongo = PyMongo(app)

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: 
# index.html to Display Data
@app.route("/")
def index():
    mars = mongo.db.mars.find()
    return render_template("index.html", mars=mars)

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
    mars_stuff = scrape_mars.master_scrape()
    return jsonify(mars_stuff)

if __name__ == "__main__":
    app.run(debug=True)
