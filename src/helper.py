import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from PyPDF2 import PdfReader

os.environ["GOOGLE_API_KEY"] = "your_api_key_here"

# ---------------------------
# Extract PDF Text
# ---------------------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


# ---------------------------
# Text Splitting
# ---------------------------
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)


# ---------------------------
# Vector Store
# ---------------------------
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_texts(text_chunks, embedding=embeddings)


# ---------------------------
# LLM + Memory + Chain
# ---------------------------
def get_conversation_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        return_source_documents=True
    )

    return conversation_chain


# ---------------------------
# Gemini Vision Model
# ---------------------------
def get_vision_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash")