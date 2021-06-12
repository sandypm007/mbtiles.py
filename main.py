#!/usr/bin/python

import os
import os.path
import random
from time import sleep
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def download_url(zoom, xtile, ytile):
    servers = ['a', 'b', 'c']
    subdomain = random.randint(0, 2)

    url = "https://" + str(servers[subdomain]) + ".tile.openstreetmap.org/%s/%s/%s.png" % (zoom, xtile, ytile)
    dir_path = "tiles/%s/%s/" % (zoom, xtile)
    download_path = "tiles/%s/%s/%s.png" % (zoom, xtile, ytile)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.isfile(download_path):
        print("downloading %r" % url)
        req = Request(
            url,
            data=None,
            headers={
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,es;q=0.8,es-ES;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            }
        )
        source = urlopen(req)
        content = source.read()
        source.close()
        destination = open(download_path, 'wb')
        destination.write(content)
        destination.close()
        print('OK :)')
    else:
        print("skipped %r" % url)


f = open('export.txt', 'r+')
lines = f.read().rstrip('\n').split('\n')
f.close()

while len(lines) > 0:
    retry = []
    for line in lines:
        try:
            zoom, xtile, ytile = line.split('/')
            download_url(zoom, xtile, ytile)
        except HTTPError as e:
            print('sending', line, 'to retry list')
            print('cause >>>', e)
            retry.append(line)
        sleep(1)  # sleep for 1 second to avoid flush blocks
    lines = retry
    if len(lines) > 0:
        print('pause 5 secs and retry', len(lines))
        sleep(5)
