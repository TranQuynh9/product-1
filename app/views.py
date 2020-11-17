from app import app
from flask import render_template, request, jsonify, send_from_directory, abort, redirect
import json
import os
import markdown
from modules import lotto_check


with open("data/data.json") as f:
    data = json.load(f)
    time = data["update_time"]
    posts = data["posts"]
    jobs = data["jobs"]


@app.route("/", methods = ["GET", "POST"])
def index():

    jobs_page = {"len" : len(jobs)}

    if jobs_page["len"] % 20 == 0:
        jobs_page["amount"] = jobs_page["len"] // 20
    else:
        jobs_page["amount"] = jobs_page["len"] // 20 + 1

    if request.method == 'POST':
        numbers = request.form['check_number']
        checked_result = lotto_check.solve(numbers.split(" "))
        return render_template("index.html", time=time, jobs=jobs, jobs_page=jobs_page, posts=posts, checked_result=checked_result)
    else:
        return render_template("index.html", time=time, jobs=jobs, jobs_page=jobs_page, posts=posts)


@app.route("/about")
def about():
    with open("aboutme.md") as f:
        md = "".join(f.readlines())
        html = markdown.markdown(md)
    return render_template("about.html", html=html)

@app.route("/cv")
def get_cv():
    path = "/".join([os.getcwd(), "data"])
    try:
        return send_from_directory(
            path, "CV_TranNgocQuynh.pdf", as_attachment = True
        )
    except FileNotFoundError:
        abort(404)

@app.route("/map")
def map():
    with open("data/cafe.geojson") as f:
        points = json.load(f)
    return render_template("map.html", points=points)

@app.route("/numbers-book")
def numbers_book():
    with open("data/numbers_book.json") as f:
        book = json.load(f)

    words = request.args.get("words")
    if words != None:
        results = [(key, book[key]) for key in book.keys() if words in key.lower()]   
        return render_template("numbers-book.html", results=results)
    else:
        return render_template("numbers-book.html")
