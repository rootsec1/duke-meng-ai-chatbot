import streamlit as st
from util import get_bot_response

# JS code to modify te decoration on top
st.image("assets/images/logo.png", use_column_width=True)

# CSS to inject specified fonts
font_css = """
<style>
@import url("https://fonts.googleapis.com/css?family=EB+Garamond:400,400i,700|Open+Sans:400,400i,700");

h1, h2, h3, h4, h5, h6, [class*="css-"] {
    font-family: 'EB Garamond', Georgia, 'Times New Roman', Times, serif;
}
body {
    font-family: 'Open Sans', 'Helvetica Neue', 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 14px;
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

st.title("Q&A Chatbot (by Abhishek Murthy)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def send_user_message(user_message: str):
    # Add user message to chat history
    st.session_state["messages"].append(
        {"role": "user", "content": user_message}
    )


def send_bot_message(bot_message: str):
    # Add bot message to chat history
    st.session_state["messages"].append(
        {"role": "assistant", "content": bot_message}
    )


# Accept user input
if prompt := st.chat_input("Ask questions about the program: Who is the program director?"):
    # Add user message to chat history
    send_user_message(prompt)
    # Echo user message as bot response and add to chat history
    bot_response = get_bot_response(prompt)
    send_bot_message(bot_response)

    # Rerun the Streamlit app to update the conversation display
    st.rerun()
