"""
Module for running full program and interacting with database
"""

# Imported to clear terminal after logout
import os
# Imported to display the user's data in an easy-to-read table
from tabulate import tabulate

# Google Sheets and gspread set-up by Code Institute Love Sandwiches project
# Imported to interact with savings_tracker database in Google Sheets
import gspread
from google.oauth2.service_account import Credentials

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


def get_user_entries(user_id):
    """
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

    return current_user


def check_exit(input_value):
    """
    Checks if user has input 'exit' to cancel current action

    Parameters: input_value: the value the user submitted in the input field

    Ouputs: (boolean) returns True if 'exit' was entered, returns False if not
    """
    if input_value.upper() == 'EXIT':
        print("Exiting function and returning to menu.\n")
        return True

    return False


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


def prevent_duplicates(month_input, user_id):
    """"""
    month_entries = [entry[1] for entry in get_user_entries(user_id)]
    try:
        month_entries.index(month_input)
        print(f"Entry already exists for {month_input}, please try again.\n")
        return False
    except ValueError:
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
        if float(amount) < 0:
            raise ValueError
    except ValueError:
        print("Amount must be a positive number (will be rounded to 2 decimal places).",
              f"You entered {amount}. Please try again\n")
        return False

    return True


def get_month_input(user_id):
    """"""
    while True:
        month = input("Month (MMM YYYY):\n").lower().capitalize()
        if check_exit(month):
            account_menu(user_id)
        elif validate_month_format(month):
            month = " ".join(month.split())
            break

    return month


def get_amount_input(user_id, input_request):
    """"""
    while True:
        amount = input(f"{input_request}:\n")
        if check_exit(amount):
            account_menu(user_id)
        elif validate_amount(amount):
            break

    return round(float(amount), 2) 


def calculate_difference(num1, num2):
    """"""
    return num1 - num2


def calc_next_entry_num(user_id):
    """
    """
    user_entries = get_user_entries(user_id)
    user_entries_nums = [int(entry[0]) for entry in user_entries]
    user_entries_nums.sort()

    try:
        entry_num = user_entries_nums[-1]+1
    except IndexError:
        entry_num = 1

    return entry_num


def add_entry(user_id):
    """
    Allows user to add a new entry for their monthly spending data

    Parameters: user_id: the unique identifier of the user's account,
    used to manipulate the data of the user who is currently logged in

    Outputs: appends user's entered spending data to the database after
    running validation checks
    """
    print("ADD NEW ENTRY:\n")
    print("Input EXIT to return to menu.\n")

    while True:
        month = get_month_input(user_id)
        if prevent_duplicates(month, user_id):
            break
    income = get_amount_input(user_id, "Income(£)")
    outgoing = get_amount_input(user_id, "Outgoing(£)")
    net = calculate_difference(income, outgoing)
    entry_num = calc_next_entry_num(user_id)
    try:
        entry_id = int(ENTRIES_SHEET.col_values(1)[-1])+1
    except IndexError:
        entry_id = 1

    ENTRIES_SHEET.append_row([entry_id, user_id, entry_num, month,
                             income, outgoing, net])


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


def get_entry_row(user_id, entry_num):
    """
    """
    all_entries = ENTRIES_SHEET.get_all_values()[1:]

    for entry in all_entries:
        uid = int(entry[1])
        num = int(entry[2])
        if uid == user_id:
            if entry_num == int(num):
                row_num = all_entries.index(entry) + 2
                return row_num


def edit_entry(user_id):
    """
    """
    user_entries = get_user_entries(user_id)

    print("EDIT ENTRY:\n")
    print("Input EXIT to return to menu.\n")
    while True:
        entry_to_edit = input("Entry Number:\n")
        if check_exit(entry_to_edit):
            account_menu(user_id)
        elif validate_entry_number(entry_to_edit, user_entries):
            break

    month = get_month_input(user_id)
    income = get_amount_input(user_id, "Income(£)")
    outgoing = get_amount_input(user_id, "Outgoing(£)")
    savings = calculate_difference(income, outgoing)

    row_num = get_entry_row(user_id, int(entry_to_edit))
    ENTRIES_SHEET.update(f'D{row_num}:G{row_num}', [[month, income, outgoing, savings]])


def remove_entry(user_id):
    """
    Allows user to remove an entry from their monthly spending data

    Parameters: user_id: the unique identifier of the user's account,
    used to manipulate the data of the user who is currently logged in

    Outputs: deletes row from entry data based on the user's unique ID
    and their inputted entry ID
    """
    user_entries = get_user_entries(user_id)

    print("REMOVE ENTRY:\n")
    print("Input EXIT to return to menu.\n")
    while True:
        entry_to_remove = input("Entry Number:\n")
        if check_exit(entry_to_remove):
            account_menu(user_id)
        elif validate_entry_number(entry_to_remove, user_entries):
            break

    row_num = get_entry_row(user_id, int(entry_to_remove))
    row_data = ENTRIES_SHEET.row_values(row_num)[2:]
    ENTRIES_SHEET.delete_rows(row_num)
    print(f"Entry {row_data} removed.\n")


# def get_user_entries(user_id):
#     """
#     """
#     all_entries = ENTRIES_SHEET.get_all_values()

#     current_user = []
#     for entry in all_entries:
#         try:
#             uid = int(entry[1])
#             if uid == user_id:
#                 current_user.append(entry[2:])
#         except ValueError:
#             pass

#     return current_user


def calculate_budget(user_id):
    """
    """
    print("EDIT BUDGET:\n")
    print("Input EXIT to return to menu.\n")

    goal_amount = get_amount_input(user_id, "Goal Amount(£)")
    goal_month = get_month_input(user_id)

    user_entries = get_user_entries(user_id)

    all_savings = [float(entry[-1]) for entry in user_entries]
    print(all_savings)
    months = [entry[1] for entry in user_entries]
    print(months)

    difference = calculate_difference(goal_amount, sum(all_savings))
    print(difference)

    months_difference = MONTHS.index(goal_month.split()[0]) - MONTHS.index(months[-1].split()[0])
    years_difference = int(goal_month.split()[1]) - int(months[-1].split()[1])
    total_months_difference = (years_difference*12) + months_difference

    print(months_difference)
    print(years_difference)
    print(total_months_difference)
    budget = round(difference/total_months_difference, 2)
    print(f"In order to save {goal_amount} by {goal_month} you'd have to save {budget} per month")

    # row_num = get_entry_row(user_id, int(entry_to_edit))

    all_users = USERS_SHEET.get_all_values()[1:]

    for entry in all_users:
        uid = int(entry[0])
        if uid == user_id:
            row_num = all_users.index(entry) + 2
            USERS_SHEET.update(f'E{row_num}:F{row_num}', [[goal_amount, goal_month]])
    
    


def display_table(user_id):
    """
    Displays all of the current user's previous table entries

    Parameters: user_id: the unique identifier of the user's account,
    used to access and display the data of the user who is currently logged in

    Outputs: prints table of current user's spending data to the console
    """
    user_entries = get_user_entries(user_id)

    sorted_by_month = []
    for m in MONTHS:
        for entry in user_entries:
            month = entry[1].split()[0]
            if m == month:
                sorted_by_month.append(entry)

    entered_years = [int(entry[1].split()[1]) for entry in sorted_by_month]
    entered_years.sort()
    # https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    remove_dupicates = list(dict.fromkeys(entered_years))

    sorted_by_year = []
    for y in remove_dupicates:
        for entry in sorted_by_month:
            year = int(entry[1].split()[1])
            if y == year:
                sorted_by_year.append(entry)

    # Code for creating a table from official tabulate documentation
    headers = ENTRIES_SHEET.row_values(1)[2:]
    print(tabulate(sorted_by_year, headers, tablefmt='psql'))
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
    3- Edit entry
    4- Edit budget
    5- Help
    6- Logout
        """)
    menu_selection = input("Input 1, 2, 3, 4, 5 or 6:\n")
    print()

    menu_choices = [{'name': add_entry, 'param1': user_id},
                    {'name': remove_entry, 'param1': user_id},
                    {'name': edit_entry, 'param1': user_id},
                    {'name': calculate_budget, 'param1': user_id},
                    {'name': display_help, 'param1': 'account',
                    'param2': user_id}, {'name': logout}]

    if validate_menu_choice(menu_selection, len(menu_choices)):
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
    # code to clear terminal from https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Successfully logged out.\n")
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

    if validate_menu_choice(menu_selection, len(menu_choices)):
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
    print("Input EXIT to return to menu.\n")

    while True:
        print("""Username must meet the following criteria:
    - 5 to 15 characters long
    - unique
    """)
        username = input("Username:\n")
        if check_exit(username):
            main_menu()
        elif validate_username_creation(username):
            break
    print(f"Username {username} is available!\n")

    while True:
        print("""Password must meet the following criteria:
    - 5 to 15 characters long
    - at least 1 uppercase and 1 lowercase letter
    - at least 1 number
    """)
        password = input("Password:\n")
        if check_exit(password):
            main_menu()
        elif validate_password_creation(password):
            break
    print(f"Password {password} is valid!\n")

    print("Finally, please tell us your name")
    name = input("Name:\n")
    if check_exit(name):
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

    Parameters: menu: string with name of menu called from/to return to
    user_id: the unique identifier of the user's account,
    used to access the data of the user who is currently logged in

    Outputs: calls back to either main or account menu based on first parameter
    """
    print("""
    BUDGE is a handy tool where you can keep track of your monthly
    spending and saving. Whether you're saving for a house or a holiday,
    BUDGE can guide  
    
    Simply input your monthly income and total outgoing and let BUDGE calcualte your savings and how this compares to your set budget.
    Need to calculate a suitable budget? BUDGe can do that too!
    """)
    input("Press enter to return\n")
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
        # code to clear terminal from https://stackoverflow.com/questions/2084508/clear-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')
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
    print("Input EXIT to return to menu.\n")

    username = input("Username:\n")
    if check_exit(username):
        main_menu()
    password = input("Password:\n")
    if check_exit(password):
        main_menu()
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

# ALL_ENTRIES = ENTRIES_SHEET.get_all_values()
# HEADERS = ENTRIES_SHEET.row_values(1)[2:]


# class UserEntries(object):
#     """
#     A class used to represent the user currently logged in

#     Attributes:
#     user_id : int
#         the user's unique identifier
#     name : str
#         name of the user
#     username : str
#         the user's chosen username
#     password : str
#         the user's chosen password
#     goal_amount : float
#         the amount (in pounds£) that the user is hoping to save
#     goal_month : str
#         the month which the user is hoping to save by

#     Methods:
#     get_entries(self)
#         gets all of the user's submitted monthly spending
#     sort_by_month(self)
#         sorts the user's entries by month
#     display_table(self)
#         displays the user's entries in an easy-to-read table
#     calculate_total_savings()
#     calculate_budget()
        
#     """
#     def __init__(self, user_id, goal_amount, goal_month):
#         self.user_id = user_id
#         # self.name = name
#         # self.username = username
#         # self.password = password
#         self.goal_amount = goal_amount
#         self.goal_month = goal_month

#     def get_entries(self):
#         user_entries = []
#         for entry in ALL_ENTRIES:
#             try:
#                 uid = int(entry[1])
#                 if uid == self.user_id:
#                     user_entries.append(entry[2:])
#             except ValueError:
#                 pass

#         return user_entries

#     def sort_by_month(self):
#         user_entries = self.get_entries()
#         user_sorted = []
#         for m in MONTHS:
#             for entry in user_entries:
#                 month = entry[1]
#                 if m == month:
#                     user_sorted.append(entry)

#         return user_sorted

#     def display_table(self):
#         sorted_entries = self.sort_by_month()
#         # Code for creating table from official tabulate documentation
#         return tabulate(sorted_entries, HEADERS, tablefmt='psql')

#     def calculate_total_savings(self):
#         user_entries = self.sort_by_month()

#         net_savings = [float(entry[-1]) for entry in user_entries]
#         total_savings = sum(net_savings)

#         return total_savings

#     def calculate_budget(self):
#         user_entries = self.sort_by_month()

#         recent_month = user_entries[-1][1]

#         amount_difference = self.goal_amount - self.calculate_total_savings()
#         months_difference = MONTHS.index(self.goal_month) - MONTHS.index(recent_month)
#         budget = round(amount_difference/months_difference, 2)
#         return f"In order to save {self.goal_amount} by {self.goal_month} you'd have to save {budget} per month"




# # class UserEntries(object):
# #     def __init__(self, entry_ids, user_id, entry_nums, months,
# #                  incomes, outgoings, net):
# #         self.user_id = user_id
# #         self.entry_ids = entry_ids
# #         self.user_id = user_id
# #         self.entry_nums = entry_nums
# #         self.months = months
# #         self.incomes = incomes
# #         self.ougoings = outgoings
# #         self.net = net

#     # def get_an_entry(self):



# # Define some students
# # becky = UserEntries(2, 700, "Nov")

# # # Now we can get to the grades easily
# # print(becky.get_entries())
# # print()
# # print(becky.sort_by_month())
# # print()
# # print(becky.display_table())
# # print()
# # print(becky.calculate_budget())