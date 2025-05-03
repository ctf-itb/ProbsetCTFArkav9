import requests
import os
import re
from flask import Flask, render_template, render_template_string, request
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
evil = lambda data: any(i in data for i in ["[", "]", ".", "<", ">", "_", "!", "'", "$"])

def clean_input(s):
    # Remove innermost {{ ... }} and {% ... %} pairs, recursively
    patterns = [r"\{\{([^{}]*)\}\}", r"\{\%([^\{\}%]*)\%\}"]
    while True:
        new_s = s
        for pattern in patterns:
            new_s = re.sub(pattern, r"\1", new_s)
        if new_s == s: break
        s = new_s
    return s

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def greeting():
    name1 = request.form["name1"]
    name2 = request.form["name2"]
    if evil(name1) or evil(name2):
        return render_template("hacker.html")
    rnd = random.random()
    mtch = False
    if rnd >= 0.69420:
        mtch = True
        res = f"Selamatt !<br><b>{clean_input(name1)}</b> dan <b>{clean_input(name2)}</b> jodoh dengan tingkat kecocokan <b>{rnd*100:.2f}%</b>!<br><br>Kapan Nikah?!"
    else:
        res = f"Wah sayang sekali, kalian <b>belum berjodoh</b> :("
    result = render_template_string(res)
    # temporarily disabling logger due to some bug
    # response = requests.post("http://internal_app:5000/log", data={"name1": name1, "name2": name2, "mtch": mtch})
    return render_template("love.html", result=result)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)
