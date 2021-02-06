################################################################
# Import  modules
################################################################

import os
import psycopg2 as db
from datetime import datetime as dt

DB_URI = os.getenv('DATABASE_URL')

################################################################
# Helper functions
################################################################


def drop_table():
    """
    Drops the searches table if it exists.
    """

    with db.connect(DB_URI, sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute(
            "DROP TABLE IF EXISTS searches;")


def create_table():
    """
    Creates the searches table if not created already.
    """

    with db.connect(DB_URI, sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS searches (\
            id SERIAL PRIMARY KEY,\
            timestamp timestamp,\
            term varchar UNIQUE);")


def add_search_entry(term):
    """
    Adds the searched term with current datetime as timestamp.
    In case record exists already, updates timestamp.

    Arguments:
        term: query phrase searched
    """
    with db.connect(DB_URI, sslmode='require') as conn:
        cur = conn.cursor()
        # Check if term is already in db
        cur.execute("SELECT * FROM searches WHERE term = %s;", (term,))
        if len(cur.fetchall()):
            # If exists update timestamp
            cur.execute(
                "UPDATE searches SET timestamp = %s WHERE term = %s;",
                (dt.utcnow(), term))
        else:
            # If not, insert the new record.
            cur.execute(
                "INSERT INTO searches (timestamp, term) VALUES(%s, %s)",
                (dt.utcnow(), term))


def get_recent_searches(term):
    """
    Queries for last 5 searches for the term.

    Arguments:
        term: query phrase to be searched for
    """
    results = []
    term_query = f"%{str(term)}%"
    with db.connect(DB_URI, sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT term FROM searches \
                WHERE term LIKE %s \
                ORDER BY timestamp DESC \
                LIMIT 5;",
            (term_query,))
        results = cur.fetchall()

    return results
