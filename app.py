################################################################
# Import modules
################################################################

import os
import json

from asyncio import get_event_loop
from importlib import import_module

from settings import REGISTERED_BOTS

################################################################
# Create and run tasks in asyncio event loop
################################################################

# Load bot tokens from environment variables
BOT_TOKENS = json.loads(os.getenv("BOT_TOKENS"))

# Get event loop
loop = get_event_loop()

# Loop over registered bots
for bot_name in REGISTERED_BOTS:
    # Import bot from modules dynamically
    bot_module = import_module(f"bots.{bot_name}")
    bot = bot_module.get_bot()
    # Create a parallel task for each bot
    loop.create_task(bot.start(BOT_TOKENS[bot_name]))

# Run event loop forever
loop.run_forever()
