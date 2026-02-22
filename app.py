import streamlit as st
from rag_engine import ask_question

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background-color: #0f0f11;
    color: white;
}

/* Hide Streamlit Header */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Center container */
.center-box {
    text-align: center;
    margin-top: 20vh;
}

/* Title */
.main-title {
    font-size: 40px;
    font-weight: 600;
    color: #e5e5e5;
    margin-bottom: 30px;
}

/* Chat container */
.chat-wrapper {
    max-width: 800px;
    margin: auto;
}

/* User bubble */
.user-msg {
    background: #1f1f23;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: right;
    color: #ffffff;
}

/* Bot bubble */
.bot-msg {
    background: #2a2a2e;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: left;
    color: #ffffff;
}

/* Input box */
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- CHAT STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- EMPTY SCREEN --------------------
if len(st.session_state.messages) == 0:
    st.markdown('<div class="center-box">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">How can I help you?</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CHAT AREA --------------------
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- INPUT --------------------
if question := st.chat_input("Type a message..."):

    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# Generate answer after rerun
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    question = st.session_state.messages[-1]["content"]

    with st.spinner("Thinking..."):
        answer = ask_question(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()