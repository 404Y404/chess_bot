from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import chess
import chess.engine

class Board():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.chess.com/")


    def parse(self, old_hod):
        end = self.browser.find_element(By.XPATH,
                                        "//chess-board/div[contains(@class, 'highlight')][1]")
        start = self.browser.find_element(By.XPATH,
                                          "//chess-board/div[contains(@class, 'highlight')][2]")
        hod = to_bot(start.get_attribute("class")) + to_bot(end.get_attribute("class"))
        while hod == old_hod or hod[2:] + hod[:2] == old_hod:
            end = self.browser.find_element(By.XPATH, "//chess-board/div[2]")
            start = self.browser.find_element(By.XPATH, "//chess-board/div[3]")
            hod = to_bot(start.get_attribute("class")) + to_bot(end.get_attribute("class"))
            if old_hod != hod and hod[2:] + hod[:2] != old_hod:
                sleep(0.3)
                end = self.browser.find_element(By.XPATH, "//chess-board/div[2]")
                start = self.browser.find_element(By.XPATH, "//chess-board/div[3]")
                hod = to_bot(start.get_attribute("class")) + to_bot(end.get_attribute("class"))
        return hod


    def move(self, element, x, y, is_end, figura, mode):
        piece = self.browser.find_element(By.CSS_SELECTOR, element)
        action = webdriver.common.action_chains.ActionChains(self.browser)
        action.move_to_element_with_offset(piece, 5, 5)
        action.click()
        action.perform()
        sleep(0.1)
        hint = self.browser.find_element(By.CSS_SELECTOR, f".square-{x}{y}")
        action = webdriver.common.action_chains.ActionChains(self.browser)
        action.move_to_element_with_offset(hint, 5, 5)
        action.click()
        action.perform()
        if is_end:
            self.browser.find_element(By.CSS_SELECTOR, f'[class="promotion-piece {mode}{figura}"]').click()



def get_class(element):
    return element.get_attribute("class")


def to_chess_com(hod):
    if len(hod) > 4:
        hod2 = hod
        letters = "abcdefgh"
        x = letters.index(hod2[2]) + 1
        y = hod2[3]
        hod2 = hod2[:2]
        hod2 = hod2.replace(hod2[0], str(letters.index(hod2[0]) + 1), 1)
        hod2 = f".square-{hod2}"
        return hod2, x, y, True, hod[-1]
    hod2 = hod
    letters = "abcdefgh"
    x = letters.index(hod2[2]) + 1
    y = hod2[3]
    hod2 = hod2[:2]
    hod2 = hod2.replace(hod2[0], str(letters.index(hod2[0]) + 1), 1)
    hod2 = f".square-{hod2}"
    return hod2, x, y, False, ""


def to_bot(hod):
    letters = "abcdefgh"
    hod = hod[17:]
    hod = hod.replace(hod[0], letters[int(hod[0]) - 1], 1)
    return hod

def main():
    hod = ""
    board = chess.Board()
    board_player = Board()
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    limit = chess.engine.Limit(time=0.5)

    input("Зайдите в игру и нажмите Enter")
    mode = input("Введите w  или  b: ")
    if mode == "w":
        c = 0
    else:
        c = 1
    while True:
        if c == 1:
            hod = board_player.parse(hod)
            move = chess.Move.from_uci(hod)
            if move in board.legal_moves:
                print(hod)
                board.push(move)
            else:
                hod = hod[2:] + hod[:2]
                print(hod)
                move = chess.Move.from_uci(hod)
                board.push(move)
        else:
            hod = str(engine.play(board, limit).move)
            move = chess.Move.from_uci(hod)
            board.push(move)
            print(hod)
            board_player.move(*to_chess_com(hod), mode)
            if len(hod) > 4:
                hod = hod[:4]
        c += 1
        c %= 2
    sleep(100)


if __name__ == '__main__':
    main()