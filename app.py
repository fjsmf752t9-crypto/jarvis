
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"answer": "Please type a question."}), 400

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return jsonify({"answer": "GROQ_API_KEY is missing in Render."}), 500

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are JARVIS, a helpful AI assistant."},
                {"role": "user", "content": question}
            ],
            timeout=30
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer or "I received an empty response."})

    except Exception:
        app.logger.exception("JARVIS request failed")
        return jsonify({
            "answer": "JARVIS could not connect to its AI service. Check Render logs."
        }), 502

if __name__ == "__main__":
    app.run()
