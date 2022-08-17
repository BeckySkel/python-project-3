"""
Module for storing supporting functions
"""

import os
from termcolor import colored


def display_logo():
    """
    Prints the logo to the terminal
    """
    # Logo created at https://patorjk.com/software/taag/
    print_colour("""
 ______  _     _ _____    ______ _______
(____  \| |   | (____ \  / _____|_______)
 ____)  ) |   | |_   \ \| /  ___ _____
|  __  (| |   | | |   | | | (___)  ___)
| |__)  ) |___| | |__/ /| \____/| |_____
|______/ \______|_____/  \_____/|_______)

""", 'green')


def check_exit(input_value: str) -> bool:
    """
    Checks if user has input 'exit' to cancel current action

    Parameters:
        input_value: str, the value the user submitted in the input field

    Outputs: bool, returns True if 'exit' was entered, returns False if not
    """
    if input_value.upper() == 'EXIT':
        print_colour("Exiting function and returning to menu.\n", 'yellow')
        return True

    return False


def calc_average(num_list: list):
    """
    Calculates the average of a list of numbers

    Parameters:
        num_list: list, the list of numbers to calculate the average of

    Outputs: float, returns the average as a float
    """
    average = sum(num_list)/len(num_list)
    return round(float(average), 2)


def clear_terminal():
    """
    Clears the termninal to hide any sensitive information
    """
    # code to clear terminal from
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')
    display_logo()


def currency(amount: str or float) -> float:
    """
    Formats input to read as standard currency

    Parameters:
        amount: str or float, the number to be formatted into currency

    Outputs: float, returns amount as float value rounded to 2 decimal places
    """
    amount_as_currency = round(float(amount), 2)
    return amount_as_currency


def print_colour(text: str, colour: str):
    """
    Uses termcolor to print coloured text to the terminal

    Parameters:
         text: str, the text to colour and print
         colour: str, the colour in which to display the text

    Outputs: prints text to terminal in desired colour
    """
    print(colored(text, colour, attrs=['bold']))
