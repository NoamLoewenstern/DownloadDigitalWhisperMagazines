import re
import os
import json
from urllib.request import urlopen
import urllib
import logging
from bs4 import BeautifulSoup

from constants import TABLE_XPATH, FULL_SHEET_XPATH, DEBUG, NUM_SHEETS, \
    DST_MAGAZINES, BASE_URL, CUR_DIR, LINK_REGEX_HREF_CONTENT, DST_MAGAZINES_JSON


def out_temp(data='', path=CUR_DIR / 'temp.html'):
    try:
        path.write_text(data)
    except:
        path.write_bytes(data)


def setup():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    if not DST_MAGAZINES.is_dir():
        os.mkdir(DST_MAGAZINES)

def get_all_magazines_links_to_download() -> dict:
    magazines = {}
    for num_sheet in range(1, 11): #NUM_SHEETS + 1):
        logging.info(f"{num_sheet=}")
        url = BASE_URL.format(num_sheet=num_sheet)
        try:
            response = urlopen(url)
        except Exception as err:
            logging.error(err)
            continue
        data = response.read() # out_temp(data)
        soup = BeautifulSoup(data, features="lxml")

        all_elems = soup.find_all('a',
                                  href=re.compile(LINK_REGEX_HREF_CONTENT))
        logging.debug(f"len(all_elems) = {len(all_elems)}")
        if not all_elems:
            logging.info('HAS NO ELEMENTS: all_elems')
            continue
        href = all_elems[0].attrs['href']
        fname = href.split('/')[-1]
        magazines[num_sheet] = [(href, fname)]
        for a_elem in all_elems[1:]:
            href = a_elem.attrs['href']
            fname = a_elem.text + '.pdf'
            magazines[num_sheet].append((href, fname))
    return magazines


def dump_magazines(magazines: dict) -> None:
    DST_MAGAZINES_JSON.write_text(json.dumps(magazines, sort_keys=True))

def download_all_magazines(magazines: dict) -> None:
    for num_sheet in sorted(int(key) for key in magazines):
        logging.info(f"{num_sheet=}")
        values = magazines[str(num_sheet)]
        dirpath = DST_MAGAZINES / str(num_sheet)
        if not dirpath.is_dir():
            os.mkdir(dirpath)
        for href, fname in values:
            try:
                with (dirpath / fname).open('wb') as out_fh:
                    resp = urlopen(href)
                    pdf_data = resp.read()
                    out_fh.write(pdf_data)
            except Exception as err:
                logging.error(err)


def main():
    setup()
    # magazines = get_all_magazines_links_to_download()
    # dump_magazines(magazines)
    magazines = json.loads(DST_MAGAZINES_JSON.read_bytes().decode(), encoding='utf8')
    download_all_magazines(magazines)


if __name__ == '__main__':
    main()