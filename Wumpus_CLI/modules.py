import os
import json

ASSET_FOLDER = os.path.join(os.path.dirname(os.path.relpath(__file__)), "assets/")
DATA = "data.json"
HIGHSCORE = "highscore.txt"


def load_json(asset):
    """Loads a JSON file from the asset folder.
    In case it does not exist an error is printed, and game exits."""
    try:
        with open(os.path.join(ASSET_FOLDER, asset), 'r') as file:
            data = json.load(file)
            return data
    except IOError as message:
        print("Missing JSON. Please re-download the folder.")
        raise SystemExit(message)


def load_data(asset):
    """Loads a data file from the asset folder.
    In case the file does not exist, it is created."""
    try:
        with open(os.path.join(ASSET_FOLDER, asset), 'r') as file:
            data = file.read().splitlines()
            return data
    except IOError:
        with open(os.path.join(ASSET_FOLDER, asset), 'w+') as file:
            data = file.read().splitlines()
            return data


def output(category, title, player_pos=""):
    """A request for a specific string has been received.
    Calls for load of JSON file and prints out the corresponding string
    in the correct category."""
    data = load_json(DATA)

    if player_pos == "":
        print(str(data[category][title]))
    else:
        print(str(data[category][title] + str(player_pos) + "."))


def check_input(query, min_value, max_value):
    """Calls for check that input is numerical and
    calls for a check that it is within the given range that the callee function has specified"""
    while True:
        choice = input(query)
        if is_numerical(choice):
            if within_range(is_numerical(choice)[1], min_value, max_value):
                break
            else:
                print("\nAnge en siffra mellan " + str(min_value) + " och " + str(max_value) + ".")
        else:
            print("\nDu måste mata in en siffra.")
    return int(choice)


def is_numerical(query):
    """Checks that the input is numerical. Returns False otherwise."""
    try:
        value = int(query)
        return True, value
    except ValueError:
        return False


def within_range(value, min_value, max_value):
    """Checks that input is within a specified range."""
    if value in range(min_value, max_value + 1):
        return True, value
    else:
        return False


def string_check(query, char_1, char_2):
    """Asks for input, converts to lower case and checks
     if it matches any of two given characters."""
    try:
        string = input(query)
        if string != "":
            char = string[0].lower()
            if char == char_1:
                return char
            elif char == char_2:
                return char
            else:
                print("Du förstår inte vad du menar med '" + string + "'.")
    except KeyboardInterrupt:
        pass


def clear():
    """Clears screen independent of platform."""
    os.system('cls' if os.name == 'nt' else 'clear')


def wait(msg):
    """Waits for input before proceeding."""
    input("\n" + msg)
    clear()
