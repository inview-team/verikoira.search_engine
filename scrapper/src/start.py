from fips.robot import Searcher


if __name__ == '__main__':
    search = Searcher()
    print(search.get_info_from_url("https://www1.fips.ru/iiss/document.xhtml?faces-redirect=true&id=5cf866b080e4ed8ed4aae41dc5f7b544"))