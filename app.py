from flask import Flask, render_template, jsonify, request
from resource.helper import huggingface_download
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from resource.prompt import *
import os


app = Flask(__name__)


load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = huggingface_download()

index_name = "med-bot"

med_db = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


retriver = med_db.as_retriever(search_type="similarity", search_kwargs={"k":3})
llm = OpenAI(temperature=0.4, max_tokens=500)


prompt = ChatPromptTemplate.from_template(system_prompt)
    #[
     #   ("system", system_prompt),
      #  ("human", "{input}"),
    #]
#)


prompt = ChatPromptTemplate.from_template(system_prompt)

chain = (
    {"context": retriver | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
#q_a_chain = create_stuff_documents_chain(llm, prompt)
#rag_chain = create_retrieval_chain(retriver, q_a_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = chain.invoke(msg)
    print(f"Response: {response}")#['answer']}")
    return str(response)#.replace('?\n\nSystem: ', ''))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)