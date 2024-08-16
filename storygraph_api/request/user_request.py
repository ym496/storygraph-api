from storygraph_api.exception_handler import request_exception
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class UserScraper:
    @staticmethod
    @request_exception
    def fetch_url(url,cookie):
        options = Options()
        options.add_argument("--headless") 
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        if cookie:
            driver.add_cookie({
                'name': 'remember_user_token',
                'value': cookie,
            })
        driver.refresh()
        SCROLL_PAUSE_TIME = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        html_content = driver.page_source
        driver.quit()
        return html_content

    @staticmethod
    def currently_reading(uname, cookie):
        url = f"https://app.thestorygraph.com/currently-reading/{uname}"
        return UserScraper.fetch_url(url,cookie)

    @staticmethod
    def to_read(uname, cookie):
        url = f"https://app.thestorygraph.com/to-read/{uname}"
        return UserScraper.fetch_url(url,cookie)

    @staticmethod
    def books_read(uname, cookie):
        url = f"https://app.thestorygraph.com/books-read/{uname}"
        return UserScraper.fetch_url(url,cookie)
