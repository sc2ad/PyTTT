
def selector(selection_string: str, options: "list[str]", default = None) -> str:
    while True:
        if default:
            input_string = f"{selection_string} ({', '.join(options)}), default={default}: "
        else:
            input_string = f"{selection_string} ({', '.join(options)}): "
        option = input(input_string).strip().lower()
        if len(option) == 0:
            if default:
                return default
        elif option in options:
            return option
        print(f"'{option}' is not a valid option! Valid options are: {', '.join(options)}")

def number(selection_string: str, min: int, max: int, default = None):
    while True:
        if default:
            input_string = f"{selection_string} default={default}: "
        else:
            input_string = f"{selection_string}: "
        option = input(input_string).strip()
        if len(option) == 0 and default:
            return default
        elif not option.isnumeric():
            print(f"'{option} must be a valid number!")
        option = int(option)
        if option < min or option > max:
            print(f"{option} must be between: {min} and {max}!")
        else:
            return option

def get_marker(player: int, markers: "list[str]", default: str = None):
    while True:
        if default:
            input_string = f"Enter the marker for player {player} default={default}: "
        else:
            input_string = f"Enter the marker for player {player}: "
        marker = input(input_string).strip()
        if len(marker) == 0 and default:
            return default
        elif len(marker) != 1:
            print(f"'{marker}' is not a valid marker! A valid marker must be exactly one character!")
        elif marker in markers:
            print(f"'{marker}' is being used by a different player!")
        else:
            return marker
        