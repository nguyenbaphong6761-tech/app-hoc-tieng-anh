import streamlit as st

# ===== CẤU HÌNH CHO MOBILE =====
st.set_page_config(
    page_title="Business English Mobile",
    page_icon="📘",
    layout="centered",   # Rất quan trọng cho mobile
    initial_sidebar_state="collapsed"  # Mặc định ẩn sidebar
)

# ===== CSS TỐI ƯU MOBILE =====
st.markdown("""
<style>
button {
    width: 100%;
    font-size: 18px !important;
}
div[data-testid="stRadio"] label {
    font-size: 18px;
}
p, li {
    font-size: 18px;
}
h1, h2, h3 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ===== TIÊU ĐỀ =====
st.title("📘 Business English")
st.caption("Học tiếng Anh thương mại – phiên bản mobile")

# ===== DỮ LIỆU =====
lessons = {
    "Chào hỏi": {
        "vocab": {
            "Meeting": "Cuộc họp",
            "Partner": "Đối tác",
            "Schedule": "Lịch trình"
        },
        "sentences": [
            "Nice to meet you.",
            "I look forward to working with you.",
            "Let's schedule a meeting."
        ]
    },
    "Bán hàng": {
        "vocab": {
            "Price": "Giá",
            "Discount": "Chiết khấu",
            "Order": "Đơn hàng"
        },
        "sentences": [
            "This is our best price.",
            "We can offer a discount.",
            "When will you place the order?"
        ]
    }
}

# ===== MENU MOBILE =====
menu = st.radio(
    "📌 Chọn chức năng",
    ["📚 Bài học", "📝 Quiz"],
    horizontal=True
)

# ===== BÀI HỌC =====
if menu == "📚 Bài học":
    lesson_name = st.selectbox("👉 Chọn bài học", lessons.keys())
    lesson = lessons[lesson_name]

    st.subheader("📌 Từ vựng")
    for word, meaning in lesson["vocab"].items():
        st.markdown(f"**{word}**  \n➡ {meaning}")
        st.divider()

    st.subheader("💬 Mẫu câu")
    for s in lesson["sentences"]:
        st.markdown(f"👉 {s}")
        st.divider()

# ===== QUIZ =====
if menu == "📝 Quiz":
    st.subheader("🧠 Kiểm tra nhanh")

    q1 = st.radio(
        "1️⃣ Discount nghĩa là gì?",
        ["Giá", "Chiết khấu", "Đơn hàng"]
    )

    q2 = st.radio(
        "2️⃣ Order nghĩa là gì?",
        ["Đối tác", "Đơn hàng", "Cuộc họp"]
    )

    if st.button("📤 Nộp bài"):
        score = 0
        if q1 == "Chiết khấu":
            score += 1
        if q2 == "Đơn hàng":
            score += 1

        st.success(f"🎯 Kết quả của bạn: {score}/2")
