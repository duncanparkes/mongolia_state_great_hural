# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import requests
import lxml.html
response = requests.get("http://www.parliament.mn/en/who?type=3")

root = lxml.html.fromstring(response.content)

cv_divs = root.cssselect("div.cvListItem")

for cv_div in cv_divs:
    name = cv_div.find('div').text_content().strip()

    data = {'name': name}

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
