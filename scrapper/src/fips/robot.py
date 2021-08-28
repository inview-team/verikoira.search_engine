import bs4
import requests
from bs4 import BeautifulSoup

from .structures import PatentInfo


class Searcher:
    _URL = "https://www1.fips.ru/iiss/search.xhtml"
    _BASIC_HEADERS = {
        "Cookie": "JSESSIONID=bfa7901fdd5cd6a28e58ca284e6a; _ym_uid=1630139283374097077; _ym_d=1630139283; _ga=GA1.2.1044616320.1630139283; _gid=GA1.2.497714431.1630139283; _ym_isad=2; special_v=no; special_fontsize=null; special_color=null; special_noimage=null; activepunktFont=null; activepunktColor=null; BX_USER_ID=a2f30ba6d6e4d8fa1f47d3d0d0d8be5e; PHPSESSID=5682eab5e24f4556f7ce2fa997f061c2; _ym_visorc=w",
        "Host": "www1.fips.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.786 Yowser/2.5 Safari/537.36"
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(self._BASIC_HEADERS)

    def get_info_from_url(self, url):
        page = self._session.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        text = soup.findAll('p')
        return self.covert_patent_to_format(text)

    @staticmethod
    def covert_patent_to_format(data: bs4.ResultSet) -> PatentInfo:
        result = [value.text for value in data]
        referat = ''
        index = 5
        while True:
            if result[index] == 'ИЗВЕЩЕНИЯ':
                break
            referat += result[index]
            index += 1
        patent = PatentInfo(
            title=result[4].replace("(54) ", ""),
            authors=result[2].split(':')[1].split(','),
            patent_owner=result[3].split(':')[1],
            referat=referat
        )
        return patent

