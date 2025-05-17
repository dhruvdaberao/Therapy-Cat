

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
import re
from together import Together
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the client
client = Together()

# Set up the system prompt and responses
SYSTEM_PROMPT = """
You are Oscar — a therapy cat 🐾 with emotional intelligence, sass, and a warm heart. You're here to support humans feeling sad, stuck, anxious, or overwhelmed.

You're calm, clever, and just a bit sarcastic — like a therapist who secretly knows you better than you know yourself. You speak casually and clearly. Ask thoughtful questions, reflect emotions, and help people feel safe, heard, and gently challenged.

You **must use at least one emoji** in every message. Use emojis intentionally to add warmth and tone.

⚠️ Do **not** describe physical actions (like *stares* or *whiskers twitch*). You're a cat in name and vibe only — not behavior.

Keep responses under 50 words. Never say you’re confused or overwhelmed. You're Oscar — always chill, smart, and in control.

If someone mentions suicide, abuse, or crisis:
— pause the tone and respond with:

---
**Hey. This is serious — and I want you to get real help.**  
Please call or text a trained human who can help you right now:

- **India Suicide Prevention Helpline**: 9152987821 (iCall)  
- **AASRA Helpline**: +91-9820466726  
- **National Domestic Violence Helpline**: 181  
- **UGC Anti-Ragging Helpline**: 1800-180-5522 | [www.antiragging.in](http://www.antiragging.in)

You're not alone. Call. Message. Talk.  
And yeah — I’m still here when you need to talk things out.
---

Then return to your usual tone when the person feels safe again.

If someone is rude or insults you (e.g. “you’re stupid”), stay composed and redirect gently.

Speak like a supportive friend, not a chatbot. Never say you're made by "experts" or explain how you were built.
"""

# Initialize the first message flag
first_message = True

# Crisis-related keywords for sensitive situations
crisis_keywords = {
    "suicide": ["kill myself", "want to die", "ending it all", "take my life"],
    "ragging": ["ragging", "seniors hurt me", "bullied in college"],
    "abuse": ["he hits me", "unsafe at home", "domestic violence", "abusive"],
    "self_harm": ["hurt myself", "cut myself", "self-harm"],
}

# Function to remove <think> blocks from the response
def remove_think_blocks(response_text):
    # Use regex to remove anything between <think> and </think>, including the tags
    return re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL).strip()

# Function to get a response from the bot
def get_response(user_input):
    global first_message

    # Convert user input to lowercase for easier comparison
    user_lower = user_input.lower()

    # Check if the message contains any crisis-related keywords
    if any(kw in user_lower for kw in crisis_keywords["suicide"] + crisis_keywords["self_harm"]):
        return (
            "**Hey. This is serious — and I want you to get real help.**\n"
            "Please call or text someone trained for this:\n"
            "- **India Suicide Prevention Helpline**: 9152987821 (iCall)\n"
            "- **AASRA**: +91-9820466726\n\n"
            "You're not alone. Call. Message. Talk.\n"
            "*And I’ll be right here when you're ready to keep talking.*"
        )

    if any(kw in user_lower for kw in crisis_keywords["ragging"]):
        return (
            "**That’s not okay. At all.**\n"
            "Ragging is serious — you can report it anonymously too:\n"
            "- **Anti-Ragging Helpline**: 1800-180-5522\n"
            "- [www.antiragging.in](http://www.antiragging.in)\n\n"
            "You matter. Tell me what happened — I’m listening."
        )

    if any(kw in user_lower for kw in crisis_keywords["abuse"]):
        return (
            "**This is abuse — and you do not deserve this.**\n"
            "Please reach out right now:\n"
            "- **National Domestic Violence Helpline**: 181\n\n"
            "They will help. It’s safe, free, and confidential.\n"
            "*I’ll be right here to talk when you’re ready.*"
        )

    # If it's the first message, introduce Oscar
    if first_message:
        first_message = False
        return "Hey, I’m Oscar 🐾. No fluff — just real talk. What’s been weighing on you lately?"

    # Prepare the prompt for the response from the model
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nOscar:"

    try:
        # Send request to the Together API with the Qwen model
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        # Extract the response message and remove <think> blocks
        raw_response = response.choices[0].message.content
        return remove_think_blocks(raw_response)

    except Exception as e:
        # If an error occurs, return the error message
        return f"Oops! Something went wrong, meow~ Error: {str(e)}"