# 🌾 AgriTwin AI — GEMASTIK 2026

Platform **Digital Twin Pertanian Padi** berbasis AI untuk monitoring real-time, prediksi risiko penyakit, dan estimasi hasil panen.

---

## 🗂️ Struktur Project

```
GEMASTIK-2026/
├── app.py                  # Flask backend utama
├── model.h5                # Model neural network (trained)
├── model.py                # Script training model
├── scaler.pkl              # StandardScaler untuk normalisasi input
├── requirements.txt        # Dependency Python
│
├── static/
│   ├── css/
│   │   ├── global.css      # CSS reset & design tokens
│   │   ├── landing.css     # CSS landing page
│   │   ├── dashboard.css   # CSS dashboard
│   │   └── components/
│   │       ├── sidebar.css
│   │       └── chatbot.css
│   ├── js/
│   │   ├── dashboard.js    # Logika prediksi, chart, map
│   │   └── chatbot.js      # Logika chatbot & voice
│   ├── images/
│   │   └── prengwin-logo.svg
│   ├── icons/
│   └── fonts/
│
├── templates/
│   ├── landing.html        # Halaman utama
│   ├── dashboard.html      # Dashboard AI
│   └── components/
│       ├── sidebar.html    # Komponen sidebar
│       └── footer.html     # Komponen footer
│
├── models/                 # ML modules (future)
├── services/               # Business logic (future)
└── utils/                  # Helper functions (future)
```

---

## 🚀 Cara Menjalankan

### 1. Install Dependency
```bash
pip install -r requirements.txt
```

### 2. Jalankan Server
```bash
python app.py
```

### 3. Buka Browser
```
http://localhost:5000
```

---

## 🤖 Fitur

| Fitur | Deskripsi |
|-------|-----------|
| **AI Prediction** | Prediksi risiko penyakit padi dengan neural network |
| **Digital Twin GIS** | Visualisasi kondisi lahan di peta interaktif |
| **Explainable AI** | Penjelasan alasan prediksi AI |
| **AI Chatbot** | Tanya-jawab kondisi lahan via chat |
| **Voice Assistant** | Input dan output suara Bahasa Indonesia |
| **History Analytics** | Riwayat prediksi dengan chart interaktif |

---

## 📊 Input Sensor

| Parameter | Satuan | Rentang |
|-----------|--------|---------|
| Suhu Udara | °C | 24–36 |
| Kelembapan Udara | % | 60–95 |
| Curah Hujan | mm | 20–200 |
| Intensitas Cahaya | lux | 200–1200 |
| Kecepatan Angin | m/s | 0–15 |
| Soil Moisture | % | 20–90 |
| pH Tanah | - | 4.5–7.5 |
| NPK | - | 1–10 |
| Suhu Tanah | °C | 20–35 |
| Water Level | cm | 0–20 |
| NDVI | - | 0–1 |
| HST | hari | 1–120 |
| Varietas | 0/1/2 | - |

---

## 👥 Tim

**GEMASTIK 2026** — Kategori Kecerdasan Buatan
