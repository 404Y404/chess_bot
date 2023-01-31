from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class Board():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.chess.com/")


    def parse(self):
        old_figures = list(map(get_class, self.browser.find_elements(By.CSS_SELECTOR, "div .piece")))
        while True:
            new_figures = list(map(get_class, self.browser.find_elements(By.CSS_SELECTOR, "div .piece")))
            for i in range(len(old_figures)):
                if old_figures[i] != new_figures[i]:
                    return old_figures[i], new_figures[i]


def get_class(element):
    return element.get_attribute("class")


def main():
    board = Board()
    input("Зайдите в игру и нажмите Enter")
    while True:
        hod = board.parse()
        print(hod)


if __name__ == '__main__':
    main()