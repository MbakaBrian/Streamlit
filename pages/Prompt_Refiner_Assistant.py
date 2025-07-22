import streamlit as st
import google.generativeai as genai
import os

dum1, actual, dum2 = st.columns([1, 3, 1])
with actual:
    st.title("Prompt Refiner Assistant")
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= gemini_api_key)

# streaming responses to the user
def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""You are an expert prompt engineer. Your task is to enhance and optimize the provided prompt for use with a large language model (LLM).

Ensure the prompt includes all relevant context and necessary details to achieve the intended output.

Clarify ambiguous language, eliminate redundancy, and improve structure for readability and efficiency.

Optimize the prompt to guide the LLM toward high-quality, accurate, and contextually relevant responses.
Provide the refined version of the prompt, along with a brief explanation of the improvements made (if applicable).

The prompt should not be very wordy. Keep it detailed, but not so long
        The prompt is {prompt}""", stream=True)
    return response

st.set_page_config(
    page_title="Prompt Refiner Assistant",
    page_icon="🤖",
    layout="wide",
)

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "prompt_messages" not in st.session_state:
    st.session_state.prompt_messages = []

# display the chat history
for msg in st.session_state.prompt_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# getting the user input and feeding it to the model
if user_msg := st.chat_input("Ask me anything"):
    st.session_state.prompt_messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            streaming_response = stream_gemini_response(user_msg)
            for chunk in streaming_response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + " ")

            placeholder.markdown(full_response)


        except Exception as e:
            st.error(e)

    # adding the assistant's final response to the chat history
    st.session_state.prompt_messages.append({"role": "assistant", "content": full_response})

