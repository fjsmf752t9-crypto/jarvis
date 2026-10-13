import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please ask me something."}), 400

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"answer": "JARVIS needs an API key configured on the server."}), 500

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are JARVIS, a helpful AI assistant. Answer clearly and accurately."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception:
        app.logger.exception("JARVIS AI request failed")
        return jsonify({"answer": "I couldn't reach my AI service. Please try again."}), 502
