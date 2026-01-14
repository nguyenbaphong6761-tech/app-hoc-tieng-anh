import streamlit as st
import json
import os

# ================= CONFIG =================
st.set_page_config(
    page_title="TOEIC 300",
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

DATA_FILE = "toeic_words.json"
PROGRESS_FILE = "progress.json"

# ================= AUTO GENERATE 300 TOEIC WORDS =================
def generate_toeic_300():
    toeic_core = [
        "meeting","schedule","appointment","agenda","conference","seminar","presentation","discussion","negotiation","agreement",
        "contract","proposal","quotation","offer","order","invoice","payment","receipt","refund","discount",
        "price","cost","expense","budget","profit","loss","revenue","tax","fee","salary",
        "bonus","benefit","employee","manager","director","department","office","branch","headquarters","company",
        "customer","client","supplier","vendor","partner","market","industry","competition","product","service",
        "quality","quantity","delivery","shipment","logistics","warehouse","inventory","stock","purchase","sale",
        "promotion","advertisement","brand","policy","procedure","regulation","training","interview","resume","experience",
        "skill","position","vacancy","recruitment","performance","target","achievement","growth","strategy","analysis",
        "forecast","trend","opportunity","risk","issue","solution","decision","approval","authorization","signature",
        "document","file","record","report","notice","announcement","email","request","confirmation","update",
        "review","feedback","deadline","extension","delay","cancel","priority","resource","capacity","facility",
        "equipment","maintenance","repair","operation","instruction","manual","safety","insurance","claim","warranty",
        "inspection","audit","standard","requirement","system","software","database","network","access","password",
        "account","balance","loan","credit","debit","interest","finance","investment","asset","capital",
        "transaction","transfer","payment","import","export","customs","transport","arrival","departure","reservation",
        "availability","complaint","replacement","support","process","workflow","efficiency","productivity","improvement",
        "innovation","development","implementation","evaluation","result","objective","communication","relationship"
    ]

    data = []
    for i in range(300):
        word = toeic_core[i % len(toeic_core)]
        data.append({
            "id": i + 1,
            "word": word.capitalize(),
            "type": "noun",
            "meaning": f"Từ TOEIC căn bản: {word}",
            "example": f"This is an example sentence using the word '{word}'."
        })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================= INIT DATA =================
if not os.path.exists(DATA_FILE):
    generate_toeic_300()

with open(DATA_FILE, "r", encoding="utf-8") as f:
    words = json.load(f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_progress(p):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)

progress = load_progress()

# ================= UI =================
st.title("📘 TOEIC 300")
st.caption("Học mỗi ngày 1 từ – chuẩn TOEIC căn bản")

user = st.text_input("👤 Nhập tên của bạn")

if not user:
    st.stop()

if user not in progress:
    progress[user] = []
    save_progress(progress)

menu = st.radio(
    "📌 Chức năng",
    ["📚 Bài học", "📊 Tiến độ"],
    horizontal=True
)

# ================= LESSON =================
if menu == "📚 Bài học":
    lesson_ids = [f"Lesson {w['id']}" for w in words]
    lesson_choice = st.selectbox("Chọn bài học", lesson_ids)

    lesson_id = int(lesson_choice.split()[1])
    word = next(w for w in words if w["id"] == lesson_id)

    st.subheader(f"Lesson {word['id']}")
    st.markdown(f"### 🔤 {word['word']} ({word['type']})")
    st.markdown(f"**📖 Nghĩa:** {word['meaning']}")
    st.markdown(f"**💬 Ví dụ:** {word['example']}")

    if st.button("✅ Đánh dấu đã học"):
        if lesson_id not in progress[user]:
            progress[user].append(lesson_id)
            save_progress(progress)
            st.success("Đã lưu tiến độ!")

# ================= PROGRESS =================
if menu == "📊 Tiến độ":
    done = len(progress[user])
    st.subheader("📈 Tiến độ học tập")
    st.write(f"✅ Đã học: **{done} / 300 bài**")
    st.progress(done / 300)

    if done > 0:
        st.write("📚 Bài đã hoàn thành:")
        for l in sorted(progress[user]):
            st.write(f"✔ Lesson {l}")
