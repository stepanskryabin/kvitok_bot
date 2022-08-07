from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from requests.cookies import RequestsCookieJar

from src.parser.models import Cookies, UserInformation
from src.settings.config import LOGIN
from src.settings.config import PASSWORD
from src.settings.config import BROWSER_DRIVER
from src.settings.config import BROWSER_TIME
from src.settings.config import URL


def manager() -> str | bool:
    options = ChromeOptions()
    options.headless = False
    browser = Chrome(executable_path="./chromedriver",
                     options=options)
    browser.implicitly_wait(10)
    browser.get("https://lk.xn--b1ajducdqh2g.xn--p1ai/cabinet.html")
    browser.find_element(by=By.ID, value="lic").clear()
    browser.find_element(by=By.ID, value="lic").send_keys(LOGIN)
    browser.find_element(by=By.ID, value="password").clear()
    browser.find_element(by=By.ID, value="password").send_keys(PASSWORD)
    browser.find_element(by=By.XPATH,
                         value="//input[@type='submit']").click()
    cookies = browser.get_cookie('SESSIONID')
    if cookies is not None:
        return cookies["value"]
    else:
        return False


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

        self.browser.find_element(by=By.ID,
                                  value="lic").clear()
        self.browser.find_element(by=By.ID,
                                  value="lic").send_keys(self.login)
        self.browser.find_element(by=By.ID,
                                  value="password").clear()
        self.browser.find_element(by=By.ID,
                                  value="password").send_keys(self.password)
        self.browser.find_element(by=By.XPATH,
                                  value=login_xpath).click()
        cookies = self.browser.get_cookie('SESSIONID')
        self.cookies.domain = cookies.get('domain')
        self.cookies.http_only = cookies.get('httpOnly')
        self.cookies.name = cookies.get('name')
        self.cookies.path = cookies.get('path')
        self.cookies.secure = cookies.get('secure')
        self.cookies.value = cookies.get('value')

    def _page_cabinet(self):
        page = "cabinet.html"
        self._get(self.url, page)

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

    def user_info(self) -> UserInformation:
        html = self._page_info()
        table = html.find('tbody').find_all('td')
        subscriber = table[0].find_next('td').find_next('td')
        address = table[1].find_next('td').find_next('td')
        living_space = table[2].find_next('td').find_next('td')
        total_space = table[3].find_next('td').find_next('td')
        ownership = table[4].find_next('td').find_next('td')
        phone = table[5].find_next('td').find_next('td')
        email = table[6].find_next('td').find_next('td')
        regpeople = table[7].find_next('td').find_next('td')
        unvpeople = table[8].find_next('td').find_next('td')
        indebt = table[9].find_next('td').find_next('td')
        fines = table[10].find_next('td').find_next('td')
        return UserInformation(subscriber=subscriber.text,
                               address=address.text,
                               living_space=int(living_space.text),
                               total_space=int(total_space.text),
                               form_of_ownership=ownership.text,
                               phone=phone.text,
                               email=email.text,
                               registered_people=regpeople.text,
                               unavailable_people=unvpeople.text,
                               indebtedness=int(indebt.text),
                               fines=int(fines.text))

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
