import os

from flask import Flask, jsonify, redirect, render_template, request, url_for

import psycopg2
from datetime import datetime
import json

import db

app = Flask(__name__)

@app.before_first_request
def initialize():
    db.setup()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/survey')
def survey():
    return render_template("survey.html")

@app.route('/decline')
def decline():
    return render_template("decline.html")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route('/people', methods=['GET', 'POST'])
def people():
    app.logger.info(f"called people function")
    if request.method == 'POST':
        #gather each item from the form into local variables
        name = request.form['name']
        app.logger.info(f"got a name: {name}")

        color = request.form['color']
        app.logger.info(f"got a color: {color}")

        music = request.form['mood']
        app.logger.info(f"got a music mood: {music}")

        breed = request.form['breed-radios']
        app.logger.info(f"got a breed: {breed}")

        terms = request.form['term-textarea']
        app.logger.info(f"got a terms: {terms}")

        with db.get_db_cursor(commit=True) as cur:
            dt = datetime.now() #get the current timestamp
            cur.execute("INSERT INTO person (name, color, music, breed, terms, time_stamp) VALUES (%s,%s,%s,%s,%s,%s)", (name, color, music, breed, terms, dt))

        return thanks()

@app.route('/api/results')
def results():
    #check for ?reverse=___ in query parameters
    query = request.args.get('reverse')

    with db.get_db_cursor() as cur:
        #gather all rows into an array of arrays
        #(each item is an array holding all the col values or that row)
        cur.execute("SELECT row_to_json(person) FROM person;")
        data = [record for record in cur] #sorted by entering timestamp

    if query:
        #reverse data to be sorted in descending timestamp order
        app.logger.info(f"query: {query}")
        data.reverse();

    return jsonify(data)

@app.route('/admin/summary')
def summary():
    # json_arr = results()

    with db.get_db_cursor() as cur:
        #gather all rows into an array of arrays
        #(each item is an array holding all the col values or that row)
        cur.execute("SELECT row_to_json(person) FROM person;")
        data = [record for record in cur] #sorted by entering timestamp

    mood_labels = ["Dance", "Happy", "Slow", "Sad", "Warm"]
    breed_labels = ["Australian Shepherd", "German Shepherd", "Golden Retriever"]

    #parse data from requests into dictionaries
    mood_data, breed_data = getData(data)

    return render_template("summary.html",
        mood_data=mood_data, mood_labels=mood_labels,
        breed_data=breed_data, breed_labels=breed_labels)

def getData(arr):
    #store votes/values in dictionary!
    mood_data = {
        "dance" : 0,
        "happy" : 0,
        "slow" : 0,
        "sad" : 0,
        "warm" : 0
    }

    breed_data = {
        "Australian Shepherd" : 0,
        "German Shepherd" : 0,
        "Golden Retriever" : 0
    }

    #tally up votes for mood_data and breed_data
    for i in range (len(arr)):
        mood_data[arr[i][0]['music']] += 1
        breed_data[arr[i][0]['breed']] += 1

    return mood_data, breed_data

if __name__ == '__main__':
    app.run()
