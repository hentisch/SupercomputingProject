import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

webpage_link = "https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts"
webpage_content = requests.get(webpage_link)

soup = BeautifulSoup(webpage_content.text, 'html.parser')

table = soup.find('table', class_='wikitable sortable')

usernames = []
for row in table.tbody.find_all('tr'):
    try:
        str_row = str(row)
        at_sym_index = str_row.index("@")
        end_of_handle = str_row[at_sym_index:].index("<") + len(str_row[:at_sym_index])
        usernames.append(str_row[at_sym_index:end_of_handle].strip().strip("@"))
    except ValueError:
        pass

with open(sys.argv[1], "w") as f:
    f.writelines([username + "\n" for username in usernames if username != "ArianaGrande"])
    # As Ariana Grande was banned from Twitter, though is still in this list, we need to not 
    # include her in the list of accounts to scrape.
    