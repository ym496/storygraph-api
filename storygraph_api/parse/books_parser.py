from storygraph_api.request.books_request import BooksScraper
from storygraph_api.exception_handler import parsing_exception
from bs4 import BeautifulSoup, Tag, NavigableString
import re
from typing import Dict, Any, List
from urllib.parse import parse_qs, urlparse

class BooksParser:
    @staticmethod
    @parsing_exception
    def book_page(book_id: str) -> Dict[str, Any]:
        content = BooksScraper.main(book_id)
        soup = BeautifulSoup(content, 'html.parser')

        h3_tag = soup.find('h3', class_="font-serif font-bold text-2xl md:w-11/12")
        if not isinstance(h3_tag, Tag):
            raise Exception("Could not find the main title header.")

        title = ""
        if h3_tag.contents and isinstance(h3_tag.contents[0], NavigableString):
            title = h3_tag.contents[0].strip()

        authors = []
        for a in h3_tag.find_all('a'):
            if isinstance(a, Tag):
                href = a.get("href")
                if isinstance(href, str) and href.startswith("/authors"):
                    authors.append(a.text)

        p_tag = soup.find('p', class_="text-sm font-light text-darkestGrey dark:text-grey mt-1")
        if not isinstance(p_tag, Tag) or not p_tag.contents:
            raise Exception("Could not find book metadata paragraph.")

        pages_text = p_tag.contents[0]
        pages = pages_text.strip().split()[0] if isinstance(pages_text, NavigableString) else "N/A"

        pub_info_span = p_tag.find('span', string=re.compile(r'first pub'))
        first_pub = pub_info_span.text.split()[-1] if pub_info_span else "N/A"

        tag_div = soup.find('div', class_="book-page-tag-section")
        tags = [tag.text for tag in tag_div.find_all('span')] if isinstance(tag_div, Tag) else []

        cover_url = None
        cover_div = soup.find('div', class_="book-cover")
        if isinstance(cover_div, Tag):
            img_tag = cover_div.find('img')
            if isinstance(img_tag, Tag):
                cover_url = img_tag.get('src')

        description = "Description not found."
        script_tag = soup.find('script', string=re.compile(r"\$\('\.read-more-btn'\)"))
        if isinstance(script_tag, Tag):
            script_content = script_tag.string
            if script_content:
                pattern = re.compile(r"\.html\('(.*)'\)", re.DOTALL)
                match = pattern.search(str(script_content))
                if match:
                    html_str = match.group(1).replace(r'\/', r'/')
                    desc_soup = BeautifulSoup(html_str, 'html.parser')
                    desc_div = desc_soup.find('div', class_='trix-content')
                    if desc_div:
                        description = desc_div.get_text(separator="\n", strip=True)

        review_content = BooksScraper.community_reviews(book_id)
        rev_soup = BeautifulSoup(review_content, 'html.parser')
        avg_rating_span = rev_soup.find('span', class_="average-star-rating")
        avg_rating = avg_rating_span.text.strip() if avg_rating_span else "N/A"

        warnings = BooksParser.content_warnings(book_id)

        data = {
            'title': title, 'authors': authors, 'pages': pages,
            'first_pub': first_pub, 'tags': tags, 'average_rating': avg_rating,
            'description': description, 'warnings': warnings,
            'cover_url': cover_url
        }
        return data

    @staticmethod
    @parsing_exception
    def reading_progress(book_id: str, cookies: Dict[str, str]) -> str:
        content = BooksScraper.book_page_authenticated(book_id, cookies)
        soup = BeautifulSoup(content, 'html.parser')

        status_label = soup.find('button', class_='read-status-label')
        if isinstance(status_label, Tag) and status_label.text.strip() == 'read':
            return "100%"

        progress_bar_div = soup.find('div', class_='progress-bar')
        if isinstance(progress_bar_div, Tag):
            progress_span = progress_bar_div.find('span')
            if isinstance(progress_span, Tag) and progress_span.string:
                return progress_span.string.strip()
            
            inner_div = progress_bar_div.find('div', style=lambda v: 'width: 0%' in v if v else False)
            if inner_div is not None:
                return "0%"
        
        to_read_button = soup.find('button', string=re.compile(r'\s*to read\s*'))
        if isinstance(to_read_button, Tag):
            return "0%"

        raise Exception("Could not determine reading status from the page.")

    @staticmethod
    @parsing_exception
    def get_read_dates(book_id: str, cookies: Dict[str, str]) -> Dict[str, Any]:
        try:
            from storygraph_api.parse.user_parser import UserParser
            from storygraph_api.request.user_request import UserScraper
            
            all_entries = []
            page = 1
            while True:
                content = UserScraper.all_journal_entries(cookies, page)
                entries = UserParser.all_journal_entries(content)
                if not entries:
                    break
                all_entries.extend(entries)
                page += 1
            
            start_date = None
            finish_date = None
            
            for entry in all_entries:
                if entry.get('book_id') == book_id:
                    if entry.get('status') == 'Started reading':
                        date_str = entry.get('date', '')
                        if date_str:
                            try:
                                from datetime import datetime
                                parsed_date = datetime.strptime(date_str, '%d %B %Y')
                                start_date = parsed_date.strftime('%Y-%m-%d')
                            except:
                                pass
                    elif entry.get('status') == 'Finished':
                        date_str = entry.get('date', '')
                        if date_str:
                            try:
                                from datetime import datetime
                                parsed_date = datetime.strptime(date_str, '%d %B %Y')
                                finish_date = parsed_date.strftime('%Y-%m-%d')
                            except:
                                pass
            
            return {'start_date': start_date, 'finish_date': finish_date}
            
        except Exception:
            pass
        
        content = BooksScraper.book_page_authenticated(book_id, cookies)
        soup = BeautifulSoup(content, 'html.parser')
        
        edit_link = soup.find('a', href=re.compile(r'/edit-(read-instance|journal-entry)-from-book'))
        if not (isinstance(edit_link, Tag) and edit_link.get('href')):
            return {'start_date': None, 'finish_date': None}

        href = edit_link['href']
        if not isinstance(href, str):
            raise Exception("Could not find a valid edit link href.")

        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        
        id_val = None
        form_content = b''
        id_type = ''

        if 'read_instance_id' in query_params:
            id_val = query_params.get('read_instance_id', [None])[0]
            id_type = 'read_instance'
            if not id_val:
                raise Exception("Could not extract read_instance_id from edit link.")
            try:
                form_content = BooksScraper.get_read_dates_form(book_id, id_val, cookies)
            except:
                return {'start_date': None, 'finish_date': None}

        elif 'journal_entry_id' in query_params:
            id_val = query_params.get('journal_entry_id', [None])[0]
            id_type = 'journal_entry'
            if not id_val:
                raise Exception("Could not extract journal_entry_id from edit link.")
            try:
                form_content = BooksScraper.get_journal_entry_form(book_id, id_val, cookies)
            except:
                return {'start_date': None, 'finish_date': None}
        
        if not form_content:
            return {'start_date': None, 'finish_date': None}

        form_soup = BeautifulSoup(form_content, 'html.parser')

        def get_date(date_prefix: str) -> str | None:
            day_select = form_soup.find('select', id=f'{id_type}_{date_prefix}day')
            month_select = form_soup.find('select', id=f'{id_type}_{date_prefix}month')
            year_select = form_soup.find('select', id=f'{id_type}_{date_prefix}year')

            if not (isinstance(day_select, Tag) and isinstance(month_select, Tag) and isinstance(year_select, Tag)):
                return None
            
            day_option = day_select.find('option', selected=True)
            month_option = month_select.find('option', selected=True)
            year_option = year_select.find('option', selected=True)

            if isinstance(day_option, Tag) and isinstance(month_option, Tag) and isinstance(year_option, Tag):
                day = day_option.get('value')
                month = month_option.get('value')
                year = year_option.get('value')
                if day and month and year:
                    return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            return None
        
        start_date_prefix = 'started_at_' if id_type == 'journal_entry' else 'start_'
        start_date = get_date(start_date_prefix)
        finish_date = get_date('finished_at_') if id_type == 'journal_entry' else get_date('')
        
        return {'start_date': start_date, 'finish_date': finish_date}

    @staticmethod
    @parsing_exception
    def get_ai_summary(book_id: str, user_id: str) -> Dict[str, str]:
        content = BooksScraper.get_ai_summary(book_id, user_id)
        soup = BeautifulSoup(content, 'html.parser')
        
        template = soup.find('template')
        if isinstance(template, Tag):
            p_tag = template.find('p')
            if isinstance(p_tag, Tag) and p_tag.string:
                return {'summary': p_tag.string.strip()}

        raise Exception("Could not parse AI summary.")

    @staticmethod
    @parsing_exception
    def content_warnings(book_id: str) -> Dict[str, List[str]]:
        warnings_content = BooksScraper.content_warnings(book_id)
        warnings_soup = BeautifulSoup(warnings_content, 'html.parser')

        standard_panes = warnings_soup.find_all('div', class_='standard-pane')
        if len(standard_panes) < 2:
            return {'graphic': [], 'moderate': [], 'minor': []}

        user_warnings_pane = standard_panes[1]
        warnings: Dict[str, List[str]] = {'graphic': [], 'moderate': [], 'minor': []}
        current_list_key = 'graphic'
        tag_re = re.compile(r'^(.*) \((\d+)\)$')

        for tag in user_warnings_pane.children:
            if not isinstance(tag, Tag): continue

            if tag.name == 'p':
                if tag.text == 'Graphic': current_list_key = 'graphic'
                elif tag.text == 'Moderate': current_list_key = 'moderate'
                elif tag.text == 'Minor': current_list_key = 'minor'
            elif tag.name == 'div':
                match = tag_re.match(tag.text)
                if match: warnings[current_list_key].append(match.group(1))
        return warnings

    @staticmethod
    @parsing_exception
    def search(query: str) -> List[Dict[str, str]]:
        content = BooksScraper.search(query)
        soup = BeautifulSoup(content, 'html.parser')
        search_results: List[Dict[str, str]] = []

        books = soup.find_all('div', class_="book-title-author-and-series w-11/12")
        for book in books:
            if not isinstance(book, Tag): continue

            title_tag = book.find('a')
            title = title_tag.text.strip() if isinstance(title_tag, Tag) else "N/A"

            href_val = title_tag.get('href') if isinstance(title_tag, Tag) else None

            href = href_val[0] if isinstance(href_val, list) else href_val
            book_id = href.split('/')[-1] if isinstance(href, str) else "N/A"

            author = "N/A"
            for a_tag in book.find_all('a'):
                if isinstance(a_tag, Tag):
                    href = a_tag.get("href")
                    if isinstance(href, str) and href.startswith('/author'):
                        author = a_tag.text.strip()
                        break

            search_results.append({'title': title, 'author': author, 'book_id': book_id})

        return search_results

    @staticmethod
    @parsing_exception
    def journal_entries(book_id: str, cookies: Dict[str, str]) -> List[Dict[str, Any]]:
        content = BooksScraper.get_journal_page(book_id, cookies)
        soup = BeautifulSoup(content, 'html.parser')
        
        journal_entries: List[Dict[str, Any]] = []
        
        entry_panes = soup.find_all('span', class_="journal-entry-panes")
        if not entry_panes:
            return journal_entries

        for entry in entry_panes[0].find_all(lambda tag: tag.name == 'div' and 'grid-cols-4' in tag.get('class', [])):
            date_tag = entry.find('p', class_="font-semibold")
            date = date_tag.text.strip().split('\n')[0] if date_tag else "N/A"

            progress_percent_tag = entry.find('div', class_="text-teal-500")
            progress_percent = int(progress_percent_tag.text.strip().replace('%', '')) if progress_percent_tag else None

            pages_read_tag = entry.find('p', class_="clear-both")
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
                'date': date,
                'status': status,
                'progress_percent': progress_percent,
                'pages_read_this_session': pages_read_this_session,
                'total_pages_read': total_pages_read,
                'total_pages': total_pages,
                'note': note
            })

        book_total_pages = None
        for entry in journal_entries:
            if entry.get('total_pages') is not None:
                book_total_pages = entry['total_pages']
                break
        
        if book_total_pages is not None:
            for entry in journal_entries:
                if entry.get('total_pages') is None:
                    entry['total_pages'] = book_total_pages

        return journal_entries
