import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
import psycopg2

import db

app = Flask(__name__)

@app.before_first_request
def initialize():
    db.setup()

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

@app.route('/people')
def people():
    conn = get_db()

    cur = conn.cursor()
    cur.execute("SELECT * FROM person;")
    names = [record[1] for record in cur]
    cur.close()

    return render_template("people.html", names=names)

if __name__ == '__main__':
    app.run()
