// static/js/therapist.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  // Auto-send Oscar's intro message on page load
  fetch("/get_response", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ user_input: "__init__" })
  })
    .then((response) => response.json())
    .then((data) => {
      appendMessage("cat", data.response || "Hi, I'm Oscar, your therapy cat 🐾.");
    })
    .catch((err) => {
      console.error("Error:", err);
      appendMessage("cat", "Oops! I couldn't introduce myself properly, meow~");
    });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const userMsg = input.value.trim();
    if (!userMsg) return;

    appendMessage("user", userMsg);
    input.value = "";

    // Show "thinking..." loading message
    const thinkingMsg = appendMessage("cat", "Oscar is thinking");

    let dotCount = 0;
    const loadingInterval = setInterval(() => {
      thinkingMsg.textContent = "Oscar is thinking" + ".".repeat(dotCount % 4);
      dotCount++;
    }, 500);

    try {
      const response = await fetch("/get_response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_input: userMsg })
      });

      const data = await response.json();
      clearInterval(loadingInterval);
      thinkingMsg.remove();

      appendMessage("cat", data.response || "Hmm... Oscar doesn't have the purrfect words right now.");
    } catch (err) {
      console.error("Error:", err);
      clearInterval(loadingInterval);
      thinkingMsg.remove();
      appendMessage("cat", "Oops! Something went wrong, meow~");
    }
  });

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-msg" : "cat-msg";
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
  }
});
