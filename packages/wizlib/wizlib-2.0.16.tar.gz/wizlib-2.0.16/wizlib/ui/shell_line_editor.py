from enum import Enum
import sys
import re

from readchar import readkey


if (sys.platform == "win32"):
    import ctypes
    from ctypes import wintypes
else:
    import termios

# https://stackoverflow.com/questions/35526014/how-can-i-get-the-cursors-position-in-an-ansi-terminal


def cursorPos():  # pragma: nocover
    if (sys.platform == "win32"):
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        OldStdinMode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)
    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            True
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        if (sys.platform == "win32"):
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)
    if (res):
        return (res.group("x"), res.group("y"))
    return (-1, -1)


def sequence(hexes: str) -> str:
    return bytes.fromhex(hexes).decode()


LEFT = sequence("1b5b44")
RIGHT = sequence("1b5b43")
BACKSPACE = sequence("7f")
BEGINNING = sequence("01")
END = sequence("05")
RETURN = sequence("0a")
ESC = sequence("1b")
TAB = sequence("09")
SHIFT_TAB = sequence("1b5b5a")
LEFT_WORD = sequence("1b62")
RIGHT_WORD = sequence("1b66")
KILL = sequence("0b")

RESET = ESC + "[0m"
FAINT = ESC + "[2m"
BOLD = ESC + "[1m"

WORD_SEPARATORS = ' -_.,'


def write(key):
    sys.stderr.write(key)
    sys.stderr.flush()


# "Fill" refers to the lighter text in the editor, to the right of (or instead
# of) user-typed text.
#
# States:
# - USER: User has typed something, so no fill
# - TAB: User has hit tab or shift-tab, show tab completion if any
# - DEFAULT: editor has a default value and user has typed nothing, so show
#   default if any
# - BLANK: user hit backspace to clear the fill

FillState = Enum('FillState', 'USER TAB DEFAULT BLANK')


class ShellLineEditor:  # pragma: nocover

    buf = ''
    pos = 0
    index = -1

    def __init__(self, choices=[], default=''):
        """Parameters:

        choices: List of string options for tab completion

        default: Starting string value, can be accepted by user pressing return
        """
        self.choices = choices
        self.default = default
        self.fillstate = FillState.DEFAULT

    def edit(self):
        write(RESET)
        while True:
            self.write_fill()
            key = readkey()
            self.clear_fill()
            if key == RETURN:
                break
            if key.isprintable():
                write(BOLD + key + self.buf[self.pos:] +
                      ('\b' * (len(self.buf) - self.pos)) + RESET)
                self.buf = self.buf[:self.pos] + key + self.buf[self.pos:]
                self.pos += 1
                self.fillstate = FillState.USER
            elif (key in [BACKSPACE, KILL]) and self.has_fill:
                # Backspace clears the fill
                self.fillstate = FillState.BLANK
            elif (key == BACKSPACE) and (self.pos > 0):
                write(BOLD + '\b' + self.buf[self.pos:] + ' ' +
                      ('\b' * (1 + len(self.buf) - self.pos)) + RESET)
                self.buf = self.buf[:self.pos-1] + self.buf[self.pos:]
                self.pos -= 1
                self.fillstate = FillState.USER if (
                    self.pos > 0) else FillState.DEFAULT
            elif key == LEFT and self.pos > 0:
                self.move_left()
                self.fillstate = FillState.USER
            elif key == RIGHT and self.pos < len(self.buf):
                self.move_right()
                self.fillstate = FillState.USER
            elif key == BEGINNING and self.pos > 0:
                self.move_beginning()
                self.fillstate = FillState.USER
            elif key == END and self.has_fill:
                self.accept_fill()
                self.fillstate = FillState.USER
            elif key == END and self.pos < len(self.buf):
                self.move_end_buf()
                self.fillstate = FillState.USER
            elif key == TAB and (choices := self.valid_choices):
                self.index = (self.index + 1) % len(choices)
                self.fillstate = FillState.TAB
            elif key == SHIFT_TAB and self.index > -1:
                self.index = (self.index - 1) % len(self.valid_choices)
                self.fillstate = FillState.TAB
            elif key == LEFT_WORD and self.pos > 0:
                while (self.pos > 0) and self.is_sep(self.pos - 1):
                    self.move_left()
                while (self.pos > 0) and not self.is_sep(self.pos - 1):
                    self.move_left()
                self.fillstate = FillState.USER
            elif key == RIGHT_WORD and self.pos < len(self.buf):
                while (self.pos < len(self.buf)) and self.is_sep(self.pos):
                    self.move_right()
                while (self.pos < len(self.buf)) and not self.is_sep(self.pos):
                    self.move_right()
                self.fillstate = FillState.USER
            elif key == KILL:
                chars = len(self.buf) - self.pos
                write(' ' * chars + '\b' * chars)
                self.buf = self.buf[:self.pos]
                self.fillstate = FillState.USER
            else:
                pass
        self.accept_fill()
        write(RETURN)
        return self.buf

    def is_sep(self, pos):
        return (self.buf[pos] in WORD_SEPARATORS)

    @property
    def has_fill(self):
        return self.fillstate in [FillState.DEFAULT, FillState.TAB]

    def accept_fill(self):
        if self.has_fill:
            write(BOLD + self.fill + RESET)
            self.buf += self.fill
            self.pos = len(self.buf)

    def move_left(self):
        write(LEFT)
        self.pos -= 1

    def move_right(self):
        write(RIGHT)
        self.pos += 1

    def move_beginning(self):
        while self.pos > 0:
            self.move_left()

    def move_end_buf(self):
        while self.pos < len(self.buf):
            self.move_right()

    def write_fill(self):
        if self.fillstate in [FillState.DEFAULT, FillState.TAB]:
            self.move_end_buf()
            write(FAINT + self.fill + '\b' * len(self.fill) + RESET)

    def clear_fill(self):
        if self.has_fill:
            self.move_end_buf()
            write(' ' * len(self.fill) + '\b' * len(self.fill))

    @property
    def fill(self):
        if self.fillstate == FillState.TAB:
            choice = self.valid_choices[self.index]
            return choice[len(self.last_word):]
        elif self.fillstate == FillState.DEFAULT:
            return self.default
        else:
            return ''

    @property
    def last_word(self):
        index = next((c for c in reversed(range(len(self.buf)))
                     if self.buf[c] in WORD_SEPARATORS), -1)
        return self.buf[index+1:]

    @property
    def valid_choices(self):
        # return [c for c in self.choices if c.startswith(self.buf)]
        return [c for c in self.choices if c.startswith(self.last_word)]
