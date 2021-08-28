from urllib.parse import urlencode

import requests

from .structures import PatentInfo


class Searcher:
    _URL = "https://yandex.com/patents"
    _BASIC_HEADERS = {
        "Host": "yandex.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.786 Yowser/2.5 Safari/537.36"
    }
    SLEEP_BETWEEN_SIMPLE_REQUEST = 5
    DOCS_PER_REQUEST = 50

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(self._BASIC_HEADERS)
        self._session.get(self._URL)

    def find_information_by_keyword(self, keyword) -> list:
        headers = {
            'Referer': f"https://yandex.com/patents?dco=RU&dco=SU&dl=ru&dt=0&dty=1&dty=2&s=0&sp=0&spp=10&st=0&{urlencode({'text': keyword})}"
        }
        result = []
        p = 0
        url = self.create_url_with_payload(keyword, p)
        json_content = self._session.get(url, headers=headers).json()
        doc_amount = json_content['TotalDocCount']
        max_page = doc_amount[0] // self.DOCS_PER_REQUEST
        while p < max_page:
            url = self.create_url_with_payload(keyword, p)
            resp = self._session.get(url, headers=headers)
            if resp.status_code != requests.codes.OK:
                break
            json_content = resp.json()
            pattents = self.convert_patent_to_format(json_content['Grouping'][0])
            print(len(pattents))
            result.extend(pattents)
            p += 1
        return result

    def create_url_with_payload(self, keyword, p) -> str:
        payload = {
            "text": keyword,
            "template": "%request% << (s_19_country:RU) << (i_doc_type:1 | i_doc_type:2)",
            "p": p,
            "how": "rlv",
            "numdoc": 50
        }

        return f"{self._URL}/api/search?{urlencode(payload)}"

    @staticmethod
    def convert_patent_to_format(groups: dict) -> list:
        result = []
        for group in groups["Group"]:
            archive = group['Document'][0]['ArchiveInfo']
            attributes = archive['GtaRelatedAttribute']
            tags = {d['Key']: d['Value'] for d in attributes}
            patent = PatentInfo(
                title=tags.get('z_ru_54_name', ''),
                authors=tags.get('z_ru_72_author', ''),
                patent_owner=tags.get('z_ru_73_owner', ''),
                referat=tags.get('z_ru_claims', '')
            )
            result.append(patent)
        return result
