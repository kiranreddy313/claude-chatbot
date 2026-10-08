import anthropic
from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

load_dotenv()
client = Anthropic()
app = Flask(__name__)

MODEL = "claude-haiku-4-5-20251001"
SYSTEM_PROMPT = (
    "You are a friendly assistant for a small software company. "
    "Keep answers short, 2 to 4 sentences, in plain text with no markdown."
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided."}), 400


    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return jsonify({
            "reply": response.content[0].text,
            "usage": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
            },
        })
    except anthropic.AuthenticationError:
        return jsonify({"error": "The server's API key is invalid."}), 500
    except anthropic.APIConnectionError:
        return jsonify({"error": "The server can't reach Anthropic."}), 503
    except anthropic.APIStatusError as e:
        return jsonify({"error": f"Claude API error ({e.status_code})."}), 502


if __name__ == "__main__":
    app.run(debug=True)