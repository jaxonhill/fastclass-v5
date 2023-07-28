from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


def initDriver(isHeadless: bool) -> WebDriver:
    options = Options()
    options.headless = isHeadless
    return webdriver.Chrome(options=options)


def getHTMLElement(
    driver: WebDriver, howManySeconds: int, retrieveBy: str, identifier: str
) -> WebElement:
    if retrieveBy not in By.__dict__.values():
        raise ValueError(f"Invalid 'retrieveBy' method provided: \"{retrieveBy}\"")
    try:
        return WebDriverWait(driver, howManySeconds).until(
            EC.presence_of_element_located((retrieveBy, identifier))
        )
    except NoSuchElementException:
        raise NoSuchElementException(
            f'Element trying to be found by: "{retrieveBy}" with identifier: "{identifier}" not found.'
        )


def getCookies(driver: WebDriver) -> list[str]:
    PSJ_SESSION_ID: str = ""
    PS_TOKEN: str = ""
    PS_TOKEN_EXPIRE: str = ""
    TS01efa3ea: str = ""
    TS0193b50d: str = ""

    cookies: list[dict] = driver.get_cookies()
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

    return [PSJ_SESSION_ID, PS_TOKEN, PS_TOKEN_EXPIRE, TS01efa3ea, TS0193b50d]


def getValidSubjectTags(select_options: list[WebElement]) -> list[str]:
    validSelectOptions: list[WebElement] = filter(__isSelectOptionValid, select_options)
    return [option.get_attribute("value") for option in validSelectOptions]


def __isSelectOptionValid(select_option: WebElement) -> bool:
    # Check that aria-invalid is not an attribute
    if "aria-invalid" in select_option.get_attribute("outerHTML"):
        return False
    # Check that the option has a value
    if not select_option.get_attribute("value"):
        return False
    return True
