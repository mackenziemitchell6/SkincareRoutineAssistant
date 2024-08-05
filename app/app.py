import streamlit as st
import sqlite3
import pandas as pd
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

from prompts import PERSONA, INITIAL_PROMPT

# Initialize Streamlit app
st.header("Skincare Routine Assistant")

# Initialize session state for messages and memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Load data from SQLite database and initialize FAISS vector store
def load_data_from_sqlite(db_name, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def initialize_faiss_with_data(df, embeddings):
    # Convert DataFrame to list of documents
    docs = df.to_dict(orient='records')

    # Create FAISS vector store and add documents
    vector_store = FAISS(embeddings)
    vector_store.add_documents(docs)

    return vector_store


# Specify the database name and table name
db_name = 'skincare.db'
table_name = 'reviews_0-250'  # Replace with your actual table name

# Load data from SQLite
df = load_data_from_sqlite(db_name, table_name)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=st.secrets["openai"]["API_KEY"])

# Initialize vector store
vector_store = initialize_faiss_with_data(df, embeddings)

# Get user input
if user_skin := st.chat_input("Please describe your skin type and current skin issues."):
    with st.chat_message("user"):
        st.markdown(user_skin)
    st.session_state.messages.append({"role": "user", "content": user_skin})

    # Create an OpenAI LLM instance
    llm = OpenAI(api_key=st.secrets["openai"]["API_KEY"], temperature=0)

    # Set up retrieval with FAISS
    retriever = vector_store.as_retriever()

    # Create a RetrievalQA chain
    rag_chain = RetrievalQA(llm=llm, retriever=retriever)

    # Use the chain to get a response
    response = rag_chain({"query": user_skin})

    with st.chat_message("assistant"):
        st.markdown(response["output"])

    st.session_state.messages.append({"role": "assistant", "content": response["output"]})

    # Update memory context
    st.session_state.memory.save_context({"input": user_skin}, {"output": response["output"]})
