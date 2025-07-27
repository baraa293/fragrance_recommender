
from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions
from perfumes import perfumes
from collections import defaultdict
import random

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Dummy image/link fetcher for now (simulate pull_images_buy.py)
def get_image_and_link(perfume_name):
    # Simulate result for now
    base_url = "https://www.amazon.com/s?k="
    query = perfume_name.replace(" ", "+")
    return f"https://via.placeholder.com/300x400?text={query}", base_url + query

@app.route("/", methods=["GET"])
def start():
    session.clear()
    session["qid"] = 0
    session["tags"] = []
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    qid = session.get("qid", 0)

    if qid >= len(questions):
        return redirect(url_for("results"))

    question = questions[qid]

    if request.method == "POST":
        answer = request.form["answer"].strip().lower()
        tags = question["choices"].get(answer, [])
        session["tags"] += tags
        session["qid"] = qid + 1
        return redirect(url_for("question"))

    return render_template("questionnaire.html", question=question, qid=qid)

@app.route("/results", methods=["GET"])
def results():
    tag_scores = defaultdict(int)
    for tag in session.get("tags", []):
        tag_scores[tag] += 1

    def perfume_score(p):
        return sum(tag_scores[t] for t in p["score_tags"])

    ranked = sorted(perfumes, key=perfume_score, reverse=True)
    session["ranked_perfumes"] = ranked
    session["perfume_index"] = 0

    return redirect(url_for("show_recommendation"))

@app.route("/recommendation", methods=["GET", "POST"])
def show_recommendation():
    ranked = session.get("ranked_perfumes", [])
    index = session.get("perfume_index", 0)

    if index >= len(ranked):
        return "<h2>No more perfumes to show. You’ve reached the end.</h2>"

    selected = ranked[index]
    image, link = get_image_and_link(selected["name"])

    session["perfume_index"] = index + 1

    return render_template("results.html", perfume=selected, image=image, link=link)
