from typing import Any
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from requests.cookies import RequestsCookieJar

from src.parser.models import Cookies, UserInformation
from src.settings.config import BROWSER_DRIVER
from src.settings.config import BROWSER_TIME
from src.settings.config import URL


class Parser:
    def __init__(self,
                 login: str,
                 password: str) -> None:
        self.login = login
        self.password = password
        self.options = ChromeOptions()
        self.options.headless = True
        self.browser = Chrome(executable_path=BROWSER_DRIVER,
                              options=self.options)
        self.browser.implicitly_wait(BROWSER_TIME)
        self.url = URL
        self.session_id = None
        self.soup = BeautifulSoup
        self.epd = None
        self.cookies = Cookies()

    def _content(self, html) -> BeautifulSoup:
        return self.soup(html, 'lxml')

    def _get(self, url, page) -> None:
        uri = "".join((url, page))
        self.browser.get(uri)

    def _login(self) -> Cookies:
        login_xpath = "//input[@type='submit']"
        page = "cabinet.html"
        url = "".join((self.url, page))
        self.browser.get(url)
        self.browser.find_element(by=By.CSS_SELECTOR,
                                  value='[name="username"]').clear()
        self.browser.find_element(by=By.CSS_SELECTOR,
                                  value='[name="username"]').send_keys(self.login)
        self.browser.find_element(by=By.CSS_SELECTOR,
                                  value='[name="password"]').clear()
        self.browser.find_element(by=By.CSS_SELECTOR,
                                  value='[name="password"]').send_keys(self.password)
        self.browser.find_element(by=By.XPATH,
                                  value=login_xpath).click()
        cookies = self.browser.get_cookie('SESSIONID')
        self.cookies.domain = cookies.get('domain')
        self.cookies.http_only = cookies.get('httpOnly')
        self.cookies.name = cookies.get('name')
        self.cookies.path = cookies.get('path')
        self.cookies.secure = cookies.get('secure')
        self.cookies.value = cookies.get('value')

    def _page_info(self) -> BeautifulSoup:
        page = "cabinet.html?page=info"
        self._get(self.url, page)
        return self._content(self.browser.page_source)

    def _page_counters(self):
        page = "cabinet.html?page=counters"
        self._get(self.url, page)

    def _page_printepd(self) -> BeautifulSoup:
        page = "cabinet.html?page=printepd"
        self._get(self.url, page)
        return self._content(self.browser.page_source)

    def _page_pays_history(self):
        page = "cabinet.html?page=pays_history"
        self._get(self.url, page)

    def _page_nach_diagramm(self):
        page = "cabinet.html?page=nach_diagramm"
        self._get(self.url, page)

    def _page_epd_delivery(self):
        page = "cabinet.html?page=epd_delivery"
        self._get(self.url, page)

    def _page_logout(self):
        page = "logout.html"
        self._get(self.url, page)

    def user_info(self) -> Any:
        self._login()
        html = self._page_info()
        table = html.find('table', attrs={"cellpadding": "1"}).find_all('td')
        return UserInformation(subscriber=table[3].text,
                               address=table[5].text,
                               living_space=table[7].text,
                               total_space=table[7].text,
                               form_of_ownership=table[9].text,
                               phone=table[11].text,
                               email=table[13].text,
                               registered_people=table[15].text,
                               unavailable_people=table[17].text,
                               indebtedness=table[19].text)

    def print_epd(self, period: str):
        builder = "".join(("/EPDBuilder/epd_",
                           self.login,
                           "_",
                          period,
                          ".pdf"))
        file_url = "".join((self.url, builder))
        jar = RequestsCookieJar()
        jar.set(name=self.cookies.name,
                value=self.cookies.value,
                domain=self.cookies.domain,
                path=self.cookies.path)
        self.epd = requests.get(file_url, cookies=jar)
        self.epd.content
