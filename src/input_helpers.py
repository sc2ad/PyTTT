"""
Holds a variety of helper functions for input handling
"""

def selector(selection_string: str, options: "list[str]", default = None) -> str:
    """
    Asks the user for an option within a list of provided options and an optional default and returns their response
    """
    while True:
        if default:
            input_string = f"{selection_string} ({', '.join(options)}), default={default}: "
        else:
            input_string = f"{selection_string} ({', '.join(options)}): "
        option = input(input_string).strip().lower()
        if len(option) == 0 and default:
            return default
        if option in options:
            return option
        print(f"'{option}' is not a valid option! Valid options are: {', '.join(options)}")

def number(selection_string: str, minimum: int, maximum: int, default = None) -> int:
    """
    Asks the user for a number within the provided minimum and maximum with optional default and returns their response
    """
    while True:
        if default:
            input_string = f"{selection_string} default={default}: "
        else:
            input_string = f"{selection_string}: "
        option = input(input_string).strip()
        if len(option) == 0 and default:
            return default
        if not option.isnumeric():
            print(f"'{option} must be a valid number!")
        option = int(option)
        if option < minimum or option > maximum:
            print(f"{option} must be between: {minimum} and {maximum}!")
        else:
            return option

def get_marker(player: int, markers: "list[str]", default: str = None):
    """
    Asks the user for a tictactoe marker with an optional default and returns it
    """
    while True:
        if default:
            input_string = f"Enter the marker for player {player} default={default}: "
        else:
            input_string = f"Enter the marker for player {player}: "
        marker = input(input_string).strip()
        if len(marker) == 0 and default:
            return default
        if len(marker) != 1:
            print(f"'{marker}' is not a valid marker! A valid marker must be exactly one character!")
        elif marker in markers:
            print(f"'{marker}' is being used by a different player!")
        else:
            return marker
