from bs4 import BeautifulSoup
import requests
import csv

### Scrape data from html file ###
# with open('simple.html') as html_file:

# soup = BeautifulSoup(html_file, 'lxml')

# Print html data from file:
# print(soup.prettify())

# for article in soup.find_all('div', class_='article'):
#    headline = article.h2.a.text
#    print(headline)
#    summary = article.p.text
#    print(summary)


### Scrape data from website ###
# source=requests.get('http://coreyms.com').text

# soup = BeautifulSoup(source, 'lxml')

# Scrape first article
# article = soup.find('article')

# Get headline
# headline = article.a.text
# print(headline)

# Scrape Article Summary
# summary = article.find('div', class_='entry-content').p.text
# print(summary)


# Scrape Video Source html
# video_source = article.find('iframe', class_='youtube-player')['src']
# video_id = video_source.split('/')[4]
# video_id = video_id.split('?')[0]

# yt_link = f'https://youtube.com/watch?v={video_id}'
# print(yt_link)




# Scrape all articles
source = requests.get('http://coreyms.com').text

soup = BeautifulSoup(source, 'lxml')

# Write information to CSV
csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'video_link'])

for article in soup.find_all('article'):
    # Get Article Headline
    headline = article.h2.a.text
    print(headline)

    # Get Summary
    summary = article.find('div', class_='entry-content').p.text
    print(summary)

    # Scrape Video Source html
    try:
        video_source = article.find('iframe', class_='youtube-player')['src']
        video_id = video_source.split('/')[4]
        video_id = video_id.split('?')[0]
        yt_link = f'https://youtube.com/watch?v={video_id}'

    except Exception as e:
        yt_line = None

    print(yt_link)
    print()

    csv_writer.writerow([headline, summary, yt_link])

csv_file.close()
