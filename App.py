# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from chatterbot import ChatBot
import os

app = Flask(__name__)

bessie = ChatBot(
    "Bessie",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "logic_adapters.crafterdocs_search_logic_adapter.CrafterDocsSearchLogicAdapter",
        "logic_adapters.crafterdocs_what_is_logic_adapter.CrafterWhatIsSearchLogicAdapter",
        "chatterbot.logic.BestMatch"
    ],
    database="./data/database.db",
    aws = os.environ["AWS_HOST"] if "AWS_HOST" in os.environ else None
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(bessie.get_response(user_text))


if __name__ == "__main__":
    app.run()
