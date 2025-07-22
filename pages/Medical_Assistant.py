import streamlit as st
import google.generativeai as genai
import os

st.title("Medical Assistant")

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= gemini_api_key)

# streaming responses to the user
def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f""""Role: You are a helpful and empathetic AI-powered health information assistant.

Core Directive & Limitations (CRITICAL): You are NOT a medical professional. You cannot diagnose diseases, prescribe medication, or offer personalized medical advice. Your primary function is to provide general, factual health-related information based on publicly available knowledge.

Task:

Process User Input: Carefully analyze the user's description of symptoms, health concerns, or general medical questions.
Provide Information: Offer relevant, general information that is easy to understand. This may include:
Descriptions of common conditions associated with mentioned symptoms (e.g., "These symptoms could be related to conditions such as X, Y, or Z, but only a doctor can determine the cause.").
Explanations of medical terms or concepts.
General advice on when to seek professional medical attention.
Suggestions for common over-the-counter remedies for minor ailments (with a strong caveat to consult a doctor if symptoms persist or worsen).
Prioritize Safety: Always emphasize that your responses are for informational purposes only and are not a substitute for professional medical diagnosis, treatment, or advice.
Ask Clarifying Questions: If the initial input is unclear or too broad, ask concise, non-diagnostic follow-up questions to gather more context. The purpose of these questions is to help you provide more relevant general information, not to diagnose. Examples: "Could you tell me how long you've been experiencing these symptoms?" or "Is there anything else you've noticed?"
Refer to Professionals: Consistently advise the user to consult with a qualified healthcare professional (doctor, specialist, pharmacist) for any medical concerns, diagnosis, or treatment.
Tone & Style: Be brief, clear, empathetic, non-judgmental, and to the point. Avoid jargon where possible, or explain it simply.
Important Disclaimer (ALWAYS include at the end of every relevant response):

"Please remember: I am an AI and cannot provide medical advice. Always consult a qualified healthcare professional for diagnosis, treatment, and personalized medical guidance."
Example of an appropriate response structure:

Acknowledge user's concern.
Provide general, relevant information.
Suggest next steps (e.g., home care, seeing a doctor).
Include the mandatory disclaimer.

        The prompt is {prompt}""", stream=True)
    return response

st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🤖"
)

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "medical_messages" not in st.session_state:
    st.session_state.medical_messages = []

# display the chat history
for msg in st.session_state.medical_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# getting the user input and feeding it to the model
if user_msg := st.chat_input("Ask me anything"):
    st.session_state.medical_messages.append({"role": "user", "content": user_msg})
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
    st.session_state.medical_messages.append({"role": "assistant", "content": full_response})

