import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

# YT Video: https://www.youtube.com/watch?v=GjKQ6V_ViQE

# Load webpage content
r = requests.get("https://keithgalli.github.io/web-scraping/webpage.html")

# Convert webpage content to BeautifulSoup object
webpage = bs(r.content, "lxml")

# Print out HTML
# print(webpage.prettify())


### Grab all of the social links from the webpage ###

# Get social links using select and for loop
# links = webpage.select("ul.socials a")
# Foor loop comprehension
# actual_links = [link['href'] for link in links]
# print(actual_links)

# Get social links using find
# ulist = webpage.find("ul", attrs={"class": "socials"})
# links = ulist.find_all("a")
# actual_links = [link['href'] for link in links]
# print(actual_links)

# Get social links using Select
# links = webpage.select("li.social a")
# actual_links = [link['href'] for link in links]
# print(actual_links)


### Get information from a table ###
# Grab table
# table = webpage.select("table.hockey-stats")[0]
# Get column names
# columns = table.find("thead").find_all("th")
# column_names = [c.string for c in columns]
# Initialize list
# l = []
# For statement with table
# table_rows = table.find("tbody").find_all("tr")
# for tr in table_rows:
#    td = tr.find_all("td")
#    row = [str(tr.get_text()).strip() for tr in td]
#    l.append(row)
# Merge into dataframe
# df = pd.DataFrame(l, columns=column_names)
# print(df)


### Parse data with reg expression ###
# facts = webpage.select("ul.fun-facts li")
# facts_with_is = [fact.find(string=re.compile("is")) for fact in facts]
# print(facts_with_is)


### Download an image ###
# Create Full Url
# url = "https://keithgalli.github.io/web-scraping/"
# images = webpage.select("div.row div.column img")
# image_url = images[0]['src']
# full_url = url + image_url
# Downlaod Image
# img_data = requests.get(full_url).content
# with open('lake_como.jpg', 'wb') as handler:
#    handler.write(img_data)


# Get data from linked files
# url = "https://keithgalli.github.io/web-scraping/"
# files = webpage.select("div.block a")
# relative_files = [f['href'] for f in files]
# for f in relative_files:
#    full_url = url + f
#    page = requests.get(full_url)
#    bs_page = bs(page.content, "lxml")
#    secret_word_element = (bs_page.find("p", attrs={"id": "secret-word"}))
#    secret_word = secret_word_element.string
#    print(secret_word)
