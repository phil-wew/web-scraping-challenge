from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# @app.route("/")
# def index():
#     articles = mongo.db.articles.find_one()
#     return render_template("index.html", articles=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_craigslist.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)