# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import requests
from urlparse import urljoin
from urllib import urlencode
import lxml.html

en_source_url = "http://www.parliament.mn/en/who"
mn_source_url = "http://www.parliament.mn/who"

types = (
    # ('chairman', 1),
    # ('vice_chairman', 2),
    ('member', 3),
    )

members_by_image_url = {}

for type_name, type_id in types:
    query = {'type': type_id}
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

