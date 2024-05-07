import pyodbc

import SQL.queries
from SQL.queries import *
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv


load_dotenv()
conn_str = SQL.queries.Server1
port = os.environ.get("PORT", "5000")

app = Flask(__name__)

conn = pyodbc.connect(conn_str)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query1")
def query():
    """Performs simple query to DB"""
    page = "<h1>Simple Query</h1>\n<ol>\n"
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP (10) * FROM [SalesLT].[Address]")
        row = cursor.fetchone()
        while row:
            page += "<li>" + str(row[1]) + " " + str(row[3]) + "</li>\n"
            row = cursor.fetchone()
    page += "</ol>"
    return page


@app.route("/query2")
def query2():
    """Performs better query to DB"""
    page = "<h1>Better Query</h1>\n<table>\n"
    page += "<tr><td>Street</td><td>City</td></tr>"
    with conn.cursor() as cursor:
        cursor.execute("""SELECT TOP (10) [AddressID],
                            [AddressLine1],
                            [City],
                            [StateProvince],
                            [CountryRegion],
                            [PostalCode]
                        FROM [SalesLT].[Address]""")
        row = cursor.fetchone()
        while row:
            page += "<tr><td>" + row.AddressLine1 + "</td><td>" + row.City + "</td></tr>\n"
            row = cursor.fetchone()
    page += "</table>"
    return page


@app.route("/query3")
def query3():
    """Performs query to DB using template to display it"""
    with conn.cursor() as cursor:
        cursor.execute("""SELECT TOP (10) [AddressID],
                            [AddressLine1],
                            [City]
                        FROM [SalesLT].[Address]
                        ORDER BY [AddressID] DESC""")
        all_rows = cursor.fetchall()
        return render_template("query3result.html", rows=all_rows)


@app.route("/edit/<int:address_id>", methods=['POST', 'GET'])
def edit(address_id):
    """Performs query to DB but display using template"""
    if request.method == 'GET':
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT [AddressID],
                                [AddressLine1],
                                [City],
                                [StateProvince],
                                [CountryRegion],
                                [PostalCode]
                            FROM [SalesLT].[Address]
                            WHERE [AddressID]='{address_id}'""")
            row = cursor.fetchone()
            return render_template("edit.html", row=row)
    else:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE [SalesLT].[Address]
                SET [AddressLine1] = ?, [City] = ?
                WHERE [AddressID] = ?""",
                           (request.form['addressline1'], request.form['city'], address_id))
            conn.commit()
        return redirect(url_for('query3'))


@app.route("/delete/<int:address_id>")
def delete(address_id):
    """Delete one item from the table"""
    with conn.cursor() as cursor:
        cursor.execute("""DELETE FROM [SalesLT].[Address]
            WHERE [AddressID] = ?""",
                       address_id)
        conn.commit()
    return redirect(url_for('query3'))


@app.route("/insert", methods=['POST', 'GET'])
def insert():
    """Inserts a new item into table"""
    if request.method == 'GET':
        return render_template("insert.html")
    else:
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO [SalesLT].[Address] 
                (AddressLine1, City, StateProvince, CountryRegion, PostalCode, ModifiedDate) 
                VALUES (?, ?, 'province', 'region', '0000', '2006-07-01 00:00:00.000' )""",
                           (request.form['addressline1'], request.form['city']))
            conn.commit()
        return redirect(url_for('query3'))


if __name__ == "__main__":
    app.run(port)
