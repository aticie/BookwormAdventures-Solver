import cv2
import os
from mss import mss
import numpy as np
import itertools
from findBookwormWindow import findWindowDims
import pyautogui


def createDict():
    print("Building dictionary . . . ")
    dict = {}
    file = open("words1.txt", "r")
    for word in file:
        word = word.strip().lower()
        sorted_word = ''.join(sorted(word))
        if sorted_word in dict:
            if word not in dict[sorted_word]:
                dict[sorted_word].append(word)
        else:
            dict[sorted_word] = [word]

    return dict


def readPresetTiles():
    tiles = os.listdir("tile")
    tiles_list = []
    for tile in tiles:
        tile_name = tile[0]
        this_tile = cv2.imread(os.path.join("tile", tile))
        this_tile = cv2.cvtColor(this_tile, cv2.COLOR_BGR2GRAY)
        thr_tile = cv2.threshold(this_tile, 5, 255, cv2.THRESH_BINARY_INV)
        tiles_list.append(thr_tile)

    return tiles_list


def printWords(frame, tiles_list):
    letters = [chr(x) for x in range(97, 123)]
    letters[16] = "qu"
    seen_tiles = []
    output = []
    for i in range(4):
        for j in range(4):
            cur_tile = frame[i * 50 + i: (i + 1) * 50 + i, j * 50: (j + 1) * 50].copy()
            seen_tiles.append(cur_tile)

    for tile in seen_tiles:
        ret, thresh_tile = cv2.threshold(tile, 5, 255, cv2.THRESH_BINARY_INV)
        errors = {}
        for tile_index, tile2 in enumerate(tiles_list):
            errors[letters[tile_index]] = np.mean(thresh_tile != tile2[1])
        key_min = min(errors.keys(), key=(lambda k: errors[k]))
        output.append(key_min)
    return output


def findPossibleWords(my_letters, dict):
    prev_results = []
    total_words = 0
    longestFound = False
    longest = ""
    i = 17
    while total_words == 0:
        i -= 1
        if i < 1:
            return
        word_count = 0
        for perm in itertools.combinations(my_letters, i):
            my_word = ''.join(sorted(perm))
            if my_word in dict:
                results = dict[my_word]
                for result in results:
                    if not result in prev_results:
                        prev_results.append(result)
                        word_count += 1
                        total_words += 1
                        print(f"{i} letter word: {result}")
                        if not longestFound:
                            longest = result
            if word_count > 0:
                break
    return longest


def clickLongestWord(longest_word, my_letters):
    if longest_word == None:
        return
    click_ind = []
    location_dict = {}

    for ind, letter in enumerate(my_letters):
        if letter not in location_dict:
            location_dict[letter] = [ind]
        else:
            location_dict[letter].append(ind)

    for ch in longest_word:
        index = location_dict[ch][0]
        click_ind.append(index)
        location_dict[ch].remove(index)

    firstRun = True
    for ind in click_ind:
        x, y, w, h = findWindowDims()
        top = y + h // 2 + 21 + 25
        left = x + w // 2 - 99 + 25
        x_shift = (ind % 4) * 50
        y_shift = (ind // 4) * 50
        click_x = left + x_shift
        click_y = top + y_shift
        pyautogui.moveTo(click_x, click_y, duration=0)
        if firstRun:
            pyautogui.click(click_x, click_y, duration=0.2)
            pyautogui.click(click_x, click_y, duration=0.2)
            firstRun = False
        pyautogui.click(click_x, click_y, duration=0.2)
        #print(top, left, click_x, click_y)
    x, y, w, h = findWindowDims()
    pyautogui.moveTo(x+w//2, y+h-40, duration=0.2)
    pyautogui.click(x+w//2, y+h-40, duration=0.2)

    return click_ind


def main(dict, tiles_list):
    with mss() as sct:
        while True:
            x, y, w, h = findWindowDims()
            monitor = {"top": y + h // 2 + 21, "left": x + w // 2 - 99, "width": 200, "height": 203}
            img = np.array(sct.grab(monitor))
            cv2.imshow("Tiles", img)

            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            img_copy = img.copy()

            key = cv2.waitKey(1)
            if key & 0xFF == ord("x"):
                my_letters = printWords(img_copy, tiles_list)
                if len(my_letters) != 16:
                    print(f"Missed {16 - len(my_letters)} letter(s)...")
                longest_word = findPossibleWords(my_letters, dict)
                clickLongestWord(longest_word, my_letters)
            if key & 0xFF == ord("q"):
                break


if __name__ == "__main__":
    dict = createDict()
    tiles_list = readPresetTiles()
    main(dict, tiles_list)
