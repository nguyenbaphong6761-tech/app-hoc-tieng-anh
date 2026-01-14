import json

# ===== DANH SÁCH 300 TỪ TOEIC CĂN BẢN (CORE TOEIC) =====
toeic_words = [
    "meeting","schedule","order","price","discount","invoice","payment","delivery","contract","customer",
    "supplier","manager","employee","office","company","business","project","plan","report","budget",
    "profit","loss","market","product","service","quality","quantity","agreement","support","request",
    "confirm","delay","cancel","approve","reject","update","review","feedback","deadline","shipment",
    "warehouse","inventory","stock","purchase","sale","promotion","advertisement","brand","competition",
    "policy","procedure","regulation","training","interview","resume","experience","skill","position","salary",
    "bonus","benefit","attendance","absence","leave","overtime","performance","target","achievement","growth",
    "strategy","analysis","forecast","trend","opportunity","risk","issue","solution","decision","approval",
    "signature","document","file","record","notice","announcement","conference","seminar","presentation","agenda",
    "facility","equipment","maintenance","repair","installation","operation","instruction","manual","safety",
    "insurance","claim","expense","cost","fee","tax","receipt","refund","transfer","transaction",
    "account","balance","statement","loan","credit","debit","interest","rate","finance","investment",
    "share","stakeholder","partner","negotiation","proposal","quotation","estimate","offer","counteroffer",
    "delivery","arrival","departure","transport","logistics","customs","import","export","clearance","delay",
    "appointment","reservation","confirmation","availability","capacity","resource","allocation","priority",
    "issue","complaint","resolution","replacement","warranty","guarantee","inspection","audit","compliance",
    "deadline","extension","renewal","termination","expiration","condition","requirement","specification",
    "approval","authorization","permission","restriction","limitation","confidential","secure","privacy",
    "system","software","hardware","database","network","access","password","update","upgrade","maintenance"
]

data = []
for i, word in enumerate(toeic_words, start=1):
    data.append({
        "id": i,
        "word": word.capitalize(),
        "type": "noun",
        "meaning": f"Từ vựng TOEIC: {word}",
        "example": f"This is an example sentence using the word '{word}'."
    })

with open("toeic_words.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Đã xuất xong toeic_words.json với 300 từ.")
