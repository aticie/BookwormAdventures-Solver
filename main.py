import cv2
import os
from mss import mss
import numpy as np
import itertools
tiles = os.listdir("tile")

tiles_list = []
letters = [chr(x) for x in range(97, 123)]

letters[16] = "qu"

dict = {}  # Create empty dictionary
file = open("words1.txt", "r")

print("Building dictionary . . . ")
for word in file:
    word = word.strip().lower()
    sorted_word = ''.join(sorted(word))  # Alphabetically sort the word
    if sorted_word in dict:  # Check if sorted_word is already a key
        if word not in dict[sorted_word]:  # Make sure word is not already in the list under the key sorted_word
            dict[sorted_word].append(word)  # Add to list under the key sorted_word
    else:  # If not in dictionary
        dict[sorted_word] = [word]



for tile in tiles:
    tile_name = tile[0]
    this_tile = cv2.imread(os.path.join("tile", tile))
    this_tile = cv2.cvtColor(this_tile, cv2.COLOR_BGR2GRAY)
    thr_tile = cv2.threshold(this_tile, 5, 255, cv2.THRESH_BINARY_INV)
    tiles_list.append(thr_tile)

if not os.path.exists("seen_tiles"):
    os.mkdir("seen_tiles")


def printWords(frame):
    output = []
    for i in range(4):
        for j in range(4):
            cur_tile = frame[i * 50 + i: (i + 1) * 50 + i, j * 50: (j + 1) * 50].copy()
            seen_tiles.append(cur_tile)
            cv2.imwrite(os.path.join("seen_tiles", "{}_{}.jpg".format(i, j)), cur_tile)

    for tile in seen_tiles:
        ret, thresh_tile = cv2.threshold(tile, 5, 255, cv2.THRESH_BINARY_INV)
        for tile_index, tile2 in enumerate(tiles_list):
            error = np.mean(thresh_tile != tile2[1])
            if error < 0.01:
                output.append(letters[tile_index])
                # cv2.imshow("seen", tile)
                # cv2.waitKey(1)
    return output


# The simplest use, save a screen shot of the 1st monitor
with mss() as sct:
    monitor = {"top": 500, "left": 760, "width": 200, "height": 203}
    while True:
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

        cv2.imshow("Tiles", img)
        seen_tiles = []
        img_copy = img.copy()

        key = cv2.waitKey(10)
        if key & 0xFF == ord("x"):
            my_letters = printWords(img_copy)
            my_word = ''.join(sorted(my_letters))
            print(my_word)

            prev_results = []
            for i in range(8, 16, 1):
                word_count = 0
                for perm in itertools.combinations(my_letters, i):
                    my_word = ''.join(sorted(perm))
                    if my_word in dict:
                        results = dict[my_word]
                        if results != prev_results:
                            prev_results = results
                            word_count += 1
                            print(results)
                    if word_count > 3:
                        break


        if key & 0xFF == ord("q"):
            break
