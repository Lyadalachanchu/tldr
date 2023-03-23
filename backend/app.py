from flask import Flask, request
import flask
from flask_cors import CORS
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/users', methods=["GET", "POST"])
def users():
    if (request.method == "GET"):
        return flask.jsonify("blah")
    if request.method == "POST":
        print("users endpoint reached...")
        recieved_data = request.get_json()
        recieved_url = recieved_data['data']
        # with open("users.json", "r") as f:
        #     data = json.load(f)
        #     data.append({
        #         "username": "user4",
        #         "pets": ["hamster"]
        #     })
        url = recieved_url
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        import openai

        openai.api_key = "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"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Please summarize the following text:"+soup.get_text(),
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1
        )
        return flask.Response(response=json.dumps(response["choices"][0]["text"].strip()), status=201)


if __name__ == "__main__":
    app.run("localhost", 6969)
