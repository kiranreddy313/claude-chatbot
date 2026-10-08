import anthropic
from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template, request  # NEW: Response

load_dotenv()
client = Anthropic()
app = Flask(__name__)

MODEL = "claude-haiku-4-5-20251001"
SYSTEM_PROMPT = (
    "You are a friendly assistant for a small software company. "
    "Keep answers short, 2 to 4 sentences, in plain text with no markdown."
)
ERROR_MARKER = "[[ERROR]]"  # NEW


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


# NEW: the streaming version
@app.route("/api/chat/stream", methods=["POST"])
def chat_stream():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided."}), 400

    def generate():
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except anthropic.AuthenticationError:
            yield ERROR_MARKER + "The server's API key is invalid."
        except anthropic.APIConnectionError:
            yield ERROR_MARKER + "The server can't reach Anthropic."
        except anthropic.APIStatusError as e:
            yield ERROR_MARKER + f"Claude API error ({e.status_code})."

    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)