from flask import Flask, request
import flask
from flask_cors import CORS
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
app = Flask(__name__)
CORS(app)

user_dictionary = {

}
API_KEY = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/ask', methods=["GET", "POST"])
def ask_endpoint():
    if (request.method == "POST"):
        print("ask endpoint reached")
        recieved_data = request.get_json()
        recieved_question = recieved_data['data']
        id = recieved_data['id']
        print("id")
        print(id)
        if (not id in user_dictionary):
            user_dictionary[id] = ms
        return flask.Response(response=json.dumps(ask(recieved_question, id)), status=201)


@app.route('/summary', methods=["GET", "POST"])
def summary():
    if (request.method == "GET"):
        return flask.jsonify("blah")
    if request.method == "POST":
        print("users endpoint reached...")
        recieved_data = request.get_json()
        recieved_url = recieved_data['data']
        id = recieved_data['id']
        print("id")
        print(id)
        if (not id in user_dictionary):
            user_dictionary[id] = ms
        print(recieved_url)
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
        # print(recieved_url)
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

        return flask.Response(response=json.dumps(get_summary(text, id)), status=201)


ms = [
    {"role": "system", "content": "You are a helpful assistant whose main purpose is to answer questions about the text and to summarize text."},
]


def get_summary(chunk, id):
    import openai
    openai.api_key = API_KEY
    print(chunk)
    user_dictionary[id].append(
        {"role": "user", "content": "Please summarize the following text:"+chunk})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_dictionary[id]
    )
    print(user_dictionary)
    # print(response)
    return response["choices"][0]["message"]["content"]


def ask(question, id):
    import openai
    openai.api_key = API_KEY
    print(question)

    user_dictionary[id].append({"role": "user", "content": question})
    print(user_dictionary)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_dictionary[id]
    )
    user_dictionary[id].pop()
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    app.run("localhost", 6969)
