import streamlit as st
import random
import time
from index import Main

generate_text = Main()

st.title("QA Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("Message QA Chatbot..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        query = [msg["content"]
                 for msg in st.session_state.messages if msg["role"] == "user"][-1].lower()

        # Process Query here and get response
        assistant_response = generate_text.process_user_query(query=query)        
        
        # # Simulate stream of response with milliseconds delay
        if "\n" in assistant_response:
            for chunk in assistant_response.split("\n"):
                for item in chunk.split():
                    full_response += item + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                full_response += "\n"
        else:
            for item in assistant_response.split():
                full_response += item + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
