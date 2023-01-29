# Importing dependencies
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import NLTKTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate

from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from langchain.llms import OpenAI

import pdfplumber as pp


# Convert the pdf file to text
def convert_pdf(file_name):
    with pp.open(file_name) as book:
        temp = ""
        page_count = 0
        for page_no, page in enumerate(book.pages, start=1):
            data = page.extract_text()
            temp += data
            page_count += 1
    return temp, page_count

pdf_file = convert_pdf('POA.pdf')

# print(pdf_file)


# Propmt Template
template = """You are an AI Asisstant who is an expert in legal/law field. 
Include any important definitions, context, and any relevant legal precedent or laws that may be applicable.
Also, usually try to avoid using jargon or technical terms that may be confusing to someone without a legal background.
Given the following legal document, create a final answer. 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
If the user asks gibberish or something, just say that you dont understand.
QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER
"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

# Ask questions regarding the uploaded document
def conversation(pdf_file, question):
    print(pdf_file)
    # Used to split the whole context into smaller chunks, here it's not splitting as the spearator is None
    text_splitter = NLTKTextSplitter(chunk_size=5000)
    texts = text_splitter.split_text(pdf_file)
    print((texts))
    # Initialize embeddings 
    embeddings = OpenAIEmbeddings()

    # Create a Faiss search index for the source, creates embedding (feature vector) for the source to make it easily searchable
    docsearch = FAISS.from_texts(texts, embeddings, metadatas=[{"source": i} for i in range(len(texts))])

    # Find similarity between the vectors (question and the source)
    docs = docsearch.similarity_search(question)

    # Create a `LangChain` chain that’s set up with the proper question-and-answering prompts. 
    # Uses the OpenAI API to power the chain and the chain_type as "refine"
    chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)
    
    # The chain is fed in with the source information and the question to be asked.
    return chain({"input_documents": docs, "question": question}, return_only_outputs=True)['output_text']




# def conversation2(pdf_file, question):
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_text(pdf_file)

#     docsearch = FAISS.from_texts(texts, embeddings, metadatas=[{"source": i} for i in range(len(texts))])

#     embeddings = OpenAIEmbeddings()

    

# print(conversation(pdf_file, "Who is a resident of Queens?"))