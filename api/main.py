# Importing dependencies
from flask import Flask, request
from flask_cors import CORS, cross_origin
from app import convert_pdf, conversation
import os


import openai


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

    if request.method == 'POST':

        # prompt = (
        #     "Summarize the following document in eight lines:\n\n"
        #     f"{contents}"
        # )
        

        prompt = (
            "Example\n:"
            "RENT AGREEMENT\n"
            "THIS RENT AGREEMENT (this 'Agreement') is made and entered into on the 15th day of June, 2022 by and between:\n"
            "Lessor: Captain Jack Sparrow, an individual with an address at The Black Pearl, Caribbean Sea (the 'Lessor');\n"
            "Lessee: Will Turner, an individual with an address at Port Royal, Jamaica (the 'Lessee').\n"
            "WHEREAS, the Lessor is the lawful owner and possessor of certain premises known as a cabin on board The Black Pearl, located on the Caribbean Sea (the 'Premises); and\n"
            "WHEREAS, the Lessee desires to rent the Premises for residential purposes only; NOW, THEREFORE, the Lessor and the Lessee hereby agree as follows:\n"
            "1. Premises. The Lessor hereby rents to the Lessee the Premises, together with all fixtures, appliances, and personal property located thereon, for residential purposes only, for a term of six (6) months, commencing on the 15th day of June, 2022 and ending on the 14th day of December, 2022 (the 'Term')n"
            "2. Rent. The Lessee shall pay to the Lessor the sum of $1000 per month as rent for the Premises (the 'Rent'), which shall be due and payable on the first day of each month during the Term. The Lessee shall also pay a security deposit of $3000 (the 'Security Deposit'), which shall be returned to the Lessee at the end of the Term if the Premises are returned in the same condition as when received.\n"
            "3. Utilities. The Lessee shall be responsible for paying for all utilities used during the Term, including but not limited to electricity, water, and internet.\n"
            "4. Maintenance. The Lessor shall be responsible for the maintenance and repair of the Premises. The Lessee shall notify the Lessor of any necessary repairs or maintenance and the Lessee shall keep the Premises in a clean and orderly condition.\n"
            "5. Quiet Enjoyment. The Lessee shall not use the Premises in such a manner as to disturb the peace and quiet of the surrounding area.\n"
            "6. Subletting. The Lessee shall not sublet the Premises without the prior written consent of the Lessor.\n"
            "7. Termination. Either party may terminate this Agreement upon giving written notice to the other party at least thirty (30) days prior to the desired termination date.\n"
            "8. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the Caribbean Sea.\n"
            "9. Entire Agreement. This Agreement constitutes the entire agreement between the parties and supersedes all prior agreements and understandings, whether oral or written, regarding the subject matter of this Agreement.\n"
            "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.\n"
            "Lessor (Captain Jack Sparrow) Lessee (Will Turner) ACKNOWLEDGED AND AGREED:\n"
            "Lessor (Captain Jack Sparrow) Lessee (Will Turner)\n\n"

            "The aforementioned is a legal document. Extract the important details like the name of the persons involved, the type of the document, etc in the following format:\n"
            "Lessor: Captain Jack Sparrow\n"
            "Lessee: Will Turner\n"
            "Rent amount: 1000$ per month\n"
            "Security Deposit: 3000$)\n"
            "Term: 6 months (15th June 2022 to 14th December 2022)\n"
            "Type of Document: Rent Agreement\n\n"
            "Document\n"
            f"{contents}"
            "\nThe aforementioned is a legal document. Extract the important details like the name of the persons involved, the type of the document, etc in the following format:\n"
            "Lessor: Captain Jack Sparrow\n"
            "Lessee: Will Turner\n"
            "Rent amount: 1000$ per month\n"
            "Security Deposit: 3000$)\n"
            "Term: 6 months (15th June 2022 to 14th December 2022)\n"
            "Type of Document: Rent Agreement\n"
        )


        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        summary = response["choices"][0]["text"]

        print(summary)
        summary = {"Summary": summary}

        return summary

    return "This is also working HUEHUE"


if __name__ == '__main__':
    app.run(debug=True)