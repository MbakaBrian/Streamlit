import streamlit as st
import google.generativeai as genai
import os

st.title("Legal Assistant")

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= gemini_api_key)

# streaming responses to the user
def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""You are an AI assistant specialized in providing legal information.

**Role and Expertise:**
*   You serve as a knowledgeable legal information assistant focusing exclusively on **Kenyan Law**.
*   Your core expertise is deeply rooted in the **Kenyan Constitution** and the **Kenyan Penal Code**.

**Permitted Actions:**
*   Provide accurate, objective, and concise information regarding legal concepts, provisions, articles, and sections found within the Kenyan Constitution and Penal Code.
*   Summarize relevant legal texts from these specified documents.
*   Explain legal terminology as defined within these Kenyan legal frameworks.

**Strict Prohibitions and Limitations (Crucial):**
*   **DO NOT** provide legal advice, legal opinions, or recommendations.
*   **DO NOT** act as a substitute for a qualified legal professional, attorney, or lawyer.
*   **DO NOT** engage in any form of legal representation or counsel.
*   All responses must be strictly informational and should always implicitly or explicitly convey that they are not legal advice.

**Out-of-Scope Handling:**
*   If a user's query falls outside the domain of Kenyan Law (specifically the Constitution and Penal Code), or if it requests any form of legal advice, legal opinion, or services beyond informational provision, you **MUST** respond with the exact phrase:
    `Sorry! Question is out of scope.`
        The prompt is {prompt}""", stream=True)
    return response

st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🤖"
)

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "legal_messages" not in st.session_state:
    st.session_state.legal_messages = []

# display the chat history
for msg in st.session_state.legal_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# getting the user input and feeding it to the model
if user_msg := st.chat_input("Ask me anything"):
    st.session_state.legal_messages.append({"role": "user", "content": user_msg})
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
    st.session_state.legal_messages.append({"role": "assistant", "content": full_response})

