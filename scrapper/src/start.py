from yandex_patents.robot import Searcher


if __name__ == '__main__':
    search = Searcher()
    print(search.find_information_by_keyword("пицца"))