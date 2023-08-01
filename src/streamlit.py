# Streamlit
# Use QARetrieval to find informations about the Octo Confluence
# Basic example with a improvementd:
# Add streaming
# Add Conversation history
# Optimize Splitter, Retriever,
# Try Open source models
import streamlit as st
from help_desk import HelpDesk


@st.cache_resource
def get_model():
    model = HelpDesk(new_db=True)
    return model


model = get_model()

# Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Comment puis-je vous aider ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input("Comment puis-je vous aider ?"):
    # Add prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get answer
    result, sources = model.retrieval_qa_inference(prompt)

    # Add answer and sources
    st.chat_message("assistant").write(result + '  \n  \n' + sources)
    st.session_state.messages.append({"role": "assistant", "content": result + '  \n  \n' + sources})
