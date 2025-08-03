# Unofficial StoryGraph API for Python

An unofficial Python wrapper for The StoryGraph API, forked from [ym496/storygraph-api](https://github.com/ym496/storygraph-api).

This fork has been significantly refactored and enhanced to be more efficient, reliable, and feature-rich.

## Key Enhancements in This Fork

* **No More Selenium**: The original dependency on Selenium and a headless browser has been completely removed. This version uses the `requests` library directly for all API communication, resulting in a much lighter, faster, and more stable experience.
* **Expanded API Coverage**: Many new features have been added, including methods to:
  * Fetch your reading progress.
  * Get your read dates for a book.
  * Retrieve all your journal entries or entries for a specific book.
  * Get a book's AI-generated summary.
  * Fetch a user's ID.
* **Modernized Codebase**: The code has been updated with type hints and a more robust project structure.
* **Cookie-Based Authentication**: Authentication is now handled by passing your browser's session cookies, which is a more reliable method than the previous implementation.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

This wrapper requires authentication for most features. You'll need to provide your StoryGraph session cookies and username.

1. **Create a `.env` file** in the root of the project.
2. **Find your cookies**:
   * Open your web browser and log in to [The StoryGraph](https://app.thestorygraph.com/).
   * Open your browser's developer tools (usually by pressing F12).
   * Go to the "Application" (in Chrome) or "Storage" (in Firefox) tab.
   * Under the "Cookies" section for `app.thestorygraph.com`, find the values for `_storygraph_session` and `remember_user_token`.
3. **Add your credentials to the `.env` file**:

   ```dotenv
   _STORYGRAPH_SESSION=your_session_cookie_value
   REMEMBER_USER_TOKEN=your_remember_token_value
   STORYGRAPH_USERNAME=your_storygraph_username
   ```

## Usage

Here's a basic example of how to use the `Book` and `User` clients.

```python
import os
import json
from dotenv import load_dotenv
from storygraph_api import Book, User

# Load environment variables from .env file
load_dotenv()

# --- Authentication ---
username = os.getenv("STORYGRAPH_USERNAME")
session_cookie = os.getenv("_STORYGRAPH_SESSION")
remember_token = os.getenv("REMEMBER_USER_TOKEN")

auth_cookies = {
    "_storygraph_session": session_cookie,
    "remember_user_token": remember_token
}

# --- Initialize Clients ---
book_client = Book()
user_client = User()

# --- User Client Examples ---

# Get user ID
user_id_json = user_client.get_user_id(username)
user_id = json.loads(user_id_json).get("user_id")
print(f"User ID: {user_id}")

# Get 'Currently Reading' list
currently_reading = user_client.currently_reading(username, auth_cookies)
print(currently_reading)

# Get 'To-Read' list
to_read = user_client.to_read(username, auth_cookies)
print(to_read)

# Get 'Read' list
books_read = user_client.books_read(username, auth_cookies)
print(books_read)

# --- Book Client Examples ---

book_id = "1c023e31-637b-41d9-ba64-260c3c1b0f3d" # Example book ID

# Search for a book
search_results = book_client.search("Dune Frank Herbert")
print(search_results)

# Get book info
book_info = book_client.book_info(book_id)
print(book_info)

# Get your reading progress for a book
progress = book_client.reading_progress(book_id, auth_cookies)
print(progress)

# Get your read dates for a book
read_dates = book_client.get_read_dates(book_id, auth_cookies)
print(read_dates)

# Get your journal entries for a book
journal_entries = book_client.get_journal_entries(book_id, auth_cookies)
print(journal_entries)

# Get the AI summary for a book
if user_id:
    ai_summary = book_client.get_ai_summary(book_id, user_id)
    print(ai_summary)
```

## Disclaimer

This is an unofficial wrapper. It is not affiliated with or endorsed by The StoryGraph. Use it at your own risk. The StoryGraph's website structure could change at any time, which might break this wrapper.
