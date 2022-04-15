#!/usr/bin/env python3

from pathlib import Path
from urllib import request
import config
# from . import config
import urllib.request
import sys
import io

# where's human readable size func?
# from common import


def download_url_to_filepath(url: str, filepath: Path):
    content_bytes = request.urlopen(url).read()
    filepath.write_bytes(content_bytes)


def download_with_progress(url: str, filepath: Path):
    resp = urllib.request.urlopen(url)
    length = resp.getheader('content-length')
    if length:
        length = int(length)
        blocksize = max(4096, length // 100)
    else:
        blocksize = 1000000  # just made something up

    # print(length, blocksize)
    print('URL: {}'.format(url))
    print('Length: {}'.format(length))

    buf = io.BytesIO()
    size = 0
    while True:
        buf1 = resp.read(blocksize)
        if not buf1:
            break
        buf.write(buf1)
        size += len(buf1)
        if length:
            print('{} %\rPercentage downloaded: '.format(
                int(size / length * 100)),
                  end='')
    print()

    content_bytes = buf.getvalue()
    filepath.write_bytes(content_bytes)
    print('Downloaded to {}'.format(filepath), end='\n' * 2)


def main() -> None:
    # globals()[sys.argv[1]](*sys.argv[2:])
    for url, filepath in config.url_filepath_mapping.items():
        if len(sys.argv) != 1 and sys.argv[1] == '--silent':
            download_url_to_filepath(url, filepath)
            return None
        else:
            download_with_progress(url, filepath)


if __name__ == '__main__':
    main()