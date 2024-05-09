# Setting up

import sys
sys.path.append('D:/Deep Learning/Diver')

from src.components.generation import generator
from config.utils import *

import streamlit as st

# Initial welcoming messages

st.set_page_config(
    page_title='Diver - diving data with AI',
    page_icon='src/assets/favicon.svg',
)

st.title("Olá,")

st.markdown("Eu sou o Diver, um chatbot alimentado por inteligência artificial. Vou te ajudar com suas perguntas sobre o blog da [Naomi Lago](https://naomilago.com/)! Uma coisa legal sobre mim é que sou poliglota, então podemos conversar no idioma em que você se sentir mais confortável :)")
st.markdown("Ah, e caso goste de mim, que tal se conectar com a própria Naomi Lago?")

linkedin, github = st.columns([0.25, 0.55])

with linkedin:
  st.link_button("Se conectar no Linkedin", "https://www.linkedin.com/in/naomilago/")
with github:
  st.link_button("Saber mais sobre mim no Github", "https://github.com/naomilago/diver")

st.divider()

# Chatbot

if 'messages' not in st.session_state:
  st.session_state.messages = []
  
for message in st.session_state.messages:
  with st.chat_message(message['role']):
    st.markdown(message['content'])
    
if input_ := st.chat_input('Ready to dive today?'):
  
  if input_.strip() == '':
    st.error('Please enter a valid message!')
  else:  
    with st.chat_message('user'):
      st.markdown(input_)
    
    st.session_state.messages.append({
      'role': 'user',
      'content': input_
    })  
    
    response = generator(
      question=input_,
      history='\n'.join(f"{item['role']}: {item['content']}" for item in st.session_state.messages),
      langchain_api_key=settings.LANGSMITH_API_KEY, 
      google_api_key=settings.GEMINI_API_KEY
    )
    
    with st.chat_message('assistant'):
      st.markdown(response)
    
    st.session_state.messages.append({
      'role': 'assistant',
      'content': response
    }) 
    