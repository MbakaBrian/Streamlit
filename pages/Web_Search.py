import streamlit as st
from openai import OpenAI
import os

from dotenv import load_dotenv

# Set page config
st.set_page_config(page_title="Web Search Assistant", page_icon="🔍")
st.title("🔍 Web Search Assistant")
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key= openai_api_key)

# Session state for messages and model
if "chat_model" not in st.session_state:
    st.session_state.chat_model = "gpt-4o-search-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Define function to stream OpenAI response
def stream_openai_response(prompt):
    system_prompt = (
        "You are an intelligent and informative assistant with access to real-time information. "
        "Use web search where needed to provide clear, concise, and helpful answers."
    )
    response = client.chat.completions.create(
        model=st.session_state.chat_model,
        web_search_options={},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    return response

# Chat input
if user_input := st.chat_input("Ask me anything..."):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            response_stream = stream_openai_response(user_input)
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Error: {e}"
            st.error(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
