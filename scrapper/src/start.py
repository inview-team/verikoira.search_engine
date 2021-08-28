from yandex_patents.robot import Searcher


if __name__ == '__main__':
    search = Searcher()
    search.find_information_by_keyword("pizza")
    # print(search.get_info_from_url("https://www1.fips.ru/iiss/document.xhtml?faces-redirect=true&id=aa0c8c9dec090a7ccc00eb61e55e2165"))