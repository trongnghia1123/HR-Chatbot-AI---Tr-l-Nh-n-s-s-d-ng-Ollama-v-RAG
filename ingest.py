import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Đường dẫn
DATA_PATH = "data"
DB_PATH = "vector_db"

# Load tất cả tài liệu
documents = []

# PDF
pdf_loader = PyPDFDirectoryLoader(DATA_PATH)
documents.extend(pdf_loader.load())

# DOCX
for file in os.listdir(DATA_PATH):
    if file.endswith(".docx"):
        loader = Docx2txtLoader(os.path.join(DATA_PATH, file))
        documents.extend(loader.load())

# TXT
for file in os.listdir(DATA_PATH):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(DATA_PATH, file), encoding="utf-8")
        documents.extend(loader.load())

print(f"Đã load {len(documents)} tài liệu")

# Chia nhỏ văn bản
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
splits = text_splitter.split_documents(documents)

print(f"Đã chia thành {len(splits)} chunks")

# ==================== SỬA Ở ĐÂY ====================
embeddings = OllamaEmbeddings(model="bge-m3")   # ← Phải là bge-m3

# Tạo vector database
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory=DB_PATH
)

print("✅ Vector database đã tạo thành công với bge-m3!")