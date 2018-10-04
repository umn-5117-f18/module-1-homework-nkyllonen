import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
import psycopg2

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
        mood = request.form['mood']
        app.logger.info(f"got a mood: {mood}")
        with db.get_db_cursor(commit=True) as cur:
            cur.execute("insert into person (name, color, mood) values (%s,%s,%s)", (name, color, mood))
        return render_template("thanks.html")
    else:
        with db.get_db_cursor() as cur:
            cur.execute("SELECT * FROM person;")
            names = [record["name"] for record in cur]

        return render_template("thanks.html")

# @app.route('/api/results')
# def results():
#     data = {
#         "message": "hello, world",
#         "isAGoodExample": False,
#         "aList": [1, 2, 3],
#         "nested": {
#             "key": "value"
#         }
#     }
#     return jsonify(data)

if __name__ == '__main__':
    app.run()
