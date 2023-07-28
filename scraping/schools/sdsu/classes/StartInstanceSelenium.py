from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import re
import time

from classes.BaseSelenium import BaseSelenium


class StartInstanceSelenium(BaseSelenium):
    def __init__(self, isHeadless: bool) -> None:
        super().__init__(isHeadless)
        self.subject_options: list[WebElement] = None

    def switchToIFrame(self, iframe_element: WebElement) -> None:
        self.driver.switch_to.frame(iframe_element)

    def getValidSubjectTags(self, select_options: list[WebElement]) -> list[str]:
        validSelectOptions: list[WebElement] = filter(
            self.__isSelectOptionValid, select_options
        )
        return [option.get_attribute("value") for option in validSelectOptions]

    def __isSelectOptionValid(self, select_option: WebElement) -> bool:
        # Check that aria-invalid is not an attribute
        if "aria-invalid" in select_option.get_attribute("outerHTML"):
            return False
        # Check that the option has a value
        if not select_option.get_attribute("value"):
            return False
        return True

    def waitUntilURLContains(self, param: str) -> None:
        WebDriverWait(self.driver, 10).until(EC.url_contains(param))

    def getSemesterCodeFromURL(self) -> str:
        pattern = r"ES_STRM=(\d+)"
        match = re.search(pattern, self.driver.current_url)
        return match.group(1)

    def waitForElement(self, retrieveBy: str, identifier: str) -> None:
        if retrieveBy not in By.__dict__.values():
            raise ValueError(f"Invalid 'retrieveBy' method provided: \"{retrieveBy}\"")
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((retrieveBy, identifier))
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                f'Element with "{retrieveBy}" "{identifier}" not found.'
            )

    def doesElementExist(self, retrieveBy: str, identifier: str) -> bool:
        if retrieveBy not in By.__dict__.values():
            raise ValueError(f"Invalid 'retrieveBy' method provided: \"{retrieveBy}\"")

        try:
            ele: WebElement = self.driver.find_element(retrieveBy, identifier)
            return True
        except NoSuchElementException:
            return False
