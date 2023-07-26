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
        self.driver = webdriver.Chrome(options=Options(headless=isHeadless))

    def goto(self, url: str) -> None:
        self.driver.get(url)

    def setNeededStaticCookieValues(self) -> None:
        pass

    def retrieveHTMLElement(self, retrieveBy: str, identifier: str) -> WebElement:
        if retrieveBy not in By.__dict__.values():
            raise ValueError(f"Invalid 'retrieveBy' method provided: {retrieveBy}.")
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((retrieveBy, identifier))
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                f"Element with '{retrieveBy}' '{identifier}' not found."
            )

    # Intialize StartInstance (headless)
    # Go to that URL
    # Get the spring_a_tag by Link Text of "Spring 2024" and click it
    # Set the cookies
    # Get the advanced_search_a_tag by ID of "SSR_CLSRCH_FLDS_PTS_ADV_SRCH" and click it
    # Get the available subjects select
    # Find children of that select element that:
    #   Are option tags
    #   Do not have aria-invalid="true" attribute
    # Get all these children's value attribute tag

    def __waitThenClickByLinkText(self, linkText: str) -> None:
        # Wait for the element to load then click it
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, linkText))
        ).click()

    def __getNeededCookieValues(self):
        # NOTE: The cookies you need are only obtained through going to a
        # class search page specifically

        # Extract the cookies
        cookies: list[dict] = self.driver.get_cookies()

        # These are the values that change from each session, so we need these
        PSJ_SESSION_ID = ""
        PS_TOKEN = ""
        PS_TOKEN_EXPIRE = ""
        TS01efa3ea = ""  # idk what this means either
        TS0193b50d = ""  # I love things we don't understand!

        # Loop through each cookie dict in the cookie list and find the values needed
        for cookie in cookies:
            if cookie["name"] == "CSDPRD-PSJSESSIONID":
                PSJ_SESSION_ID = cookie["value"].strip()
            elif cookie["name"] == "TS01efa3ea":
                TS01efa3ea = cookie["value"].strip()
            elif cookie["name"] == "TS0193b50d":
                TS0193b50d = cookie["value"].strip()
            elif cookie["name"] == "PS_TOKEN":
                PS_TOKEN = cookie["value"].strip()
            elif cookie["name"] == "PS_TOKENEXPIRE":
                PS_TOKEN_EXPIRE = cookie["value"].strip()

        # Return them in the order we will pass them in main for continuity
        return [TS01efa3ea, TS0193b50d, PSJ_SESSION_ID, PS_TOKEN, PS_TOKEN_EXPIRE]
