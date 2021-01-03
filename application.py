import os
from flask import Flask, flash, jsonify, redirect, url_for, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import time


# Configure application
app = Flask(__name__)
app.secret_key = "jose"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html")
    if request.method == "POST":
        time=request.form.get("interval")
        breakTime=request.form.get("break")
        quantity=request.form.get("quantity")

        # Makes sure the boxes are filled out
        try:
            if int(time) < 1:
                return "Please enter a valid inverval"
            if int(breakTime) < 1:
                return "Please enter a valid break time"
            if int(quantity) < 1:
                return "Please enter a valid quantity"
        except:
            return "Please enter a positive integer in all of the boxes"

        session["time"] = time
        session["breakTime"] = breakTime
        session["quantity"] = quantity
        session["counter"] = 0
        print(session["quantity"])
        return redirect(url_for("timer"))

@app.route("/timer")
def timer():
    print(session["counter"])
    if int(session["counter"]) == int(session["quantity"]):
        return redirect(url_for("index"))
    session["counter"] += 1
    return render_template("timer.html", time=session["time"])

@app.route("/break")
def breakTime():
    return render_template("break_timer.html", time=session["breakTime"])


# @app.route("/buy", methods=["GET", "POST"])
# def buy():

#     if request.method == "GET":
#         return render_template("buy.html")
#     if request.method == "POST":
#         ticker = request.form.get("ticker")
#         quantity = request.form.get("quantity").replace(',', '')
#         if not ticker or not lookup(ticker):
#             return apology("Please enter a ticker symbol", 403)
#         try:
#             if int(quantity) < 1:
#                 return apology("Please enter a valid quantity", 403)
#         except:
#             return apology("Please enter a positive integer as the quantity", 403)

#         looked_ticker = lookup(ticker)
#         list_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
#         cash = list_cash[0]['cash']
#         if cash - looked_ticker['price'] * int(quantity) >= 0:
#             # Something with the square brackets below throws error.
#             db.execute("INSERT INTO purchases (id, ticker, price, date, shares, company_name) VALUES (?,?,?,?,?,?)", session['user_id'], ticker.upper(), looked_ticker['price'], datetime.datetime.now(), quantity, looked_ticker['name'])
#             db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - (looked_ticker['price'] * int(quantity)), session['user_id'])
#             flash(f"You have bought {quantity} share{'s' if int(quantity) > 1 else ''} of {ticker.upper()}")
#             return redirect("/")

#         else:
#             return apology("You don't have enough cash remaining")

