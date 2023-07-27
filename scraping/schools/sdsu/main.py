from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
import time

from classes.BaseSelenium import BaseSelenium
from classes.StartInstanceSelenium import StartInstanceSelenium

START_PAGE_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL"
SPRING_2024_LINK_TEXT: str = "Spring 2024"
ADVANCED_SEARCH_LINK_CSS_ID: str = "SSR_CLSRCH_FLDS_PTS_ADV_SRCH"
ADVANCED_SEARCH_IFRAME_CSS_SELECTOR: str = "ptModFrame_0"
SUBJECTS_SELECT_CSS_SELECTOR: str = "#SSR_CLSRCH_ADV_SSR_ADVSRCH_OP2\$0"
SEARCH_BUTTON_CSS_SELECTOR: str = "#SSR_CLSRCH_FLDS_SSR_SEARCH_PB_1\$0"
PARAM_FOR_SEMESTER_CODE: str = "ES_STRM"


def main():
    # Start selenium driver, click on Spring 2024 to set cookie that identifies this for later
    startInstance: StartInstanceSelenium = StartInstanceSelenium(isHeadless=False)
    startInstance.goto(START_PAGE_URL)
    startInstance.retrieveHTMLElement(By.LINK_TEXT, SPRING_2024_LINK_TEXT).click()
    startInstance.setStaticCookieValues()

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
    print(semester_code)


if __name__ == "__main__":
    main()


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
