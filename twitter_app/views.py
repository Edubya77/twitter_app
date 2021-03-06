import datetime
from flask import render_template
from flask import request, redirect, url_for, Response

from flask import flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask.ext.login import login_required

from .database import session, Tweet, User
import json
import pandas as pd
from . import app

from nvd3 import pieChart
from collections import Counter
from collections import defaultdict

@app.route("/")   
def homepage():
    db_tweet = session.query(Tweet).all()
    db_tweet_location = session.query(Tweet.location)
    db_tweet_location_decoded = []
    for item in db_tweet_location:
        db_tweet_location_decoded.append(item)
    print (len(db_tweet))
    return render_template("base.html",db_tweet=db_tweet, db_tweet_location_decoded=db_tweet_location_decoded)

@app.route("/user_lang")
def user_language():
    return render_template("user_lang.html")

@app.route("/user_language_api")
def user_language_api():
    user_language = session.query(Tweet.user_lang)
    user_language_test = []
    for i in user_language:
        user_language_test.append(i[0])
    d = Counter(user_language_test)
    chart_values = [{"value": value, "label": key} for key, value in d.items()]
    data = [{"values": chart_values, "key": "Series 1"}]
    return Response(json.dumps(data), 201, mimetype="application/json")
    
@app.route("/location")
def user_location():
    x = []
    user_location = session.query(Tweet.location)
    for i in user_location:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("location.html", json_data=json_data)

@app.route("/coordinates")
def coordinates():
    x = []
    coordinates = session.query(Tweet.coordinates)
    for i in coordinates:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("coordinates.html", json_data=json_data)

@app.route("/created_at_api")
def created_at_api():
    x = []
    x2 = []
    date_clean = []
    created_at = session.query(Tweet.created_at)
    for i in created_at:
        x.append(i)
    for i in created_at:
        x2.append(i[0])
    for i in x2:
        date_clean.append(datetime.datetime.strptime(i, "%a  %b %d %H:%M:%S %z %Y").strftime("%b %d %Y"))
    #count them up
    date_counter = Counter(date_clean)
    #build the chart values for day
    chart_values_date = []
    counter = 0
    for key, value in date_counter.items():
        chart_values_date.append({"y": value, "x": key})
        counter += 1
    chart_values_date.sort(key=lambda i: datetime.datetime.strptime(i["x"], "%b %d %Y"))
    print(chart_values_date)
    data = [{"yAxis": "1","values": chart_values_date, "key": "Date"}]
    return Response(json.dumps(data), 201, mimetype="application/json")
    
@app.route("/created_at")
def created_at():
    return render_template("created_at.html")

@app.route("/favorite_count")
def favorite_count():
    x = []
    favorite_count = session.query(Tweet.favorite_count)
    for i in favorite_count:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("favorite_count.html", json_data=json_data)

@app.route("/tweet_language_api")
def tweet_language_api():
    tweet_language = session.query(Tweet.tweet_lang)
    tweet_language_test = []
    for i in tweet_language:
        tweet_language_test.append(i[0])
    d = Counter(tweet_language_test)
    chart_values = [{"value": value, "label": key} for key, value in d.items()]
    data = [{"values": chart_values, "key": "Series 1"}]
    return Response(json.dumps(data), 201, mimetype="application/json")

@app.route("/tweet_lang")
def tweet_language():
    return render_template("tweet_lang.html")

@app.route("/retweet_count")
def retweet_count():
    x = []
    retweet_count = session.query(Tweet.retweet_count)
    for i in retweet_count:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("retweet_count.html", json_data=json_data)

@app.route("/filter")
def filter():
    x = []
    tweet_language_test = []
    user_language_test = []
    favorite_count_test = []
    location_test = []
    coordinates_test = []
    created_at_test = []
    favorites_test = []
    retweet_count_test = []
    text = session.query(Tweet.text).order_by(Tweet.id).all()
    tweet_language = session.query(Tweet.tweet_lang).order_by(Tweet.id).all()
    user_language = session.query(Tweet.user_lang).order_by(Tweet.id).all()
    favorite_count = session.query(Tweet.favorite_count).order_by(Tweet.id).all()
    location = session.query(Tweet.location).order_by(Tweet.id).all()
    coordinates = session.query(Tweet.coordinates).order_by(Tweet.id).all()
    created_at = session.query(Tweet.created_at).order_by(Tweet.id).all()
    favorites = session.query(Tweet.favorite_count).order_by(Tweet.id).all()
    retweet_count = session.query(Tweet.retweet_count).order_by(Tweet.id).all()
    for i in text:
        x.append(i[0])
    for i in tweet_language:
        tweet_language_test.append(i[0])
    for i in user_language:
        user_language_test.append(i[0])
    for i in favorite_count:
        favorite_count_test.append(i[0])
    for i in location:
        location_test.append(i[0])
    for i in coordinates:
        coordinates_test.append(i[0])
    for i in created_at:
        created_at_test.append(i[0])
    for i in favorites:
        favorites_test.append(i[0])
    for i in retweet_count:
        retweet_count_test.append(i[0])
    return render_template("filter.html", values=zip(x, tweet_language_test, user_language_test, favorite_count_test, location_test, coordinates_test, created_at_test, favorites_test, retweet_count_test))

@app.route("/text")
def text():
    x = []
    text = session.query(Tweet.text)
    for i in text:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("text.html", json_data=json_data)

@app.route("/hashtag")
def hashtag():
    x = []
    hashtag = session.query(Tweet.hashtag)
    for i in hashtag:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("hashtag.html", json_data=json_data)

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('login.html'))

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))

