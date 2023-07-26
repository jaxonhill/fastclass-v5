from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
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
