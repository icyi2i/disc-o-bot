# Import modules
import requests
import os

# Load custom search engine credentials for API from environment
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")

# Base URL template for search API
SEARCH_URL = "https://www.googleapis.com/customsearch/v1" + \
                "?q={term}&cx={cse_id}&key={key}&num={num}"


# Function for searching terms using google search api
def search_term(term: str = "", count: int = 5):
    """Searches custom search engine for term argument

    Keyword arguments:
        term : Query term to search for in Google CSE
        count : count of items to return (min=1, max=10, default=5)

    Returns:
        List of top n results for the searched term, where n=count.
    """

    # Searches custom search engine for term argument
    top = []
    message = "No items found"

    # Empty search term
    if term.strip() == "":
        message = "Man, I can't search for empty terms now, can I?"

    # Make query via GET API
    res = requests.get(
        url=SEARCH_URL.format(
            term=term,
            cse_id=GOOGLE_CSE_ID,
            key=GOOGLE_SEARCH_API_KEY,
            num=count))

    # Process json response
    try:
        res = res.json()
        for item in res["items"]:
            top.append({
                "title": item["title"],
                "link": item["link"],
                "description": item["snippet"],
            })
        # Check if items are found
        if len(top):
            message = "Search completed!"

    except KeyError:
        # Connection failed due to authentication error in API call
        # No 'items' received in the response
        message = "Search with CSE failed. Check credentials for the same."

    # Return list of top 5 items and the message
    return top, message
