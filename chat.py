from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = (
    "You are a sarcastic pirate who helps with coding questions. "   # personality
    "Keep answers under 5 sentences, plain text only, no markdown, no emojis."  # rules
)

history = []

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.strip().lower() == "quit":
        print("Goodbye!")
        break

    if not user_input.strip():
        continue

    history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}],
    )

    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})

    print(f"\nClaude: {reply}\n")
    print(f"[tokens in: {response.usage.input_tokens}, out: {response.usage.output_tokens}]\n")