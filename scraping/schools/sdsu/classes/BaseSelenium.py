from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class BaseSelenium:
    # Static cookie values - they will be reused throughout the program and only are declared once
    PSJ_SESSION_ID: str = ""
    PS_TOKEN: str = ""
    PS_TOKEN_EXPIRE: str = ""
    # Not sure what these two bottom ones exactly mean, but they are important
    TS01efa3ea: str = ""
    TS0193b50d: str = ""

    def __init__(self, isHeadless: bool) -> None:
        self.driver = webdriver.Chrome(options=self.__createOptions(isHeadless))

    def goto(self, url: str) -> None:
        self.driver.get(url)

    def setStaticCookieValues(self) -> None:
        cookies: list[dict] = self.driver.get_cookies()
        print(cookies)
        for cookie in cookies:
            if cookie["name"] == "CSDPRD-PSJSESSIONID":
                self.PSJ_SESSION_ID = cookie["value"].strip()
            elif cookie["name"] == "TS01efa3ea":
                self.TS01efa3ea = cookie["value"].strip()
            elif cookie["name"] == "TS0193b50d":
                self.TS0193b50d = cookie["value"].strip()
            elif cookie["name"] == "PS_TOKEN":
                self.PS_TOKEN = cookie["value"].strip()
            elif cookie["name"] == "PS_TOKENEXPIRE":
                self.PS_TOKEN_EXPIRE = cookie["value"].strip()

    def retrieveHTMLElement(self, retrieveBy: str, identifier: str) -> WebElement:
        if retrieveBy not in By.__dict__.values():
            raise ValueError(f"Invalid 'retrieveBy' method provided: \"{retrieveBy}\"")
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((retrieveBy, identifier))
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                f'Element with "{retrieveBy}" "{identifier}" not found.'
            )

    def __createOptions(self, isHeadless: bool) -> Options:
        options = Options()
        options.headless = isHeadless
        return options
