import re
import sys
import HTMLParser
import time
import os

import requests

deck_urls = sys.argv[1]

out_dir = '/home/axlan/data/goldfish_scrape/commander_out/'

deck_num_re = re.compile(r'https://www.mtggoldfish.com/deck/([0-9]+)')
deck_re = re.compile(r'<input type="hidden" name="deck_input\[deck\]" id="deck_input_deck" value="(.+?)" />', re.DOTALL | re.MULTILINE)
h = HTMLParser.HTMLParser()

retries = 10

with open(deck_urls) as fd:
    for url in fd.readlines():
        deck_num = deck_num_re.match(url).group(1)
        file_name = out_dir + deck_num
        if os.path.isfile(file_name):
            continue
        failed = True
        for i in range(retries):
            time.sleep(0.1)
            resp = requests.get(url)
            if resp.status_code != 200:
                continue
            page = resp.text
            m = deck_re.search(page)
            if m:
                failed = False
                deck_data = m.group(1)
                deck_data = h.unescape(deck_data)
                with open(file_name, 'w') as out_fd:
                    out_fd.write(deck_data)
            break
        if failed:
            print "Load failed " + url
