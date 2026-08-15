// ===========================
// CHATBOT JS - AgriTwin AI
// GEMASTIK 2026
// ===========================

// === Fungsi Kirim Pesan Chat ===
async function sendChat() {
  let msg = document.getElementById("chatInput").value.trim();
  if (msg === "") return;

  let box = document.getElementById("chatBox");

  // Tampilkan pesan user dulu
  box.innerHTML += `<p><b style="color:#22c55e">Anda:</b> ${msg}</p>`;
  document.getElementById("chatInput").value = "";
  box.scrollTop = box.scrollHeight;

  try {
    let res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    let r = await res.json();

    // Tampilkan balasan AI
    box.innerHTML += `<p><b style="color:#a78bfa">AgriTwin AI:</b> ${r.reply}</p><hr>`;
    box.scrollTop = box.scrollHeight;

    // Text-to-speech
    if (window.speechSynthesis) {
      let speech = new SpeechSynthesisUtterance(r.reply);
      speech.lang = "id-ID";
      speech.rate = 0.95;
      speechSynthesis.speak(speech);
    }
  } catch (err) {
    box.innerHTML += `<p style="color:#dc2626"><b>Error:</b> Gagal terhubung ke server.</p><hr>`;
    box.scrollTop = box.scrollHeight;
    console.error("Error chat:", err);
  }
}

// === Fungsi Voice Recognition ===
function startVoice() {
  let SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Browser kamu tidak mendukung voice recognition. Coba pakai Chrome.");
    return;
  }

  let recognition = new SpeechRecognition();
  recognition.lang = "id-ID";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.start();

  recognition.onresult = function (event) {
    let text = event.results[0][0].transcript;
    document.getElementById("chatInput").value = text;
    sendChat();
  };

  recognition.onerror = function (event) {
    console.error("Voice error:", event.error);
    alert("Gagal mendengar suara. Pastikan mikrofon aktif.");
  };
}

// === Enter key untuk kirim chat ===
document.addEventListener("DOMContentLoaded", function () {
  let chatInput = document.getElementById("chatInput");
  if (chatInput) {
    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        sendChat();
      }
    });
  }
});
