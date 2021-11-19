from flask import Flask, jsonify
from datetime import datetime
from sqlalchemy import or_
import threading
import time
import requests

# Initializing the app
app = Flask(__name__)
# Setting a relative path for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search_results.db'

from Models import db, SearchResult

db.create_all()  # Creating the Database and tables
items = []

# Enter your search query
search_query = "football"
# Put your GOOGLE API KEY Here!
API_KEY = ''
# Limits to 20 data objects at a time, but you are free to change it
data_limit = 20


# Gets all the objects from the Youtube API and stores it in a list
def get_items():
    items.clear()
    base_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={data_limit}&q={search_query}&type=video&key={API_KEY}"
    queries = requests.get(base_url)
    resp = queries.json()["items"]
    for i in resp:
        item = i["snippet"]
        title = item["title"];
        description = item["description"]
        date_and_time = item["publishedAt"]
        thumbnail = item["thumbnails"]["high"]["url"]
        items.append(
            {'title': title, 'description': description, 'date_and_time': date_and_time, 'thumbnail': thumbnail})


# Adds all the objects from the list to the sqlite database
def add_items_to_database():
    # Removing existing data if present
    try:
        db.session.query(SearchResult).delete()
        db.session.commit()
    except:
        db.session.rollback()

    # Inserting data into the database from items list
    for k in items:
        s = k['date_and_time']
        dt = datetime.fromisoformat(s[:-1])
        result = SearchResult(title=k['title'], description=k['description'], date_created=dt, thumbnail=k['thumbnail'])
        try:
            db.session.add(result)
            db.session.commit()
        except Exception as e:
            print(e)

# Function to continously update data in the database every 10 seconds. Starts execution before the first request
@app.before_first_request
def activate_job():
    def run_job():
        while True:
            get_items()
            add_items_to_database()
            time.sleep(10)
    thread = threading.Thread(target=run_job)
    thread.start()


# Displays all the results
@app.route('/')
def getAllResults():
    all_result = []
    for u in db.session.query(SearchResult).order_by(SearchResult.date_created.desc()).all():
        k = u.__dict__;
        k.pop('_sa_instance_state')
        all_result.append(k);
    return jsonify(all_result)


# Search functionality to filter results with respect to title and description
@app.route('/search/<string:query>')
def searchResult(query):
    filtered_result = SearchResult.query.filter(
        or_(SearchResult.title.like('%' + query + '%'),
            SearchResult.description.like('%' + query + '%'))
    )
    all_result = []
    for u in filtered_result:
        k = u.__dict__;
        k.pop('_sa_instance_state')
        all_result.append(k);
    return jsonify(all_result)


if __name__ == '__main__':
    app.run(debug=True)
