from storygraph_api.request.user_request import UserScraper
from storygraph_api.exception_handler import parsing_exception
from bs4 import BeautifulSoup, Tag
from typing import Dict
import re

class UserParser:
    @staticmethod
    @parsing_exception
    def get_user_id(username: str) -> Dict[str, str]:
        content = UserScraper.get_profile_page(username)
        soup = BeautifulSoup(content, 'html.parser')
        profile_pane = soup.find('div', id='profile-heading-pane')
        if isinstance(profile_pane, Tag):
            user_id = profile_pane.get('data-user-id')
            if user_id and isinstance(user_id, str):
                return {'user_id': user_id}
        raise Exception(f"Could not find user_id for username '{username}'.")

    @staticmethod
    @parsing_exception
    def parse_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        books_list = []
        books = soup.find_all('div', class_="book-title-author-and-series")
        for book in books:
            title = book.find('a').text.strip()
            book_id = book.find('a')['href'].split('/')[-1]
            books_list.append({
                'title': title,
                'book_id': book_id
                })
        data = list({(book['title'], book['book_id']): book for book in books_list}.values())
        return data

    @staticmethod
    def currently_reading(uname, cookie):
        content = UserScraper.currently_reading(uname, cookie)
        return UserParser.parse_html(content)

    @staticmethod
    def to_read(uname, cookie):
        content = UserScraper.to_read(uname, cookie)
        return UserParser.parse_html(content)

    @staticmethod
    def books_read(uname, cookie):
        content = UserScraper.books_read(uname, cookie)
        return UserParser.parse_html(content)

    @staticmethod
    @parsing_exception
    def all_journal_entries(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        journal_entries = []
        
        for entry in soup.find_all('div', class_="mb-7"):
            try:
                book_title_tag = entry.find('p', class_="font-semibold text-sm md:text-base font-semibold").find('a')
                book_title = book_title_tag.text.strip() if book_title_tag else "N/A"
                
                book_id = book_title_tag['href'].split('/')[-1] if book_title_tag else "N/A"
                
                date_tag = entry.find('p', class_="font-semibold text-xs md:text-sm")
                date = date_tag.text.strip().split('\n')[0] if date_tag else "N/A"

                progress_percent_tag = entry.find('div', class_="text-teal-500")
                progress_percent = int(progress_percent_tag.text.strip().replace('%', '')) if progress_percent_tag else None

                pages_read_tag = entry.find('p', class_=re.compile(r'clear-both.*'))
                pages_read_this_session = None
                total_pages_read = None
                total_pages = None
                
                if pages_read_tag:
                    pages_text = pages_read_tag.text
                    session_match = re.search(r'(\d+) pages read', pages_text)
                    if session_match:
                        pages_read_this_session = int(session_match.group(1))
                    
                    total_match = re.search(r'\((\d+) pages out of (\d+)\)', pages_text)
                    if total_match:
                        total_pages_read = int(total_match.group(1))
                        total_pages = int(total_match.group(2))
                
                note_tag = entry.find('div', class_="trix-content")
                note = note_tag.text.strip() if note_tag else None
                
                status_tag = entry.find('span', class_=lambda x: x and 'inline-flex' in x)
                status = status_tag.text.strip() if status_tag else None
                
                if status == "Started reading":
                    if progress_percent is None:
                        progress_percent = 0
                    if pages_read_this_session is None:
                        pages_read_this_session = 0
                    if total_pages_read is None:
                        total_pages_read = 0
                elif status == "Finished":
                    if progress_percent is None:
                        progress_percent = 100
                
                journal_entries.append({
                    'book_title': book_title,
                    'book_id': book_id,
                    'date': date,
                    'status': status,
                    'progress_percent': progress_percent,
                    'pages_read_this_session': pages_read_this_session,
                    'total_pages_read': total_pages_read,
                    'total_pages': total_pages,
                    'note': note
                })
            except Exception:
                continue
        
        book_total_pages = {}
        
        for entry in journal_entries:
            book_id = entry.get('book_id')
            if book_id and entry.get('total_pages') is not None:
                book_total_pages[book_id] = entry['total_pages']
        
        for entry in journal_entries:
            book_id = entry.get('book_id')
            if book_id and entry.get('total_pages') is None and book_id in book_total_pages:
                entry['total_pages'] = book_total_pages[book_id]
            
        return journal_entries
