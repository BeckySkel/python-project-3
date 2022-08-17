"""
Module for storing functions used to validate input data
"""

from constants import MONTHS
import utils
import google_sheets


def validate_month_format(month_input: str) -> bool:
    """
    Checks the format and spelling of the user's 'month' input against a list
    of all 12 months when adding/editing an entry to ensure consistency and
    correctness. Also checks if year is integer in YYYY format.

    Parameters:
        month_input: str, users's month input from add_entry, edit_entry
        or edit_budget functions

    Outputs: bool, returns True if input correctly formatted and present
    in month list, False if not
    """
    try:
        month, year = month_input.split()
        MONTHS.index(f"{month}")
        int(year)
        if len(year) != 4:
            raise ValueError()
    except ValueError:
        utils.print_colour("Month must be in format MMM YYYY, e.g. Jan 2022\n"
                           "Please try again.\n", 'red')
        return False

    return True


def is_month_duplicate(month_input: str, user_id: int) -> bool:
    """
    Checks if entered month already exists in table

    Parameters:
        month_input: str, users's month input from add_entry function
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: bool, return True if month present or False if not
    """
    month_entries = [entry[1] for entry in
                     google_sheets.get_user_entries(user_id)]
    try:
        month_entries.index(month_input)
        utils.print_colour(f"Entry already exists for {month_input}.\n"
                           "Please try again.\n", 'red')
        return True
    except ValueError:
        return False


def validate_amount(amount: str) -> bool:
    """
    Checks that the amount entered can be converted to a float and is therefore
    a valid currency entry

    Parameters:
        amount: str, users's income or outgoing input from add_entry,
        edit_entry or edit_budget functions

    Outputs: bool, returns True if input can be converted to a float value,
    False if not or if below 0
    """
    try:
        if float(amount) < 0:
            raise ValueError
    except ValueError:
        utils.print_colour("Must be a positive number.\n"
                           f"You entered {amount}. Please try again\n", 'red')
        return False

    return True


def validate_entry_number(entry_num: str, user_entries: list) -> bool:
    """
    Validates that the number input is an integer and is present in the
    user's entry numbers

    Parameters:
        entry_num: str, entry that the user wishes to edit or remove
        user_entries: list, list of user's entry numbers

    Outputs: bool, returns True if valid or False if not
    """
    try:
        int(entry_num)
        entry_nums = []
        for entry in user_entries:
            entry_nums.append(int(entry[0]))
        if int(entry_num) not in entry_nums:
            utils.print_colour("Entry does not exist."
                               "Please input one of the following:", 'red')
            print(entry_nums)
            raise ValueError()
    except ValueError:
        return False

    return True


def validate_username_creation(username: str) -> bool:
    """
    Validates username input by checking length and whether
    username already in use.

    Parameters:
        username: str, The user's chosen username

    Outputs: bool, returns True if valid, False if not
    """
    usernames = google_sheets.get_usernames()

    username_length = len(username)
    if username_length < 5:
        utils.print_colour("Username too short, please try again\n", 'red')
        return False
    elif username_length > 15:
        utils.print_colour("Username too long, please try again\n", 'red')
        return False
    else:
        if username in usernames:
            utils.print_colour("Username unavailable, please try again\n",
                               'red')
            return False

    return True


def validate_password_creation(password: str) -> bool:
    """
    Validates user's chosen password. Checks if it meets criteria for length
    and minimums of each character-type (upper, lower and numbers)

    Parameters:
        password: str, The user's chosen username

    Outputs: bool, returns True if valid, False if not
    """
    pass_length = len(password)
    length_valid = True if pass_length >= 5 and pass_length <= 15 else False

    uppercase_count = 0
    lowercase_count = 0
    number_count = 0
    for char in password:
        try:
            int(char)
            number_count += 1
        except ValueError:
            if char.isupper():
                uppercase_count += 1
            if char.islower():
                lowercase_count += 1

    if length_valid and uppercase_count and lowercase_count and number_count:
        utils.print_colour("Password valid!\n", 'green')
        return True
    else:
        utils.print_colour("Password invalid. Please try again\n", 'red')
        return False


def validate_login_details(login_attempt: dict) -> bool:
    """
    Validates the user's login request

    Parameters:
        login_attempt: a dictionary with the username as the key and
        password as the value

    Outputs: bool, returns True if username and password combination
    present in database
    """
    usernames = google_sheets.get_usernames()
    passwords = google_sheets.get_passwords()

    login_list = []
    for username, password in zip(usernames, passwords):
        user = {username: password}
        login_list.append(user)

    try:
        login_list.index(login_attempt)
        utils.clear_terminal()
        print("Welcome back!\n")
        return True
    except ValueError:
        utils.print_colour("Username/password incorrect. Please try again\n",
                           'red')
        return False


def validate_menu_choice(response: str, limit: int) -> bool:
    """
    checks menu selection is integer and present in menu limit,
    raises error if selection is outside the limit.

    Parameters:
        response: str, user's input response to menu selection
        limit: int, number of options in menu

    Outputs: bool, returns True if input is within limit and an integer,
    returns False if not.
    """
    try:
        int(response)
        if int(response) > limit or int(response) < 1:
            raise ValueError()
        return True
    except ValueError:
        utils.print_colour("Invalid selection:\n"
                           f"Please choose a number between 1 and {limit}.\n"
                           f"You entered: {response}\n", 'red')
        return False


def confirm_action(action: str) -> bool:
    """
    Requests confirmation from user that they wish to continue with action

    Parameters:
        action: str, included in confirmation message desiplayed to user

    Outputs: bool, returns True if action confirmed, False if cancelled.
    Function repeats if invalid input.
    """
    print()
    print(f"Please enter 1 to confirm {action} or 2 to cancel.")
    menu_selection = input("Input 1 or 2:\n")
    print()
    if validate_menu_choice(menu_selection, 2):
        return True if int(menu_selection) == 1 else False
    else:
        confirm_action(action)
