const form = document.getElementById("contactForm");
const message = document.getElementById("responseMessage");

const API_BASE = "http://127.0.0.1:8000";

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    full_name: document.getElementById("full_name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
    message: document.getElementById("message").value
  };

  try {
    const response = await fetch(`${API_BASE}/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      message.style.color = "red";
      message.textContent = "Failed to send message.";
      return;
    }

    message.style.color = "green";
    message.textContent = "Message sent successfully!";
    form.reset();

  } catch (error) {
    message.style.color = "red";
    message.textContent = "Server error. Please try again later.";
  }
});
