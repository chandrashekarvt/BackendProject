from flask import Flask, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_
import threading
import time
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search_results.db'

# initialize the database
db = SQLAlchemy(app)


# create db model
class SearchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    thumbnail = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.id


db.create_all()
items = []

search_query = "football"
API_KEY = ''
data_limit = 20


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


def add_items_to_database():
    try:
        db.session.query(SearchResult).delete()
        db.session.commit()
    except:
        db.session.rollback()
    for k in items:
        s = k['date_and_time']
        dt = datetime.fromisoformat(s[:-1])
        result = SearchResult(title=k['title'], description=k['description'], date_created=dt,thumbnail=k['thumbnail'])
        try:
            db.session.add(result)
            db.session.commit()
            print(f"Add item titled {k['title']} to database")
        except Exception as e:
            print(e)
        print(len(items))


@app.before_first_request
def activate_job():
    def run_job():
        print("Hello")
        while True:
            get_items()
            add_items_to_database()
            time.sleep(10)
    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/')
def getAllResults():
    all_result = []
    for u in db.session.query(SearchResult).order_by(SearchResult.date_created.desc()).all():
        k = u.__dict__;
        k.pop('_sa_instance_state')
        all_result.append(k);
    return jsonify(all_result)


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