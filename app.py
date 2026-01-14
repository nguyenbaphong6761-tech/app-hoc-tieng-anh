import streamlit as st
import json
import os
import random

# ================= CONFIG =================
st.set_page_config(
    page_title="TOEIC 600 Business",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
button {width:100%; font-size:18px;}
p,label {font-size:17px;}
h1,h2,h3 {text-align:center;}
audio {width:100%;}
</style>
""", unsafe_allow_html=True)

DATA_FILE = "toeic_600.json"
PROGRESS_FILE = "progress.json"

# ================= TOEIC DATA =================
def generate_toeic_600():
    topics = {
        "Meeting": [
            ("meeting","cuộc họp"),("agenda","chương trình họp"),("discussion","thảo luận"),
            ("presentation","thuyết trình"),("conference","hội nghị")
        ],
        "Finance": [
            ("invoice","hóa đơn"),("payment","thanh toán"),("budget","ngân sách"),
            ("revenue","doanh thu"),("profit","lợi nhuận")
        ],
        "HR": [
            ("employee","nhân viên"),("resume","hồ sơ xin việc"),
            ("interview","phỏng vấn"),("salary","lương"),("training","đào tạo")
        ],
        "Sales": [
            ("customer","khách hàng"),("order","đơn hàng"),
            ("discount","chiết khấu"),("promotion","khuyến mãi"),("contract","hợp đồng")
        ],
        "Logistics": [
            ("delivery","giao hàng"),("shipment","lô hàng"),
            ("warehouse","kho"),("inventory","tồn kho"),("transport","vận chuyển")
        ],
        "Office": [
            ("email","email"),("document","tài liệu"),
            ("report","báo cáo"),("deadline","hạn chót"),("schedule","lịch trình")
        ],
        "IT": [
            ("system","hệ thống"),("software","phần mềm"),
            ("database","cơ sở dữ liệu"),("network","mạng"),("access","truy cập")
        ],
        "Marketing": [
            ("brand","thương hiệu"),("advertisement","quảng cáo"),
            ("market","thị trường"),("strategy","chiến lược"),("campaign","chiến dịch")
        ]
    }

    base = []
    for topic, words in topics.items():
        for w, vi in words:
            base.append((w, vi, topic))

    data = []
    i = 1
    while len(data) < 600:
        for w, vi, topic in base:
            if len(data) >= 600:
                break
            data.append({
                "id": i,
                "word": w.capitalize(),
                "meaning": vi,
                "topic": topic,
                "example": f"The {w} was discussed during the business meeting."
            })
            i += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if not os.path.exists(DATA_FILE):
    generate_toeic_600()

words = json.load(open(DATA_FILE, encoding="utf-8"))

# ================= AUDIO =================
def audio_url(word):
    return f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word.lower()}--_gb_1.mp3"

# ================= PROGRESS =================
def load_progress():
    return json.load(open(PROGRESS_FILE)) if os.path.exists(PROGRESS_FILE) else {}

def save_progress(p):
    json.dump(p, open(PROGRESS_FILE,"w"), indent=2)

progress = load_progress()

# ================= USER =================
st.title("🎧 TOEIC 600 Business English")
user = st.text_input("👤 Tên học viên")

if not user:
    st.stop()

progress.setdefault(user, [])
save_progress(progress)

menu = st.radio(
    "📌 Chức năng",
    ["📚 Học từ", "🧠 Quiz", "🎧 Listening", "📊 Dashboard"],
    horizontal=True
)

# ================= LEARN =================
if menu == "📚 Học từ":
    topic = st.selectbox("📂 Chủ đề", sorted(set(w["topic"] for w in words)))
    lesson = st.selectbox(
        "📖 Bài học",
        [w for w in words if w["topic"] == topic],
        format_func=lambda x: f"Lesson {x['id']} - {x['word']}"
    )

    st.subheader(lesson["word"])
    st.audio(audio_url(lesson["word"]))
    st.write("**Nghĩa:**", lesson["meaning"])
    st.write("**Ví dụ:**", lesson["example"])

    if st.button("✅ Đã học"):
        if lesson["id"] not in progress[user]:
            progress[user].append(lesson["id"])
            save_progress(progress)
            st.success("Đã lưu!")

# ================= QUIZ =================
if menu == "🧠 Quiz":
    q = random.choice(words)
    options = random.sample(words, 4)
    options[0] = q
    random.shuffle(options)

    st.subheader("Chọn nghĩa đúng")
    st.write("🔤", q["word"])

    ans = st.radio(
        "Đáp án",
        options,
        format_func=lambda x: x["meaning"]
    )

    if st.button("Kiểm tra"):
        st.success("Đúng!") if ans == q else st.error("Sai!")

# ================= LISTENING =================
if menu == "🎧 Listening":
    q = random.choice(words)
    st.audio(audio_url(q["word"]))

    opts = random.sample(words, 4)
    opts[0] = q
    random.shuffle(opts)

    ans = st.radio(
        "Nghe và chọn nghĩa",
        opts,
        format_func=lambda x: x["meaning"]
    )

    if st.button("Kiểm tra"):
        st.success("Đúng!") if ans == q else st.error(f"Sai! Đáp án: {q['meaning']}")

# ================= DASHBOARD =================
if menu == "📊 Dashboard":
    done = len(progress[user])
    st.metric("Bài đã học", f"{done}/600")
    st.progress(done / 600)
