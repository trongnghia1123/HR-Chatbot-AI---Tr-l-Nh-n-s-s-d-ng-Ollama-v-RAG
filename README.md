# 🤖 HR Chatbot AI - Trợ lý Nhân sự sử dụng Ollama và RAG

## Giới thiệu

HR Chatbot AI là dự án xây dựng chatbot hỗ trợ trả lời các câu hỏi liên quan đến Nhân sự như:

* Quy định và chính sách công ty
* Lương, thưởng và phụ cấp
* Chế độ phúc lợi
* Nghỉ phép, tăng ca
* Quy trình và thủ tục nội bộ
* Các câu hỏi thường gặp của nhân viên

Hệ thống được xây dựng theo kiến trúc **Retrieval-Augmented Generation (RAG)**, sử dụng các mô hình AI chạy cục bộ thông qua **Ollama**, giúp đảm bảo tính bảo mật dữ liệu và giảm phụ thuộc vào các dịch vụ AI bên ngoài.

---

# Kiến trúc hệ thống

Hệ thống sử dụng 2 mô hình chính:

## 1. Qwen2.5:7B-Instruct

**Model:** `qwen2.5:7b-instruct-q5_K_M`

Chức năng:

* Tiếp nhận câu hỏi từ người dùng
* Hiểu ngữ cảnh và nội dung truy vấn
* Tạo câu trả lời tự nhiên dựa trên dữ liệu được truy xuất

## 2. BGE-M3

**Model:** `bge-m3`

Chức năng:

* Chuyển đổi tài liệu HR thành vector embedding
* Chuyển đổi câu hỏi của người dùng thành vector
* Tìm kiếm ngữ nghĩa (Semantic Search) trong cơ sở dữ liệu vector

---

# Luồng hoạt động

```text
Người dùng đặt câu hỏi
            │
            ▼
Tạo Embedding bằng BGE-M3
            │
            ▼
Tìm kiếm dữ liệu liên quan trong Vector Database
            │
            ▼
Lấy các tài liệu phù hợp nhất
            │
            ▼
Gửi Context + Câu hỏi vào Qwen2.5
            │
            ▼
Sinh câu trả lời cho người dùng
```

---

# Công nghệ sử dụng

* Python
* Ollama
* LangChain
* Chainlit
* ChromaDB (Vector Database)
* Qwen2.5:7B-Instruct
* BGE-M3 Embedding Model

---

# Cấu trúc thư mục

```text
.
├── .chainlit/              # Thư mục môi trường và cấu hình Chainlit
├── data/                   # Chứa tài liệu HR đầu vào
├── mtchat/                 # Các module xử lý chính
├── public/                 # Tài nguyên giao diện Chainlit
├── vector_db/              # Cơ sở dữ liệu vector sau khi ingest

├── app.py                  # Chạy chatbot bằng Command Line
├── ui_app.py               # Chạy chatbot với giao diện Chainlit
├── ingest.py               # Tạo Vector Database từ tài liệu
├── chainlit.md             # Nội dung trang chào mừng Chainlit
├── requirements.txt        # Danh sách thư viện cần cài đặt

└── __pycache__/            # File cache của Python
```

---

# Cài đặt dự án

## 1. Clone source code

```bash
git clone <repository_url>
cd HR-Chatbot
```

## 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## 3. Cài đặt các mô hình trên Ollama

```bash
ollama pull qwen2.5:7b-instruct-q5_K_M
ollama pull bge-m3
```

Kiểm tra danh sách model đã cài:

```bash
ollama list
```

---

# Tạo Vector Database

Đặt các tài liệu HR vào thư mục `data`.

Sau đó chạy:

```bash
python ingest.py
```

Chương trình sẽ:

* Đọc dữ liệu từ thư mục `data`
* Sinh embedding bằng mô hình `bge-m3`
* Lưu vector vào thư mục `vector_db`

---

# Chạy ứng dụng

## Chạy bằng Command Line

```bash
python app.py
```

## Chạy bằng giao diện Chainlit

```bash
chainlit run ui_app.py
```

Sau khi chạy thành công, truy cập đường dẫn được Chainlit cung cấp trên trình duyệt.

---

# Ví dụ câu hỏi

* Chính sách nghỉ phép năm của công ty là gì?
* Mức thưởng Tết được tính như thế nào?
* Quy định về làm thêm giờ ra sao?
* Nhân viên thử việc được hưởng những quyền lợi gì?
* Tôi có bao nhiêu ngày nghỉ phép trong năm?

---

# Hướng phát triển

* Hỗ trợ nhiều ngôn ngữ
* Upload tài liệu trực tiếp từ giao diện
* Quản lý lịch sử hội thoại
* Phân quyền người dùng
* Trích dẫn nguồn tài liệu trong câu trả lời
* Kết nối với hệ thống HRM/ERP
* Triển khai trên server nội bộ doanh nghiệp

---

# Mục đích dự án

Dự án được thực hiện nhằm nghiên cứu và ứng dụng:

* Large Language Models (LLM)
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Database
* Local AI Deployment với Ollama

Đồng thời cung cấp một giải pháp hỗ trợ tra cứu thông tin nhân sự nhanh chóng, chính xác và bảo mật cho doanh nghiệp.

---

# Tác giả

Dự án được phát triển với mục tiêu học tập, nghiên cứu và ứng dụng AI vào lĩnh vực Nhân sự (HR).
