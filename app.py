from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import joblib
from ai_edge_litert.interpreter import Interpreter
from datetime import datetime
import re
import difflib

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

USERS = {
    "ben": generate_password_hash("ben12345")
}
# =========================
# LOAD MODEL
# =========================
interpreter = Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
scaler = joblib.load("scaler.pkl")

history = []
latest_result = {}



# =========================
# CHATBOT INTENT ENGINE
# =========================

TERM_GLOSSARY = {
    "ndvi": "NDVI (Normalized Difference Vegetation Index) mengukur kehijauan & kesehatan tanaman dari citra. Makin dekat ke 1, tanaman makin sehat.",
    "hst": "HST = Hari Setelah Tanam, menandai umur tanaman padi sejak awal tanam.",
    "npk": "NPK adalah kandungan Nitrogen, Fosfor, Kalium di tanah — tiga unsur hara utama untuk padi.",
    "ph": "pH tanah menunjukkan tingkat keasaman. Padi tumbuh optimal di kisaran pH 5.5–7.",
    "soil moisture": "Soil moisture adalah kadar kelembapan tanah, dipakai untuk menentukan kebutuhan irigasi.",
}

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def keyword_score(msg_norm, keywords):
    score = 0
    words = msg_norm.split()
    for kw in keywords:
        if kw in msg_norm:
            score += 2
        else:
            for w in words:
                if difflib.SequenceMatcher(None, w, kw).ratio() > 0.82:
                    score += 1
                    break
    return score

def need_data(latest_result):
    return not latest_result

def h_greeting(msg, latest_result, hist):
    return "Halo! Saya AgriTwin AI 🌾. Tanya soal: kondisi, risiko, hasil, penyakit, confidence, saran, riwayat, bandingkan, atau istilah (misal 'apa itu NDVI')."

def h_thanks(msg, latest_result, hist):
    return "Sama-sama! Semoga panennya melimpah 🌾"

def h_kondisi(msg, latest_result, hist):
    if need_data(latest_result): return "Silakan lakukan analisis dulu di dashboard."
    return f"{latest_result['status']} — {latest_result['analysis']}"

def h_risiko(msg, latest_result, hist):
    if need_data(latest_result): return "Silakan lakukan analisis dulu di dashboard."
    return f"Tingkat risiko saat ini: {latest_result['risk']}"

def h_hasil(msg, latest_result, hist):
    if need_data(latest_result): return "Silakan lakukan analisis dulu di dashboard."
    return f"Estimasi hasil panen: {latest_result['yield']} ton/ha"

def h_penyakit(msg, latest_result, hist):
    if need_data(latest_result): return "Silakan lakukan analisis dulu di dashboard."
    return f"Deteksi: {latest_result['disease']}"

def h_confidence(msg, latest_result, hist):
    if need_data(latest_result): return "Silakan lakukan analisis dulu di dashboard."
    return f"Tingkat keyakinan model: {latest_result['confidence']}%"

def h_saran(msg, latest_result, hist):
    if need_data(latest_result): return "Silakan lakukan analisis dulu di dashboard."
    return "Rekomendasi: " + ", ".join(latest_result["action"])

def h_riwayat(msg, latest_result, hist):
    if not hist: return "Belum ada riwayat analisis."
    lines = [f"{h['timestamp']}: risiko {h['risk']}, hasil {h['yield']} ton/ha" for h in hist[-3:]]
    return "Riwayat 3 analisis terakhir:\n" + "\n".join(lines)

def h_bandingkan(msg, latest_result, hist):
    if len(hist) < 2: return "Data belum cukup untuk dibandingkan (minimal 2 analisis)."
    now, prev = hist[-1], hist[-2]
    trend = "naik" if now["yield"] > prev["yield"] else ("turun" if now["yield"] < prev["yield"] else "stabil")
    return f"Dibanding sebelumnya, estimasi hasil {trend} (dulu {prev['yield']} ton/ha → sekarang {now['yield']} ton/ha)."

def h_istilah(msg, latest_result, hist):
    for term, exp in TERM_GLOSSARY.items():
        if term in msg:
            return exp
    return "Istilah yang saya kenal: NDVI, HST, NPK, pH, soil moisture. Coba: 'apa itu ndvi?'"

INTENTS = [
    {"keywords": ["halo", "hai", "selamat pagi", "selamat siang"], "handler": h_greeting},
    {"keywords": ["makasih", "terima kasih", "thanks"], "handler": h_thanks},
    {"keywords": ["apa itu", "istilah", "ndvi", "hst", "npk", "arti"], "handler": h_istilah},
    {"keywords": ["bandingkan", "dibanding", "trend"], "handler": h_bandingkan},
    {"keywords": ["riwayat", "history", "kemarin"], "handler": h_riwayat},
    {"keywords": ["kondisi", "keadaan", "status lahan"], "handler": h_kondisi},
    {"keywords": ["risiko", "resiko", "bahaya"], "handler": h_risiko},
    {"keywords": ["hasil", "panen", "produksi"], "handler": h_hasil},
    {"keywords": ["penyakit", "hama", "serangan"], "handler": h_penyakit},
    {"keywords": ["confidence", "yakin", "akurat"], "handler": h_confidence},
    {"keywords": ["saran", "rekomendasi", "harus apa"], "handler": h_saran},
]

FALLBACK_REPLY = ("Maaf, saya belum paham pertanyaan itu. Coba tanya: kondisi, risiko, hasil, "
                   "penyakit, confidence, saran, riwayat, bandingkan, atau istilah (misal 'apa itu NDVI').")

# =========================
# LANDING PAGE
# =========================
@app.route("/")
def home():
    return render_template("landing.html")  

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and check_password_hash(USERS[username], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Username atau password salah.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


# =========================
# PREDICT
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    global latest_result

    data = request.json

    def safe_float(x):
        try:
            return float(x)
        except:
            return 0.0

    features = np.array([[
        safe_float(data["suhu_udara"]),
        safe_float(data["kelembapan_udara"]),
        safe_float(data["curah_hujan"]),
        safe_float(data["cahaya"]),
        safe_float(data["angin"]),

        safe_float(data["soil_moisture"]),
        safe_float(data["ph"]),
        safe_float(data["npk"]),
        safe_float(data["soil_temp"]),
        safe_float(data["water_level"]),

        safe_float(data["ndvi"]),
        safe_float(data["hst"]),
        safe_float(data["varietas"])
    ]])

    scaled = scaler.transform(features).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], scaled)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])

    kelas = int(np.argmax(prediction))
    confidence = round(float(np.max(prediction)) * 100, 2)

    base_yield = 6

    if kelas == 2:
        risk = "TINGGI"
        yield_est = 4
        disease = "Potensi Blas / Hawar Daun"
        status = "KRITIS"
        analysis = "Kondisi lingkungan sangat mendukung penyakit."
        action = ["Kurangi air", "Fungisida", "Monitoring harian"]

    elif kelas == 1:
        risk = "SEDANG"
        yield_est = 5
        disease = "Risiko ringan"
        status = "WASPADA"
        analysis = "Kondisi cukup stabil."
        action = ["Pantau kelembapan", "Pemupukan seimbang"]

    else:
        risk = "RENDAH"
        yield_est = 7
        disease = "Tidak terdeteksi"
        status = "SEHAT"
        analysis = "Kondisi optimal."
        action = ["Pertahankan irigasi"]

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    result = {
        "id": len(history) + 1,
        "risk": risk,
        "yield": yield_est,
        "confidence": confidence,
        "disease": disease,
        "status": status,
        "analysis": analysis,
        "action": action,
        "timestamp": timestamp,
        "kelas": kelas
    }

    latest_result = result
    history.append(result)

    return jsonify(result)

# =========================
# HISTORY
# =========================
@app.route("/history")
def get_history():
    return jsonify(history)

# =========================
# CHATBOT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    raw_msg = request.json.get("message", "")
    msg_norm = normalize(raw_msg)

    best_intent, best_score = None, 0
    for intent in INTENTS:
        score = keyword_score(msg_norm, intent["keywords"])
        if score > best_score:
            best_score, best_intent = score, intent

    if best_intent:
        reply = best_intent["handler"](msg_norm, latest_result, history)
    else:
        reply = FALLBACK_REPLY

    return jsonify({"reply": reply})

# =========================
# STATUS
# =========================
@app.route("/status")
def status():
    return jsonify({
        "system": "AgriTwin AI",
        "version": "2.2",
        "status": "ONLINE",
        "total_predictions": len(history)
    })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)