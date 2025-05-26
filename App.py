import streamlit as st
from agent import ai_agent
import random 
import time

st.set_page_config(page_title="Movie Companion Bot", page_icon="🎥")

st.title("🎬 Movie Companion Bot")


# Streamed Responses
def response_generator(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

#Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages=[]
    greeting="Hello there! How can I assist you today?"
    st.session_state.messages.append({'role':'assistant','content':greeting})


# Display chat message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# input box
prompt=st.chat_input('Say something')

if prompt:

    # display user message
    with st.chat_message("user"):
        st.markdown(f"User: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call the agent
    with st.spinner("Thinking..."):
        response = ai_agent(prompt)
        
    
    # typing animation for assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        animated_text = ""
        for chunk in response_generator(response):
            animated_text += chunk
            message_placeholder.markdown(animated_text + "▌")
        message_placeholder.markdown(animated_text)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})