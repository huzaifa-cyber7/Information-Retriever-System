import streamlit as st
import base64
from pathlib import Path

def set_professional_background():
    """
    Apply a futuristic, glassmorphic background using the JPG in assets/background.jpg
    """
    img_path = Path(__file__).parent / "background.jpg"
    if not img_path.exists():
        st.warning("⚠️ Background image not found!")
        return

    with open(img_path, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()

    css = f"""
    <style>
    section[data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main {{
        background: rgba(0,0,0,0.55) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        color: #ffffff !important;
    }}
    .stSidebar {{
        background: rgba(10,10,10,0.7) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        backdrop-filter: blur(6px) !important;
        -webkit-backdrop-filter: blur(6px) !important;
        color: #ffffff !important;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        border: none !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        cursor: pointer !important;
    }}
    .chat-bubble-user {{
        background: linear-gradient(90deg,#0A84FF,#3BB3FF);
        color: white;
        padding: 12px;
        border-radius: 16px;
        margin: 6px 6px 6px 0;
        display: inline-block;
        max-width: 80%;
    }}
    .chat-bubble-ai {{
        background: rgba(44,44,46,0.9);
        color: white;
        padding: 12px;
        border-radius: 16px;
        margin: 6px 0 6px 6px;
        display: inline-block;
        max-width: 80%;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
