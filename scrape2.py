import requests
from bs4 import BeautifulSoup as bs
import re

# Load Webpage Content
r = requests.get("https://keithgalli.github.io/web-scraping/example.html")

# Convert to BeautifulSoup Object
soup = bs(r.content, "lxml")


# Get Header Elements
# first_header = soup.find_all(['h1', 'h2'])
# print(first_header)


# Pass attributes into find/find_all
# paragraph = soup.find_all("p", attrs={"id": "paragraph-id"})
# print(paragraph)


# Nest Find/Find_all calls
# body = soup.find("body")
# div = body.find('div')
# header = div.find('h1')
# print(header)


# Search for specific strings in find_all statement using regexpressions
# paragraph = soup.find_all("p", string=re.compile("Some"))
# headers = soup.find_all("h2", string=re.compile("(H|h)eader"))
# print(headers)


# CSS Selector
# Select specific item from a class
# content = soup.select("div p")
# print(content)

# Select specific item that follows a class
# paragraphs = soup.select("h2 ~ p")
# print(paragraphs)

# Select specific element with specific id
# bold_text = soup.select("p#paragraph-id b")
# print(bold_text)

# Nested Select Calls
# paragraphs = soup.select("body > p")
# for paragraph in paragraphs:
#    print(paragraph.select("i"))


# Get Properties of HTML
# header = soup.find("h2")

# Print out element with text only
# print(header.string)

# If multiple child elements
# print(header.get_text())

# Get links
# link = soup.find("a")
# print(link['href'])


# PARENT, SIBLING AND CHILD using Find_next
# siblings = soup.body.find("div").find_next_siblings()
# print(siblings)
