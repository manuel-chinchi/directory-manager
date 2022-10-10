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

import os
import json


DEFAULT__JSON_CONFIG = "config.json"

DEFAULT__DIR = "."


OPTION_MIN = 1
OPTION_MAX = 2
OPTION__CANCEL = "c"
OPTION__LIST_DIRECTORIES = 1
OPTION__INTERACTIVELY_DIRECTORIES = 2
OPTION__TOP_DIRECTORY = ".."


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
TEXT__SELECT_OPTION          = "> Select option ('c' -> cancel):\n"
TEXT__RETRY_SELECT_OPTION    = "> Please, select option ('c' -> cancel):\n"
TEXT__SELECT_DIRECTORY       = "> Select directory or index ('c' -> cancel | '..' -> top level):\n"
TEXT__RETRY_SELECT_DIRECTORY = "> Please, select directory or index ('c' -> cancel | '..' -> top level):\n"
TEXT__FINISH_SCRIPT          = "> Finish script"
TEXT__NO_DIRECTORIES         = "> Empty"
TEXT__YOU_HERE               = "> You here: %s"


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

def load_config(file_config=DEFAULT__JSON_CONFIG):
    with open(file_config) as f:
        json_data = json.load(f)

    os.chdir(json_data["path"])

def run_option():

    option = input_option(TEXT__SELECT_OPTION)
    while is_valid_option(option) == False:
        option = input_option(TEXT__RETRY_SELECT_OPTION)

    if option == OPTION__CANCEL:
        exit(TEXT__FINISH_SCRIPT)

    elif option == OPTION__LIST_DIRECTORIES:
        print(TEXT__LINE_WIDTH_X80)
        list_directories()
        print(TEXT__LINE_WIDTH_X80_END)

    elif option == OPTION__INTERACTIVELY_DIRECTORIES:
        select_dir = None
        current_dir = get_current_dir()

        while select_dir != OPTION__CANCEL:
            print(TEXT__LINE_WIDTH_X80)

            if len(get_directories()) == 0:
                print(TEXT__NO_DIRECTORIES)
            else:
                list_directories()

            print(TEXT__LINE_WIDTH_X80_END)
            print(TEXT__YOU_HERE % current_dir)
            
            select_dir = input_option(TEXT__SELECT_DIRECTORY)
            while select_dir != OPTION__CANCEL and \
                select_dir != OPTION__TOP_DIRECTORY and \
                (
                    select_dir not in get_directories() and \
                    select_dir not in list((get_enum_directories()).keys()) \
                ):
                select_dir = input_option(TEXT__RETRY_SELECT_DIRECTORY)

                if select_dir == OPTION__CANCEL:
                    break
                pass

            if select_dir == OPTION__CANCEL:
                exit(TEXT__FINISH_SCRIPT)
            elif select_dir == OPTION__TOP_DIRECTORY:
                os.chdir(current_dir + "\\" + select_dir)
            else: # OPTION__CHANGE_DIRECTORY
                # TODO refactor this section
                if isinstance(select_dir, int) == True:
                    select_dir = get_enum_directories()[select_dir]
                os.chdir(current_dir + "\\" + select_dir)
                
            current_dir = os.getcwd()
            print("")
    exit()

def main():
    print(TEXT__HEADER_SCRIPT)
    print(TEXT__MENU_SCRIPT)
    load_config()
    run_option()

main()
