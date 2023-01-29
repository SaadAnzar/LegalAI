# Importing dependencies
from flask import Flask, request
from flask_cors import CORS, cross_origin
from app import convert_pdf, conversation
import os
import openai

import os

openai.api_key = os.environ.get("OPENAI_API_KEY")


# Create Flask instance
app = Flask(__name__)

# config to handle CORS requests
CORS(app)


@cross_origin('*')
@app.route('/', methods=["POST"])
def home():

    # pdf & text upload path
    path_pdf = os.environ.get("path_pdf")
    path_txt = os.environ.get("path_txt")

    # fetch filename from Node backend
    query = request.json["fileName"]
    # print(query)

    # convert pdf to text
    stored_document = convert_pdf(path_pdf + query)

    # save the converted pdf as txt to retrieve later
    with(open(f"{path_txt}file.txt", 'w')) as file:
        file.write(stored_document[0])      # select the first element i.e the text content

    return "PDF RECIEVED!!!"



@cross_origin("*", supports_credentials=True)
@app.route('/chat', methods=["POST", "GET"])
def chat():
    
    # text upload path
    path_txt = os.environ.get("path_txt")


    # fetch user's question
    question = request.data
    # Change the byteString to String
    modified_question = question.decode().rstrip('"}').lstrip()[12:]

    # Load the uploaded txt file (Legal Doc)
    with(open(f"{path_txt}file.txt", "r")) as file:
        contents = file.read()

    # generate answers 
    answer = conversation(contents, modified_question)
    # print(answer)

    res = {"Answer": answer}
    # print(res)

    return res


@cross_origin("*", supports_credentials=True)
@app.route('/summarize', methods=["POST", "GET"])
def summarize():

    path_txt = os.environ.get("path_txt")

    with(open(f"{path_txt}file.txt", "r")) as file:
        contents = file.read()

    prompt = (
        "Summarize the following document in eight lines:\n\n"
        f"{contents}"
    )
    if request.method == "POST":

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        summary = response["choices"][0]["text"].lstrip('.')

        return {"Summary": summary}
    return "<h1>This is working HUEHUE</h1>"


if __name__ == '__main__':
    app.run(debug=True)