__title__ = 'CTk Theme Builder'
__author__ = 'Clive Bostock'
__license__ = 'MIT - see LICENSE.md'

# A hat tip and thankyou, to Tom Schimansky for his excellent work with CustomTkinter.
# Credit to my friend and colleague Jan Bejec, as well as my wife for their contributions to my logo.
# Also, a thankyou to Akash Bora for producing the excellent CTkToolTip and CTkMessagebox widgets.

import argparse
from ctk_themio.view.control_panel import ControlPanel
from argparse import HelpFormatter
from operator import attrgetter
import os
import re
from ctk_themio.view.ctk_theme_preview import PreviewPanel
from ctk_themio.model.ctk_theme_builder import log_call

# import lib.CTkMessagebox.ctkmessagebox

DEBUG = 0

preview_panel = None
PROG = os.path.basename(__file__)


@log_call
def valid_theme_name(theme_name):
    """
    Check if a theme name is safe for file paths and internal processing.
    
    Valid names contain only alphanumeric characters, underscores, parentheses, 
    and spaces. Returns True if valid, False otherwise.
    """
    pattern = re.compile(r"[A-Za-z0-9_()\s]+")
    if pattern.fullmatch(theme_name):
        return True
    else:
        return False


@log_call
def all_widget_attributes(widget_attributes):
    """
    Flatten a view schema into a single list of widget properties.
    
    The UI uses view schema files (like Basic.json) that group widget 
    properties into categories (e.g. "Colors", "Geometry"). This flattens 
    that nested dictionary into a simple list of property strings.
    """
    all_attributes = []
    for value_list in widget_attributes.values():
        all_attributes = all_attributes + value_list
    return all_attributes


def run_preview_panel(appearance_mode, theme_file):
    """
    Launch the preview panel standalone.
    
    This is used when the app is launched with a specific theme file 
    via CLI arguments, typically by the QA background process to 
    preview theme changes live.
    """
    global preview_panel
    preview_panel = PreviewPanel(appearance_mode=appearance_mode, theme_file=theme_file)


class SortingHelpFormatter(HelpFormatter):
    """Custom argparse formatter that sorts arguments alphabetically."""
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter('option_strings'))
        super(SortingHelpFormatter, self).add_arguments(actions)


def main():
    """
    Main entry point for CTk Theme Builder.
    
    Parses CLI arguments to determine launch mode:
    1. Normal mode (no args): Launches the full Control Panel editor.
    2. Preview mode (`-t theme.json`): Launches only the live preview panel. 
       This is used internally by the builder to spawn a separate preview process.
    """
    ap = argparse.ArgumentParser(formatter_class=SortingHelpFormatter,
                                 description=f"{PROG}: Welcome to CTk Theme Builder, which is designed to help you "
                                             f"design themes to run with the CustomTkinter framework")

    ap.add_argument("-a", '--set-appearance', required=False, action="store",
                    help="Set the CustomTkinter appearance mode. Used for colour preview only.",
                    dest='appearance_mode', default='Dark')

    ap.add_argument("-t", '--set-theme', required=False, action="store",
                    help="Set the CustomTkinter theme. Used for colour preview only.",
                    dest='theme_file', default=None)

    args_list = vars(ap.parse_args())
    appearance_mode = args_list["appearance_mode"]
    theme_file = args_list["theme_file"]

    # If theme is set, we assume we are running in "preview" mode.
    # This is how the QA background process launches.
    if theme_file is not None:
        run_preview_panel(appearance_mode=appearance_mode, theme_file=theme_file)
    else:
        ControlPanel()


if __name__ == "__main__":
    main()
