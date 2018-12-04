import re
import time

import requests


#python -m autopep8 -i scraper.py

formats = ['standard', 'modern', 'pauper', 'legacy', 'vintage', 'penny_dreadful', 'commander', 'brawl', 'duel_commander', 'arena_singleton',
           'arena_standard', 'canadian_highlander', 'old_school', 'no_banned_list_modern', 'frontier', 'tiny_leaders', 'limited', 'block', 'free_form']

deck_type = 'commander'

retries = 100
url_template = 'https://www.mtggoldfish.com/deck/custom/{}#paper'
page_template = '{}?page={}'

url = url_template.format(deck_type)
first_page = requests.get(url).text
last_page = None
for line in first_page.splitlines():
    if "pagination" in line:
        m = re.search(r'>([0-9]+)</a> <a class="next_page"', line)
        last_page = int(m.group(1))
if last_page is None:
    print('First page load failed')
    exit(1)

# print '{} pages found'.format(last_page)

deck_url_re = re.compile(r'<a href="/deck/([0-9]+)#paper">.+</a>')

out_file = "commander_url2.txt"
cache_file = "commander_url2_cache.txt"

try:
    with open(cache_file) as fd:
        read_pages = [int(line) for line in fd.readlines()]
except:
    read_pages = []


with open(cache_file, 'a') as fd_c:
    with open(out_file, 'a') as fd:
        for page in range(1, last_page+1):
            if page in read_pages:
                continue
            url = url_template.format(page_template.format(deck_type, page))
            failed = True
            for i in range(retries):
                time.sleep(0.2)
                resp = requests.get(url)
                if resp.status_code != 200:
                    continue
                page_text = resp.text
                for line in page_text.splitlines():
                    m = deck_url_re.match(line)
                    if m:
                        fd.write('https://www.mtggoldfish.com/deck/{}#paper\n'.format(m.group(1)))
                        failed = False
                if not failed:
                    fd_c.write('{}\n'.format(page))
                    break
            if failed:
                    print "Load failed " + url
