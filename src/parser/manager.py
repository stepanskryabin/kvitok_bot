from typing import Any
from bs4 import BeautifulSoup
from requests import Session

from src.parser.models import Cookies, UserInformation
from src.settings.config import URL
from src.settings.config import USER_AGENT


class Parser:
    def __init__(self,
                 login: str,
                 password: str) -> None:
        self.login = login
        self.password = password
        self.session = Session()
        self.url = URL
        self.uri = "".join((self.url, "cabinet.html"))
        self.session_id = None
        self.soup = BeautifulSoup
        self.epd = None
        self.cookies = None
        self.session.headers.update({"User-Agent": USER_AGENT})
        self._login()

    def _content(self, html) -> BeautifulSoup:
        return self.soup(html, 'lxml')

    def _post(self,
              payload: dict,
              page: str | None = None) -> Session:
        if page is None:
            return self.session.post(self.url, data=payload)
        else:
            return self.session.post(self.url,
                                     params={"page": page},
                                     data=payload)

    def _login(self) -> Cookies:
        auth = {"username": self.login,
                "password": self.password}
        login = self.session.post(self.uri, data=auth)
        self.cookies = login.cookies
        self.login_result = login.status_code

    def _page_info(self) -> BeautifulSoup:
        page = "info"
        result = self.session.get(self.uri, params={"page": page})
        if result.apparent_encoding == 'windows-1251':
            result.encoding = "cp1251"
        return self._content(result.text)

    def _page_counters(self) -> BeautifulSoup:
        page = "counters"
        result = self._get(self.url, page)
        return self._content(result.text)

    def _page_printepd(self) -> BeautifulSoup:
        page = "printepd"
        self._get(self.url, page)
        return self._content(self.browser.page_source)

    def _page_pays_history(self):
        page = "pays_history"
        self._get(self.url, page)

    def _page_nach_diagramm(self):
        page = "nach_diagramm"
        self._get(self.url, page)

    def _page_epd_delivery(self):
        page = "epd_delivery"
        self._get(self.url, page)

    def _page_logout(self):
        page = "logout.html"
        self._get(self.url, page)

    def user_info(self) -> Any:
        if self.login_result != '200':
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
        self.epd = self.session.get(file_url, cookies=self.cookies)
