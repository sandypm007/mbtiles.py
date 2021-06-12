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

    url = "http://" + str(servers[subdomain]) + ".tile.openstreetmap.org/%s/%s/%s.png" % (zoom, xtile, ytile)
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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        source = urlopen(req)
        content = source.read()
        source.close()
        destination = open(download_path, 'wb')
        destination.write(content)
        destination.close()
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
        except HTTPError:
            print('sending', line, 'to retry list')
            retry.append(line)
        sleep(10)  # sleep for 10 seconds to avoid flush blocks
    lines = retry
    print('pause 5 secs and retry', len(lines))
    sleep(5)
