import streamlit as st
from rag_engine import ask_question

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# -------------------- ENHANCED CUSTOM CSS --------------------
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Root Variables for Consistent Theming */
:root {
    --bg-primary: linear-gradient(135deg, #0c0c14 0%, #1a1a2e 50%, #16213e 100%);
    --bg-secondary: rgba(26, 26, 46, 0.8);
    --bg-card: rgba(45, 45, 65, 0.95);
    --bg-glass: rgba(255, 255, 255, 0.05);
    --text-primary: #f0f4f8;
    --text-secondary: #b8c2cc;
    --accent-primary: #7c3aed;
    --accent-secondary: #a78bfa;
    --accent-glow: rgba(124, 58, 237, 0.3);
    --border-light: rgba(255, 255, 255, 0.1);
    --shadow-main: 0 20px 40px rgba(0, 0, 0, 0.3);
    --shadow-glow: 0 0 30px rgba(124, 58, 237, 0.2);
}

/* Global Styles */
.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    backdrop-filter: blur(10px);
}

/* Hide Streamlit Elements */
header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {visibility: hidden;}

/* Center Container */
.center-box {
    text-align: center;
    margin-top: 15vh;
    padding: 2rem;
}

/* Enhanced Title with Glow */
.main-title {
    font-size: 4.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-primary) 50%, var(--accent-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 40px var(--accent-glow);
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}

.main-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    color: var(--text-secondary);
    margin-bottom: 3rem;
    opacity: 0.9;
}

/* Chat Container */
.chat-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
    height: 70vh;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--accent-primary) transparent;
}

.chat-wrapper::-webkit-scrollbar {
    width: 6px;
}

.chat-wrapper::-webkit-scrollbar-track {
    background: transparent;
}

.chat-wrapper::-webkit-scrollbar-thumb {
    background: var(--accent-primary);
    border-radius: 3px;
}

/* Message Bubbles with Glassmorphism */
.user-msg {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    backdrop-filter: blur(15px);
    padding: 1.2rem 1.8rem;
    border-radius: 24px 24px 8px 24px;
    margin: 1rem 0 1rem 10%;
    max-width: 80%;
    box-shadow: var(--shadow-main), 0 0 20px var(--accent-glow);
    border: 1px solid var(--border-light);
    position: relative;
    animation: slideInRight 0.3s ease-out;
}

.user-msg::before {
    content: '';
    position: absolute;
    left: -12px;
    top: 20px;
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-right-color: var(--accent-primary);
}

.bot-msg {
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    padding: 1.2rem 1.8rem;
    border-radius: 24px 24px 24px 8px;
    margin: 1rem 10% 1rem 0;
    max-width: 80%;
    box-shadow: var(--shadow-main);
    border: 1px solid var(--border-light);
    position: relative;
    animation: slideInLeft 0.3s ease-out;
}

.bot-msg::after {
    content: '';
    position: absolute;
    right: -12px;
    top: 20px;
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-left-color: var(--bg-glass);
}

/* Enhanced Input */
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-radius: 28px;
    padding: 1rem 2rem;
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-main), 0 0 30px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}

div[data-testid="stChatInput"]:hover {
    box-shadow: var(--shadow-main), 0 0 40px var(--accent-glow);
    border-color: var(--accent-primary);
}

div[data-testid="column"] > div > div > div > div {
    border-radius: 20px !important;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
}

/* Spinner Enhancement */
div[data-testid="stSpinner"] {
    text-align: center;
    color: var(--accent-primary);
    font-weight: 500;
}

/* Animations */
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-title {
        font-size: 3rem;
    }
    
    .chat-wrapper {
        padding: 1rem;
        height: 60vh;
    }
    
    div[data-testid="stChatInput"] {
        width: calc(100vw - 2rem);
        bottom: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- CHAT STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- EMPTY SCREEN --------------------
if len(st.session_state.messages) == 0:
    st.markdown('<div class="center-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">College AI Assistant Mithra...</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Your intelligent academic companion, ready to assist with research, questions, and college life.</p>', unsafe_allow_html=True)
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
if question := st.chat_input("💬 Ask me anything about college, research, or academics..."):
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# Generate answer after rerun
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    question = st.session_state.messages[-1]["content"]

    with st.spinner("🧠 Generating response..."):
        answer = ask_question(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
