"""
Module for running full program
"""

import utils
import validations
from constants import ENTRIES_SHEET, USERS_SHEET
import google_sheets


def get_month_input(user_id: int, input_request: str) -> str:
    """
    Prompts the user to input a month and runs through validation

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in
        input_request: str, request to display in input

    Outputs: str, returns the validated month input as a string
    """
    while True:
        month = input(f"{input_request}:\n").lower().capitalize()
        if utils.check_exit(month):
            account_menu(user_id)
        elif validations.validate_month_format(month):
            # Splitting and joining string to remove extra whitespace
            # in user response inspired by below tutorial
            # https://www.geeksforgeeks.org/python-program-split-join-string/#:~:text=the%20split()%20method%20in,joined%20by%20the%20str%20separator.
            month = " ".join(month.split())
            return month


def get_amount_input(user_id: int, input_request: str) -> float:
    """
    Prompts the user to input an amount and runs through validation

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in
        input_request: str, request to display in input

    Outputs: float, returns the validated amount input in correct currency
    format
    """
    while True:
        amount = input(f"{input_request}:\n")
        if utils.check_exit(amount):
            account_menu(user_id)
        elif validations.validate_amount(amount):
            break

    return utils.currency(amount)


def calc_next_entry_num(user_id: int) -> int:
    """
    Calculates the next entry number for the user's input

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: int, entry number for user's next entry input
    """
    user_entries = google_sheets.get_user_entries(user_id)
    user_entries_nums = [int(entry[0]) for entry in user_entries]
    user_entries_nums.sort()

    try:
        entry_num = user_entries_nums[-1]+1
    except IndexError:
        entry_num = 1

    return entry_num


def get_entry_to_edit(user_id: int) -> int:
    """
    Prompts the user to input an entry to edit and runs through validation

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: int, returns the validated entry number
    """
    user_entries = google_sheets.get_user_entries(user_id)

    while True:
        entry_to_edit = input("Entry Number:\n")
        if utils.check_exit(entry_to_edit):
            account_menu(user_id)
        elif validations.validate_entry_number(entry_to_edit, user_entries):
            break

    return entry_to_edit


def add_entry(user_id: int):
    """
    Allows user to add a new entry to their monthly spending data

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: appends user's entered spending data to the database after
    running validation checks
    """
    utils.print_colour("ADD NEW ENTRY:\n", 'cyan')
    utils.print_colour("Input EXIT to return to menu.\n", 'magenta')

    while True:
        month = get_month_input(user_id, "Month (MMM YYYY)")
        if not validations.is_month_duplicate(month, user_id):
            break
    income = get_amount_input(user_id, "Income(£)")
    outgoing = get_amount_input(user_id, "Outgoing(£)")
    savings = utils.currency(income - outgoing)
    entry_num = calc_next_entry_num(user_id)
    entry_id = google_sheets.next_entry_id()

    entry_list = [entry_id, user_id, entry_num, month, income,
                  outgoing, savings]

    print()
    utils.print_colour("Add below information to the table?", 'yellow')
    print(entry_list[2:])
    if validations.confirm_action('add entry'):
        google_sheets.append_row(entry_list, 'entries')
    else:
        print("Action cancelled. Data not saved")


def edit_entry(user_id: int):
    """
    Allows user to edit an entry from their monthly spending data

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: updates entered spending data to the correct entry in the
    database after running validation checks
    """
    utils.print_colour("EDIT ENTRY:\n", 'cyan')
    utils.print_colour("Input EXIT to return to menu.\n", 'magenta')

    entry_to_edit = int(get_entry_to_edit(user_id))
    row_num = google_sheets.get_entry_row(user_id, int(entry_to_edit))

    month = get_month_input(user_id, "Month (MMM YYYY)")
    income = get_amount_input(user_id, "Income(£)")
    outgoing = get_amount_input(user_id, "Outgoing(£)")
    savings = utils.currency(income - outgoing)

    previous_data = ENTRIES_SHEET.row_values(row_num)[2:]
    new_data = [entry_to_edit, month, income, outgoing, savings]

    print()
    utils.print_colour("Replace", 'yellow')
    print(previous_data)
    utils.print_colour("with", 'yellow')
    print(f"{new_data}?")
    if validations.confirm_action('edit entry'):
        ENTRIES_SHEET.update(f'D{row_num}:G{row_num}', [new_data[1:]])
    else:
        print("Action cancelled. Data not saved")


def remove_entry(user_id: int):
    """
    Allows user to remove an entry from their monthly spending data

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: deletes row from entry data based on the user's unique ID
    and their inputted entry ID
    """
    utils.print_colour("REMOVE ENTRY:\n", 'cyan')
    utils.print_colour("Input EXIT to return to menu.\n", 'magenta')

    entry_to_remove = get_entry_to_edit(user_id)

    row_num = google_sheets.get_entry_row(user_id, int(entry_to_remove))
    row_data = ENTRIES_SHEET.row_values(row_num)[2:]

    print()
    utils.print_colour("Remove below information from the table?", 'yellow')
    print(row_data)
    if validations.confirm_action('remove entry'):
        ENTRIES_SHEET.delete_rows(row_num)
    else:
        print("Action cancelled. Data not removed")


def edit_budget(user_id: int):
    """
    Allows user to input their savings goal and edit their budget

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to manipulate the data of the user who is currently logged in

    Outputs: updates entered savings goal info to the correct user
    """
    utils.print_colour("EDIT BUDGET:\n", 'cyan')
    utils.print_colour("Input EXIT to return to menu.\n", 'magenta')

    while True:
        goal_amount = get_amount_input(user_id, "Savings Goal(£)")
        if goal_amount > google_sheets.calculate_total_savings(user_id):
            break
        else:
            utils.print_colour("Must be more than current total savings.\n"
                               "Please try again", 'red')

    try:
        while True:
            goal_date = get_month_input(user_id, "Goal Month(MMM YYYY)")
            if google_sheets.calc_months_difference(user_id, goal_date) > 0:
                break
            else:
                print("Goal month must be later than last entry.",
                      "Please try again")
    except IndexError:
        print("No spending data available.\n"
              "You must add at least 1 entry before setting a budget.")
        return

    budget = google_sheets.calculate_budget(user_id, goal_amount, goal_date)
    user_entries = google_sheets.get_user_entries(user_id)
    average_income = utils.calc_average([float(entry[2])
                                        for entry in user_entries])
    spending_budget = utils.currency(average_income - budget)

    print()
    print(f"In order to save {goal_amount} by {goal_date}\n"
          f"You'd have to save {budget} per month.\n")
    print(f"Based on your average income of {average_income},\n"
          f"this means limiting your spending to around {spending_budget}\n")

    utils.print_colour("Save budget information?", 'yellow')
    if validations.confirm_action('and save'):
        google_sheets.save_budget_info(user_id, goal_amount, goal_date)
    else:
        print("Action cancelled. Budget information not stored.")


def account_menu(user_id: int):
    """
    Displays the account menu with options for the user to add a new entry,
    remove a previous entry, edit their goals, view app information or logout

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to access the data of the user who is currently logged in

    Outputs: calls action_menu_choice function to select the next function to
    run based on user's input. Provides funtcion name and parameters via a
    list of dictionaries named menu_choices. Loops until user logs out
    """
    utils.print_colour("ACCOUNT:\n", 'cyan')
    google_sheets.display_table(user_id)
    utils.print_colour("""Please select an option from the below menu
    1- Add new entry
    2- Remove entry
    3- Edit entry
    4- Edit budget
    5- Help
    6- Logout
        """, 'magenta')
    menu_selection = input("Input 1, 2, 3, 4, 5 or 6:\n")
    print()

    menu_choices = [{'name': add_entry, 'param1': user_id},
                    {'name': remove_entry, 'param1': user_id},
                    {'name': edit_entry, 'param1': user_id},
                    {'name': edit_budget, 'param1': user_id},
                    {'name': display_help, 'param1': 'account',
                    'param2': user_id}, {'name': logout}]

    if validations.validate_menu_choice(menu_selection, len(menu_choices)):
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
    utils.print_colour("Logout?", 'yellow')
    if validations.confirm_action('logout'):
        utils.clear_terminal()
        utils.print_colour("Successfully logged out.\n", 'yellow')
        main_menu()


def save_account_details(username: str, password: str, name: str):
    """
    Checks user is happy to submit and save their account details and continue
    with creation

    Parameters:
        username: str, the user's chosen username
        password: str, the user's chosen password
        name: str, the user's name

    Outputs: calls action_menu_choice function to select the next function to
    run based on user's input. Provides function name and parameters via a
    list of dictionaries named menu_choices. Loops if invalid input
    """
    user_id = google_sheets.next_user_id()
    user_row = [user_id, name, username, password]

    utils.print_colour("Please enter 1 to save details and setup account\n"
                       "or 2 to reset details and start again:\n", 'magenta')
    menu_selection = input("Input 1 or 2:\n")
    print()

    menu_choices = [{'name': account_menu, 'param1': user_id},
                    {'name': create_account}]

    if validations.validate_menu_choice(menu_selection, len(menu_choices)):
        if int(menu_selection) == 1:
            utils.clear_terminal()
            print(f"Welcome {user_row[1]}!")
            print("Account susccessfully created\n")
            google_sheets.append_row(user_row, 'users')
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
    utils.print_colour("ACCOUNT SETUP:\n", 'cyan')
    utils.print_colour("Input EXIT to return to menu.\n", 'magenta')

    while True:
        print("""Username must meet the following criteria:
    - 5 to 15 characters long
    - unique
    """)
        username = input("Username:\n")
        if utils.check_exit(username):
            main_menu()
        elif validations.validate_username_creation(username):
            break
    utils.print_colour(f"Username {username} is available!\n", 'green')

    while True:
        utils.print_colour("""Password must meet the following criteria:
    - 5 to 15 characters long
    - at least 1 uppercase and 1 lowercase letter
    - at least 1 number
    """, 'magenta')
        password = input("Password:\n")
        if utils.check_exit(password):
            main_menu()
        elif validations.validate_password_creation(password):
            break
    print(f"Password {password} is valid!\n")

    print("Finally, please tell us your name")
    name = input("Name:\n")
    if utils.check_exit(name):
        main_menu()

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

    Parameters:
        menu: str, name of menu called from/to return to
        user_id: int, the unique identifier of the user's account,
        used to access the data of the user who is currently logged in

    Outputs: calls back to either main or account menu based on first parameter
    """
    utils.print_colour("""
    BUDGE is a handy tool where you can keep track of your monthly spending
    and saving. Whether you're saving for a house or a holiday, BUDGE provides
    a friendly push in the right direction by analysing your spending data
    and providing insights on how much you should be saving each month.

    Start by entering your monthly incoming and outgoing and BUDGE
    will calculate your savings. After you've entered a few months data,
    why not set a saving goal and see how much you'll need to save each month
    in order to reach it?
    """, 'green')
    input("Press enter to return\n")
    if menu == 'main':
        main_menu()
    else:
        account_menu(user_id)


def login():
    """
    Prompts the user to input their username and password to
    access their account

    Parameters: none

    Outputs: calls validate_login_details() function with a dictionary of
    the user's input username and password
    """
    utils.print_colour("ACCOUNT LOGIN:\n", 'cyan')
    utils.print_colour("Input EXIT to return to menu.\n", 'magenta')

    username = input("Username:\n")
    if utils.check_exit(username):
        main_menu()
    password = input("Password:\n")
    if utils.check_exit(password):
        main_menu()
    print()

    login_attempt = {username: password}
    if validations.validate_login_details(login_attempt):
        index = USERS_SHEET.get_all_values()[2].index(username)
        user_id = google_sheets.uid_by_index(index)
        account_menu(user_id)
    else:
        main_menu()


def action_menu_choice(response: int, functions: list):
    """
    Calls the correct function based on user's input

    Parameters:
        repsonse: user's input response to menu selection,
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
    utils.print_colour("MAIN MENU:\n", 'cyan')
    utils.print_colour(
        """Please select an option from the below menu
    1- Login
    2- Create Account
    3- Help
        """, 'magenta')
    menu_selection = input("Input 1, 2 or 3:\n")
    print()

    menu_choices = [{'name': login}, {'name': create_account},
                    {'name': display_help, 'param1': 'main', 'param2': '0'}]

    if validations.validate_menu_choice(menu_selection, 3):
        action_menu_choice(menu_selection, menu_choices)
    else:
        main_menu()


# Greet user and open the main menu
utils.display_logo()
utils.print_colour('Welcome to Budge: The budget and savings tracker!\n',
                   'blue')
main_menu()
