from urllib.parse import urlencode

import requests

from .structures import PatentInfo


class Searcher:
    _URL = "https://yandex.com/patents"
    _BASIC_HEADERS = {
        "Host": "yandex.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.786 Yowser/2.5 Safari/537.36"
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(self._BASIC_HEADERS)
        self._session.get(self._URL)

    def find_information_by_keyword(self, keyword) -> list:
        headers = {
            'Referer': f"https://yandex.com/patents?dco=RU&dco=SU&dl=ru&dt=0&dty=1&dty=2&s=0&sp=0&spp=10&st=0&{urlencode({'text': keyword})}"
        }
        payload = {
            "text": keyword,
            "template": "%request% << (s_19_country:RU) << (i_doc_type:1 | i_doc_type:2)",
            "p": 0,
            "how": "rlv",
            "numdoc": 10
        }
        url = f"{self._URL}/api/search?{urlencode(payload)}"
        json_content = self._session.get(url, headers=headers).json()
        return self.convert_patent_to_format(json_content['Grouping'][0])

    def get_patent_by_doc_id(self, doc_id: str):
        pass

    @staticmethod
    def convert_patent_to_format(groups: dict) -> list:
        result = []
        for group in groups["Group"]:
            attributes = group['Document'][0]['ArchiveInfo']['GtaRelatedAttribute']
            tags = {d['Key']: d['Value'] for d in attributes}
            patent = PatentInfo(
                title=tags.get('z_ru_54_name', ''),
                authors=tags.get('z_ru_72_author', ''),
                patent_owner=tags.get('z_ru_73_owner', ''),
                referat=tags.get('z_ru_claims', '')
            )
            result.append(patent)
        return result