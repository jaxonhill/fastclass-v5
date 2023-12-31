## FAQ

Ok, not exactly a FAQ, but more of "Why did you make this choice?" type of questions that I am writing for myself for future reference or for any programmers that onboard onto the project. There are countless weird things I am running into, and I have only been scraping RateMyProfessors and SDSU so far. I can only imagine how some other schools' websites are. SDSU itself is using Oracle, XML, and Vanilla JavaScript from what I can gather based on their internal API calls and code.

## Table of Contents
- [FAQ](#faq)
- [Table of Contents](#table-of-contents)
- [Scraping](#scraping)
  - [Why Python for the scraping?](#why-python-for-the-scraping)
  - [Why do you have to search for the advanced search iframe by tag name?](#why-do-you-have-to-search-for-the-advanced-search-iframe-by-tag-name)
- [Might Want To Think About Later](#might-want-to-think-about-later)


## Scraping

### Why Python for the scraping?

I wish I had some elaborate answer, but I went with Python for the scraping because I'm currently Leetcoding and practicing for interview questions and I want to remain sharp on my Python skills. Although this is actually the main reason, there are still some benefits to Python:

* Minimal syntax that reads like English, so you can better understand what is actually happening with the scrapers
* Popular, staple libraries such as requests, BeautifulSoup, and Selenium
* Due to above point, there are many examples for extremely weird edge cases I might run into

The only thing I wish I had in Python for scraping especially is stronger, enforced types. I use type hints wherever it is suitable; however, if this were to scale to other schools, I would heavily consider TypeScript and then just refactoring the SDSU scraper. Using TypeScript and types for scraping is incredibly useful -- especially if you are pulling from APIs.

### Why do you have to search for the advanced search iframe by tag name?

I tried to search for it by CSS Selector, but it would always break. The site uses a different CSS selector every time you open the site I believe. I'm not sure how this is even possible, but there will only be one iframe at the time you call the function anyway -- so just use the tag name of "iframe" and save yourself the headache.

## Might Want To Think About Later

* Add exponential backoff for the WebDriverWaits and standardize them - if they fail like a 60 second wait or something, then the servers are down