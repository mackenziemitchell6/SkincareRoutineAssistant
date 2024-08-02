import streamlit as st

from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from prompts import PERSONA, INITIAL_PROMPT

st.header("Skincare Routine Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if user_skin := st.chat_input("Please describe your skin type and current skin issues."):
    with st.chat_message("user"):
        st.markdown(user_skin)
    st.session_state.messages.append({"role": "user", "content": user_skin})

    # Create an OpenAI LLM instance
    llm = OpenAI(
        api_key=st.secrets["openai"]["API_KEY"],
        temperature=0
    )

    # Create a chat prompt template with initial messages
    prompt = ChatPromptTemplate(
        input_variables=["chat_history", "input"],
        messages=[
            SystemMessagePromptTemplate.from_template(PERSONA.format(st.session_state.memory)),
            HumanMessagePromptTemplate.from_template("{input}")
        ]
    )

    # Create an LLMChain with the LLM, prompt, and memory
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=st.session_state.memory
    )

    # Get a prediction from the chain
    chat_history = "\n".join([msg["content"] for msg in st.session_state.messages])
    response = chain.predict(chat_history=chat_history, input=user_skin)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Update memory context
    st.session_state.memory.save_context({"input": user_skin}, {"output": response})
