import curses
import os

import more_itertools

from pyhstr.util import Counter


PATH = os.path.expanduser("~/.python_history")
COLORS = {
    "normal": 1,
    "highlighted-white": 2,
    "highlighted-green": 3
}
PYHSTR_LABEL = "Type to filter, UP/DOWN move, RET/TAB select, DEL remove, C-f add favorite, ESC quit"
PYHSTR_STATUS = f"- mode:std (C-/) - match:exact (C-e) - case:sensitive (C-t) - 0/8"
 

class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.all_entries = self.read_history()
        self.search_string = ""
        self.page = Counter()
        self.selected = Counter()

    def _addstr(self, y_coord, x_coord, text, color_info):
        """
        Works around curses' limitation of drawing at bottom right corner
        of the screen, as seen on https://stackoverflow.com/q/36387625
        """
        screen_height, screen_width = self.stdscr.getmaxyx()
        if x_coord + len(text) == screen_width and y_coord == screen_height-1:
            try:
                self.stdscr.addstr(y_coord, x_coord, text, color_info)
            except curses.error:
                pass
        else:
            self.stdscr.addstr(y_coord, x_coord, text, color_info)

    def read_history(self):
        history = []
        with open(PATH, "r") as f:
            for command in f:
                command = command.strip()
                if command not in history:
                    history.append(command)
        return list(more_itertools.sliced(history, curses.LINES - 3)) # account for 3 lines at the top

    def populate_screen(self, entries):
        self.stdscr.clear()
        for index, entry in enumerate(entries):
            if index == self.selected.value:
                self._addstr(index + 3, 0, entry.ljust(curses.COLS), curses.color_pair(COLORS["highlighted-green"]))
            else:
                self._addstr(index + 3, 0, entry.ljust(curses.COLS), curses.color_pair(COLORS["normal"]))
        self._addstr(1, 0, PYHSTR_LABEL, curses.color_pair(COLORS["normal"]))
        self._addstr(2, 0, PYHSTR_STATUS.ljust(curses.COLS), curses.color_pair(COLORS["highlighted-white"]))
        self._addstr(0, 0, f">>> {self.search_string}", curses.color_pair(COLORS["normal"]))

    def init_color_pairs(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, 0, 15)
        curses.init_pair(3, 15, curses.COLOR_GREEN)


def main(stdscr):
    app = App(stdscr)
    app.init_color_pairs()
    app.populate_screen(app.all_entries[app.page.value])

    while True:
        try:
            user_input = app.stdscr.getch()
        except curses.error:
            continue

        if user_input == 27: # ESC
            break

if __name__ == "__main__":
    curses.wrapper(main)
