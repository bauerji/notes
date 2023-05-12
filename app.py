from random import choice, shuffle
import requests

from flask import Flask, render_template, request

moll = {
    "a": "o.V.",
    "e": "1#",
    "h": "2#",
    "fis": "3#",
    "cis": "4#",
    "gis": "5#",
    "es": "6b",
    "dis": "6#",
    "b": "5b",
    "f": "4b",
    "c": "3b",
    "g": "2b",
    "d": "1b",
}

dur = {
    "C": "o.V.",
    "G": "1#",
    "D": "2#",
    "A": "3#",
    "E": "4#",
    "H": "5#",
    "Fis": "6#",
    "Ges": "6b",
    "Des": "5b",
    "As": "4b",
    "Es": "3b",
    "B": "2b",
    "F": "1b",
}


def get_giff_image_url(tag: str) -> str:
    url = f"https://api.giphy.com/v1/gifs/random?api_key=0UTRbFtkMxAplrohufYco5IY74U8hOes&tag={tag}&rating=pg-13"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]["images"]["fixed_width"]["url"]
    except:
        return ""


def x():
    a = {"Dur": dur, "Moll": moll}
    b = choice(list(a.keys()))

    c = a[b]

    key = choice(list(c.keys()))

    correct = c[key]
    wrong_options = list({value for value in c.values() if value != correct})[:3]
    all_options = [correct] + wrong_options
    shuffle(all_options)
    return key, all_options, correct, b


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    key, all_options, correct, b = x()
    value_1, value_2, value_3, value_4 = all_options
    return render_template(
        "index.html",
        value_1=value_1,
        value_2=value_2,
        value_3=value_3,
        value_4=value_4,
        question=f"{key} {b}",
        correct=correct,
    )


@app.route("/guess", methods=["POST"])
def guess():
    x = request.form.get("action")
    guess, correct = x.split(":")
    if guess == correct:
        return render_template("result.html", message="correct", img_src=get_giff_image_url("success"))
    return render_template(
        "result.html", message=f"Wrong - the correct response is {correct}", img_src=get_giff_image_url("fail")
    )
