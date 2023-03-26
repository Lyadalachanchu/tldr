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


@app.route('/ask', methods=["GET", "POST"])
def ask_endpoint():
    if (request.method == "POST"):
        print("ask endpoint reached")
        recieved_data = request.get_json()
        recieved_question = recieved_data['data']
        return flask.Response(response=json.dumps(ask(recieved_question)), status=201)


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

        text = soup.get_text()
        # n = 3000
        # chunks = [text[i:i+n] for i in range(0, len(text), n)]
        # summarized_chunks = []
        # combined_chunks = []

        # while (len(combined_chunks) != 1):
        #     for i in range(len(chunks)):
        #         curr_chunk = chunks[i]
        #         summarized_chunks.append(get_summary(curr_chunk))

        #     combined_chunks = [''.join(x) for x in zip(
        #         summarized_chunks[0::2], summarized_chunks[1::2])]
        #     if (len(combined_chunks) != 1):
        #         chunks = combined_chunks
        #         summarized_chunks = []

        return flask.Response(response=json.dumps(get_summary(text)), status=201)


ms = [
    {"role": "system", "content": "You are a helpful assistant whose main purpose is to answer questions about the text and to summarize text."},
]


def get_summary(chunk):
    import openai
    openai.api_key = "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"
    import openai
    ms.append(
        {"role": "user", "content": "Please summarize the following text:"+chunk})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=ms
    )
    return response["choices"][0]["message"]["content"]


def ask(question):
    import openai
    openai.api_key = "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"
    print(question)
    ms.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=ms
    )
    ms.pop()
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    app.run("localhost", 6969)
