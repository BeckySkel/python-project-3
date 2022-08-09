"""
Module for running full program and interacting with database
"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Google Sheets and gspread set-up by Code Institute Love Sandwiches project
# Imported to interact with savings_tracker database in Google Sheets
import gspread
from google.oauth2.service_account import Credentials
# Imported to display the user's data in an easy-to-read table
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Global constants
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('savings_tracker')
USERS_SHEET = SHEET.worksheet('users')
ENTRIES_SHEET = SHEET.worksheet('entries')
MONTHS = [
    'Jan', 'Feb', 'Mar',
    'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep',
    'Oct', 'Nov', 'Dec'
    ]


def validate_month(month_input):
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
        MONTHS.index(f"{month_input}")
    except ValueError:
        print("Month must be in format Jan, Feb, Jul, Nov, etc.",
              "Please try again.\n")
        return False

    return True


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
        float(amount)
    except ValueError:
        print("Amount must be a number (will be rounded to 2 decimal places).",
              f"You entered {amount}. Please try again")
        return False

    return True


def add_entry(user_id):
    """
    Allows user to add a new entry for their monthly spending data

    Parameters: user_id: the unique identifier of the user's account,
    used to manipulate the data of the user who is currently logged in

    Outputs: appends user's entered spending data to the database after
    running validation checks
    """
    print("ADD NEW ENTRY:\n")
    while True:
        month = input("Month:\n").lower().capitalize()
        if validate_month(month):
            break

    while True:
        income = input("Incoming(£):\n")
        if validate_amount(income):
            break

    while True:
        outgoing = input("Outgoing(£):\n")
        if validate_amount(outgoing):
            break

    income = round(float(income), 2)
    outgoing = round(float(outgoing), 2)
    net = income - outgoing
    entry_id = int(ENTRIES_SHEET.col_values(1)[-1])+1

    all_entries = ENTRIES_SHEET.get_all_values()
    user_entries_nums = []
    for entry in all_entries:
        try:
            uid = int(entry[1])
            if uid == user_id:
                user_entries_nums.append(int(entry[2]))
        except ValueError:
            pass
    user_entries_nums.sort()
    # create seperate function for fitering entries?

    entry_num = user_entries_nums[-1]+1

    ENTRIES_SHEET.append_row([entry_id, user_id, entry_num, month,
                             income, outgoing, net])


def remove_entry(user_id):
    """
    Allows user to remove an entry from their monthly spending data

    Parameters: user_id: the unique identifier of the user's account,
    used to manipulate the data of the user who is currently logged in

    Outputs: deletes row from entry data based on the user's unique ID
    and their inputted entry ID
    """
    print("REMOVE ENTRY:\n")
    entry_to_remove = input("Entry Number:\n")

    entry_dicts = ENTRIES_SHEET.get_all_records()

    for e_d in entry_dicts:
        uid = e_d.get('User ID')
        entry_num = e_d.get('Entry Number')
        if uid == user_id:
            if entry_num == int(entry_to_remove):
                entry = entry_dicts.index(e_d) + 2
                ENTRIES_SHEET.delete_rows(entry)
    # ADD VALIDATION??


def edit_goal(user_id):
    """
    PLACEHOLDER
    """
    print(f"success {user_id}")


def display_table(user_id):
    """
    Displays all of the current user's previous table entries

    Parameters: user_id: the unique identifier of the user's account,
    used to access and display the data of the user who is currently logged in

    Outputs: prints table of current user's spending data to the console
    """
    all_entries = ENTRIES_SHEET.get_all_values()

    current_user = []
    for entry in all_entries:
        try:
            uid = int(entry[1])
            if uid == user_id:
                current_user.append(entry[2:])
        except ValueError:
            pass
    # create seperate function for fitering entries?

    current_user.sort(key=MONTHS.index)

    # Code for creating a table from official tabulate documentation
    headers = ENTRIES_SHEET.row_values(1)[2:]
    print(tabulate(current_user, headers, tablefmt='psql'))
    print("Goal: \n")


def account_menu(user_id):
    """
    Displays the account menu with options for the user to add a new entry,
    remove a previous entry, edit their goals, view app information or logout

    Parameters: user_id: the unique identifier of the user's account,
    used to access the data of the user who is currently logged in

    Outputs: calls action_menu_choice function to select the next function to
    run based on user's input. Provides funtcion name and parameters via a
    list of dictionaries named menu_choices. Loops until user logs out
    """
    print("ACCOUNT:\n")
    display_table(user_id)
    print("""Please select an option from the below menu
    1- Add new entry
    2- Remove entry
    3- Edit Goal
    4- Help
    5- Logout
        """)
    menu_selection = input("Input 1, 2, 3, 4 or 5:\n")
    print()

    menu_choices = [{'name': add_entry, 'param1': user_id},
                    {'name': remove_entry, 'param1': user_id},
                    {'name': edit_goal, 'param1': user_id},
                    {'name': display_help, 'param1': 'account',
                    'param2': user_id}, {'name': logout}]

    if validate_menu_choice(menu_selection, 5):
        action_menu_choice(menu_selection, menu_choices)
    else:
        account_menu(user_id)

    print()
    account_menu(user_id)


def logout():
    """
    Returns the user to the main menu and lets them know that they have
    successfully logged out of the portal

    Parameters: none

    Outputs: prints a message to the console and calls the main_menu() function
    """
    print("Successfully logged out.")
    main_menu()


def validate_username_creation(username):
    """
    Prompts the user to choose a username. Validates by checking length
    and whether username already in use. Loops if invalid

    Parameters: none

    Outputs: returns username when passes validation
    """
    username_length = len(username)

    usernames = USERS_SHEET.col_values(3)[1:]

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


def append_user_row(row):
    """
    PLACEHOLDER
    """
    USERS_SHEET.append_row(row)
    print(f"Welcome {row[1]}!")
    print("Account susccessfully created\n")

    account_menu(row[0])


def save_account_details(username, password, name):
    """
    Checks user is happy to submit and save their account details and continue
    with creation

    Parameters: username: the user's chosen username, password: the user's
    chosen password, name: the user's name

    Outputs: calls action_menu_choice function to select the next function to
    run based on user's input. Provides function name and parameters via a
    list of dictionaries named menu_choices. Loops if invalid input
    """
    user_id = int(USERS_SHEET.col_values(1)[-1])+1
    user_row = [user_id, name, username, password]

    print("Please enter 1 to save details and setup account or 2 to reset",
          "details and start again:\n")
    menu_selection = input("Input 1 or 2:\n")
    print()

    menu_choices = [{'name': append_user_row, 'param1': user_row},
                    {'name': create_account}]

    if validate_menu_choice(menu_selection, 2):
        action_menu_choice(menu_selection, menu_choices)
    else:
        save_account_details(username, password, name)


def create_account():
    """
    Begins the account creation process. Runs validation functions to request
    and validate account details

    Parameters: none

    Outputs: calls save_account_details() function with validated username,
    validated password and name parameters
    """
    print("ACCOUNT SETUP:\n")

    while True:
        print("""Username must meet the following criteria:
    - 5 to 15 characters long
    - unique
    """)
        username = input("Username:\n")
        if validate_username_creation(username):
            break
    print(f"Username {username} is available!\n")

    while True:
        print("""Password must meet the following criteria:
    - 5 to 15 characters long
    - at least 1 uppercase and 1 lowercase letter
    - at least 1 number
    """)
        password = input("Password:\n")
        if validate_password_creation(password):
            break
    print(f"Password {password} is valid!\n")

    print("Finally, please tell us your name")
    name = input("Name:\n")

    print(f"""
You have entered the following details:
    Username: {username}
    Password: {password}
    Name: {name}
    """)

    save_account_details(username, password, name)


def display_help(menu, user_id):
    """
    Called from either the main menu or account menu,
    displays information about the program and how to use it

    Parameters: menu: string with name of menu called from/to return to
    user_id: the unique identifier of the user's account,
    used to access the data of the user who is currently logged in

    Outputs: calls back to either main or account menu based on first parameter
    """
    print("""The budget and savings tracker is a handy tool where you can keep
    track of your monthly earnings and spending and calculate a budget.
    """)
    input("Press enter to return to menu\n")
    if menu == 'main':
        main_menu()
    else:
        account_menu(user_id)


def validate_login_details(login_attempt):
    """
    Validates the user's login request

    Parameters: login_attempt: a dictionary of the user's input username and
    password

    Outputs: runs account menu if login valid, returns to login if invalid
    """
    usernames = USERS_SHEET.col_values(3)[1:]
    passwords = USERS_SHEET.col_values(4)[1:]

    login_list = []
    for username, password in zip(usernames, passwords):
        user = {username: password}
        login_list.append(user)

    try:
        index = login_list.index(login_attempt) + 1
        user_id = int(USERS_SHEET.col_values(1)[index])
        print("Welcome back!\n")
        account_menu(user_id)
    except ValueError:
        print("Username or password incorrect. Please try again\n")
        login()


def login():
    """
    Prompts the user to input their username and password to
    access their account

    Parameters: none

    Outputs: calls validate_login_details() function with a dictionary of
    the user's input username and password
    """
    print("ACCOUNT LOGIN:\n")
    username = input("Username:\n")
    password = input("Password:\n")
    print()

    login_attempt = {username: password}
    validate_login_details(login_attempt)


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


def action_menu_choice(response, functions):
    """
    Calls the correct function based on user's input

    Parameters: repsonse: user's input response to menu selection,
    functions: list of dictionaries with function names and parameters
    to be unpacked

    Outputs: calls correct function based on user's input
    """
    function = functions[int(response)-1]

    function_name = function['name']
    parameters = []
    for i in range(1, len(function)):
        parameters.append(function['param' + str(i)])

    function_name(*parameters)


def main_menu():
    """
    Displays the main menu with options for the user to login, create account
    or view program information and instructions

    Parameters: none

    Outputs: calls action_menu_choice function to select the next function to
    run based on user's input. Provides function name and parameters via a
    list of dictionaries named menu_choices. Loops if invalid input
    """
    print("MAIN MENU:\n")
    print(
        """Please select an option from the below menu
    1- Login
    2- Create Account
    3- Help
        """)
    menu_selection = input("Input 1, 2 or 3:\n")
    print()

    menu_choices = [{'name': login}, {'name': create_account},
                    {'name': display_help, 'param1': 'main', 'param2': '0'}]

    if validate_menu_choice(menu_selection, 3):
        action_menu_choice(menu_selection, menu_choices)
    else:
        main_menu()


# Greet user and open the main menu
# Logo created at https://patorjk.com/software/taag/#p=display&f=Stop&t=BUDGE
print("""
 ______  _     _ _____    ______ _______
(____  \| |   | (____ \  / _____|_______)
 ____)  ) |   | |_   \ \| /  ___ _____ 
|  __  (| |   | | |   | | | (___)  ___)
| |__)  ) |___| | |__/ /| \____/| |_____
|______/ \______|_____/  \_____/|_______)

""")
print("Welcome to Budge: The budget and savings tracker!\n")
main_menu()
