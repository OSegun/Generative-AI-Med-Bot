---
title: AI Medical Bot
---
# Introduction

This document will walk you through the implementation of the Generative AI Med Bot, a chatbot designed to assist users with medical inquiries using generative AI technology. The bot leverages several technologies to understand user queries and provide accurate, relevant responses based on a document of medical knowledge.

We will cover:

1. How environment variables are managed.
2. The setup of the Pinecone Vector database and its role.
3. The creation of the retrieval and language model chain.
4. The integration of the Flask web framework for handling requests.

# Managing environment variables

<SwmSnippet path="/app.py" line="15">

---

Environment variables are crucial for storing sensitive information like API keys. In this implementation, we load environment variables using `load_dotenv()` to access the OpenAI and Pinecone API keys.

```
app = Flask(__name__)


load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
```

---

</SwmSnippet>

# Setting up the Pinecone Vector database

<SwmSnippet path="/app.py" line="24">

---

The Pinecone Vector database is used to store and retrieve embeddings. We download embeddings using a helper function and set up the database with an existing index named "med-bot". This allows the bot to perform similarity searches on medical data.

```
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = huggingface_download()

index_name = "med-bot"

med_db = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
```

---

</SwmSnippet>

# Creating the retrieval and language model chain

<SwmSnippet path="/app.py" line="37">

---

The retrieval chain is created using the Pinecone database as a retriever. We configure it to perform similarity searches with a specified number of results. The OpenAI language model is initialized with specific parameters to generate responses. These components are combined into a processing chain that handles user input and generates responses.

```
retriver = med_db.as_retriever(search_type="similarity", search_kwargs={"k":3})
llm = OpenAI(temperature=0.4, max_tokens=500)


prompt = ChatPromptTemplate.from_template(system_prompt)
    #[
     #   ("system", system_prompt),
      #  ("human", "{input}"),
    #]
#)
```

---

</SwmSnippet>

# Integrating Flask for request handling

<SwmSnippet path="/app.py" line="61">

---

Flask is used to create a web application as a chatbot interface. We define routes to render the chat interface and handle user messages. The `/get` route processes user input, invokes the processing chain, and returns the generated response.

```
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
```

---

</SwmSnippet>

# Running the application

<SwmSnippet path="/app.py" line="77">

---

Finally, the Flask application is set to run on a specified host and port, with debugging enabled for Continuous Development and Continuous Integration (CICD) purposes.

```
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
```

---

</SwmSnippet>

This setup ensures that the Generative AI Med Bot can effectively process medical inquiries and provide valuable information to users.

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBR2VuZXJhdGl2ZS1BSS1NZWQtQm90JTNBJTNBT1NlZ3Vu" repo-name="Generative-AI-Med-Bot"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
