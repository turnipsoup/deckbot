import requests, json
import bs4 as bs

# The wiki page
WIKI_PAGE = 'https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_keywords'

# Get the wikipage initially
wiki = requests.get(WIKI_PAGE)
wikisoup = bs.BeautifulSoup(wiki.content, 'lxml')
def_soup = wikisoup.find('div', {'class': 'mw-parser-output'})
defs_list = []
defs_dict = {}


for keyword in def_soup:
    defs_list.append(keyword)

for i in range(len(defs_list)):
    if defs_list[i].name == 'h3':
        keyword_name = defs_list[i].text.replace('[edit]','').lower()
        keyword_def = defs_list[i+2].text
        defs_dict[keyword_name] = keyword_def

with open("./mtg-keyword-defs.json", "w") as f:
    f.write(json.dumps(defs_dict))