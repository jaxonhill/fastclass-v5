from selenium.webdriver.common.by import By

from classes.BaseSelenium import BaseSelenium

# NOTE: LAYOUT OF THE ACTUAL PROGRAM

# OOP LAYOUT

# Base class for a selenium headless browser (static variable cookies)
#   Method to create the headless browser
#   Method to go to a URL
#   Method to retrieve an object based on CSS selector, class name, etc.
# StartSeleniumInstance
# MoreThan50ClassOptionsSeleniumInstance

# TODO: Just get the base class and the start done!

# MAKE NOTES OF HOW THIS SYSTEM COULD BE IMPROVED FURTHER FOR 100% COVERAGE FOR EDGE CASES, etc.
# MAKE NOTES OF "WEIRDNESS" IN SDSU SYSTEM SO YOU UNDERSTAND LATER

# GET ALL SUBJECTS AND COOKIES
# Open headless selenium and go to start URL
# Select term (ex. Spring 2024)
# Get cookies for later
# Open advanced search and get all the abbreviations of the class categories

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

START_PAGE_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL"
SPRING_2024_LINK_TEXT: str = "Spring 2024"


def main():
    # Intialize StartInstance (headless)
    startInstance: BaseSelenium = BaseSelenium(isHeadless=True)
    # Go to that URL
    startInstance.goto(START_PAGE_URL)
    # Get the spring_a_tag by Link Text of "Spring 2024" and click it
    startInstance.retrieveHTMLElement(By.LINK_TEXT, SPRING_2024_LINK_TEXT)
    # Set the cookies
    # Get the advanced_search_a_tag by ID of "SSR_CLSRCH_FLDS_PTS_ADV_SRCH" and click it
    # Get the available subjects select
    # Find children of that select element that:
    #   Are option tags
    #   Do not have aria-invalid="true" attribute
    # Get all these children's value attribute tag

    pass


if __name__ == "__main__":
    main()
