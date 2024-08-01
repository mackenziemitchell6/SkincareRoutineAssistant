import streamlit as st

from openai import OpenAI

from prompts import PERSONA, INITIAL_PROMPT

client = OpenAI(api_key=st.secrets["openai"]["API_KEY"])

st.header("Skincare Routine Assistant")

user_skin = st.text_input("Please describe your skin type and current skin issues.")

if user_skin:
   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[
           {"role": "system", "content": PERSONA},
           {"role": "user", "content": INITIAL_PROMPT.format(user_skin)}
       ]
   )

   st.write(response.choices[0].message.content)
