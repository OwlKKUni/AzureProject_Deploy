import os
import pyodbc
import SQL.queries
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
conn_str = SQL.queries.Server1
port = os.environ.get("PORT", "5000")  # Get from env, if not - use 5000

app = Flask(__name__)

conn = pyodbc.connect(conn_str)


@app.route("/")
def goto_index():
    return render_template("index.html")


@app.route("/about")
def goto_about():
    return render_template("about.html")


@app.route("/all_dives")
def goto_all_dives():
    return render_template("all_dives.html")


@app.route("/data")
def goto_data():
    return render_template("data.html")


@app.route("/display_table")
def goto_display_table():
    return render_template("display_table.html")


@app.route("/dive")
def goto_dive():
    return render_template("dive.html")


if __name__ == "__main__":
    app.run(port)
