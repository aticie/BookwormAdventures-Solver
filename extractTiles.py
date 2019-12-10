import cv2
import numpy as np
import os
from findBookwormWindow import findWindowDims
from mss import mss

cwd = os.getcwd()
os.makedirs("tiles", exist_ok=True)

tiles = os.listdir("tile")
tiles_dict = {}
for tile in tiles:
    tile_name = tile[0]
    this_tile = cv2.imread(os.path.join("tile", tile))
    this_tile = cv2.cvtColor(this_tile, cv2.COLOR_BGR2GRAY)
    thr_tile = cv2.threshold(this_tile, 5, 255, cv2.THRESH_BINARY_INV)
    tiles_dict[tile_name] = thr_tile

save_path = os.path.join(cwd, "tiles")

with mss() as sct:
    frameNo = 0
    start = False
    while True:
        frameNo += 1
        x, y, w, h = findWindowDims()
        top = y + h // 2 + 21
        left = x + w // 2 - 99

        monitor = {"top": top, "left": left, "width": 200, "height": 203}

        img = np.array(sct.grab(monitor))
        cv2.imshow("Tiles", img)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord(' '):
            if not start:
                start = True
            else:
                start = False

        if not start:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        ret, thresh = cv2.threshold(img, 5, 255, cv2.THRESH_BINARY_INV)

        seen_tiles = []

        for i in range(4):
            for j in range(4):
                cur_tile = thresh[i * 50 + i: (i + 1) * 50 + i, j * 50: (j + 1) * 50].copy()
                seen_tiles.append(cur_tile)

        unknown = 0

        for tile in seen_tiles:
            errors = {}
            for tile_name, tile2 in tiles_dict.items():
                errors[tile_name] = np.mean(tile != tile2[1])

            key_min = min(errors.keys(), key=(lambda k: errors[k]))
            save_folder = os.path.join(save_path, key_min)
            os.makedirs(save_folder, exist_ok=True)
            save_this = os.path.join(save_folder, f"{frameNo}.jpg")
            cv2.imwrite(save_this, tile)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break


