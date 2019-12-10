import win32gui

def callback(hwnd, extra):

    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    #print(win32gui.GetWindowText(hwnd))
    if win32gui.GetWindowText(hwnd) == "Bookworm Adventures Deluxe 1.0 ":
        #print(f"Window found: {win32gui.GetWindowText(hwnd)}")
        extra.append(((x, y), (w, h)))

def findWindowDims():
    extra = []
    win32gui.EnumWindows(callback, extra)
    (x, y), (w, h) = extra[0]
    return x, y, w, h

if __name__ == "__main__":

    a = findWindowDims()
    print(a)

