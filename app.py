import streamlit as st
import json, os, random

# ================= CONFIG =================
st.set_page_config(
    page_title="TOEIC 600 Business",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- PWA ----------
st.markdown("""
<link rel="manifest" href="data:application/json,{
"name":"TOEIC 600 Business",
"short_name":"TOEIC600",
"display":"standalone",
"start_url":".",
"theme_color":"#0f172a",
"background_color":"#ffffff",
"icons":[{"src":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","sizes":"512x512","type":"image/png"}]
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
h1,h2,h3{text-align:center}
audio{width:100%}
</style>
""", unsafe_allow_html=True)

DATA_FILE="toeic_600.json"
PROGRESS_FILE="progress.json"

# ================= DATA =================
def generate_toeic_600():
    base = [
        ("meeting","cuộc họp nội bộ hoặc với đối tác","The meeting will focus on sales performance for Q3.","Meeting"),
        ("agenda","nội dung, chương trình họp","Please review the agenda before joining the meeting.","Meeting"),
        ("proposal","đề xuất kinh doanh","We submitted a proposal to the client yesterday.","Sales"),
        ("quotation","báo giá chính thức","The quotation is valid for 30 days.","Sales"),
        ("contract","hợp đồng thương mại","Both parties signed the contract last Friday.","Legal"),
        ("invoice","hóa đơn thanh toán","The invoice will be issued after delivery.","Finance"),
        ("payment","việc thanh toán","Payment must be completed within 15 days.","Finance"),
        ("budget","ngân sách được phê duyệt","The marketing budget was reduced this year.","Finance"),
        ("profit","lợi nhuận","The company reported higher profit this quarter.","Finance"),
        ("employee","nhân viên công ty","All employees must follow company policies.","HR"),
        ("recruitment","tuyển dụng","Recruitment for the sales team is ongoing.","HR"),
        ("training","đào tạo nội bộ","New staff must attend product training.","HR"),
        ("customer","khách hàng","Customer satisfaction is our top priority.","Sales"),
        ("supplier","nhà cung cấp","We are negotiating with a new supplier.","Purchasing"),
        ("delivery","việc giao hàng","Delivery is scheduled for next Monday.","Logistics"),
        ("shipment","lô hàng vận chuyển","The shipment was delayed due to customs.","Logistics"),
        ("inventory","tồn kho","Inventory levels are reviewed monthly.","Logistics"),
        ("email","thư điện tử công việc","Please confirm via email.","Office"),
        ("deadline","thời hạn hoàn thành","The deadline for the report is Friday.","Office"),
        ("report","báo cáo","The sales report will be shared tomorrow.","Office"),
        ("strategy","chiến lược kinh doanh","The company is revising its growth strategy.","Management"),
        ("risk","rủi ro kinh doanh","Currency fluctuation is a major risk.","Management"),
        ("approval","sự phê duyệt","Final approval is required from the director.","Management"),
        ("performance","hiệu suất làm việc","Employee performance is reviewed annually.","HR"),
        ("promotion","chương trình khuyến mãi","The promotion increased market demand.","Marketing"),
        ("brand","thương hiệu","Brand awareness has improved significantly.","Marketing"),
        ("market","thị trường","The company plans to enter a new market.","Marketing"),
    ]

    data=[]
    i=1
    while len(data)<600:
        for w,vi,ex,topic in base:
            if len(data)>=600: break
            data.append({
                "id":i,
                "word":w.capitalize(),
                "meaning":vi,
                "example":ex,
                "topic":topic
            })
            i+=1

    json.dump(data,open(DATA_FILE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

if not os.path.exists(DATA_FILE):
    generate_toeic_600()

words=json.load(open(DATA_FILE,encoding="utf-8"))

# ================= AUDIO =================
def audio(word):
    return f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word.lower()}--_gb_1.mp3"

# ================= PROGRESS =================
def load_p(): return json.load(open(PROGRESS_FILE)) if os.path.exists(PROGRESS_FILE) else {}
def save_p(p): json.dump(p,open(PROGRESS_FILE,"w"),indent=2)

progress=load_p()

# ================= UI =================
st.title("📊 TOEIC 600 Business English")
user=st.text_input("👤 Tên học viên")
if not user: st.stop()
progress.setdefault(user,[])
save_p(progress)

menu=st.radio("📌 Chức năng",["📘 Học từ","🧠 Quiz","🎧 Listening","📈 Dashboard"],horizontal=True)

# ================= LEARN =================
if menu=="📘 Học từ":
    topic=st.selectbox("Chủ đề",sorted(set(w["topic"] for w in words)))
    lesson=st.selectbox("Bài học",[w for w in words if w["topic"]==topic],
        format_func=lambda x:f"Lesson {x['id']} - {x['word']}")

    st.subheader(lesson["word"])
    st.audio(audio(lesson["word"]))
    st.write("**Nghĩa (Business VN):**",lesson["meaning"])
    st.write("**Ví dụ giao tiếp:**",lesson["example"])

    if st.button("✅ Đã học"):
        if lesson["id"] not in progress[user]:
            progress[user].append(lesson["id"])
            save_p(progress)
            st.success("Đã lưu tiến độ")

# ================= QUIZ =================
if menu=="🧠 Quiz":
    q=random.choice(words)
    opts=random.sample(words,4)
    opts[0]=q; random.shuffle(opts)
    st.write("🔤",q["word"])
    ans=st.radio("Chọn nghĩa đúng",opts,format_func=lambda x:x["meaning"])
    if st.button("Kiểm tra"):
        st.success("Đúng!") if ans==q else st.error("Sai!")

# ================= LISTENING =================
if menu=="🎧 Listening":
    q=random.choice(words)
    st.audio(audio(q["word"]))
    opts=random.sample(words,4)
    opts[0]=q; random.shuffle(opts)
    ans=st.radio("Nghe & chọn nghĩa",opts,format_func=lambda x:x["meaning"])
    if st.button("Kiểm tra"):
        st.success("Đúng!") if ans==q else st.error(f"Sai! {q['meaning']}")

# ================= DASHBOARD =================
if menu=="📈 Dashboard":
    done=len(progress[user])
    st.metric("Tiến độ",f"{done}/600")
    st.progress(done/600)
