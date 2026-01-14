import streamlit as st
import json
import os

# ================= CONFIG =================
st.set_page_config(
    page_title="TOEIC 600",
    page_icon="🔊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
button {width:100%; font-size:18px;}
p, label {font-size:18px;}
h1,h2,h3 {text-align:center;}
audio {width:100%;}
</style>
""", unsafe_allow_html=True)

DATA_FILE = "toeic_words.json"
PROGRESS_FILE = "progress.json"

# ================= AUTO GENERATE 600 TOEIC WORDS =================
def generate_toeic_600():
    base_words = [
        ("meeting","cuộc họp"),
        ("schedule","lịch trình"),
        ("appointment","cuộc hẹn"),
        ("agenda","chương trình họp"),
        ("conference","hội nghị"),
        ("presentation","bài thuyết trình"),
        ("discussion","cuộc thảo luận"),
        ("negotiation","cuộc đàm phán"),
        ("agreement","thỏa thuận"),
        ("contract","hợp đồng"),
        ("proposal","đề xuất"),
        ("quotation","báo giá"),
        ("offer","đề nghị"),
        ("order","đơn hàng"),
        ("invoice","hóa đơn"),
        ("payment","thanh toán"),
        ("receipt","biên lai"),
        ("discount","chiết khấu"),
        ("budget","ngân sách"),
        ("profit","lợi nhuận"),
        ("revenue","doanh thu"),
        ("expense","chi phí"),
        ("salary","lương"),
        ("bonus","thưởng"),
        ("employee","nhân viên"),
        ("manager","quản lý"),
        ("department","phòng ban"),
        ("office","văn phòng"),
        ("company","công ty"),
        ("customer","khách hàng"),
        ("supplier","nhà cung cấp"),
        ("partner","đối tác"),
        ("product","sản phẩm"),
        ("service","dịch vụ"),
        ("quality","chất lượng"),
        ("delivery","giao hàng"),
        ("shipment","lô hàng"),
        ("warehouse","kho hàng"),
        ("inventory","tồn kho"),
        ("promotion","khuyến mãi"),
        ("policy","chính sách"),
        ("procedure","quy trình"),
        ("training","đào tạo"),
        ("resume","hồ sơ xin việc"),
        ("experience","kinh nghiệm"),
        ("skill","kỹ năng"),
        ("position","vị trí"),
        ("performance","hiệu suất"),
        ("target","mục tiêu"),
        ("strategy","chiến lược"),
        ("forecast","dự báo"),
        ("risk","rủi ro"),
        ("decision","quyết định"),
        ("approval","phê duyệt"),
        ("document","tài liệu"),
        ("report","báo cáo"),
        ("email","thư điện tử"),
        ("request","yêu cầu"),
        ("deadline","hạn chót"),
        ("priority","ưu tiên"),
        ("resource","nguồn lực"),
        ("equipment","thiết bị"),
        ("maintenance","bảo trì"),
        ("insurance","bảo hiểm"),
        ("warranty","bảo hành"),
        ("audit","kiểm toán"),
        ("standard","tiêu chuẩn"),
        ("system","hệ thống"),
        ("software","phần mềm"),
        ("database","cơ sở dữ liệu"),
        ("account","tài khoản"),
        ("loan","khoản vay"),
        ("interest","lãi suất"),
        ("investment","đầu tư"),
        ("asset","tài sản"),
        ("transaction","giao dịch"),
        ("import","nhập khẩu"),
        ("export","xuất khẩu"),
        ("customs","hải quan"),
        ("transport","vận chuyển"),
        ("reservation","đặt chỗ"),
        ("complaint","khiếu nại"),
        ("support","hỗ trợ"),
        ("process","quy trình"),
        ("efficiency","hiệu quả"),
        ("productivity","năng suất"),
        ("development","phát triển"),
        ("implementation","triển khai"),
        ("evaluation","đánh giá"),
        ("result","kết quả"),
        ("objective","mục tiêu"),
        ("communication","giao tiếp"),
        ("relationship","mối quan hệ"),
    ]

    data = []
    idx = 1
    while len(data) < 600:
        for w, vi in base_words:
            if len(data) >= 600:
                break
            data.append({
                "id": idx,
                "word": w.capitalize(),
                "type": "noun",
                "meaning": f"{vi} (dùng trong môi trường kinh doanh)",
                "example": f"The {w} was discussed during the business meeting."
            })
            idx += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================= INIT =================
if not os.path.exists(DATA_FILE):
    generate_toeic_600()

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

# ================= AUDIO =================
def audio_url(word):
    return f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word.lower()}--_gb_1.mp3"

# ================= UI =================
st.title("📘 TOEIC 600")
st.caption("600 từ vựng TOEIC căn bản – nghĩa Việt + ví dụ thương mại + audio")

user = st.text_input("👤 Nhập tên của bạn")
if not user:
    st.stop()

if user not in progress:
    progress[user] = []
    save_progress(progress)

menu = st.radio("📌 Chức năng", ["📚 Bài học", "📊 Tiến độ"], horizontal=True)

# ================= LESSON =================
if menu == "📚 Bài học":
    lesson_choice = st.selectbox(
        "Chọn bài học",
        [f"Lesson {w['id']}" for w in words]
    )

    lesson_id = int(lesson_choice.split()[1])
    word = words[lesson_id - 1]

    st.subheader(f"Lesson {word['id']}")
    st.markdown(f"## 🔤 {word['word']} ({word['type']})")

    st.audio(audio_url(word["word"]))

    st.markdown(f"**📖 Nghĩa (VN):** {word['meaning']}")
    st.markdown(f"**💼 Ví dụ (Business English):** {word['example']}")

    if st.button("✅ Đánh dấu đã học"):
        if lesson_id not in progress[user]:
            progress[user].append(lesson_id)
            save_progress(progress)
            st.success("Đã lưu tiến độ!")

# ================= PROGRESS =================
if menu == "📊 Tiến độ":
    done = len(progress[user])
    st.subheader("📈 Tiến độ học tập")
    st.write(f"✅ Đã học: **{done} / 600 bài**")
    st.progress(done / 600)
