# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# 
# [Directory Manager]
# 
# Author: Manuel Chinchi
# Version: 1.0.0
# Licence: GPL
# 
# -----------------------------------------------------------

# utils
# https://stackoverflow.com/questions/1679384/converting-dictionary-to-list

import json
import os

DEFAULT__LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT__FILE_CONFIG = "config.json"

DEFAULT__DIR = "."


OPTION_MIN = 1
OPTION_MAX = 2
OPTION__CANCEL = "e"
OPTION__LIST_DIRECTORIES = 1
OPTION__INTERACTIVELY_DIRECTORIES = 2
OPTION__TOP_DIRECTORY = "."


TEXT__HEADER_SCRIPT = \
"""\
@-------------------------@
|    Utils for Windows    |
|           ---           |
|         (v 1.0)         |
@-------------------------@
"""
TEXT__HEADER_SCRIPT = ""
TEXT__MENU_SCRIPT = \
"""\
1. List all directories
2. Interactive directory tree
"""
TEXT__LINE_WIDTH_X80         = ("-"*3)+"DIRECTORIES"+("-"*77)
TEXT__LINE_WIDTH_X80_END     = ("-"*3)+"___________"+("-"*77)
TEXT__SELECT_OPTION          = "> Select option ('e' -> exit):\n"
TEXT__RETRY_SELECT_OPTION    = "> Please, select option ('e' -> exit):\n"
TEXT__SELECT_DIRECTORY       = "> Select index of directory or write name ('c' -> exit | '..' -> top level):\n"
TEXT__RETRY_SELECT_DIRECTORY = "> Please, select index of directory or write name ('c' -> exit | '..' -> top level):\n"
TEXT__FINISH_SCRIPT          = "> Finish script"
TEXT__NO_DIRECTORIES         = "> Empty"
TEXT__YOU_HERE               = "> You here: %s"
TEXT__EMPTY                  = ""

class TextStyle:
    AFTER = 1
    BEFORE = 2

class MapCharStyle:
    DEFAULT = {
        'corner_left'   : '+',
        'corner_right'  : '+',
        'horizontal'    : '-',
        'vertical'      : '|',
        'border_left'   : '|',
        'border_right'  : '|',
        'space'         : ' ',
        'indicator'     : '¬',
        'corner_left2'  : '+',
        'corner_right2' : '+',
        'cursor'        : ':'
    }
    SIMPLE_BORDER = {
        'corner_left'   : '┌', # 219
        'corner_right'  : '┐', # 192
        'horizontal'    : '─', # 197
        'vertical'      : '│', # 180
        'border_left'   : '┤',
        'border_right'  : '├',
        'space'         : ' ',
        'indicator'     : '→', # 175,
        'corner_left2'  : '└',
        'corner_right2' : '┘',
        'cursor'        : '►'
    }
    DOUBLE_BORDER = {
        'corner_left'   : '╔', # 202
        'corner_right'  : '╗', # 188
        'horizontal'    : '═', # 206
        'vertical'      : '║', # 187
        'border_left'   : '╣', # 186
        'border_right'  : '╠', # 205
        'space'         : ' ',
        'indicator'     : '»',  # 175
        'corner_left2'  : '╚',
        'corner_right2' : '╝',
        'cursor'        : '►'
    }

class GUIConsole:
    import sys
    sys.stdout.reconfigure(encoding='utf-8') # configuration for ascii extended chars

    def __init__(self, map_chars, width=80):
        self.map_chars = map_chars
        self.width = width
        self.text_title = ""
        self.text_body = ""
        self.text_fotter = ""

    def draw_title(self, text=""):
        title_text = text if text != "" else self.text_title
        large_text = self.width - len(text) - 6
        large_text_left = int(large_text / 2)
        large_text_right = int(large_text / 2)

        final_text = \
            self.map_chars['corner_left'] + \
            self.map_chars['horizontal'] * large_text_left + \
            self.map_chars['border_left'] + \
            self.map_chars['space'] + \
            title_text + \
            self.map_chars['space'] + \
            self.map_chars['border_right'] + \
            self.map_chars['horizontal'] * large_text_right + \
            self.map_chars['corner_right']

        if len(final_text) < self.width:
            final_text = \
                final_text[:-1] + \
                self.map_chars['horizontal'] + self.map_chars['corner_right']
        print(final_text)

    def draw_body(self, text=None):
        body_text = text if text != None else self.text_body
        for l in body_text:
            print("{} {}".format(self.map_chars['vertical'], l))

    def draw_footer(self, text=None):
        footer_text = text if text != None else self.text_fotter
        large_text = self.width - 2
        pre_final_text = \
            self.map_chars['border_right'] + \
            self.map_chars['horizontal'] * large_text + \
            self.map_chars['border_left']


        pos_final_text = \
            self.map_chars['corner_left2'] + \
            self.map_chars['horizontal'] * large_text + \
            self.map_chars['corner_right2']

        print(pre_final_text)
        for l in footer_text:
            print("{} {} {}".format(
                self.map_chars['vertical'],
                self.map_chars['indicator'],
                l))
        print(pos_final_text)

    def input(self, text=""):
        value = input("{}{}".format(text, self.map_chars['cursor']))
        return value

def list_directories(dir=DEFAULT__DIR):
    """Show list directories in order."""
    arr_dirs = os.listdir(dir)
    arr_dirs.sort()
    for i, d in enumerate(arr_dirs):
        if " " in d:
            print("{}. '{}'".format(i+1, d))
        else:
            print("{}. {}".format(i+1, d))

def get_directories(dir=DEFAULT__DIR, order=False):
    """Get list of directories in order."""
    dirs = os.listdir(dir)
    dirs.sort()
    return dirs

def get_enum_directories(dir=DEFAULT__DIR):
    return dict(enumerate(get_directories(dir), start=1))

def is_valid_option(option):
    """Check that the option input of user are valid."""
    return \
        (
            isinstance(option, int) and \
            (option >= OPTION_MIN and option <= OPTION_MAX) \
        ) or \
        (
            isinstance(option, str) and \
            option == OPTION__CANCEL
        )

def is_valid_option_C2(option, list_dirs):
    return \
        option in list_dirs \
        or \
        option == OPTION__CANCEL \
        or \
        option == OPTION__TOP_DIRECTORY

def get_current_dir():
    return os.getcwd()

def set_current_dir(dir):
    os.chdir(dir)

def input_option(message=""):
    """Handles input exception that may occur when entering an option."""
    try:
        option = input(message)
        option = int(option)
    except ValueError as e:
        return option
    finally:
        return option

def load_config(file_config=DEFAULT__FILE_CONFIG):
    with open(file_config) as f:
        json_data = json.load(f)

    os.chdir(json_data["origin_path"])

def run_option():
    gc = GUIConsole(map_chars=MapCharStyle.SIMPLE_BORDER, width=80)
    # TODO
    # change logic loop menu
    option = 2

    if option == OPTION__CANCEL:
        exit("Finish script")

    elif option == OPTION__LIST_DIRECTORIES:
        lines_body = ["{}. {}".format(k,v) for k,v in get_enum_directories().items()]
        gc.draw_body(lines_body)

    elif option == OPTION__INTERACTIVELY_DIRECTORIES:
        select_dir = None
        current_dir = get_current_dir()

        while select_dir != OPTION__CANCEL:
            gc.draw_title(get_current_dir())

            if len(get_directories()) == 0:
                gc.draw_body(["--No directories--"])
            else:
                lines_body = ["{}. {}".format(k,v) for k,v in get_enum_directories().items()]
                gc.draw_body(lines_body)

            gc.draw_footer(["[e] Exit", "[.] Top directory"])            
            select_dir = gc.input(" ")
            try:
                select_dir = int(select_dir)
            except ValueError:
                select_dir = select_dir

            while select_dir != OPTION__CANCEL and \
                select_dir != OPTION__TOP_DIRECTORY and \
                (
                    select_dir not in get_directories() and \
                    select_dir not in list((get_enum_directories()).keys()) \
                ):
                select_dir = gc.input(" Error:\n ")

                if select_dir == OPTION__CANCEL:
                    break
                pass

            if select_dir == OPTION__CANCEL:
                exit(" Finish script")
            elif select_dir == OPTION__TOP_DIRECTORY:
                select_dir = ".."
                os.chdir(current_dir + "\\" + select_dir)
            else: # OPTION__CHANGE_DIRECTORY
                # TODO refactor this section
                if isinstance(select_dir, int) == True:
                    select_dir = get_enum_directories()[select_dir]
                os.chdir(current_dir + "\\" + select_dir)
                
            current_dir = os.getcwd()
            print(TEXT__EMPTY)

        print(select_dir)
    exit()

def main():
    load_config(DEFAULT__LOCAL_PATH + "\\config.json")
    run_option()

main()
