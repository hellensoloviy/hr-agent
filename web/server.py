from flask import Flask, render_template, request, jsonify
from agent.loop import run_agent_turn

_history = []


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/chat", methods=["POST"])
    def chat():
        global _history
        data = request.json
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        response, _history, tools_used = run_agent_turn(user_message, _history)
        return jsonify({"response": response, "tools_used": tools_used})

    @app.route("/reset", methods=["POST"])
    def reset():
        global _history
        _history = []
        return jsonify({"ok": True})

    return app