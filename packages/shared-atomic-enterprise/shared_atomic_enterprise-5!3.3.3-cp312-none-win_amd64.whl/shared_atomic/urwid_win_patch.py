"""
Patch urwid on Windows and WSL.

On Windows, install the package "windows-curses".
"""
import curses
def initscr():
    import _curses, curses
    # we call setupterm() here because it raises an error
    # instead of calling exit() in error cases.
    #setupterm(term=_os.environ.get("TERM", "unknown"),
    #          fd=_sys.__stdout__.fileno())
    stdscr = _curses.initscr()
    for key, value in _curses.__dict__.items():
        if key[0:4] == 'ACS_' or key in ('LINES', 'COLS'):
            setattr(curses, key, value)

    return stdscr
curses.initscr=initscr

import platform
import re

import urwid
import urwid.curses_display
import urwid.raw_display

IS_WSL = ("Linux" in platform.platform()) and ("Microsoft" in platform.platform())
IS_WINDOWS = ("Windows" in platform.platform()) and ("Linux" not in platform.platform())

if IS_WSL:
    # Filter out SI/SO under WSL. See:
    # https://github.com/mitmproxy/mitmproxy/blob/8dfb8a9a7471e00b0f723de66d3b63bd089e9802/mitmproxy/tools/console/window.py#L316-L323
    wsl_patch_orig_write = urwid.raw_display.Screen.write
    wsl_patch_write_re = re.compile("[\x0e\x0f]")

    def wsl_patch_write(self, data):
        data = wsl_patch_write_re.sub("", data)
        return wsl_patch_orig_write(self, data)

    urwid.raw_display.Screen.write = wsl_patch_write

if IS_WINDOWS:
    def win_patch_tty_signal_keys(self, intr=None, quit=None, start=None, stop=None, susp=None, fileno=None):
        pass  # no signals on Windows; not needed for resize
    urwid.display_common.RealTerminal.tty_signal_keys = win_patch_tty_signal_keys

    win_patch_orig__start = urwid.curses_display.Screen._start
    def win_patch__start(self):
        win_patch_orig__start(self)
        # halfdelay() seems unnecessary and causes everything to slow down a lot.
        curses.nocbreak()  # exits halfdelay mode
        # keypad(1) is needed, or we get no special keys (cursor keys, etc.)
        self.s.keypad(1)
    urwid.curses_display.Screen._start = win_patch__start

    # The getch functions in urwid.curses_display really don't work well on Windows
    # for some reason. You end up with >1s delays on input. It looks like halfdelay()
    # might work differently under windows-curses (which wraps PDCurses), or possibly
    # not support delays and blocking/non-blocking modes exactly correctly. These rewrites
    # simplify urwid's implementation a lot: they ignore most of urwid's delay handling,
    # but they seem to work ok.
    def win_patch__getch(self, wait_tenths):
        if wait_tenths == 0:
            return self._getch_nodelay()

        self.s.nodelay(False)
        return self.s.getch()
    urwid.curses_display.Screen._getch = win_patch__getch

    def win_patch__getch_nodelay(self):
        self.s.nodelay(True)
        return self.s.getch()
    urwid.curses_display.Screen._getch_nodelay = win_patch__getch_nodelay

    # The Windows terminal uses a different colour numbering.
    def win_patch__setup_colour_pairs(self):
        if not self.has_color:
            return

        self.has_default_colors = False
        colour_correct = [
            curses.COLOR_BLACK,
            curses.COLOR_RED,
            curses.COLOR_GREEN,
            curses.COLOR_YELLOW,
            curses.COLOR_BLUE,
            curses.COLOR_MAGENTA,
            curses.COLOR_CYAN,
            curses.COLOR_WHITE,
        ]
        for fg in range(8):
            for bg in range(8):
                if fg == curses.COLOR_WHITE and \
                   bg == curses.COLOR_BLACK:
                    continue

                curses.init_pair(bg * 8 + 7 - fg, colour_correct[fg], colour_correct[bg])
    urwid.curses_display.Screen._setup_colour_pairs = win_patch__setup_colour_pairs

    # Default to curses on Windows
    win_patch_orig_main_loop___init__ = \
        urwid.main_loop.MainLoop.__init__ if urwid.__version__ < '2.2.0' else urwid.MainLoop.__init__
    def win_patch_main_loop__init__(self, widget, palette=(), screen=None,
            handle_mouse=True, input_filter=None, unhandled_input=None,
            event_loop=None, pop_ups=False):
        if screen == None:
            screen = urwid.curses_display.Screen()
        win_patch_orig_main_loop___init__(self, widget, palette, screen,
            handle_mouse, input_filter, unhandled_input, event_loop, pop_ups)
        if urwid.__version__ < '2.2.0':
            urwid.main_loop.MainLoop.__init__ = win_patch_main_loop__init__
        else:
            urwid.MainLoop.__init__ = win_patch_main_loop__init__


    # Some special keys seem to have different key codes under Windows.
    urwid.escape._keyconv[351] = 'shift tab'
    urwid.escape._keyconv[358] = 'end'
    urwid.curses_display.KEY_RESIZE = 546