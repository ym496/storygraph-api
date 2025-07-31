import os
import json
from dotenv import load_dotenv

from storygraph_api import Book, User

def run_tests():
    print("🚀 Starting StoryGraph API tests...")

    print("\n--- 1. Loading Environment & Initializing Clients ---")
    load_dotenv()

    username = os.getenv("STORYGRAPH_USERNAME")
    session_cookie = os.getenv("_STORYGRAPH_SESSION")
    remember_token = os.getenv("REMEMBER_USER_TOKEN")

    if not all([username, session_cookie, remember_token]):
        print("🛑 Error: Missing one or more required environment variables.")
        print("Please ensure _STORYGRAPH_SESSION, REMEMBER_USER_TOKEN, and STORYGRAPH_USERNAME are in your .env file.")
    else:
        auth_cookies = {
            "_storygraph_session": session_cookie,
            "remember_user_token": remember_token
        }

        book_client = Book()
        user_client = User()
        print("✅ Setup complete.")

        print("\n--- 2. Testing User Client ---")

        user_id = None
        try:
            print("\nFetching User ID for:", username)
            user_id_json = user_client.get_user_id(username)
            user_id_data = json.loads(user_id_json)
            if "user_id" in user_id_data:
                user_id = user_id_data["user_id"]
                print(f"✅ Success! User ID found: {user_id}")
            else:
                print(f"⚠️ Could not extract user_id from response: {user_id_json}")
        except Exception as e:
            print(f"🛑 Error fetching user ID: {e}")

        try:
            print("\nFetching 'Currently Reading' list...")
            currently_reading = user_client.currently_reading(username, auth_cookies)
            print("✅ Success! Result:")
            print(currently_reading)
        except Exception as e:
            print(f"🛑 Error fetching 'Currently Reading' list: {e}")
            
        try:
            print("\nFetching 'To-Read' list...")
            to_read = user_client.to_read(username, auth_cookies)
            print("✅ Success! Result:")
            print(to_read)
        except Exception as e:
            print(f"🛑 Error fetching 'To-Read' list: {e}")
            
        try:
            print("\nFetching 'Read' list...")
            books_read = user_client.books_read(username, auth_cookies)
            print("✅ Success! Result:")
            print(books_read)
        except Exception as e:
            print(f"🛑 Error fetching 'Read' list: {e}")

        try:
            print("\nFetching all journal entries...")
            all_journal_entries = user_client.get_all_journal_entries(auth_cookies)
            all_journal_data = json.loads(all_journal_entries)
            if isinstance(all_journal_data, list):
                print(f"✅ All Journal Entries: {len(all_journal_data)} entries found.")
                print(all_journal_entries)
            else:
                print(f"🛑 Error: All journal entries not returned as a list.")
        except Exception as e:
            print(f"🛑 Error fetching all journal entries: {e}")

        print("\n--- 3. Testing Book Client ---")
        
        finished_book_id = "1c023e31-637b-41d9-ba64-260c3c1b0f3d"
        reading_book_id = "87ca0994-06fb-4360-a0bf-660918a7fbc4"
        unread_book_id = "c89e808f-39db-49f0-98af-6028d98097f9"
        search_query = "Dune Frank Herbert"

        try:
            print(f"\nSearching for '{search_query}'...")
            search_results = book_client.search(search_query)
            print("✅ Success! Result:")
            print(search_results)
        except Exception as e:
            print(f"🛑 Error searching for book: {e}")

        try:
            print(f"\nFetching info for book ID: {finished_book_id}")
            book_info = book_client.book_info(finished_book_id)
            print("✅ Success! Result:")
            print(book_info)
            info = json.loads(book_info)
            cover_url = info.get('cover_url')
            if cover_url and isinstance(cover_url, str) and cover_url.startswith("https://cdn.thestorygraph.com/"):
                print(f"✅ cover_url present and valid: {cover_url}")
            else:
                print(f"🛑 cover_url missing or invalid: {cover_url}")
        except Exception as e:
            print(f"🛑 Error fetching book info: {e}")

        print("\nFetching reading progress for all 3 test cases...")
        try:
            progress_finished = book_client.reading_progress(finished_book_id, auth_cookies)
            print(f"✅ Finished Book Progress: {json.loads(progress_finished).get('progress')}")

            progress_reading = book_client.reading_progress(reading_book_id, auth_cookies)
            print(f"✅ Currently Reading Book Progress: {json.loads(progress_reading).get('progress')}")

            progress_unread = book_client.reading_progress(unread_book_id, auth_cookies)
            print(f"✅ Unread Book Progress: {json.loads(progress_unread).get('progress')}")
        except Exception as e:
            print(f"🛑 Error fetching reading progress: {e}")
            
        print("\nFetching read dates for all 3 test cases...")
        try:
            dates_finished = book_client.get_read_dates(finished_book_id, auth_cookies)
            print(f"✅ Finished Book Dates: {dates_finished}")

            dates_reading = book_client.get_read_dates(reading_book_id, auth_cookies)
            print(f"✅ Currently Reading Book Dates: {dates_reading}")
            
            dates_unread = book_client.get_read_dates(unread_book_id, auth_cookies)
            print(f"✅ Unread Book Dates: {dates_unread}")
        except Exception as e:
            print(f"🛑 Error fetching read dates: {e}")

        print("\nFetching journal entries for a finished book and an unread book...")
        try:
            journal_entries_finished = book_client.get_journal_entries(finished_book_id, auth_cookies)
            journal_data = json.loads(journal_entries_finished)
            if isinstance(journal_data, list):
                print(f"✅ Finished Book Journal Entries: {len(journal_data)} entries found.")
                print(journal_entries_finished)
            else:
                print(f"🛑 Error: Journal entries for finished book not returned as a list.")

            journal_entries_unread = book_client.get_journal_entries(unread_book_id, auth_cookies)
            journal_data_unread = json.loads(journal_entries_unread)
            if isinstance(journal_data_unread, list) and len(journal_data_unread) == 0:
                print(f"✅ Unread Book Journal Entries: Correctly returned an empty list.")
            else:
                print(f"🛑 Error: Journal entries for unread book did not return an empty list.")
        except Exception as e:
            print(f"🛑 Error fetching journal entries: {e}")

        if user_id:
            try:
                print(f"\nFetching AI summary for book ID: {finished_book_id}")
                ai_summary = book_client.get_ai_summary(finished_book_id, user_id)
                print("✅ Success! Result:")
                print(ai_summary)
            except Exception as e:
                print(f"🛑 Error fetching AI summary: {e}")
        else:
            print("\n⚠️ Skipping AI Summary test because user_id could not be retrieved.")

        print("\n🎉 All tests complete!")

if __name__ == "__main__":
    run_tests()
