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
        month = month_input.split()[0]
        year = month_input.split()[1]
        MONTHS.index(f"{month}")
        int(year)
        if len(year) != 4:
            raise ValueError()
    except (ValueError, IndexError):
        print("Month must be in format MMM YYYY", "e.g. Jan 2021, Nov 1998",
              "Please try again.\n")
        return False

    return True


def is_month_duplicate(month_input, user_id):
    """"""
    month_entries = [entry[1] for entry in
                     google_sheets.get_user_entries(user_id)]
    try:
        month_entries.index(month_input)
        print(f"Entry already exists for {month_input}, please try again.\n")
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
        print("Must be a positive number (rounded to 2 decimal places).\n"
              f"You entered {amount}. Please try again\n")
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
            print("Entry does not exist."
                  f"Please input one of the following: {entry_nums}")
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
    # usernames = USERS_SHEET.col_values(3)[1:]
    usernames = google_sheets.get_usernames()

    username_length = len(username)
    if username_length < 5:
        print("Username too short, please try again\n")
        return False
    elif username_length > 15:
        print("Username too long, please try again\n")
        return False
    else:
        if username in usernames:
            print("That username is unavailable, please try again\n")
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
        print("Password valid!\n")
        return True
    else:
        print("Password invalid. Please try again\n")
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
        # run.account_menu(user_id)
        return True
    except ValueError:
        print("Username or password incorrect. Please try again\n")
        # run.login()
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
        print("Invalid selection:",
              f"Please choose a number between 1 and {limit}.",
              f"You entered: {response}\n")
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
