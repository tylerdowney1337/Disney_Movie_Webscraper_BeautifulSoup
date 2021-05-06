from bs4 import BeautifulSoup as bs
import requests
import json
import re
from datetime import datetime
import pickle
import urllib
import pandas as pd

# Tutorial YT Link: https://www.youtube.com/watch?v=Ewgy-G9cmbg 2:53

# Functions
def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
    elif row_data.find("br"):
        return [text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0", " ")


### Get One Movie ###
def get_one_movie(url):
    # Load webapage
    r = requests.get(url)

    # Convert to beautifulsoup object
    soup = bs(r.content, "lxml")

    # Grab infobox table
    infobox = soup.find(class_="infobox vevent")

    # Get table rows
    info_rows = infobox.find_all("tr")

    # Save rows to dictionary
    movie_info = {}

    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip=True)
        else:
            content_key = row.find("th").get_text(" ", strip=True)
            content_value = get_content_value(row.find("td"))
            movie_info[content_key] = content_value

# Clean up Sup and Span tags
def clean_tags(soup):
    for tag in soup.find_all(["sup", "span"]):
        tag.decompose()


### Get multiple movies ###
# Load webapage
def get_info_box(url):

    r = requests.get(url)
    soup = bs(r.content, "lxml")
    info_box = soup.find(class_="infobox vevent")
    info_rows = info_box.find_all("tr")

    clean_tags(soup)

    movie_info = {}

    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip=True)
        else:
            header = row.find('th')
            if header:
                content_key = row.find("th").get_text(" ", strip=True)
                content_value = get_content_value(row.find("td"))
                movie_info[content_key] = content_value

    return movie_info

# Get multiple Films
def get_multiple_films():
    # Get film links
    r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
    soup = bs(r.content, "lxml")
    movies = soup.select(".wikitable.sortable i a")

    base_path = "https://en.wikipedia.org/"

    movie_info_list = []

    for index, movie in enumerate(movies):
        try:
            relative_path = movie['href']
            full_path = base_path + relative_path
            title = movie['title']

            movie_info_list.append(get_info_box(full_path))

        except Exception as e:
            print(movie.get_text())
            print(e)


# load data from json file
def load_data(title):
    with open(title, encoding="utf-8") as f:
        return json.load(f)

movie_info_list = load_data("disney_data_cleaned.json")

# Clean Data
def minutes_to_integer(running_time):
    if running_time == "N/A":
        return None

    if isinstance(running_time, list):
        return int(running_time[0].split(" ")[0])
    else:
        return int(running_time.split(" ")[0])




for movie in movie_info_list:
    movie['Running time (int)'] = minutes_to_integer(movie.get("Running time", "N/A"))



### Dollar Value Parsing (money_conversion) ###
amounts = r"thousand|million|billion"
number = r"\d+(,\d{3})*\.*\d*"

value_re = rf"\${number}"
word_re = fr"\${number}(-|\sto\s|—)?({number})?\s({amounts})"

# Convert word to value
def word_to_value(word):
    value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    return value_dict[word]

# Parse Value and word syntax function
def parse_value_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    return value

def parse_word_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    word = re.search(amounts, string, flags=re.I).group().lower()
    word_value = word_to_value(word)
    return value * word_value

# Money Conversion Function
def money_conversion(money):
    if money == "N/A":
        return None

    if isinstance(money, list):
        money = money[0]

    word_syntax = re.search(word_re, money, flags=re.I)
    value_syntax = re.search(value_re, money)

    if word_syntax:
        return parse_word_syntax(word_syntax.group())
    elif value_syntax:
        return parse_value_syntax(value_syntax.group())
    else:
        return None

for movie in movie_info_list:
    movie['Budget (float)'] = money_conversion(movie.get('Budget', 'N/A'))
    movie['Box office (float)'] = money_conversion(movie.get('Box office', "N/A"))


# Convert dates into datetime objects
dates = [movie.get('Release date', 'N/A') for movie in movie_info_list]

def clean_date(date):
    return date.split("(")[0].strip()

def date_conversion(date):
    if isinstance(date, list):
        date = date[0]

    if date == "N/A":
        return None

    date_str = clean_date(date)

    fmts = ["%B %d, %Y", "%d %B %Y"]
    for fmt in fmts:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            pass

    return None

for movie in movie_info_list:
    movie['Release date (datetime)'] = date_conversion(movie.get('Release date', 'N/A'))

# Save Data
def save_data_pickle(name, data):
    with open(name, 'wb') as f:
        pickle.dump(data, f)


# Load Data
def load_data_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

# save_data_pickle("disney_movie_data_cleaned_more.pickle", movie_info_list)

movie_data = load_data_pickle("disney_movie_data_cleaned_more.pickle")

# Request Info From API
def get_omdb_info(title):
    base_url = f"http://www.omdbapi.com/?apikey=8d772ee9&"
    parameters = {'t': title}
    params_encoded = urllib.parse.urlencode(parameters)
    full_url = base_url + params_encoded
    return requests.get(full_url).json()

def get_rotten_tomato_score(omdb_info):
    ratings = omdb_info.get('Ratings', [])
    for rating in ratings:
        if rating['Source'] == 'Rotten Tomatoes':
            return rating['Value']
    return None

# Iterate over movies to get ratings from OMDB API
# for movie in movie_info_list:
#     title = movie['title']
#     omdb_info = get_omdb_info(title)
#     movie['imdb'] = omdb_info.get('imdbRating', None)
#     movie['metascore'] = omdb_info.get('Metascore', None)
#     movie['rotten_tomatoes'] = get_rotten_tomato_score(omdb_info)

# save_data_pickle("disney_movie_data_complete.pickle", movie_info_list)

movie_info_list = load_data_pickle("disney_movie_data_complete.pickle")


# Convert file to json

movie_info_copy = [movie.copy() for movie in movie_info_list]

for movie in movie_info_copy:
    current_date = movie['Release date (datetime)']
    if current_date:
        movie['Release date (datetime)'] = current_date.strftime("%B %d, %Y")
    else:
        movie['Release date (datetime)'] = None

# Save movie_info_copy to json
def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# save_data("disney_data_final.json", movie_info_copy)

# Create CSV File from JSON File
df = pd.DataFrame(movie_info_list)

# Save to CSV File
# df.to_csv("disney_movie_data_final.csv")

# Test DF
running_times = df.sort_values(['Running time (int)'], ascending=True)
print(running_times)
