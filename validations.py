from constants import MONTHS
import utils
import google_sheets


def validate_month_format(month_input):
    """
    Checks the format and spelling of the user's 'month' input against a list
    of all 12 months when adding/editing an entry to ensure consistency and
    correctness.

    Parameters: month_input: users's month input from add_entry or edit_entry
    functions

    ROutputs: (boolean) returns True if input correctly formatted and present
    in month list, False if not
    """
    try:
        month, year = month_input.split()
        MONTHS.index(f"{month}")
        int(year)
        if len(year) != 4:
            raise ValueError()
    except (ValueError):
        utils.print_colour("Month must be in format MMM YYYY, e.g. Jan 2022\n"
                           "Please try again.\n", 'red')
        return False

    return True


def is_month_duplicate(month_input, user_id):
    """"""
    month_entries = [entry[1] for entry in
                     google_sheets.get_user_entries(user_id)]
    try:
        month_entries.index(month_input)
        utils.print_colour(f"Entry already exists for {month_input}.\n"
                           "Please try again.\n", 'red')
        return True
    except ValueError:
        return False


def validate_amount(amount):
    """
    Checks that the amount entered can be converted to a float and is therefore
    a valid income/outgoing entry

    Parameters: amount: users's income or outgoing input from add_entry or
    edit_entry functions

    Outputs:(boolean) returns True if input can be converted to a float value,
    False if not
    """
    try:
        if float(amount) < 0:
            raise ValueError
    except ValueError:
        utils.print_colour("Must be a positive number.\n"
                           f"You entered {amount}. Please try again\n", 'red')
        return False

    return True


def validate_entry_number(entry_num, user_entries):
    """
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
            return False
    except ValueError:
        return False

    return True


def validate_username_creation(username):
    """
    Prompts the user to choose a username. Validates by checking length
    and whether username already in use. Loops if invalid

    Parameters: none

    Outputs: returns username when passes validation
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


def validate_password_creation(password):
    """
    Prompts the user to choose a password. Checks if it meets all
    validation criteria and loops if it doesn't

    Parameters: none

    Outputs: returns password when passes validation
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


def validate_login_details(login_attempt):
    """
    Validates the user's login request

    Parameters: login_attempt: a dictionary of the user's input username and
    password

    Outputs: runs account menu if login valid, returns to login if invalid
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


def validate_menu_choice(response, limit):
    """
    Validates menu selection and raises error if invalid response entered

    Parameters: response: user's input response to menu selection,
    limit: limit of options in menu

    Outputs: (boolena) returns True if input is within limit and an integer,
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


def confirm_action(action):
    """"""
    print()
    print(f"Please enter 1 to confirm {action} or 2 to cancel.")
    menu_selection = input("Input 1 or 2:\n")
    print()
    if validate_menu_choice(menu_selection, 2):
        return True if int(menu_selection) == 1 else False
    else:
        confirm_action(action)
