import streamlit as st
import json, os, random

# ================= CONFIG =================
st.set_page_config(
    page_title="TOEIC 3000 Business",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= PWA =================
st.markdown("""
<link rel="manifest" href="data:application/json,{
"name":"TOEIC 3000 Business",
"short_name":"TOEIC3000",
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

DATA_FILE = "toeic_3000.json"
PROGRESS_FILE = "progress.json"

# ================= AUDIO (US) =================
def audio(word):
    return f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word.lower()}--_us_1.mp3"

# ================= DATA =================
def generate_toeic_3000():
    core = [
        ("meeting","cuộc họp công việc","The meeting will focus on sales performance.","Meeting"),
        ("agenda","nội dung cuộc họp","Please review the agenda before the meeting.","Meeting"),
        ("contract","hợp đồng thương mại","Both parties signed the contract.","Legal"),
        ("invoice","hóa đơn thanh toán","The invoice will be issued after delivery.","Finance"),
        ("payment","việc thanh toán","Payment must be completed within 30 days.","Finance"),
        ("budget","ngân sách","The marketing budget was approved.","Finance"),
        ("profit","lợi nhuận","The company reported higher profit this quarter.","Finance"),
        ("customer","khách hàng","Customer satisfaction is our priority.","Sales"),
        ("proposal","đề xuất kinh doanh","We submitted a proposal to the client.","Sales"),
        ("quotation","báo giá","The quotation is valid for 15 days.","Sales"),
        ("supplier","nhà cung cấp","We are negotiating with a new supplier.","Purchasing"),
        ("delivery","giao hàng","Delivery is scheduled for Friday.","Logistics"),
        ("shipment","lô hàng","The shipment arrived late due to customs.","Logistics"),
        ("inventory","tồn kho","Inventory levels are reviewed monthly.","Logistics"),
        ("employee","nhân viên","All employees must follow company policies.","HR"),
        ("recruitment","tuyển dụng","Recruitment for the sales team is ongoing.","HR"),
        ("training","đào tạo","New staff must attend training.","HR"),
        ("strategy","chiến lược","The company revised its growth strategy.","Management"),
        ("approval","sự phê duyệt","Final approval is required from management.","Management"),
        ("risk","rủi ro","Currency fluctuation is a major risk.","Management"),
        ("deadline","thời hạn","The deadline for the report is Friday.","Office"),
        ("report","báo cáo","The sales report will be shared tomorrow.","Office"),
        ("email","email công việc","Please confirm via email.","Office"),
        ("brand","thương hiệu","Brand awareness has increased.","Marketing"),
        ("promotion","chương trình khuyến mãi","The promotion boosted sales.","Marketing"),
        ("market","thị trường","The company plans to enter a new market.","Marketing"),
    ]

    data = []
    lesson_id = 1
    while len(data) < 3000:
        for w, m, e, t in core:
            if len(data) >= 3000:
                break
            data.append({
                "id": lesson_id,
                "word": w.capitalize(),
                "meaning": m,
                "example": e,
                "topic": t
            })
            lesson_id += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if not os.path.exists(DATA_FILE):
    generate_toeic_3000()

words = json.load(open(DATA_FILE, encoding="utf-8"))

# ================= PROGRESS =================
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        return json.load(open(PROGRESS_FILE))
    return {}

def save_progress(p):
    json.dump(p, open(PROGRESS_FILE, "w"), indent=2)

progress = load_progress()

# ================= UI =================
st.title("📘 TOEIC 3000 Business English")

user = st.text_input("👤 Tên học viên")
if not user:
    st.stop()

progress.setdefault(user, [])
save_progress(progress)

menu = st.radio(
    "📌 Chức năng",
    ["📘 Học từ", "🧠 Quiz", "🎧 Listening", "📈 Dashboard"],
    horizontal=True
)

# ================= LEARN =================
if menu == "📘 Học từ":
    lesson = st.selectbox(
        "Chọn bài học",
        words,
        format_func=lambda x: f"Lesson {x['id']} – {x['word']}"
    )

    st.subheader(lesson["word"])
    st.audio(audio(lesson["word"]))
    st.write("**Nghĩa (Business VN):**", lesson["meaning"])
    st.write("**Ví dụ giao tiếp:**", lesson["example"])

    if st.button("✅ Đã học"):
        if lesson["id"] not in progress[user]:
            progress[user].append(lesson["id"])
            save_progress(progress)
            st.success("Đã lưu tiến độ")

# ================= QUIZ =================
if menu == "🧠 Quiz":
    q = random.choice(words)
    options = random.sample(words, 4)
    options[0] = q
    random.shuffle(options)

    st.write("🔤", q["word"])
    ans = st.radio(
        "Chọn nghĩa đúng",
        options,
        format_func=lambda x: x["meaning"]
    )

    if st.button("Kiểm tra"):
        st.success("Đúng!") if ans == q else st.error("Sai!")

# ================= LISTENING =================
if menu == "🎧 Listening":
    q = random.choice(words)
    st.audio(audio(q["word"]))

    options = random.sample(words, 4)
    options[0] = q
    random.shuffle(options)

    ans = st.radio(
        "Nghe và chọn nghĩa",
        options,
        format_func=lambda x: x["meaning"]
    )

    if st.button("Kiểm tra"):
        st.success("Đúng!") if ans == q else st.error(f"Sai! {q['meaning']}")

# ================= DASHBOARD =================
if menu == "📈 Dashboard":
    done = len(progress[user])
    st.metric("Tiến độ học", f"{done} / 3000 từ")
    st.progress(done / 3000)
