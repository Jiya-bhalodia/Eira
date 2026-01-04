// Chat state
let chatStep = 0;
let userData = {
  age: "",
  skin_type: "",
  concern: "",
  budget: "",
  routine: "",
  allergies: ""
};

const stepKeys = ["age", "skin_type", "concern", "budget", "routine", "allergies"];

const chatQuestions = [
  "😊 Great! First, how old are you?",
  "🧴 What is your skin type? (oily / dry / combination / sensitive)",
  "😣 What's your main skin concern (acne, pigmentation, dullness)?",
  "💰 What's your budget? (low / balanced / premium)",
  "🧼 Can you describe your current skincare routine?",
  "🚫 Do you have any allergies or ingredient sensitivities?"
];

// Scroll to section
function scrollToSection(id) {
  document.getElementById(id).scrollIntoView({ behavior: "smooth" });
}

// Chat logic
async function sendMessage() {
  const input = document.getElementById("userInput");
  const messages = document.getElementById("chatMessages");

  if (!input.value.trim()) return;

  const userText = input.value.trim();
  messages.innerHTML += `<div class="user-msg">${userText}</div>`;
  
  if (chatStep < stepKeys.length) {
    userData[stepKeys[chatStep]] = userText;
  }

  input.value = "";

  try {
    const response = await fetch("http://127.0.0.1:3001/extract", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: userText })
    });

    const extracted = await response.json();

    for (let key of stepKeys) {
      if (extracted[key]) {
        userData[key] = extracted[key];
      }
    }
  } catch (err) {
    console.error("Entity extraction failed:", err);
  }

  const nextEmptyIndex = stepKeys.findIndex(key => userData[key] === "");
  if (nextEmptyIndex !== -1) {
    chatStep = nextEmptyIndex;
  } else {
    chatStep = chatQuestions.length; 
  }

  setTimeout(() => {
    if (chatStep < chatQuestions.length) {
      messages.innerHTML += `<div class="bot-msg">${chatQuestions[chatStep]}</div>`;
    } else {
      messages.innerHTML += generateRoutine();
    }
    messages.scrollTop = messages.scrollHeight;
  }, 600);
}

// Image analysis logic
document.addEventListener("DOMContentLoaded", () => {
  const analyzeButton = document.getElementById("analyzeBtn");
  const imageInput = document.getElementById("imageInput");
  const resultBox = document.getElementById("analysisResult");

  if (!analyzeButton) return;

  analyzeButton.addEventListener("click", async () => {
    if (!imageInput.files.length) {
      alert("Please upload an image first");
      return;
    }

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);
    resultBox.innerHTML = "🔍 Analyzing your skin...";

    try {
      const response = await fetch("http://127.0.0.1:3001/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Server error");

      const data = await response.json();
      
      // Injecting the Tabbed UI back in
      resultBox.innerHTML = `
        <div class="result-card">
          <span class="severity-badge">${data.severity}</span>
          <h3>Skin Analysis Results</h3>

          <div class="condition-chip">${data.conditions[0]}</div>

          <p class="confidence">Confidence Score: ${Math.round(data.confidence * 100)}%</p>

          <h4>Personalized Skincare Plans</h4>

          <div class="budget-tabs">
            <button class="tab active" onclick="switchBudget('low', event)">💚 Low</button>
            <button class="tab" onclick="switchBudget('balanced', event)">💛 Balanced</button>
            <button class="tab" onclick="switchBudget('premium', event)">💜 Premium</button>
          </div>

          <ul id="productList" class="product-list">
            <li>Minimalist Salicylic Acid Cleanser</li>
            <li>Dot & Key Niacinamide Serum</li>
            <li>The Derma Co Sunscreen SPF 50</li>
          </ul>

          <button class="chat-btn" onclick="scrollToSection('chat')">
            💬 Continue in Chat
          </button>
        </div>
      `;
    } catch (err) {
      console.error(err);
      resultBox.innerHTML = "⚠️ Backend not reachable. Make sure Flask is running.";
    }
  });
});

// Budget tab switching
function switchBudget(type, event) {
  const products = {
    low: [
      "Minimalist Salicylic Acid Cleanser",
      "Dot & Key Niacinamide Serum",
      "The Derma Co Sunscreen SPF 50"
    ],
    balanced: [
      "CeraVe Foaming Cleanser",
      "The Ordinary Alpha Arbutin",
      "La Roche-Posay SPF 60"
    ],
    premium: [
      "Skinceuticals Gentle Cleanser",
      "Paula’s Choice BHA",
      "EltaMD UV Clear SPF 46"
    ]
  };

  // Update active tab styling
  document.querySelectorAll(".tab").forEach(btn => btn.classList.remove("active"));
  if (event) {
    event.target.classList.add("active");
  }

  // Update product list
  const list = document.getElementById("productList");
  if (list) {
    list.innerHTML = products[type].map(p => `<li>${p}</li>`).join("");
  }
}

// Routine 
function generateRoutine() {
  const plans = {
    low: { cleanser: "Simple Refreshing Face Wash", moisturizer: "Pond's Super Light Gel", sunscreen: "Aqualogica SPF 50" },
    balanced: { cleanser: "CeraVe Foaming Cleanser", moisturizer: "Cetaphil Moisturising Cream", sunscreen: "La Roche-Posay Anthelios" },
    premium: { cleanser: "Skinceuticals Gentle Cleanser", moisturizer: "Clinique Moisture Surge", sunscreen: "EltaMD UV Clear SPF 46" }
  };

  const budgetKey = (userData.budget || "balanced").toLowerCase();
  const p = plans[budgetKey] || plans.balanced;

  return `
    <div class="bot-msg">
      🌿 Thanks for sharing! Based on your skin, routine & budget, here's what I recommend:
      <br><br>🧼 <b>Cleanser:</b> ${p.cleanser}
      <br>🧴 <b>Moisturizer:</b> ${p.moisturizer}
      <br>☀️ <b>Sunscreen:</b> ${p.sunscreen}
      <br><br>⚠️ I've noted your allergies: <i>${userData.allergies || "None"}</i>
    </div>
  `;
}