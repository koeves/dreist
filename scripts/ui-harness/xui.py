#!/usr/bin/env python3
"""Drive the standalone's window on Linux (X11 or XWayland) from a script:
find it, drag its window sizer, click and press keys. Only libX11 and libXtst
through ctypes, no extra packages.

  xui.py find <title>                                  window id and geometry
  xui.py sizer <title> <seconds> [hz] [grow_x grow_y]  drag the window sizer
  xui.py click <title> <x> <y>                         left click (window coordinates)
  xui.py key <title> <combo>...                        keys, e.g. space ctrl+z

Synthetic input goes to whatever window is under the pointer, so every
command checks that the app's window is there first and stops otherwise; it
never raises or focuses the window (start the app with DREIST_BACKGROUND_GUI=1
and keep it uncovered). The pointer moves for real while a command runs.
"""
import ctypes as C
import ctypes.util
import sys
import time

x11 = C.CDLL(ctypes.util.find_library("X11"))
xtst = C.CDLL(ctypes.util.find_library("Xtst"))

Window = C.c_ulong
Atom = C.c_ulong
x11.XOpenDisplay.restype = C.c_void_p
x11.XOpenDisplay.argtypes = [C.c_char_p]
x11.XDefaultRootWindow.restype = Window
x11.XDefaultRootWindow.argtypes = [C.c_void_p]
x11.XInternAtom.restype = Atom
x11.XInternAtom.argtypes = [C.c_void_p, C.c_char_p, C.c_int]
x11.XGetWindowProperty.argtypes = [C.c_void_p, Window, Atom, C.c_long, C.c_long, C.c_int, Atom, C.POINTER(Atom), C.POINTER(C.c_int),
                                   C.POINTER(C.c_ulong), C.POINTER(C.c_ulong), C.POINTER(C.c_void_p)]
x11.XQueryTree.argtypes = [C.c_void_p, Window, C.POINTER(Window), C.POINTER(Window), C.POINTER(C.POINTER(Window)), C.POINTER(C.c_uint)]
x11.XQueryPointer.argtypes = [C.c_void_p, Window, C.POINTER(Window), C.POINTER(Window), C.POINTER(C.c_int), C.POINTER(C.c_int),
                              C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(C.c_uint)]
x11.XFree.argtypes = [C.c_void_p]
x11.XFlush.argtypes = [C.c_void_p]
x11.XSync.argtypes = [C.c_void_p, C.c_int]
x11.XGetGeometry.argtypes = [C.c_void_p, Window, C.POINTER(Window), C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(C.c_uint),
                             C.POINTER(C.c_uint), C.POINTER(C.c_uint), C.POINTER(C.c_uint)]
x11.XTranslateCoordinates.argtypes = [C.c_void_p, Window, Window, C.c_int, C.c_int, C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(Window)]
x11.XStringToKeysym.restype = C.c_ulong
x11.XStringToKeysym.argtypes = [C.c_char_p]
x11.XKeysymToKeycode.restype = C.c_ubyte
x11.XKeysymToKeycode.argtypes = [C.c_void_p, C.c_ulong]
xtst.XTestFakeMotionEvent.argtypes = [C.c_void_p, C.c_int, C.c_int, C.c_int, C.c_ulong]
xtst.XTestFakeButtonEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]
xtst.XTestFakeKeyEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]

dpy = x11.XOpenDisplay(None)
if not dpy:
    sys.exit("no X display (DISPLAY not set?)")
root = x11.XDefaultRootWindow(dpy)


def prop(w, name, typ):
    a = x11.XInternAtom(dpy, name.encode(), 1)
    if not a:
        return None
    t, f, n, left, data = Atom(), C.c_int(), C.c_ulong(), C.c_ulong(), C.c_void_p()
    if x11.XGetWindowProperty(dpy, w, a, 0, 1024, 0, typ, C.byref(t), C.byref(f), C.byref(n), C.byref(left), C.byref(data)) != 0 or not data:
        return None
    try:
        return C.string_at(data, n.value) if f.value == 8 else None
    finally:
        x11.XFree(data)


def children(w):
    r, p, kids, n = Window(), Window(), C.POINTER(Window)(), C.c_uint()
    if not x11.XQueryTree(dpy, w, C.byref(r), C.byref(p), C.byref(kids), C.byref(n)):
        return []
    ids = [kids[i] for i in range(n.value)]
    if kids:
        x11.XFree(kids)
    return ids


def windows(w):
    for k in children(w):
        yield k
        yield from windows(k)


def find(title):
    """The app's own top-level window: titled <title>, not a window manager
    frame (mutter draws its frames as X windows with the same title)."""
    utf8 = x11.XInternAtom(dpy, b"UTF8_STRING", 0)
    for w in windows(root):
        name = prop(w, "_NET_WM_NAME", utf8) or prop(w, "WM_NAME", 31)  # 31 = XA_STRING
        cls = prop(w, "WM_CLASS", 31) or b""
        if name and name.decode(errors="replace") == title and cls and b"mutter-x11-frames" not in cls:
            return w
    sys.exit(f"no window titled {title!r}")


def geometry(w):
    r, x, y, wd, ht, b, d = Window(), C.c_int(), C.c_int(), C.c_uint(), C.c_uint(), C.c_uint(), C.c_uint()
    x11.XGetGeometry(dpy, w, C.byref(r), C.byref(x), C.byref(y), C.byref(wd), C.byref(ht), C.byref(b), C.byref(d))
    ax, ay, child = C.c_int(), C.c_int(), Window()
    x11.XTranslateCoordinates(dpy, w, root, 0, 0, C.byref(ax), C.byref(ay), C.byref(child))
    return ax.value, ay.value, wd.value, ht.value


def under_pointer():
    """The deepest X window under the pointer."""
    w = root
    while True:
        r, child, rx, ry, wx, wy, mask = Window(), Window(), C.c_int(), C.c_int(), C.c_int(), C.c_int(), C.c_uint()
        x11.XQueryPointer(dpy, w, C.byref(r), C.byref(child), C.byref(rx), C.byref(ry), C.byref(wx), C.byref(wy), C.byref(mask))
        if not child.value:
            return w
        w = child.value


def point_at(w, x, y):
    """Move the pointer to (x, y) in screen coordinates and stop unless the
    app's window (or one inside it) is what it lands on."""
    xtst.XTestFakeMotionEvent(dpy, -1, x, y, 0)
    x11.XSync(dpy, 0)
    time.sleep(0.05)
    inside = {w, *windows(w)}
    if under_pointer() not in inside:
        sys.exit("the app's window is covered at the target point; nothing was pressed")


def sizer(title, seconds, hz=60.0, grow_x=0, grow_y=0, shrink=0.25):
    """Drag the window sizer (the bottom-right 15x15 corner) back and forth
    for <seconds>, as a hand does: a 2 s triangle between the start size and
    start + grow (or (1 - shrink) of it without grow), then release."""
    w = find(title)
    ax, ay, w0, h0 = geometry(w)
    sx, sy = ax + w0 - 7, ay + h0 - 7
    point_at(w, sx, sy)
    xtst.XTestFakeButtonEvent(dpy, 1, 1, 0)
    x11.XFlush(dpy)
    steps = max(1, int(hz))
    end = time.time() + seconds
    i = sent = 0
    widest = (w0, h0)
    while time.time() < end:
        p = abs((i % (2 * steps)) - steps) / steps  # 1 -> 0 -> 1 over 2 s
        if grow_x or grow_y:
            dx, dy = int(grow_x * (1 - p)), int(grow_y * (1 - p))
        else:
            dx, dy = -int(w0 * shrink * (1 - p)), -int(h0 * shrink * (1 - p))
        xtst.XTestFakeMotionEvent(dpy, -1, sx + dx, sy + dy, 0)
        x11.XFlush(dpy)
        sent += 1
        i += 1
        time.sleep(1.0 / hz)
        if i % steps == 0:  # an end of the triangle: the window should have followed
            _, _, wn, hn = geometry(w)
            if (wn, hn) != (w0, h0):
                widest = (wn, hn)
    xtst.XTestFakeMotionEvent(dpy, -1, sx, sy, 0)
    xtst.XTestFakeButtonEvent(dpy, 1, 0, 0)
    x11.XSync(dpy, 0)
    time.sleep(0.5)
    _, _, w1, h1 = geometry(find(title))
    if widest == (w0, h0) and (w1, h1) == (w0, h0):
        sys.exit(f"sizer: the window stayed {w0}x{h0} during the drag (no window sizer in its bottom-right corner?)")
    print(f"sizer: {sent} moves over {seconds:g}s; window {w0}x{h0} -> {w1}x{h1} (moved to {widest[0]}x{widest[1]})")


def click(title, x, y):
    w = find(title)
    ax, ay, _, _ = geometry(w)
    point_at(w, ax + x, ay + y)
    xtst.XTestFakeButtonEvent(dpy, 1, 1, 0)
    xtst.XTestFakeButtonEvent(dpy, 1, 0, 20)
    x11.XFlush(dpy)


def key(title, *combos):
    """Keys go to the window with the keyboard focus: point at the app's
    window first (it takes the keys while the pointer is over it)."""
    w = find(title)
    ax, ay, wd, ht = geometry(w)
    point_at(w, ax + wd // 2, ay + ht // 2)
    alias = {"ctrl": "Control_L", "shift": "Shift_L", "alt": "Alt_L"}
    for combo in combos:
        codes = [x11.XKeysymToKeycode(dpy, x11.XStringToKeysym(alias.get(k, k).encode())) for k in combo.split("+")]
        for c in codes:
            xtst.XTestFakeKeyEvent(dpy, c, 1, 0)
        for c in reversed(codes):
            xtst.XTestFakeKeyEvent(dpy, c, 0, 10)
        x11.XFlush(dpy)
        time.sleep(0.05)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, title, a = sys.argv[1], sys.argv[2], sys.argv[3:]
    if cmd == "find":
        win = find(title)
        print(hex(win), "%d,%d %dx%d" % geometry(win))
    elif cmd == "sizer":
        sizer(title, float(a[0]), float(a[1]) if len(a) > 1 else 60.0, int(a[2]) if len(a) > 2 else 0, int(a[3]) if len(a) > 3 else 0)
    elif cmd == "click":
        click(title, int(a[0]), int(a[1]))
    elif cmd == "key":
        key(title, *a)
    else:
        sys.exit(__doc__)
