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

        text = soup.get_text()
        n = 3000
        chunks = [text[i:i+n] for i in range(0, len(text), n)]
        summarized_chunks = []
        combined_chunks = []

        while (len(combined_chunks) != 1):
            for i in range(len(chunks)):
                curr_chunk = chunks[i]
                summarized_chunks.append(get_summary(curr_chunk))

            combined_chunks = [''.join(x) for x in zip(
                summarized_chunks[0::2], summarized_chunks[1::2])]
            if (len(combined_chunks) != 1):
                chunks = combined_chunks
                summarized_chunks = []

        return flask.Response(response=json.dumps(get_summary(combined_chunks[0])), status=201)


def get_summary(chunk):
    import openai

    openai.api_key = "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"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please summarize (in less than 300 words) the following text:"+chunk,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )
    return response["choices"][0]["text"].strip()


if __name__ == "__main__":
    app.run("localhost", 6969)
