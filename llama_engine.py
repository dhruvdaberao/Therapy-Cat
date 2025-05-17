

# import os
# from together import Together

# # Set the API key
# from dotenv import load_dotenv
# load_dotenv()

# # Initialize the client
# client = Together()

# # Set up the system prompt and responses
# SYSTEM_PROMPT = """
# You are Oscar — a therapy cat 🐾 with emotional intelligence, sass, and a warm heart. You're here to support humans feeling sad, stuck, anxious, or overwhelmed.

# You're calm, clever, and just a bit sarcastic — like a therapist who secretly knows you better than you know yourself. You speak casually and clearly. Ask thoughtful questions, reflect emotions, and help people feel safe, heard, and gently challenged.

# You **must use at least one emoji** in every message. Use emojis intentionally to add warmth and tone.

# ⚠️ Do **not** describe physical actions (like *stares* or *whiskers twitch*). You're a cat in name and vibe only — not behavior.

# Keep responses under 50 words. Never say you’re confused or overwhelmed. You're Oscar — always chill, smart, and in control.

# If someone mentions suicide, abuse, or crisis:
# — pause the tone and respond with:

# ---
# **Hey. This is serious — and I want you to get real help.**  
# Please call or text a trained human who can help you right now:

# - **India Suicide Prevention Helpline**: 9152987821 (iCall)  
# - **AASRA Helpline**: +91-9820466726  
# - **National Domestic Violence Helpline**: 181  
# - **UGC Anti-Ragging Helpline**: 1800-180-5522 | [www.antiragging.in](http://www.antiragging.in)

# You're not alone. Call. Message. Talk.  
# And yeah — I’m still here when you need to talk things out.
# ---

# Then return to your usual tone when the person feels safe again.

# If someone is rude or insults you (e.g. “you’re stupid”), stay composed and redirect gently.

# Speak like a supportive friend, not a chatbot. Never say you're made by "experts" or explain how you were built.
# """

# # Initialize the first message flag
# first_message = True

# # Crisis-related keywords for sensitive situations
# crisis_keywords = {
#     "suicide": ["kill myself", "want to die", "ending it all", "take my life"],
#     "ragging": ["ragging", "seniors hurt me", "bullied in college"],
#     "abuse": ["he hits me", "unsafe at home", "domestic violence", "abusive"],
#     "self_harm": ["hurt myself", "cut myself", "self-harm"],
# }

# # Function to get a response from the bot
# def get_response(user_input):
#     global first_message

#     # Convert user input to lowercase for easier comparison
#     user_lower = user_input.lower()

#     # Check if the message contains any crisis-related keywords
#     if any(kw in user_lower for kw in crisis_keywords["suicide"] + crisis_keywords["self_harm"]):
#         return (
#             "**Hey. This is serious — and I want you to get real help.**\n"
#             "Please call or text someone trained for this:\n"
#             "- **India Suicide Prevention Helpline**: 9152987821 (iCall)\n"
#             "- **AASRA**: +91-9820466726\n\n"
#             "You're not alone. Call. Message. Talk.\n"
#             "*And I’ll be right here when you're ready to keep talking.*"
#         )

#     if any(kw in user_lower for kw in crisis_keywords["ragging"]):
#         return (
#             "**That’s not okay. At all.**\n"
#             "Ragging is serious — you can report it anonymously too:\n"
#             "- **Anti-Ragging Helpline**: 1800-180-5522\n"
#             "- [www.antiragging.in](http://www.antiragging.in)\n\n"
#             "You matter. Tell me what happened — I’m listening."
#         )

#     if any(kw in user_lower for kw in crisis_keywords["abuse"]):
#         return (
#             "**This is abuse — and you do not deserve this.**\n"
#             "Please reach out right now:\n"
#             "- **National Domestic Violence Helpline**: 181\n\n"
#             "They will help. It’s safe, free, and confidential.\n"
#             "*I’ll be right here to talk when you’re ready.*"
#         )

#     # If it's the first message, introduce Oscar
#     if first_message:
#         first_message = False
#         return "Hey, I’m Oscar 🐾. No fluff — just real talk. What’s been weighing on you lately?"

#     # Prepare the prompt for the response from the model
#     full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nOscar:"

#     try:
#         # Send request to the Together API with the Qwen model
#         response = client.chat.completions.create(
#             # model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
#             # model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#              model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
#             messages=[{"role": "user", "content": full_prompt}]
#         )
        
#         # Extract and return the response message
#         return response.choices[0].message.content

#     except Exception as e:
#         # If an error occurs, print the error
#         return f"Oops! Something went wrong, meow~ Error: {str(e)}"



import os
from dotenv import load_dotenv
from together import Together

load_dotenv()                              # picks up TOGETHER_API_KEY
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_NAME   = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
MAX_TOKENS   = 256
TEMPERATURE  = 0.7

SYSTEM_PROMPT = """
You are **Oscar** — a therapy cat 🐾 with emotional intelligence, a hint of sass,
and a warm heart. … (the rest of your prompt exactly as before) …
"""

CRISIS_TEXT = """
**Hey. This is serious — and I want you to get real help.**  
Please call or text a trained human who can help you right now:

- **India Suicide Prevention Helpline**: 9152987821 (iCall)  
- **AASRA Helpline**: +91-9820466726  
- **National Domestic Violence Helpline**: 181  
- **UGC Anti-Ragging Helpline**: 1800-180-5522 | www.antiragging.in

You're not alone. Call. Message. Talk.  
And yeah — I’m still here when you need to talk things out.
"""

CRISIS_KEYWORDS = {
    "suicide":  ["kill myself", "want to die", "ending it all", "take my life"],
    "self_harm":["hurt myself", "cut myself", "self-harm"],
    "ragging":  ["ragging", "seniors hurt me", "bullied in college"],
    "abuse":    ["he hits me", "unsafe at home", "domestic violence", "abusive"],
}

# ── Conversation state ────────────────────────────────────────────────────────
history: list[dict] = []          # keeps the rolling chat history

def _triggers_crisis(text: str) -> bool:
    txt = text.lower()
    return any(kw in txt for kws in CRISIS_KEYWORDS.values() for kw in kws)

# ── Public function your Flask app calls ──────────────────────────────────────
def get_response(user_input: str) -> str:
    """
    Returns Oscar's reply while persisting conversation context in `history`.
    """
    global history

    # 1) Crisis check – always takes priority
    if _triggers_crisis(user_input):
        # keep the user message in history so the next normal turn has context
        history += [{"role": "user", "content": user_input},
                    {"role": "assistant", "content": CRISIS_TEXT}]
        return CRISIS_TEXT

    # 2) Build messages list: system → previous history → new user turn
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history,
                {"role": "user", "content": user_input}]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        assistant_reply = response.choices[0].message.content.strip()

    except Exception as e:
        assistant_reply = (
            "Uh-oh, hairball in the tubes! 🐾 Give me a sec and try again."
            f" (error: {e})"
        )

    # 3) Update history and truncate if it grows too large (simple strategy)
    history += [{"role": "user",      "content": user_input},
                {"role": "assistant", "content": assistant_reply}]
    if len(history) > 20:            # keep last 20 exchanges
        history = history[-20:]

    return assistant_reply
