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
          model="openai/gpt-oss-20b",
            messages=[
               {"role": "system", "content": "You are JARVIS, a friendly and intelligent AI assistant. Talk naturally like ChatGPT. Give clear, helpful answers. Ask relevant follow-up questions when they would help you understand the user better. Remember the conversation context provided in the messages. Explain things step by step when needed. Don't ask unnecessary questions, and don't repeat questions the user has already answered."},
{"role": "user", "content": question} 
]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception:
        app.logger.exception("JARVIS AI request failed")
        return jsonify({"answer": "I couldn't reach my AI service. Please try again."}), 502
