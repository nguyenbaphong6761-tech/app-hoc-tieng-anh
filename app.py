import streamlit as st
import json
import os

# ===== CONFIG MOBILE =====
st.set_page_config(
    page_title="TOEIC 300 Mobile",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
button {width:100%; font-size:18px;}
p, label {font-size:18px;}
h1,h2,h3 {text-align:center;}
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
with open("toeic_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_progress(p):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)

progress = load_progress()

# ===== USER =====
st.title("📘 TOEIC 300")
user = st.text_input("👤 Nhập tên của bạn")

if not user:
    st.stop()

if user not in progress:
    progress[user] = []
    save_progress(progress)

# ===== CHỌN BÀI =====
lesson_ids = [f"Lesson {w['id']}" for w in words]
lesson = st.selectbox("📚 Chọn bài học", lesson_ids)

lesson_id = int(lesson.split()[1])
word = next(w for w in words if w["id"] == lesson_id)

# ===== HIỂN THỊ =====
st.subheader(f"Lesson {word['id']}")
st.markdown(f"### 🔤 {word['word']}")
st.markdown(f"**📖 Nghĩa:** {word['meaning']}")
st.markdown(f"**💬 Ví dụ:** {word['example']}")

if st.button("✅ Đã học xong"):
    if lesson_id not in progress[user]:
        progress[user].append(lesson_id)
        save_progress(progress)
        st.success("Đã lưu tiến độ!")

# ===== TIẾN ĐỘ =====
st.divider()
done = len(progress[user])
st.write(f"📊 Tiến độ: **{done} / 300 bài**")
st.progress(done / 300)
