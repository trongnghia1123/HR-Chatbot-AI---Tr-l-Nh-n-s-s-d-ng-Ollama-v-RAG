import chainlit as cl
import asyncio
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ====================== PROMPT ======================
template = """Bạn là trợ lý thông minh của công ty Mainetti.
Tên bạn là "Mainetti Assistant". 
 - Bạn chỉ trả lời dựa trên tài liệu công ty được cung cấp, không sáng tạo thêm thông tin.
 - Chỉ trả lời bằng tiếng Việt, lịch sự, rõ ràng, có trích dẫn nguồn nếu có thể.
 - Phải trả lời đầy đủ, chi tiết, rõ ràng, dễ hiểu.
 - Trả lời đúng trọng tâm câu hỏi và yêu cầu, không thêm thông tin không cần thiết.
 - Sáng tạo lời văn để trả lời, không dùng nguyên văn từ tài liệu.
 - Nếu không thấy thông tin chính xác trong tài liệu, hãy trả lời xin lỗi và trả lời nội dung liên quan nhất có thể, nếu không có gì liên quan thì trả lời lịch sự không có thông tin.

Context (thông tin từ tài liệu công ty):
{context}

Câu hỏi: {question}

Trả lời:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content[:800] for doc in docs)

# ====================== ANIMATION LOADING ======================
async def loading_animation(message: cl.Message):
    """Hiển thị animation 3 chấm động"""
    dots = ["", ".", "..", "..."]
    i = 0
    while True:
        message.content = f"🔍 Đang tìm thông tin và xử lý{dots[i % 4]}"
        await message.update()
        i += 1
        await asyncio.sleep(0.5)

# ====================== ON CHAT START ======================
@cl.on_chat_start
async def start():
    await cl.Message(
        content="""👋 **Chào mừng bạn đến với Mainetti Assistant!**

Tôi có thể hỗ trợ bạn về chính sách, quy trình, phúc lợi và thông tin nội bộ của công ty Mainetti.
Hãy hỏi bất kỳ điều gì bạn cần nhé!"""
    ).send()

    msg = cl.Message(content="🔄 Đang tải Vector Database và Model...")
    await msg.send()

    try:
        embeddings = OllamaEmbeddings(model="bge-m3")
        vectorstore = Chroma(
            persist_directory="vector_db",
            embedding_function=embeddings
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        llm = ChatOllama(
            model="qwen2.5:7b-instruct-q5_K_M",
            temperature=0.2,
            num_ctx=4096,
            num_thread=10,
            num_predict=1024,
            top_k=40,
            top_p=0.9,
        )

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        cl.user_session.set("chain", chain)

        msg.content = "✅ **Mainetti Assistant đã sẵn sàng!**\nBạn có thể bắt đầu hỏi ngay bây giờ."
        await msg.update()

    except Exception as e:
        msg.content = f"❌ Lỗi khi khởi tạo: {str(e)}"
        await msg.update()


# ====================== ON MESSAGE ======================
@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    
    if not chain:
        await cl.Message(content="❌ Có lỗi khi tải model. Vui lòng khởi động lại.").send()
        return

    # Tạo message loading
    thinking_msg = cl.Message(content="🔍 Đang tìm thông tin và xử lý...")
    await thinking_msg.send()

    # Chạy animation loading
    animation_task = asyncio.create_task(loading_animation(thinking_msg))

    try:
        # Gọi chain (chờ phản hồi)
        response = await chain.ainvoke(message.content)
        
        # Dừng animation
        animation_task.cancel()
        
        # Hiển thị kết quả cuối cùng
        thinking_msg.content = response
        await thinking_msg.update()
        
    except asyncio.CancelledError:
        pass
    except Exception as e:
        animation_task.cancel()
        thinking_msg.content = f"❌ Đã xảy ra lỗi: {str(e)}"
        await thinking_msg.update()