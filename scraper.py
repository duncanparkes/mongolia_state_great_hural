# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import requests
from urlparse import urljoin
import lxml.html
source_url = "http://www.parliament.mn/en/who?type=3"
response = requests.get(source_url)

root = lxml.html.fromstring(response.content)

cv_divs = root.cssselect("div.cvListItem")

for cv_div in cv_divs:
    name = cv_div.find('div').text_content().strip()
    image = urljoin(source_url, cv_div.getprevious().get('src'))

    data = {
        'name': name,
        'image': image,
        }

    ### Scraperwiki saving bits below.

    scraperwiki.sqlite.save(unique_keys=('name',), data=data)

# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
