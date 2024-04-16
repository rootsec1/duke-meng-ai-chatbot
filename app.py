import streamlit as st

st.title("Duke MEng AI Program Chatbot")

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
if prompt := st.chat_input("Type your message:"):
    # Add user message to chat history
    send_user_message(prompt)
    # Echo user message as bot response and add to chat history
    bot_response = f"Bot = {prompt}"
    send_bot_message(bot_response)

    # Rerun the Streamlit app to update the conversation display
    st.rerun()
