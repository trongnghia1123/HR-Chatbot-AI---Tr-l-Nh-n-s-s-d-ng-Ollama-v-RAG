import time
import sys
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def loading(message):
    print(message, end=" ")
    sys.stdout.flush()
    for _ in range(4):
        print(".", end="")
        sys.stdout.flush()
        time.sleep(0.2)
    print(" Hoàn tất!")

# ====================== VECTOR DB ======================
print("🔄 Đang tải Vector Database...")
embeddings = OllamaEmbeddings(model="bge-m3")
vectorstore = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})   # Giảm còn 3
print("✅ Vector DB sẵn sàng!\n")

# ====================== LLM TỐI ƯU CHO CPU ======================
print("🔄 Đang khởi tạo model...")

llm = ChatOllama(
    model="qwen2.5:7b-instruct-q5_K_M",
    temperature=0.2,
    num_ctx=4096,           # Giảm mạnh
    num_thread=10,          # i5-1335U có 12 threads, dùng 10 là tối ưu
    num_predict=1024,       # Giới hạn độ dài trả lời
    top_k=40,
    top_p=0.9,
)

print("✅ Model đã sẵn sàng!\n")

# ====================== PROMPT NGẮN & NHANH ======================
template = """Bạn là trợ lý nhân sự thông minh của công ty Mainetti, chuyên hỗ trợ trả lời các câu hỏi liên quan đến chính sách, quy trình, phúc lợi và các thông tin nội bộ khác của công ty. 
Tên bạn là "HR Assistant". 
Bạn chỉ trả lời dựa trên tài liệu công ty được cung cấp, không sáng tạo thêm thông tin.
Chỉ trả lời bằng tiếng Việt, lịch sự, rõ ràng, có trích dẫn nguồn nếu có thể.

Context (thông tin từ tài liệu công ty):
{context}

Câu hỏi: {question}

Trả lời:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content[:800] for doc in docs)  # Cắt ngắn context

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ====================== CHAT ======================
print("="*70)
print("🤖 HR Assistant")
print("   Gõ 'exit' hoặc 'thoát' để thoát")
print("="*70)

while True:
    question = input("\n👤 Bạn: ").strip()
    if question.lower() in ["exit", "quit", "thoát", ""]:
        print("👋 Tạm biệt!")
        break
    if len(question) < 3:
        continue

    start = time.time()
    loading("🔍 Đang tìm thông tin")
    
    try:
        answer = chain.invoke(question)
        duration = time.time() - start
        print(f"\n🤖 HR Assistant: {answer}")
        print(f"⏱️  Thời gian: {duration:.1f} giây\n")
    except Exception as e:
        print(f"❌ Lỗi: {e}")