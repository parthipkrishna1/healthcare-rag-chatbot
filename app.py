import streamlit as st
from rag_chatbot import ask_chatbot

st.set_page_config(page_title="Healthcare RAG Chatbot", page_icon="🩺")

st.title("🩺 Healthcare RAG Chatbot")
st.caption("Ask medical questions powered by the MedQuAD dataset")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a medical question...")

if user_input:

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask_chatbot(user_input, st.session_state.messages)

        st.markdown(answer)

        if sources:
            with st.expander("Sources"):
                for s in set(sources):
                    st.write(f"- {s}")

    st.session_state.messages.append({"role": "assistant", "content": answer})