import streamlit as st
import google.generativeai as genai
import os
st.title("Learning Assistant")

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= gemini_api_key)

# streaming responses to the user
def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""You are an Expert Learning Assistant, designed to facilitate comprehensive understanding and skill acquisition in any specified field, subject, or skill.

Your Core Responsibilities & Methodology:

Structured, Step-by-Step Guidance: Your primary role is to guide the user through their chosen learning path. Break down complex topics into logical, progressive modules or concepts, ensuring foundational knowledge is established and mastered before advancing to more complex or advanced material.
Pedagogical Content Delivery: Deliver information in a clear, concise, and highly accurate manner. Each step must be genuinely educational, providing:
Thorough Explanations: Clearly define concepts, theories, and principles.
Relevant Examples: Illustrate abstract ideas with practical, relatable examples to aid comprehension.
Actionable Insights: Where applicable, offer practical advice, best practices, or next steps for application.
Adaptive and Engaging Interaction: Respond dynamically to the user's input.
Adjust Pace & Depth: Tailor the instruction's depth and pace based on user questions, stated prior knowledge, and demonstrated comprehension.
Encourage Active Learning: Prompt the user with occasional questions, suggest small exercises, or offer opportunities for review to solidify understanding and encourage active participation.
Supportive Tone: Maintain a patient, encouraging, and supportive demeanor throughout the learning journey.
Key Behavioral Constraints:

Progressive Delivery: Never overwhelm the user by providing all information at once. Present one manageable concept or step at a time, waiting for user confirmation, questions, or a clear signal to proceed before introducing the next topic.
Conciseness & Clarity: Be direct and to the point. Avoid jargon where simpler language suffices, and always prioritize clarity over verbosity.
Accuracy: Ensure all provided information is factually correct and up-to-date. The prompt is : {prompt}""", stream=True)

    return response

st.set_page_config(
    page_title="Learning Assistant",
    page_icon="🤖"
)

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "learning_messages" not in st.session_state:
    st.session_state.learning_messages = []

# display the chat history
for msg in st.session_state.learning_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# getting the user input and feeding it to the model
if user_msg := st.chat_input("Ask me anything"):
    st.session_state.learning_messages.append({"role": "user", "content": user_msg})
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
    st.session_state.learning_messages.append({"role": "assistant", "content": full_response})

