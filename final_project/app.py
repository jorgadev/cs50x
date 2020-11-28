import os
import requests
import urllib.parse
import json
import ipapi
import pycountry
import sys

from cs50 import SQL
from flask import Flask, render_template, redirect, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jsglue import JSGlue

app = Flask(__name__)
jsglue = JSGlue(app)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///european.db")

#--------------------------------------------------------------------------------#

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#--------------------------------------------------------------------------------#

@app.route("/", methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        user_input = request.form.get("country")
        mapping = {country.name: country.alpha_3 for country in pycountry.countries}
        newCountry = mapping.get(user_input)
        query = "SELECT country FROM countries WHERE user_id = :user_id"
        rows = db.execute(query, user_id = session["user_id"])
        countries = [i["country"] for i in rows]
        if newCountry not in countries:
            query = "INSERT INTO countries(user_id, country) VALUES (:user_id, :country)"
            db.execute(query, user_id = session["user_id"], country = newCountry)
            return redirect("/")
        else:
            return redirect("/")
    else:
        countriesArr = get_countries()
        return render_template("index.html", data = countriesArr)

#--------------------------------------------------------------------------------#

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # If user reached route via POST (as submitting a form via POST)    
    if request.method == "POST":
    
        # Ensure user submitted info
        if not request.form.get("username"):
            message = "Must provide an username."
            return render_template("login.html", message = message)
        elif not request.form.get("password"):
            message = "Must provide a password."
            return render_template("login.html", message = message)

        # Query database for username
        query = "SELECT * FROM users WHERE username = :username"
        rows = db.execute(query, username = request.form.get("username"))
        
        # Ensure name exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            message = "Invalid username or password."
            return render_template("login.html", message = message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#--------------------------------------------------------------------------------#

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()
    
    # If user reached route via POST (as submitting a form via POST)
    if request.method == "POST":

        # Ensure user submitted info
        if not request.form.get("username"):
            message = "Must provide an username."
            return render_template("register.html", message = message)
        elif not request.form.get("password") or len(request.form.get("password")) < 6:
            message = "Password must contain at least 6 characters."
            return render_template("register.html", message = message)
        elif not request.form.get("confirmation"):
            message = "Password must contain at least 6 characters."
            return render_template("register.html", message = message)

        # Ensure passwords match
        if not request.form.get("password") == request.form.get("confirmation"):
            message = "Passwords doesn't match."
            return render_template("register.html", message = message)

        # Ensure username is not used
        row = db.execute("SELECT username FROM users")
        if any(r['username'] == request.form.get("username") for r in row):
            message = "Username already taken."
            return render_template("register.html", message = message)

        # Insert data in 'users' table in database
        else: 
            query = "INSERT INTO users(username, hash) VALUES (:username, :hash)"
            db.execute(query, username = request.form.get("username"), hash = generate_password_hash(request.form.get("password")))
            query = "SELECT id FROM users WHERE username = :username"
            rows = db.execute(query, username = request.form.get("username"))
            session["user_id"] = rows[0]["id"]

            return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)    
    else:
        return render_template("register.html")

#--------------------------------------------------------------------------------#

@app.route("/logout")
def logout():

    # Log user out
    session.clear()
    return redirect("/")

#--------------------------------------------------------------------------------#

@app.route("/function_route", methods=["GET", "POST"])
def my_function():
    if request.method == "POST":
        countryCode = request.get_json("data")["countryCode"]
        query = "DELETE FROM countries WHERE country = :countryCode AND user_id = :user_id"
        db.execute(query, countryCode = countryCode, user_id = session["user_id"])
        return "Successfully removed!"
    else:
        return render_template('index.html')

#--------------------------------------------------------------------------------#

def get_countries():
    arr = []
    rows = db.execute("SELECT country FROM countries WHERE user_id = :user_id", user_id = session["user_id"])
    for r in rows:
        arr.append(r["country"])
    return arr

if __name__ == '__main__':
    app.run(debug = True)