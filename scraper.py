# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import requests
from urlparse import urljoin
from urllib import urlencode
import lxml.html

en_source_url = "http://www.parliament.mn/en/who"
mn_source_url = "http://www.parliament.mn/who"

members_by_image_url = {}

query = {'type': 3} # 3 is members
query_string = '?' + urlencode(query)

# First get all the members in Mongolian

mn_response = requests.get(mn_source_url + query_string)
mn_root = lxml.html.fromstring(mn_response.text)

cv_lists = mn_root.cssselect("div#cvList")

for cv_list in cv_lists:
    for a in cv_list:
        homepage_src = urljoin(mn_source_url, a.get('href'))

        cv_div = a.cssselect('div.cvListItem')[0]

        image = urljoin(mn_source_url, a.cssselect('img')[0].get('src'))
        member_dict = members_by_image_url.setdefault(image, {})
        member_dict['name_mn'] = cv_div.find('div').text_content().strip()

        homepage_src = urljoin(mn_source_url, a.get('href'))
        home_resp = requests.get(homepage_src)
        home_root = lxml.html.fromstring(home_resp.content)

        email = home_root.cssselect('a[href^="mailto"]')[0].get('href')
        if email.startswith('mailto:'):
            member_dict['email'] = email[7:]

# While we're here, let's see if we can get a list of
# party names in Mongolian
parties_by_url = dict(
    [(urljoin(mn_source_url, x.get('href')), x.text) for x in
     mn_root.cssselect('#collapseCv5')[0].cssselect('a')]
    )

for party_url, party_name in parties_by_url.iteritems():
    party_resp = requests.get(party_url)
    party_root = lxml.html.fromstring(party_resp.content)
    cv_images = party_root.cssselect('img#cvImage')

    for x in cv_images:
        image_url = urljoin(mn_source_url, x.get('src'))
        members_by_image_url.get(image_url)['party_name_mn'] = party_name

# Now repeat in English, matching on the images.

en_response = requests.get(en_source_url + query_string)
en_root = lxml.html.fromstring(en_response.text)

cv_lists = en_root.cssselect("div#cvList")

for cv_list in cv_lists:
    for a in cv_list:
        image_rel = a.cssselect('img')[0].get('src')

        # Strip off the language code to make this match the Mongolian
        if image_rel.startswith('/en'):
            image_rel = image_rel[3:]

        image = urljoin(mn_source_url, image_rel)

        # Putting image inside the per member dict as well as using it as a
        # key to find it for convenience later
        member_dict = members_by_image_url.setdefault(image, {})

        cv_div = a.cssselect('div.cvListItem')[0]
        member_dict['name_en'] = cv_div.find('div').text_content().strip()


for image, member_dict in members_by_image_url.items():
    member_dict['image'] = image
    scraperwiki.sqlite.save(unique_keys=('image',), data=member_dict)

