from os.path import realpath, dirname
from pathlib import Path
TABLE_XPATH = r'//*[@id="content"]/div/div[1]/span/div/table/tbody'
FULL_SHEET_XPATH = r'//*[@id="content"]/div/div[1]/div[1]/a'
DEBUG = False
NUM_SHEETS = 121 if not DEBUG else 1
CUR_DIR = Path(dirname(realpath(__file__)))

BASE_URL = r'https://www.digitalwhisper.co.il/issue{num_sheet}'
LINK_REGEX_HREF_CONTENT = r'(http://www.digitalwhisper.co.il|\.\.)/files/Zines/0x(\d|[a-fA-F]){0,4}/.+?\.pdf'
DST_MAGAZINES = CUR_DIR / 'all_magazines'
DST_MAGAZINES_JSON = DST_MAGAZINES / 'magazines.json'