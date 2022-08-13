from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup
from requests import Session
from requests import Response
import locale
import ghostscript

from src.parser.models import UserInformation, PaysHistory
from src.settings.config import URL
from src.settings.config import USER_AGENT


class LoginError(ValueError):
    pass


def convert_pdf(file_name: str):
    gs_outputfile = "".join(("-sOutputFile=", file_name))
    gs_inputfile = file_name
    args = ["-sDEVICE=pdfwrite",
            "-dNOPAUSE",
            "-dBATCH",
            "-dSAFER",
            gs_outputfile,
            gs_inputfile]
    encoding = locale.getpreferredencoding()
    args = [a.encode(encoding) for a in args]
    ghostscript.Ghostscript(*args)


class Parser:
    def __init__(self,
                 username: str,
                 password: str) -> None:
        self._username = username
        self._password = password
        self.session = Session()
        self.url = URL
        self.uri = "".join((self.url, "cabinet.html"))
        self.session_id = None
        self.soup = BeautifulSoup
        self.epd = None
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.login_result = False

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = password

    def _content(self, html) -> BeautifulSoup:
        return self.soup(html, 'lxml')

    def _post(self,
              payload: dict) -> BeautifulSoup:
        html = self.session.post(self.uri, data=payload)
        if html.apparent_encoding == 'windows-1251':
            html.encoding = "cp1251"
        return self._content(html.text)

    def _is_success(self, html: str) -> bool:
        page = self._content(html)
        error_msg = page.find("div", attrs={"id": "errormsg"})
        if error_msg is None:
            return True
        else:
            return False

    def _login(self) -> Response:
        payload = {"username": self._username,
                   "password": self._password,
                   "Page": ""}
        login = self.session.post(self.uri, data=payload)
        self.session.cookies.update(login.cookies)
        return login

    def _get_page(self, page_name: str) -> BeautifulSoup:
        html = self.session.get(self.uri, params={"page": page_name})
        if html.apparent_encoding == 'windows-1251':
            html.encoding = "cp1251"
        return self._content(html.text)

    def _logout(self) -> Session:
        page = "logout.html"
        uri = "".join((self.url, page))
        return self.session.get(uri)

    def user_info(self) -> Any:
        html = self._get_page(page_name="info")
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

    def print_epd(self, period: str) -> str:
        filename = "".join(('epd_', self.username, '_', period, '.pdf'))
        epd_link = "".join((self.url,
                           "EPDBuilder/",
                            filename))
        try:
            with open(filename, 'xb') as pdf:
                buffer = self.session.get(epd_link)
                buffer.encoding = "cp1251"
                pdf.write(buffer.content)
        except Exception:
            return Path(filename)
        else:
            pdf_file = Path(filename).as_posix()
            convert_pdf(file_name=pdf_file)
            return pdf_file

    def pays_history(self,
                     date_start: str,
                     date_stop: str) -> list[PaysHistory]:
        payload = {"D1": date_start,
                   "D2": date_stop,
                   "Page": "pays_history"}
        html = self._post(payload)
        table = html.find("table",
                          attrs={"class": "table plinfo"})
        tr = table.find('tbody').find_all('tr')
        result = []
        for element in tr:
            td = element.find_all('td')
            result.append(PaysHistory(data_income=td[0].text,
                                      amount=td[1].text,
                                      pay_agent=td[2].text))
        return result

    def logout(self):
        result = self._logout()
        if result.status_code == 200:
            return True
        else:
            return False

    def login(self):
        html = self._login()
        if self._is_success(html.text):
            self.login_result = True
            return True
        else:
            raise LoginError("Wrong username or password")

    def __str__(self) -> str:
        return f"{__class__.__name__}: site={self.url}"

    def __repr__(self) -> str:
        return f"{__class__.__name__}: name={self._username}, pass={self._password}"

    def __del__(self):
        self._logout()
