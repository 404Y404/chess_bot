from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import chess
import chess.engine

class Board():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.chess.com/")


    def parse(self):
        old_figures = list(map(get_class, self.browser.find_elements(By.CSS_SELECTOR, "#board-vs-personalities > .piece")))
        while True:
            print("start parse")
            new_figures = list(map(get_class, self.browser.find_elements(By.CSS_SELECTOR, "#board-vs-personalities > .piece")))
            for i in range(len(old_figures)):
                if old_figures[i] != new_figures[i] and "dragging" not in new_figures[i]:
                    return old_figures[i], new_figures[i]


    def move(self, element, x, y):
        piece = self.browser.find_element(By.CSS_SELECTOR, element)
        action = webdriver.common.action_chains.ActionChains(self.browser)
        action.move_to_element_with_offset(piece, 5, 5)
        action.click()
        action.perform()
        print("click")
        print(element, x, y)
        sleep(0.5)
        hint = self.browser.find_element(By.CSS_SELECTOR, f".square-{x}{y}")
        action = webdriver.common.action_chains.ActionChains(self.browser)
        action.move_to_element_with_offset(hint, 5, 5)
        action.click()
        action.perform()


def get_class(element):
    return element.get_attribute("class")


def to_chess_com(hod):
    letters = "abcdefgh"
    x = letters.index(hod[2]) + 1
    y = hod[3]
    hod = hod[:2]
    hod = hod.replace(hod[0], str(letters.index(hod[0]) + 1), 1)
    hod = f".square-{hod}"
    return hod, x, y


def to_bot(hod):
    letters = "abcdefgh"
    h1 = hod[0][16:]
    h2 = hod[1][16:]
    h1 = h1.replace(h1[0], letters[int(h1[0]) - 1], 1)
    h2 = h2.replace(h2[0], letters[int(h2[0]) - 1], 1)
    return h1 + h2

def main():
    board = chess.Board()
    board_player = Board()
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    limit = chess.engine.Limit(time=1.0)

    input("Зайдите в игру и нажмите Enter")
    c = 0
    while True:
        if c == 1:
            print("black")
            hod = board_player.parse()
            board.push(to_bot(hod))
        else:
            print("white")
            hod = str(engine.play(board, limit).move)
            move = chess.Move.from_uci(hod)
            board.push(move)
            print(hod)
            board_player.move(*to_chess_com(hod))
        hod = board_player.parse()
        c += 1
        c %= 2


    sleep(100)


if __name__ == '__main__':
    main()