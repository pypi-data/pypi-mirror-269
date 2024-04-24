import sys

from readchar import readkey
from wizlib.rlinput import rlinput
from wizlib.ui import UI
from wizlib.ui.shell_line_editor import ShellLineEditor

INTERACTIVE = sys.stdin.isatty()


class ShellUI(UI):

    """The UI to execute one command passed in through the shell. There will be
    limited interactivity, if the user omits an argument on the command line,
    but otherwise this is a run and done situation.
    """

    name = "shell"

    def send(self, value: str):
        """Output some text"""
        if value:
            print(value, file=sys.stderr)

    def get_option_mini(self, chooser):
        """Get a choice from the user with a single keystroke"""
        # key = rlinput(chooser.prompt_string)
        print(chooser.prompt_string, end='', file=sys.stderr, flush=True)
        if INTERACTIVE:
            key = readkey()
        else:
            key = sys.stdin.read(1)
        print(file=sys.stderr, flush=True)
        return chooser.choice_by_key(key)

    def get_text(self, prompt):
        """Allow the user to input an arbitrary line of text"""
        sys.stderr.write(prompt)
        sys.stderr.flush()
        value = ShellLineEditor().edit()
        # value = input()
        return value
