import streamlit as st
import json
import os

# ===== FILE LƯU TIẾN ĐỘ =====
DATA_FILE = "progress.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== CẤU HÌNH MOBILE =====
st.set_page_config(
    page_title="Business English Mobile",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
button {width:100%; font-size:18px;}
p, li, label {font-size:18px;}
h1, h2, h3 {text-align:center;}
</style>
""", unsafe_allow_html=True)

# ===== DỮ LIỆU BÀI HỌC =====
lessons = {
    "Chào hỏi": {
        "vocab": ["Meeting", "Partner", "Schedule"],
        "sentences": [
            "Nice to meet you.",
            "I look forward to working with you."
        ]
    },
    "Bán hàng": {
        "vocab": ["Price", "Discount", "Order"],
        "sentences": [
            "This is our best price.",
            "When will you place the order?"
        ]
    }
}

# ===== LOAD DATA =====
data = load_data()

# ===== USER LOGIN ĐƠN GIẢN =====
st.title("📘 Business English")
user = st.text_input("👤 Nhập tên của bạn")

if not user:
    st.stop()

if user not in data:
    data[user] = {"lessons": [], "quiz_score": 0}
    save_data(data)

menu = st.radio(
    "📌 Chọn chức năng",
    ["📚 Bài học", "📝 Quiz", "📊 Tiến độ"],
    horizontal=True
)

# ===== BÀI HỌC =====
if menu == "📚 Bài học":
    lesson_name = st.selectbox("Chọn bài học", lessons.keys())
    lesson = lessons[lesson_name]

    st.subheader("📌 Từ vựng")
    for v in lesson["vocab"]:
        st.write("👉", v)

    st.subheader("💬 Mẫu câu")
    for s in lesson["sentences"]:
        st.write("•", s)

    if st.button("✅ Đánh dấu đã học"):
        if lesson_name not in data[user]["lessons"]:
            data[user]["lessons"].append(lesson_name)
            save_data(data)
            st.success("Đã lưu tiến độ!")

# ===== QUIZ =====
if menu == "📝 Quiz":
    st.subheader("Kiểm tra nhanh")

    q1 = st.radio("Discount nghĩa là gì?", ["Giá", "Chiết khấu", "Đơn hàng"])
    q2 = st.radio("Order nghĩa là gì?", ["Đối tác", "Đơn hàng", "Cuộc họp"])

    if st.button("📤 Nộp bài"):
        score = 0
        if q1 == "Chiết khấu":
            score += 1
        if q2 == "Đơn hàng":
            score += 1

        data[user]["quiz_score"] = score
        save_data(data)
        st.success(f"🎯 Điểm của bạn: {score}/2")

# ===== TIẾN ĐỘ =====
if menu == "📊 Tiến độ":
    st.subheader("📈 Tiến độ học tập")

    st.write("📚 Bài đã hoàn thành:")
    for l in data[user]["lessons"]:
        st.write("✅", l)

    st.write(f"📝 Điểm Quiz gần nhất: **{data[user]['quiz_score']} / 2**")
