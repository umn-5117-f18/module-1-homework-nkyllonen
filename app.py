import os

from flask import Flask, jsonify, redirect, render_template, request, url_for

import psycopg2
from datetime import datetime

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
            dt = datetime.now()
            cur.execute("INSERT INTO person (name, color, music, breed, terms, time_stamp) VALUES (%s,%s,%s,%s,%s,%s)", (name, color, music, breed, terms, dt))

        return render_template("thanks.html")
    else:
        with db.get_db_cursor() as cur:
            cur.execute("SELECT * FROM person;")
            names = [record["name"] for record in cur]

        return render_template("thanks.html")

@app.route('/api/results')
def results():
    with db.get_db_cursor() as cur:
        cur.execute("SELECT row_to_json(person) FROM person;")
        data = [record for record in cur]
    #     cur.execute("SELECT * FROM person;")
    #     names = [record["name"] for record in cur]
    #     colors = [record["color"] for record in cur]
    #     moods = [record["music"] for record in cur]
    #     breeds = [record["breed"] for record in cur]
    #     all_terms = [record["terms"] for record in cur]
    # data = {
    #     ""
    # }

    return jsonify(data)

if __name__ == '__main__':
    app.run()
