# from flask import Flask, request, render_template
# from pull_images_buy import search_perfume

# app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def home():
#     image = link = None
#     if request.method == "POST":
#         fragrance = request.form["fragrance"]
#         image, link = search_perfume(fragrance)

#     return render_template("index.html", image=image, link=link)


from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    return redirect(url_for("questionnaire", qid=1))

@app.route("/questionnaire/<int:qid>", methods=["GET", "POST"])
@app.route("/questionnaire/<int:qid>", methods=["GET", "POST"])
def questionnaire(qid):
    if "responses" not in session:
        session["responses"] = {}

    if request.method == "POST":
        answer = request.form.get("answer")
        session["responses"][str(qid)] = answer

        return redirect(url_for("questionnaire", qid=qid + 1))

    if qid > len(questions):
        return redirect(url_for("result"))

    question = questions[qid - 1]
    return render_template("questionnaire.html", question=question, qid=qid)

@app.route("/result")
def result():
    responses = session.get("responses", {})
    return render_template("result.html", responses=responses)