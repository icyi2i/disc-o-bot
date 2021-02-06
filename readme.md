# disc-o-bot

A collection of open source discord bots built with python.

## Getting started

1. Clone [Github Repository](https://github.com/icyi2i/disc-o-bot)

2. Export the following environment variables.
   1. BOT_TOKENS = '{"search": "discord_bot_token"}'
   2. GOOGLE_SEARCH_API_KEY = api_key
   3. GOOGLE_CSE_ID = google_cse_id
   4. DATABASE_URL = Postgresql database URL

3. Install dependencies

    ```pip install -r requirements.txt```

4. Run the `app.py` file

    ```python app.py```

## Bots

Currently the following bots are added.

1. Search bot

More bots can be configured by adding package name to `REGISTERED_BOTS` variable in `settings.py` file

### Search bot

#### **Purpose**

Learning building a discord bot with python

#### **Features and commands**

- Replies "hey" to your "hi"

- Allows to search a term/phrase on google (top links) through discord. Usage:

    `!google nodejs`

- Allows to search for recent queries through the search history. Usage:

    `!recent game`

- Persistent search history using a postgresql database
