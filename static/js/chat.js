



document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const optionsContainer = document.getElementById("options");
  const userAnswers = []; // store user choices

  let userName = "";
  let currentQuestionIndex = 0;
  let askingName = true;

  const questions = [
    { text: "How are you feeling today?", options: ["Happy", "Sad", "Anxious", "Neutral"] },
    { text: "On a scale of 1–10, how would you rate your current stress level?", options: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] },
    { text: "How are you sleeping lately?", options: ["Very well", "Okay", "Poorly"] },
    { text: "Are you eating healthy meals regularly?", options: ["Yes", "Sometimes", "No"] },
    { text: "How often do you exercise?", options: ["Daily", "Few times", "Rarely"] },
    { text: "Do you have someone to talk to?", options: ["Yes", "Sometimes", "No"] },
    { text: "Are you satisfied with your daily routine?", options: ["Very satisfied", "Neutral", "Not satisfied"] },
    { text: "What’s one thing that made you happy recently?", options: ["Family/Friends", "Achievement", "Nature/Relaxing"] },
    { text: "How often do you relax or enjoy hobbies?", options: ["Daily", "Sometimes", "Rarely"] },
    { text: "Are you feeling overwhelmed at work/school?", options: ["Yes", "Sometimes", "No"] },
    { text: "On a scale of 1–10, how connected do you feel with people?", options: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] },
    { text: "Do you take care of yourself emotionally?", options: ["Yes", "Trying", "No"] },
    { text: "How motivated are you lately?", options: ["Highly motivated", "Somewhat", "Not motivated"] },
    { text: "Are you happy with your lifestyle?", options: ["Yes", "Somewhat", "No"] },
    { text: "Would you like to set a goal for this week?", options: ["Yes", "Maybe", "No"] }
  ];

  const responses = {
    "Start": [
      "Purrfect! Let's begin 🐾",
      "Let's embark on a cozy chat 🛋️",
      "Ready to explore your feelings together 🐱",
      "Your therapy cat is ready! 🐾",
      "Let's make today brighter! 🌞"
    ],
    "Happy": [
      "That's wonderful, {name}! 😸",
      "Yay {name}! Keep smiling! 🎉",
      "So glad you're feeling happy, {name}! 🌈",
      "Your happiness is contagious, {name}! 😻",
      "Stay golden, {name}! ✨"
    ],
    "Sad": [
      "It's okay to feel sad sometimes, {name}. 🤗",
      "I'm here for you, {name}. 🐾",
      "You're not alone, {name}. 🫂",
      "Sending you warm purrs, {name}. 🐱",
      "We'll get through this together, {name}. 🌈"
    ],
    "Anxious": [
      "Take a deep breath, {name}. You're stronger than you think. 🧘",
      "Let's calm those jitters together, {name}. 🐾",
      "Anxiety passes like clouds, {name}. ☁️",
      "You are safe, {name}. 🌟",
      "One paw at a time, {name}. 🐾"
    ],
    "Neutral": [
      "Thanks for sharing, {name}! 🌟",
      "Even small emotions matter, {name}. 💖",
      "It's good to check in, {name}. 🛋️",
      "A balanced mood is powerful, {name}. ⚖️",
      "Not every day needs fireworks, {name}. 🎇"
    ],
    "1-3": [
      "You seem calm and composed, {name}! 🌊",
      "Low stress is a great sign, {name}! 🐾",
      "You're riding the peaceful waves, {name}. 🏄",
      "A serene mind is a treasure, {name}. 💎",
      "Stay steady, {name}! 🌟"
    ],
    "4-6": [
      "You're managing stress pretty well, {name}! 💪",
      "Moderate stress is normal, {name}! 🌱",
      "You're doing your best, {name}. Keep going! 🌟",
      "You're navigating life like a pro, {name}. 🧭",
      "Keep breathing and moving, {name}. 🐾"
    ],
    "7-10": [
      "It sounds overwhelming, {name}, but you're strong! 🐾",
      "Big hugs, {name}! You’re not alone. 🤗",
      "It’s brave to admit when things are heavy, {name}. 🛋️",
      "Let's take it one step at a time, {name}. 🐾",
      "You are more resilient than you realize, {name}. 🌟"
    ],
    "Very well": [
      "Excellent, {name}! Good sleep powers everything! 😴",
      "You must feel so refreshed, {name}! 🌸",
      "Your dreams must be magical, {name}. 🌠",
      "Keep cherishing your rest, {name}. 🛌",
      "A well-rested {name} is unstoppable! 🚀"
    ],
    "Okay": [
      "Not bad, {name}! Sleep can always improve 🛏️",
      "You're holding steady, {name}. 🌟",
      "A little more snooze time can work wonders, {name}. 💤",
      "Step by step, better sleep will come, {name}. 🌙",
      "Thanks for being honest, {name}. 🐾"
    ],
    "Poorly": [
      "Rest matters, {name}. Let’s work on better sleep 💭",
      "Your dreams deserve more room, {name}. 🌠",
      "We can build better rest habits together, {name}. 🌟",
      "You deserve sweet dreams, {name}. 💤",
      "Let's tuck worries away, {name}. 🛏️"
    ],
    "Yes": [
      "Awesome, {name}! Keep nurturing yourself! 🥗",
      "Self-care is your superpower, {name}! 🌟",
      "Proud of you, {name}! 🐾",
      "You're showing up for yourself, {name}. 💖",
      "Go, {name}! You're glowing! ✨"
    ],
    "Sometimes": [
      "Every effort counts, {name}! 🌱",
      "You're doing better than you think, {name}. 🌟",
      "Small wins build big success, {name}. 🐾",
      "Keep watering your garden, {name}. 🌻",
      "Progress is progress, {name}. 🎯"
    ],
    "No": [
      "No worries, {name}. Small steps make big changes 🍴",
      "There's always time to start, {name}. 🌟",
      "You deserve love and care, {name}. 💖",
      "Let's take tiny steps together, {name}. 🐾",
      "Your well-being matters, {name}. 🌼"
    ],
    "Daily": [
      "Wow, fitness champ {name}! 🏃‍♂️",
      "Your energy is inspiring, {name}! ✨",
      "Way to go staying active, {name}! 💪",
      "You’re a movement master, {name}! 🐾",
      "Keep running toward greatness, {name}! 🛤️"
    ],
    "Few times": [
      "Good job staying active, {name}! 🏋️",
      "Every move matters, {name}. 🌟",
      "You’re keeping the spark alive, {name}! 🔥",
      "Way to make time for yourself, {name}! 🧘",
      "Balance is beautiful, {name}. ⚖️"
    ],
    "Rarely": [
      "Every step matters, {name}! 🐾",
      "Starting small leads to big changes, {name}. 🌱",
      "You're not alone, {name}. We all start somewhere. 🌟",
      "Tiny steps are still steps forward, {name}. 🚶",
      "Believe in your momentum, {name}. 🛤️"
    ],
    "Family/Friends": [
      "Precious bonds make life sweeter, {name}! 💖",
      "Loved ones are pure treasures, {name}. 🎁",
      "Connection is healing, {name}. 🫂",
      "Family and friends fuel your spirit, {name}. 🔥",
      "Cherish those lovely moments, {name}. 🌸"
    ],
    "Achievement": [
      "Celebrate yourself, {name}! 🎉",
      "Your wins are worth cheering for, {name}! 🏆",
      "You did it, {name}! 👏",
      "Achievement unlocked, {name}! 🛡️",
      "You’re a star, {name}! 🌟"
    ],
    "Nature/Relaxing": [
      "Nature heals beautifully, {name}! 🌳",
      "Relaxation recharges the soul, {name}. 🧘",
      "Breathe in the calm, {name}. 🍃",
      "The outdoors love you back, {name}. 🏞️",
      "Rest and nature are powerful together, {name}. 🌻"
    ],
    "Trying": [
      "Progress over perfection, {name}! 🌱",
      "Trying is winning, {name}. 🏆",
      "Every effort is powerful, {name}. 💪",
      "Small steps, big heart, {name}. 🐾",
      "I'm proud of your effort, {name}. 🌟"
    ],
    "Highly motivated": [
      "You're unstoppable, {name}! 🚀",
      "Energy like yours moves mountains, {name}! 🏔️",
      "Nothing can slow you down, {name}! 🐾",
      "Your fire is inspiring, {name}! 🔥",
      "Chase those dreams, {name}! 🌈"
    ],
    "Somewhat": [
      "Small sparks make big fires, {name}! 🔥",
      "You're on your way, {name}! 🛤️",
      "Tiny actions are huge wins, {name}. 🐾",
      "Keep the momentum alive, {name}! ✨",
      "Progress is made one step at a time, {name}. 🚶"
    ],
    "Not motivated": [
      "It's okay to pause, {name}! 🌙",
      "Rest is part of the journey, {name}. 🐾",
      "You deserve kindness, {name}. 💖",
      "We'll find your spark again, {name}. ✨",
      "Be gentle with yourself, {name}. 🌸"
    ],
    "Maybe": [
      "Even considering it is progress, {name}! 🛤️",
      "Tiny hopes lead to big dreams, {name}. 🌈",
      "Maybe today, yes tomorrow, {name}. ✨",
      "You're opening a new door, {name}. 🚪",
      "Possibilities await you, {name}. 🌟"
    ]
  };

  function addMessage(content, isUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;
    messageDiv.innerHTML = `<p>${content}</p>`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function getRandomResponse(key) {
    const responseList = responses[key];
    if (responseList) {
      const randomIndex = Math.floor(Math.random() * responseList.length);
      return responseList[randomIndex].replace("{name}", userName || "friend");
    }
    return "Thanks for sharing! 🌟";
  }

  function addOptions(options) {
    optionsContainer.classList.remove("animate");
    void optionsContainer.offsetWidth; // Force reflow for animation
    optionsContainer.classList.add("animate");
    optionsContainer.innerHTML = '';
    options.forEach(option => {
      const button = document.createElement("button");
      button.className = "option-button";
      button.innerText = option;
      button.onclick = () => handleOptionSelect(option);
      optionsContainer.appendChild(button);
    });
  }

  function handleNameInput(name) {
    addMessage(name, true);
    userName = name.trim() || "friend";
    askingName = false;
    setTimeout(() => {
      addMessage(`Nice to meet you, ${userName}! 🐱`);
      setTimeout(askQuestion, 800);
    }, 400);
  }

  function handleOptionSelect(option) {
    addMessage(option, true);
    userAnswers.push(option);
    let botResponse = "";

    if (["1", "2", "3"].includes(option)) botResponse = getRandomResponse("1-3");
    else if (["4", "5", "6"].includes(option)) botResponse = getRandomResponse("4-6");
    else if (["7", "8", "9", "10"].includes(option)) botResponse = getRandomResponse("7-10");
    else botResponse = getRandomResponse(option);

    setTimeout(() => {
      addMessage(botResponse);
      currentQuestionIndex++;
      if (currentQuestionIndex < questions.length) {
        setTimeout(askQuestion, 800);
      } else {
        setTimeout(showFinalButton, 800);
      }
    }, 400);
  }

  function askQuestion() {
    const question = questions[currentQuestionIndex];
    addMessage(question.text);
    addOptions(question.options);
  }

  // function showFinalButton() {
  //   addMessage(`You're doing amazing, ${userName}! 🎉 Let's analyze your journey!`);
  //   optionsContainer.innerHTML = '';
  //   const finalButton = document.createElement("button");
  //   finalButton.className = "option-button";
  //   finalButton.innerText = "Analyze My Results";
  //   finalButton.onclick = () => alert("Analysis will be ready soon 🚀");
  //   optionsContainer.appendChild(finalButton);
  // }

  function showFinalButton() {
    addMessage(`You're doing amazing, ${userName}! 🎉 Let's analyze your journey!`);
    optionsContainer.innerHTML = '';
  
    const finalButton = document.createElement("button");
    finalButton.className = "option-button";
    finalButton.innerText = "Analyze My Results";
  
    finalButton.onclick = () => {
      const inputData = {};
  
      // Map answers to model input field names
      const fieldNames = [
        "feeling_today",
        "stress_level",
        "sleep_quality",
        "eating_healthy",
        "exercise_frequency",
        "social_support",
        "routine_satisfaction",
        "recent_happiness",
        "relaxation_frequency",
        "overwhelmed",
        "social_connection",
        "emotional_selfcare",
        "motivation",
        "lifestyle_happiness",
        "goal_setting"
      ];
  
      for (let i = 0; i < fieldNames.length; i++) {
        inputData[fieldNames[i]] = userAnswers[i];
      }
  
      // Send data to Flask via POST
      fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(inputData)
      })
      .then(response => response.json())
      .then(data => {
        // Redirect to results page with query params (or use session storage)
        localStorage.setItem("resultData", JSON.stringify(data));
        window.location.href = "/result";
      })
      .catch(error => {
        console.error("Prediction failed:", error);
      });
    };
  
    optionsContainer.appendChild(finalButton);
  }
  

  function startConversation() {
    addMessage("Hey! I'm Oscar your Therapy Cat 🐱, answer my basic questions to help me analyze your mental health. By the way what should I call you?");
    optionsContainer.innerHTML = '';

    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Enter your name";
    input.className = "name-input";
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && input.value.trim() !== "") {
        handleNameInput(input.value.trim());
      }
    });
    optionsContainer.appendChild(input);
    input.focus();
  }

  startConversation();
});
