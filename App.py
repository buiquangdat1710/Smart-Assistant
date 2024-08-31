import streamlit as st
from openai_client import OpenAIClient
import os
from dotenv import load_dotenv
import time
import pandas as pd
import io
import streamlit.components.v1 as com
com.iframe("https://lottie.host/embed/93f9466d-a267-4078-ad98-a29abbdc8844/sFVT8gWDzp.json")

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://images.pexels.com/photos/845254/pexels-photo-845254.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
  background-size: cover;
}

h2 {
    font-family: 'Arial', sans-serif;
    color: #FFFFFF;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    text-shadow: 2px 2px 5px #000000;
    margin-bottom: 20px;
}


.chat-bubble {
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    max-width: 70%;
    display: inline-block;
    white-space: normal;
    overflow-wrap: break-word;
    background-color: rgba(0, 0, 0, 0.4);  /* Set transparency for chat bubbles */
}

.user-bubble {
    color: #c6c6c6;
    text-align: left;
    animation: fadeInLeft 0.5s;
}

.assistant-bubble {
    color: white;
    text-align: right;
    animation: fadeInRight 0.5s;
}

input[type="text"], textarea {
    background-color: rgba(0,0,0,1);
}

div.stButton > button {
    background-color: green;
    color: white;
}

@keyframes fadeInLeft {
    from {
        transform: translateX(-20px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes fadeInRight {
    from {
        transform: translateX(20px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
</style>

'''


st.markdown(page_bg_img, unsafe_allow_html=True)

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create instance of OpenAIClient
openai_client = OpenAIClient(api_key)

st.markdown("<h2>Smart Assistant</h2>", unsafe_allow_html=True)

# Create a list to store the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate a response using OpenAIClient
def generate_response(prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for msg in st.session_state.messages:
        messages.append({"role": "user", "content": msg['user']})
        messages.append({"role": "assistant", "content": msg['assistant']})
    
    messages.append({"role": "user", "content": prompt})

    # Use OpenAIClient to send message and receive response
    response = openai_client.chat(messages)
    
    return response

# Function to handle user input and generate a response
def handle_input():
    user_input = st.session_state.input_text
    if user_input:
        # Get the assistant's response
        response = generate_response(user_input)

        # Store the conversation
        st.session_state.messages.append({"user": user_input, "assistant": response})

        # Clear the input field after submission
        st.session_state.input_text = ""
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# Display the chat history
for chat in st.session_state.messages[:-1]:
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-start; color: white;">
        <div style="background-color:rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>You:</strong> {chat['user']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; color: white;">
        <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>Assistant:</strong> {chat['assistant']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Placeholder for the current assistant's response, displayed in real-time
if st.session_state.messages:
    current_chat = st.session_state.messages[-1]
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-start; color: white;">
        <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
            <strong>You:</strong> {current_chat['user']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    assistant_response = st.empty()
    response_words = current_chat['assistant'].split()
    displayed_response = ""

    for word in response_words:
        displayed_response += word + " "
        assistant_response.markdown(f"""
        <div style="display: flex; justify-content: flex-end; color: white;">
            <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                <strong>Assistant:</strong> {displayed_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

# Input from user at the bottom of the screen
st.text_input("You: ", key="input_text", on_change=handle_input)
