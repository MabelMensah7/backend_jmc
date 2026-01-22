const form = document.getElementById("appointmentForm");
const message = document.getElementById("responseMessage");

const API_BASE = "https://backend-jmc-2.onrender.com"; 

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    full_name: document.getElementById("full_name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
    department: document.getElementById("department").value,
    date: document.getElementById("date").value,
    time: document.getElementById("time").value,
    notes: document.getElementById("notes").value || null
  };

  try {
    const response = await fetch(`${API_BASE}/appointments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      message.style.color = "red";
      message.textContent = result.detail || "Something went wrong";
      return;
    }

    message.style.color = "green";
    message.textContent = "Appointment booked successfully! Check your email.";
    form.reset();

  } catch (error) {
    message.style.color = "red";
    message.textContent = "Server error. Please try again later.";
  }
});
