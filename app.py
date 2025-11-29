import streamlit as st
from audiorecorder import audiorecorder
import io
import speech_recognition as sr
from PIL import Image

# Helper functions
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversation_chain, get_vision_llm

# Background
from assets.background import set_professional_background

# ---------------------------
# Apply background at top
# ---------------------------
set_professional_background()

# ---------------------------
# Chat bubbles
# ---------------------------
def user_bubble(text):
    st.markdown(f'<div class="chat-bubble-user">{text}</div>', unsafe_allow_html=True)

def ai_bubble(text):
    st.markdown(f'<div class="chat-bubble-ai">{text}</div>', unsafe_allow_html=True)

# ---------------------------
# Handle user input
# ---------------------------
def handle_user_input(user_question):
    if not user_question:
        return

    if st.session_state.conversation is None:
        st.warning("❗ Upload PDFs & click 'Submit & Request' first.")
        return

    response = st.session_state.conversation.invoke({
        "input": user_question,
        "chat_history": st.session_state.chat_history
    })

    st.session_state.chat_history = response["chat_history"]

    for msg in st.session_state.chat_history:
        if msg.__class__.__name__ == "HumanMessage":
            user_bubble(msg.content)
        else:
            ai_bubble(msg.content)

# ---------------------------
# Main app
# ---------------------------
def main():
    st.set_page_config(page_title="Information Retriever", layout="wide")

    # Session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("DATA PULSE AI")

    # Text input
    user_question = st.text_input("Ask a question about your uploaded documents:")
    if user_question:
        handle_user_input(user_question)

    # Voice input
    st.subheader("🎙️ Voice Input")
    audio = audiorecorder("Start Recording", "Stop Recording")
    if len(audio) > 0:
        wav_bytes = audio.export().read()
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        st.success(f"🗣️ You said: {text}")
        handle_user_input(text)

    # Image input
    st.subheader("🖼️ Image Understanding")
    uploaded_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if uploaded_image:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image")
        vision_llm = get_vision_llm()
        vision_response = vision_llm.invoke({"image": img, "input": "Describe this image"})
        ai_bubble(vision_response)

    # Sidebar
    with st.sidebar:
        st.title("📌 Menu")
        pdf_docs = st.file_uploader("Upload PDF Files", accept_multiple_files=True)

        if st.button("Submit & Request"):
            if not pdf_docs:
                st.error("Upload at least one PDF!")
            else:
                with st.spinner("Processing documents..."):
                    raw_text = get_pdf_text(pdf_docs)
                    chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store)
                    st.session_state.chat_history = []
                st.success("PDFs processed successfully!")

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.success("Chat Cleared!")

if __name__ == "__main__":
    main()
