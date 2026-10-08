import anthropic
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

MODEL = "claude-haiku-4-5-20251001"
SYSTEM_PROMPT = (
    "You are a friendly assistant for a small software company. "
    "Keep answers short, 2 to 4 sentences, in plain text with no markdown."
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

    try:
        print("\nClaude: ", end="", flush=True)

        with client.messages.stream(
            model=MODEL,
            max_tokens=30,
            system=SYSTEM_PROMPT,
            messages=history,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            final = stream.get_final_message()

        reply = final.content[0].text
        history.append({"role": "assistant", "content": reply})

        if final.stop_reason == "max_tokens":
            print("\n[Reply was cut off: it hit the max_tokens limit]")

        print(f"\n[tokens in: {final.usage.input_tokens}, out: {final.usage.output_tokens}]\n")

    except anthropic.AuthenticationError:
        print("\n[Error] Your API key is invalid. Check your .env file.\n")
        history.pop()
        break
    except anthropic.RateLimitError:
        print("\n[Error] Too many requests. Wait a few seconds and try again.\n")
        history.pop()
    except anthropic.APIConnectionError:
        print("\n[Error] Can't reach Anthropic. Check your internet connection.\n")
        history.pop()
    except anthropic.APIStatusError as e:
        print(f"\n[Error] The API returned an error ({e.status_code}): {e.message}\n")
        history.pop()