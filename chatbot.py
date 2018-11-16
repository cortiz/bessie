# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import os
# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    "Bessie",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
         "logic_adapters.crafterdocs_search_logic_adapter.CrafterDocsSearchLogicAdapter",
         "logic_adapters.crafterdocs_what_is_logic_adapter.CrafterWhatIsSearchLogicAdapter",
         "chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    database="./database.db",
    aws=os.environ["AWS_HOST"]
)

print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
