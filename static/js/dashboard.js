// ===========================
// DASHBOARD JS - AgriTwin AI
// GEMASTIK 2026
// ===========================

let historyChart = null;
let confidenceChart = null;
let scoreChart = null;

// === Inisialisasi Map Leaflet ===
let map = L.map("map").setView([-6.2, 106.8], 10);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "OpenStreetMap",
}).addTo(map);
let marker = L.marker([-6.2, 106.8]).addTo(map);

// === Fungsi Prediksi AI ===
async function predict() {
  let data = {};
  document.querySelectorAll("input[id]").forEach((i) => {
    if (i.id !== "chatInput") {
      data[i.id] = i.value;
    }
  });

  try {
    let res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    let r = await res.json();

    // Update KPI Cards
    document.getElementById("riskCard").innerText = r.risk;
    document.getElementById("yieldCard").innerText = r.yield + " t/ha";
    document.getElementById("confidenceCard").innerText = r.confidence + "%";
    document.getElementById("statusCard").innerText = r.status;

    // Update Result Box
    document.getElementById("riskText").innerText = "Risk : " + r.risk;
    document.getElementById("yieldText").innerText = "Yield : " + r.yield + " t/ha";
    document.getElementById("analysisText").innerText = r.analysis;
    document.getElementById("diseaseText").innerText = r.disease;
    document.getElementById("scoreText").innerText = r.ai_score ?? "-";

    // Update Explainable AI
    let reasonHTML = "";
    if (r.reasons && r.reasons.length > 0) {
      r.reasons.forEach((x) => {
        reasonHTML += `<li>${x}</li>`;
      });
    } else {
      reasonHTML = "<li>Tidak ada penjelasan tambahan</li>";
    }
    document.getElementById("reasonList").innerHTML = reasonHTML;

    // Update Map Popup
    marker
      .bindPopup(`<b>${r.risk}</b><br>Yield : ${r.yield} t/ha`)
      .openPopup();

    loadHistory();
  } catch (err) {
    console.error("Error prediksi:", err);
    alert("Gagal melakukan prediksi. Cek koneksi ke server.");
  }
}

// === Fungsi Load History & Charts ===
async function loadHistory() {
  try {
    let res = await fetch("/history");
    let data = await res.json();

    let labels = data.map((x, i) => "T" + (i + 1));

    let riskData = data.map((x) => {
      if (x.risk === "TINGGI") return 3;
      if (x.risk === "SEDANG") return 2;
      return 1;
    });

    let yieldData = data.map((x) => x.yield);
    let confidenceData = data.map((x) => x.confidence);
    let scoreData = data.map((x) => x.ai_score ?? 0);

    // History Chart (Line)
    if (historyChart) historyChart.destroy();
    historyChart = new Chart(document.getElementById("historyChart"), {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Risk Level",
            data: riskData,
            borderColor: "#dc2626",
            backgroundColor: "rgba(220, 38, 38, 0.1)",
            borderWidth: 3,
            tension: 0.4,
          },
          {
            label: "Yield (t/ha)",
            data: yieldData,
            borderColor: "#22c55e",
            backgroundColor: "rgba(34, 197, 94, 0.1)",
            borderWidth: 3,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#94a3b8" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#1f2937" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#1f2937" } },
        },
      },
    });

    // Confidence Chart (Bar)
    if (confidenceChart) confidenceChart.destroy();
    confidenceChart = new Chart(document.getElementById("confidenceChart"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Confidence (%)",
            data: confidenceData,
            backgroundColor: "rgba(34, 197, 94, 0.7)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        plugins: { legend: { labels: { color: "#94a3b8" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#1f2937" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#1f2937" } },
        },
      },
    });

    // AI Score Chart (Line)
    if (scoreChart) scoreChart.destroy();
    scoreChart = new Chart(document.getElementById("scoreChart"), {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "AI Score",
            data: scoreData,
            borderColor: "#a78bfa",
            backgroundColor: "rgba(167, 139, 250, 0.1)",
            borderWidth: 3,
            tension: 0.4,
          },
        ],
      },
      options: {
        plugins: { legend: { labels: { color: "#94a3b8" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#1f2937" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#1f2937" } },
        },
      },
    });

    // Update History Table
    let html = "";
    data
      .slice()
      .reverse()
      .forEach((row) => {
        let badge = "badge-low";
        if (row.risk === "SEDANG") badge = "badge-mid";
        if (row.risk === "TINGGI") badge = "badge-high";
        html += `
<tr>
  <td>${row.timestamp}</td>
  <td><span class="${badge}">${row.risk}</span></td>
  <td>${row.yield} t/ha</td>
  <td>${row.confidence}%</td>
  <td>${row.status}</td>
</tr>`;
      });
    document.getElementById("historyTable").innerHTML = html;
  } catch (err) {
    console.error("Error load history:", err);
  }
}

// === Init ===
loadHistory();
