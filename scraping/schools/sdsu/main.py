# main.py - Runs the whole program through an initial Selenium request and then requests.

# Libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
import requests
from bs4 import BeautifulSoup
import time

# Helper functions
from selenium_utils import *

# Constants
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
    getElement(driver, 10, By.LINK_TEXT, SPRING_2024_LINK_TEXT).click()
    (
        PSJ_SESSION_ID,
        PS_TOKEN,
        PS_TOKEN_EXPIRE,
        TS01efa3ea,
        TS0193b50d,
    ) = getCookies(driver)

    # Switch to advanced search iframe
    getElement(driver, 10, By.ID, ADVANCED_SEARCH_LINK_CSS_ID).click()
    iframe: WebElement = getElement(driver, 10, By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # Get subject select options and filter them for only valid subject tags
    subjects_select_ele: Select = Select(
        getElement(driver, 10, By.CSS_SELECTOR, SUBJECTS_SELECT_CSS_SELECTOR)
    )
    subject_select_options: list[WebElement] = subjects_select_ele.options
    subject_tags: list[str] = getValidSubjectTags(subject_select_options)

    # Select first option and hit search button to get semester code from the URL
    subjects_select_ele.select_by_value(subject_tags[0])
    getElement(driver, 10, By.CSS_SELECTOR, SEARCH_BUTTON_CSS_SELECTOR).click()
    waitForElement(driver, 10, By.CSS_SELECTOR, H1_TITLE_CSS_SELECTOR)
    semester_code: str = getSemesterCodeFromURL(driver)

    # Need individual methods for:
    #   isNoClassesFoundErrorPresent
    #   isTooManyClassesFoundErrorPresent
    #   isClassOptionTableFound

    # Iterate through all subjects and go to the URLs using Selenium
    # Wait for title
    # Remove the "Open Classes" option by hitting the X
    # If red text there
    #   Get last element of the table and figure out the first number that is after the code
    #       (ex. ART 531) -> 5
    #   Now search equivalent to "ART 5" up to "ART 9" `ES_CNBR=5` -> `ES_CNBR=9`
    #   If red text still there
    #       Search even further like "ART 50" up to "ART 59"
    # Else

    # Figure out which classes have more than 50 options, and put them in an array
    # Figure out which classes have 50 or less options, and put them in an array, but with the
    #   class ID and the class number

    # NOTE: I think that if you use the class number that pops up when you have no open classes option,
    #   then you will also get waitlisted classes on the API call, which is what you want

    # requests part here

    # Create two different arrays
    #   -> 1. classes with less than or equal to 50 classes (will use requests later)
    #   -> 2. classes with more than 50 classes (have to use selenium due to weird SDSU API calls)

    # MAKE API CALL USING REQUESTS FOR EACH CLASS
    # Iterate through the class array for classes with 50 or less classes

    #

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


if __name__ == "__main__":
    main()
