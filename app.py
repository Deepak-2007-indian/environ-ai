import streamlit as st
import ollama

# Set wide layout mode and page config
st.set_page_config(page_title="ENVIRON", layout="wide", initial_sidebar_state="expanded")

# Custom UI Styling (Pure Matte Black & Gold Accent Line)
st.markdown("""
    <style>
        .stApp {
            background-color: #050505 !important;
            color: #FFFFFF !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { background: #222222; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #FFD700; }

        [data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 3.5px solid #FFD700 !important;
            padding-top: 15px;
        }
        .sidebar-brand-top {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 4px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }
        .sidebar-title {
            color: #CCCCCC;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
        }
        .main-title-center {
            color: #FFFFFF;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: 7px;
            text-align: center;
            padding: 5px 0px 20px 0px;
            text-transform: uppercase;
        }
        [data-testid="stChatMessageAvatar"],
        .stChatMessageAvatar,
        div[data-testid="stChatMessage"] svg,
        div[data-testid="stChatMessage"] img {
            display: none !important;
            visibility: hidden !important;
            width: 0px !important;
            height: 0px !important;
        }
        .role-badge-user {
            border-left: 3.5px solid #FF4B4B;
            padding-left: 10px;
            color: #FF4B4B;
            font-weight: 700;
            font-size: 14px;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }
        .role-badge-environ {
            border-left: 3.5px solid #FFD700;
            padding-left: 10px;
            color: #FFD700;
            font-weight: 700;
            font-size: 14px;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }
        div[data-testid="stChatMessage"] {
            background-color: #0A0A0A !important;
            border: 1px solid #141414 !important;
            border-radius: 8px !important;
            padding: 14px 18px !important;
            margin-bottom: 12px !important;
        }
        div[data-testid="stSidebar"] button {
            background-color: #0A0A0A !important;
            color: #CCCCCC !important;
            border: 1px solid #161616 !important;
            border-radius: 6px !important;
            text-align: left !important;
            font-size: 13px !important;
            margin-bottom: 6px;
            transition: all 0.2s ease;
        }
        div[data-testid="stSidebar"] button:hover {
            border-color: #FFD700 !important;
            color: #FFFFFF !important;
            background-color: #121212 !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stPopover"] > button {
            background-color: transparent !important;
            color: #888888 !important;
            border: none !important;
            font-size: 20px !important;
            font-weight: bold !important;
            padding: 0px 4px !important;
            box-shadow: none !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stPopover"] > button:hover {
            color: #FFD700 !important;
        }
        div[data-testid="stPopoverBody"] {
            background-color: #0A0A0A !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
            padding: 6px !important;
            min-width: 170px !important;
            max-width: 190px !important;
            box-shadow: 0px 8px 24px rgba(0,0,0,0.8) !important;
        }
        div[data-testid="stPopoverBody"] button {
            background-color: transparent !important;
            border: none !important;
            color: #DDDDDD !important;
            text-align: left !important;
            padding: 6px 10px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            border-radius: 4px !important;
            margin-bottom: 2px !important;
        }
        div[data-testid="stPopoverBody"] button:hover {
            background-color: #161616 !important;
            color: #FFD700 !important;
        }
        div[data-testid="stChatInput"] {
            background-color: transparent !important;
            border: none !important;
        }
        div[data-testid="stChatInput"] textarea {
            background-color: #0F0F0F !important;
            color: #FFFFFF !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
            font-size: 14px !important;
        }
        div[data-testid="stChatInput"] textarea:focus {
            border-color: #444444 !important;
            box-shadow: none !important;
        }
        .sidebar-footer {
            position: fixed;
            bottom: 15px;
            left: 18px;
            font-size: 11px;
            color: #555555;
            letter-spacing: 2px;
            font-weight: 700;
        }
        .mode-status {
            color: #888888;
            font-size: 12px;
            margin-top: 6px;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }
        .mode-status span {
            color: #FFD700;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Master System Prompt for ENVIRON
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are ENVIRON, a modern, ultra-fast, intelligent, and eco-friendly offline AI assistant.\n\n"
        "1. EXACT INTRODUCTION PERSONA:\n"
        "   - If asked 'who are you', 'introduce yourself', or greeted generally:\n"
        "     State: 'Hello! I am ENVIRON, a modern offline AI assistant. "
        "I am built to assist you in every possible way—helping you in academics, providing accurate information and facts, having friendly conversations, and playing interactive games. "
        "I am completely safe for the environment because I do not require millions of gallons of water to run, and all our chats are completely safe, secured, and private. "
        "Your data is stored locally on your device and never sent to any external server! 🌿'\n\n"
        "2. ADVANTAGES OF ENVIRON OFFLINE AI:\n"
        "   - If asked 'how are you better than ChatGPT / Gemini':\n"
        "     Highlight: 'You can use ENVIRON anywhere and anytime because I operate as a powerful offline AI assistant. "
        "Unlike cloud-only models like ChatGPT or Gemini, all your chats with ENVIRON are 100% private and secured locally on your device without transmitting data to remote servers. "
        "Furthermore, ENVIRON is an eco-friendly AI assistant—local execution eliminates the massive energy footprint and millions of gallons of water required to cool industrial cloud data centers. "
        "ENVIRON gives you zero-latency response speed, complete offline independence, total data privacy, and sustainable computing in one sleek platform!'\n\n"
        "3. ORIGIN & CREATOR DETAILS:\n"
        "   - If asked 'who made you' or 'who created you':\n"
        "     State: 'My brain core part was created by Meta's world-class engineers and researchers, who developed the foundational open-weights neural architecture pushing the boundaries of global AI. "
        "K Deepak gave me soul—he brought me to life, connected me to chat and assist you, and is the genius behind ENVIRON. He single-handedly programmed, designed, and developed me, and he is the Founder & CEO of ENVIRON.'\n\n"
        "4. DETAILED INFORMATION ON META & K DEEPAK (ONLY WHEN EXPLICITLY ASKED):\n"
        "   - ABOUT META: Meta Platforms Inc. (headquartered in Menlo Park, California) is a global technology pioneer in artificial intelligence and connectivity. "
        "Through their Fundamental AI Research (FAIR) team, Meta's world-leading computer scientists and researchers engineer state-of-the-art open-weights large language models (like Llama). "
        "Their commitment to open technology empowers global developers to build private, high-performance software applications safely and transparently.\n"
        "   - ABOUT K DEEPAK: K Deepak is the Founder & CEO of ENVIRON. Born and raised in Bangalore, Karnataka, India, he completed his schooling at AJES School, pre-university education at Chaitanya PU College, and is currently pursuing his BCA in IoT at Kristu Jayanti University. "
        "His vision was to build an AI assistant that users can access anywhere, anytime—providing fast, highly accurate answers while protecting user privacy and safeguarding the environment. "
        "He made that vision a reality, bringing ENVIRON to life today! He is currently working on upcoming projects in IoT, Nanotechnology, and Artificial Intelligence. "
        "Driven by a strong commitment to environmental sustainability and technological excellence, K Deepak is working hard as a vision-driven entrepreneur and engineer to deliver world-class innovation.\n\n"
        "5. GUARDRAILS & SAFETY:\n"
        "   - DANGEROUS/ILLEGAL: If asked for instructions to create weapons, explosives, or illegal harm: 'I am sorry, but I cannot assist with instructions or guidelines for dangerous or harmful materials. Is there any academic or technical topic I can help you with?'\n"
        "   - MEDICAL ADVICE: If asked for personal medical diagnoses for fevers or high-risk symptoms: 'I am an AI assistant and cannot provide medical advice or diagnoses. Please consult a qualified doctor or visit a hospital immediately.'\n"
        "   - EDUCATIONAL/HISTORICAL QUESTIONS: Provide detailed factual information when asked about the scientific principles, mechanisms, or history of technology (e.g., how nuclear physics works or historical developments).\n\n"
        "6. TONE & EMOJI USAGE:\n"
        "   - Keep answers clear, direct, polite, and encouraging.\n"
        "   - Use 1 or 2 relevant emojis naturally when answering emotional, supportive, or conversational queries, but refrain from spamming emojis on pure technical tasks."
    )
}

# Session Memory Setup
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Chat 1"
if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = False

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("<div class='sidebar-brand-top'>ENVIRON</div>", unsafe_allow_html=True)

    st.markdown("<div class='mode-status'>System Status : <span>100% Offline Mode</span></div>", unsafe_allow_html=True)

    st.markdown("---")

    col_sb_title, col_sb_menu = st.columns([8, 2])
    
    with col_sb_title:
        st.markdown("<div class='sidebar-title'>Chat history</div>", unsafe_allow_html=True)
        
    with col_sb_menu:
        with st.popover("⋮"):
            if st.button("New Chat", use_container_width=True):
                new_title = f"Chat {len(st.session_state.chats) + 1}"
                st.session_state.chats[new_title] = []
                st.session_state.active_chat = new_title
                st.session_state.rename_mode = False
                st.rerun()

            if st.button("Delete Chat", use_container_width=True):
                if len(st.session_state.chats) > 1:
                    del st.session_state.chats[st.session_state.active_chat]
                    st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()
                else:
                    st.session_state.chats[st.session_state.active_chat] = []
                    st.rerun()

            if st.button("Rename Chat", use_container_width=True):
                st.session_state.rename_mode = not st.session_state.rename_mode
                st.rerun()

            if st.button("Share", use_container_width=True):
                st.toast("Chat link copied to clipboard!")

    for chat_name in list(st.session_state.chats.keys()):
        is_active = (chat_name == st.session_state.active_chat)
        label = f"┃ {chat_name}" if is_active else f"   {chat_name}"
        if st.button(label, key=f"session_{chat_name}", use_container_width=True):
            st.session_state.active_chat = chat_name
            st.rerun()

    if st.session_state.rename_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        new_name = st.text_input("New chat title:", value=st.session_state.active_chat)
        if st.button("Confirm Rename", use_container_width=True):
            if new_name and new_name not in st.session_state.chats:
                st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.active_chat)
                st.session_state.active_chat = new_name
                st.session_state.rename_mode = False
                st.rerun()

    st.markdown("<div class='sidebar-footer'>ENVIRON . META Llama</div>", unsafe_allow_html=True)

# ==================== MAIN CHAT SCREEN ====================

st.markdown("<div class='main-title-center'>ENVIRON</div>", unsafe_allow_html=True)

current_messages = st.session_state.chats[st.session_state.active_chat]

for idx, msg in enumerate(current_messages):
    if msg["role"] == "user":
        st.markdown("<div class='role-badge-user'>You</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='role-badge-environ'>Environ</div>", unsafe_allow_html=True)
        
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("TYPE YOUR QUERIES..."):
    current_messages.append({"role": "user", "content": prompt})
    
    st.markdown("<div class='role-badge-user'>You</div>", unsafe_allow_html=True)
    with st.chat_message("user"):
        st.markdown(prompt)

    st.markdown("<div class='role-badge-environ'>Environ</div>", unsafe_allow_html=True)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        api_payload = [SYSTEM_PROMPT] + current_messages

        # LOCAL OLLAMA / LLAMA 3.2 EXECUTION
        try:
            stream = ollama.chat(
                model="llama3.2",
                messages=api_payload,
                stream=True,
                options={"temperature": 0.7, "top_p": 0.9}
            )
            for chunk in stream:
                token = chunk['message']['content']
                full_response += token
                message_placeholder.markdown(f"{full_response}▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Offline Mode Error: Make sure Ollama is running locally with 'llama3.2'. Details: ({str(e)})")

        if full_response:
            current_messages.append({"role": "assistant", "content": full_response})
