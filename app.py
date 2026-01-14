import streamlit as st
import json, os, random

# ================= CONFIG =================
st.set_page_config(
    page_title="TOEIC Business 600",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= PWA =================
st.markdown("""
<link rel="manifest" href="data:application/json,{
"name":"TOEIC Business 600",
"short_name":"TOEIC600",
"display":"standalone",
"start_url":".",
"theme_color":"#0f172a",
"background_color":"#ffffff"
}">
<script>
if('serviceWorker' in navigator){
navigator.serviceWorker.register(
URL.createObjectURL(new Blob([`
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('fetch',e=>{});
`],{type:'text/javascript'}))
}
</script>
""", unsafe_allow_html=True)

st.markdown("""
<style>
button{width:100%;font-size:18px}
p,label{font-size:17px}
audio{width:100%}
h1,h2,h3{text-align:center}
</style>
""", unsafe_allow_html=True)

# ================= FILES =================
DATA_FILE = "toeic_600_business.json"
PROGRESS_FILE = "progress.json"

# ================= AUDIO (US TOEIC) =================
def audio_url(word):
    return f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word.lower()}--_us_1.mp3"

# ================= LOAD DATA =================
with open(DATA_FILE, encoding="utf-8") as f:
    words = json.load(f)

# ================= PROGRESS =================
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        return json.load(open(PROGRESS_FILE, encoding="utf-8"))
    return {}

def save_progress(p):
    json.dump(p, open(PROGRESS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

progress = load_progress()

# ================= UI =================
st.title("📘 TOEIC Business 600")

user = st.text_input("👤 Tên học viên")
if not user:
    st.stop()

progress.setdefault(user, [])
save_progress(progress)

menu = st.radio(
    "📌 Chức năng",
    ["📘 Học theo chủ đề", "🧠 Quiz", "🎧 Listening", "📈 Dashboard"],
    horizontal=True
)

# ================= LEARN BY TOPIC =================
if menu == "📘 Học theo chủ đề":
    topic = st.selectbox(
        "📚 Chọn chủ đề",
        sorted(set(w["topic"] for w in words))
    )

    lessons = [w for w in words if w["topic"] == topic]

    lesson = st.selectbox(
        "📖 Chọn bài học",
        lessons,
        format_func=lambda x: f"Lesson {x['id']} – {x['word'].capitalize()}"
    )

    st.subheader(lesson["word"].capitalize())
    st.audio(audio_url(lesson["word"]))

    st.markdown("### 🇻🇳 Nghĩa trong môi trường kinh doanh")
    st.write(lesson["meaning"])

    st.markdown("### 💼 Ví dụ giao tiếp thương mại")
    st.write(lesson["example"])

    if st.button("✅ Đánh dấu đã học"):
        if lesson["id"] not in progress[user]:
            progress[user].append(lesson["id"])
            save_progress(progress)
            st.success("Đã lưu tiến độ học")

# ================= QUIZ =================
if menu == "🧠 Quiz":
    q = random.choice(words)
    options = random.sample(words, 4)
    options[0] = q
    random.shuffle(options)

    st.markdown("### 🔤 Chọn nghĩa đúng")
    st.write(q["word"].capitalize())

    ans = st.radio(
        " ",
        options,
        format_func=lambda x: x["meaning"]
    )

    if st.button("Kiểm tra"):
        if ans == q:
            st.success("✅ Chính xác")
        else:
            st.error(f"❌ Sai – Đáp án đúng: {q['meaning']}")

# ================= LISTENING =================
if menu == "🎧 Listening":
    q = random.choice(words)
    st.audio(audio_url(q["word"]))

    options = random.sample(words, 4)
    options[0] = q
    random.shuffle(options)

    ans = st.radio(
        "Nghe và chọn nghĩa đúng",
        options,
        format_func=lambda x: x["meaning"]
    )

    if st.button("Kiểm tra"):
        if ans == q:
            st.success("✅ Nghe đúng")
        else:
            st.error(f"❌ Sai – Nghĩa đúng: {q['meaning']}")

# ================= DASHBOARD =================
if menu == "📈 Dashboard":
    done = len(progress[user])
    total = len(words)
    st.metric("Tiến độ học", f"{done} / {total} từ")
    st.progress(done / total)

    st.markdown("### 📊 Trạng thái học tập")
    st.write("Tiếp tục duy trì đều đặn mỗi ngày để đạt hiệu quả TOEIC cao nhất.")
