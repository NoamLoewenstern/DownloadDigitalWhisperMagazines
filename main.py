import re
import os
from os.path import join
from urllib.request import urlopen
from lxml import etree
from bs4 import BeautifulSoup

from constants import TABLE_XPATH, FULL_SHEET_XPATH, DEBUG, NUM_SHEETS, \
    DST_MAGAZINES, BASE_URL, CUR_DIR, LINK_REGEX_HREF_CONTENT

def get_all_magazines_links_to_download() -> dict:
    magazines = {}
    for num_sheet in range(1, NUM_SHEETS + 1):
        url = BASE_URL.format(num_sheet=num_sheet)
        response = urlopen(url)
        data = response.read()
        soup = BeautifulSoup(data, features="lxml")

        all_elems = soup.find_all('a',
                                  href=re.compile(LINK_REGEX_HREF_CONTENT))
        href = all_elems[0].attrs['href']
        fname = href.split('/')[-1]
        magazines[num_sheet] = [(href, fname)]
        for a_elem in all_elems[1:]:
            href = a_elem.attrs['href']
            fname = a_elem.text + '.pdf'
            magazines[num_sheet].append((href, fname))
    return magazines

def download_all_magazines(magazines: dict) -> None:
    for num_sheet, values in magazines.items():
        dirpath = join(CUR_DIR, DST_MAGAZINES, str(num_sheet))
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        for href, fname in values:
            with open(join(dirpath, fname), 'wb') as out_fh:
                resp = urlopen(href)
                pdf_data = resp.read()
                out_fh.write(pdf_data)


def main():
    if os.path.isdir(join(CUR_DIR, DST_MAGAZINES)):
        os.mkdir(join(CUR_DIR, DST_MAGAZINES))
    magazines = get_all_magazines_links_to_download()
    download_all_magazines(magazines)


if __name__ == '__main__':
    main()