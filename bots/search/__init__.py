################################################################
# Import  modules
################################################################

from discord.ext import commands
from .utils import search_term
from .db import create_table, add_search_entry, get_recent_searches

# Confirm that searches table is created in database
create_table()

# Create discord bot
search_bot = commands.Bot(command_prefix="!")


# Function to access bot in module
def get_bot():
    """Common function in all bot modules that returns bot variable"""
    return search_bot

################################################################
# EVENTS
################################################################


# Event triggered on bot connection
@search_bot.event
async def on_ready():
    """Triggered when the bot connects to discord."""

    print("Status : search_bot connected")


# Event triggered when a message is sent to the server
@search_bot.event
async def on_message(message):
    """Captures message event and process message content."""

    # Get channel the message is attached to
    channel = message.channel

    # Flag/variable to check if message needs to be responded
    response = False

    # Replies for specific messages. Eg. Reply 'hi' with 'hey'
    if message.content.lower() == "hi":
        response = "hey"

    # Send a response if the flag is set
    if response:
        await channel.send(response)

    # Continue processing commands in the message content
    await search_bot.process_commands(message)


################################################################
# BOT COMMANDS
################################################################


# Test command to ping
@search_bot.command(
    name="ping",
    help="Simple ping-pong to test if bot responds :) Usage: !ping")
async def ping(ctx):
    await ctx.send("pong!")


# Google command
@search_bot.command(
    name="google",
    help="Search terms with google command. Usage: !google term")
async def google(ctx, *args):

    # Check if search term argument is passed with command
    if not len(args):
        res = "No term provided. Usage : !google term"
    else:
        # Concatenate multiple args with space to search for phrase
        # Eg. (!google hello world) is same as (!google "hello world")
        term = " ".join(args)

        # Search for the term
        results, message = search_term(term)

        if len(results):
            # If results has items
            res = f"Results for {term}"
            for i, item in enumerate(results):
                res += f'\n{i + 1}. **{item["title"]}** :"' + \
                        item["description"] + \
                        f'\n{item["link"]}\n\n'

        else:
            # Reply with message if no items are found
            res = message

        # Add searched term to database
        add_search_entry(term=term)

    # Send to the server
    await ctx.send(res)


# Recent searches command
@search_bot.command(
    name="recent",
    help="Display recently searches containing the term. Usage: !recent term")
async def recent(ctx, *args):

    # Check if search term argument is passed with command
    if not len(args):
        res = "No term provided. Usage : !recent term"
    else:
        # Concatenate multiple args with space to search for phrase
        # Eg. (!recent hello world) is same as (!recent "hello world")
        term = " ".join(args)

        # Get recent searches from the db that match the term
        results = get_recent_searches(term=term)
        if len(results):
            res = f"Recent searches for '{term}' :\n"
            for i, result in enumerate(results):
                res += f"\n{i + 1}. {result[0]}"
        else:
            res = f"No recent searches containing '{term}'"

    # Send to the server
    await ctx.send(res)
