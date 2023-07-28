from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
import requests
from bs4 import BeautifulSoup
import time

from selenium_utils import *

from classes.BaseSelenium import BaseSelenium
from classes.StartInstanceSelenium import StartInstanceSelenium

START_PAGE_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL"
SPRING_2024_LINK_TEXT: str = "Spring 2024"
ADVANCED_SEARCH_LINK_CSS_ID: str = "SSR_CLSRCH_FLDS_PTS_ADV_SRCH"
ADVANCED_SEARCH_IFRAME_CSS_SELECTOR: str = "ptModFrame_0"
SUBJECTS_SELECT_CSS_SELECTOR: str = "#SSR_CLSRCH_ADV_SSR_ADVSRCH_OP2\$0"
SEARCH_BUTTON_CSS_SELECTOR: str = "#SSR_CLSRCH_FLDS_SSR_SEARCH_PB_1\$0"
PARAM_FOR_SEMESTER_CODE: str = "ES_STRM"
H1_TITLE_CSS_SELECTOR: str = "#PT_PANEL2_TITLE"
ERROR_NO_CLASSES_FOUND_DIV_SELECTOR: str = "#win1divPTS_SRCH_PTS_INDEXTIME_GB"
SUBJECT_CLASS_TABLE_DIV_SELECTOR: str = "#win1divPTS_RSLTS_GL_GB"


def main():
    # Start selenium driver, click on designated semester and return cookie values for session
    driver = initDriver(isHeadless=False)
    driver.get(START_PAGE_URL)
    getHTMLElement(driver, 10, By.LINK_TEXT, SPRING_2024_LINK_TEXT).click()
    (
        PSJ_SESSION_ID,
        PS_TOKEN,
        PS_TOKEN_EXPIRE,
        TS01efa3ea,
        TS0193b50d,
    ) = getCookies(driver)

    # Switch to advanced search iframe
    getHTMLElement(driver, 10, By.ID, ADVANCED_SEARCH_LINK_CSS_ID).click()
    iframe: WebElement = getHTMLElement(driver, 10, By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # Get subject select options and filter them for only valid subject tags
    subject_select_options: list[WebElement] = Select(
        getHTMLElement(driver, 10, By.CSS_SELECTOR, SUBJECTS_SELECT_CSS_SELECTOR)
    ).options
    subject_tags: list[str] = getValidSubjectTags(subject_select_options)
    print(subject_tags)

    return

    #

    # Start selenium driver, click on Spring 2024 to set cookie that identifies this for later
    startInstance: StartInstanceSelenium = StartInstanceSelenium(isHeadless=False)
    startInstance.goto(START_PAGE_URL)
    startInstance.retrieveHTMLElement(By.LINK_TEXT, SPRING_2024_LINK_TEXT).click()
    (
        PSJ_SESSION_ID,
        PS_TOKEN,
        PS_TOKEN_EXPIRE,
        TS01efa3ea,
        TS0193b50d,
    ) = startInstance.getCookies()

    # Switch to advanced search iframe and get all the subject tags for current semester
    startInstance.retrieveHTMLElement(By.ID, ADVANCED_SEARCH_LINK_CSS_ID).click()
    # Check reference FAQ, we MUST search by Tag Name and just look for an iframe
    iframe_element: WebElement = startInstance.retrieveHTMLElement(
        By.TAG_NAME, "iframe"
    )
    startInstance.switchToIFrame(iframe_element)
    subject_select_element: Select = Select(
        startInstance.retrieveHTMLElement(By.CSS_SELECTOR, SUBJECTS_SELECT_CSS_SELECTOR)
    )
    select_options: list[WebElement] = subject_select_element.options
    subject_tags: list[str] = startInstance.getValidSubjectTags(select_options)

    # Select a subject option and submit to get semester code from resulting URL
    subject_select_element.select_by_value(subject_tags[0])
    startInstance.retrieveHTMLElement(
        By.CSS_SELECTOR, SEARCH_BUTTON_CSS_SELECTOR
    ).click()
    startInstance.waitUntilURLContains("ES_STRM=")
    semester_code: str = startInstance.getSemesterCodeFromURL()
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)

    # TODO: NEED TO FIX TECH DEBT

    # Probably need to move a lot of stuff actually internal to the class and make new methods

    # Almost need a method that is like: waitForSubjectPageLoad that waits for the subject page to load
    # by checking if that h1 text is there, like you are below

    # Need individual methods for:
    #   isNoClassesFoundErrorPresent
    #   isTooManyClassesFoundErrorPresent
    #   isClassOptionTableFound

    # Iterate through all subjects and go to the URLs using Selenium
    # Wait for title
    # If red text there
    #   Get last element of the table and figure out the first number that is after the code
    #       (ex. ART 531) -> 5
    #   Now search equivalent to "ART 5" up to "ART 9" `ES_CNBR=5` -> `ES_CNBR=9`
    #   If
    # Else
    #

    #

    # Error div
    startInstance.goto(
        "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=2243&ES_ADV=Y&ES_SUB=ART&ES_CNBR=9&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID"
    )
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    test = startInstance.doesElementExist(
        By.CSS_SELECTOR, ERROR_NO_CLASSES_FOUND_DIV_SELECTOR
    )
    assert test  # Should be true and pass
    startInstance.goto(
        "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=2243&ES_ADV=Y&ES_SUB=ART&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID"
    )
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    test = startInstance.doesElementExist(
        By.CSS_SELECTOR, ERROR_NO_CLASSES_FOUND_DIV_SELECTOR
    )
    assert not test  # Should be false and pass

    # Red text
    startInstance.goto(
        "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=2243&ES_ADV=Y&ES_SUB=ART&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID"
    )
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    test = startInstance.doesElementExist(By.TAG_NAME, "font")
    assert test  # Should be true and pass
    startInstance.goto(
        "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=2243&ES_ADV=Y&ES_SUB=ACCTG&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID"
    )
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    test = startInstance.doesElementExist(By.TAG_NAME, "font")
    assert not test  # Should be false and pass

    # Regular table
    startInstance.goto(
        "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=2243&ES_ADV=Y&ES_SUB=ACCTG&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID"
    )
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    test = startInstance.doesElementExist(
        By.CSS_SELECTOR, SUBJECT_CLASS_TABLE_DIV_SELECTOR
    )
    assert test  # Should be true and pass
    startInstance.goto(
        "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=2243&ES_ADV=Y&ES_SUB=ART&ES_CNBR=9&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID"
    )
    startInstance.waitForElement(By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    test = startInstance.doesElementExist(
        By.CSS_SELECTOR, SUBJECT_CLASS_TABLE_DIV_SELECTOR
    )
    assert not test  # Should be false and pass

    #


if __name__ == "__main__":
    main()


def hello():
    pass

    # GOOD REQUEST
    # URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CRSE_INFO_FL.GBL"
    # payload = {
    #     "Page": "SSR_CRSE_INFO_FL",
    #     "Action": "U",
    #     "Page": "SSR_CS_WRAP_FL",
    #     "Action": "U",
    #     "ACAD_CAREER": "UGRD",
    #     "CRSE_ID": "038518",
    #     "CRSE_OFFER_NBR": "1",
    #     "INSTITUTION": "SDCMP",
    #     "STRM": "2243",
    #     "CLASS_NBR": "9313",
    #     "pts_Portal": "EMPLOYEE",
    #     "pts_PortalHostNode": "SA",
    #     "pts_Market": "GBL",
    #     "cmd": "uninav",
    #     "ICAJAX": "1",
    #     "ICMDTarget": "start",
    #     "ICPanelControlStyle": "pst_side1-fixed pst_panel-mode",
    # }
    # headers = {
    #     "Accept": "*/*",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Connection": "keep-alive",
    #     "Cookie": f"TS0193b50d={TS0193b50d}; ExpirePage=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; PS_TokenSite=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/?CSDPRD-PSJSESSIONID; PS_LOGINLIST=https://cmsweb.cms.sdsu.edu/CSDPRD; SignOnDefault=; ps_theme=node:SA portal:EMPLOYEE theme_id:SD_DEFAULT_THEME_FLUID css:DEFAULT_THEME_FLUID css_f:SD_PT_BRAND_FLUID_TEMPLATE_857 accessibility:N macroset:SD_PT_DEFAULT_MACROSET_857 formfactor:3 piamode:2; PS_TOKEN={PS_TOKEN}; PS_DEVICEFEATURES=width:1920 height:1200 pixelratio:1 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; CSDPRD-PSJSESSIONID={PSJ_SESSION_ID}; https%3a%2f%2fcmsweb.cms.sdsu.edu%2fpsp%2fcsdprd%2femployee%2fsa%2frefresh=list: %3ftab%3ddefault|%3frp%3ddefault|%3ftab%3dsd_ad_workcenter|%3frp%3dsd_ad_workcenter|%3ftab%3dremoteunifieddashboard|%3frp%3dremoteunifieddashboard; PS_LASTSITE=https://cmsweb.cms.sdsu.edu/psp/CSDPRD/; TS01efa3ea={TS01efa3ea}; psback=%22%22url%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD_1%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_MD_SP_FL.GBL%3Fpage%3DSSR_MD_TGT_PAGE_FL%22%20%22label%22%3A%22Manage%20Classes%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD_1%2FEMPLOYEE%2FSA%22%22; PS_TOKENEXPIRE={PS_TOKEN_EXPIRE}",
    #     "Host": "cmsweb.cms.sdsu.edu",
    #     "Referer": "https://cmsweb.cms.sdsu.edu/psc/CSDPRD_1/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV&Page=SSR_CS_WRAP_FL&Action=U&ACAD_CAREER=UGRD&CRSE_ID=038518&CRSE_OFFER_NBR=1&INSTITUTION=SDCMP&STRM=2243&CLASS_NBR=9313&pts_Portal=EMPLOYEE&pts_PortalHostNode=SA&pts_Market=GBL&cmd=uninav",
    #     "Sec-Fetch-Dest": "empty",
    #     "Sec-Fetch-Mode": "cors",
    #     "Sec-Fetch-Site": "same-origin",
    #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    #     "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": '"Linux"',
    # }

    # r = requests.get(URL, params=payload, headers=headers)
    # print(r.text)


# OOP LAYOUT

# StartSeleniumInstance
# MoreThan50ClassOptionsSeleniumInstance

# MAKE NOTES OF HOW THIS SYSTEM COULD BE IMPROVED FURTHER FOR 100% COVERAGE FOR EDGE CASES, etc.
# MAKE NOTES OF "WEIRDNESS" IN SDSU SYSTEM SO YOU UNDERSTAND LATER


# DETERMINE HOW MANY COURSES FOR EACH CLASS AND CREATE ARRAYS
# Iterate through these class category abbreviations as URLs using requests library
# (testing):
#   * Create a pandas dataframe with abbreviation and class
#   * Count up how many classes for each abbreviation
#   * For the ones that have more than 50 or are close, check their actual total classes
#   *       to ensure the scraper is working correctly and counting the right number
#   * This shouldn't be a problem for this actual part of the website for some reason
#   * Document this weirdness here
# Create two different arrays
#   -> 1. classes with less than or equal to 50 classes (will use requests later)
#   -> 2. classes with more than 50 classes (have to use selenium due to weird SDSU API calls)

# MAKE API CALL USING REQUESTS FOR EACH CLASS
# Iterate through the class array for classes with 50 or less classes
