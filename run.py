# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Google Sheets and gspread set-up by Code Institute Love Sandwiches project
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('savings_tracker')
USERS_SHEET = SHEET.worksheet('users')
ENTRIES_SHEET = SHEET.worksheet('entries')


def remove_entry(user_id):
    """
    Allows user to remove an entry from their monthly spending
    """
    print("REMOVE ENTRY:\n")
    entry_to_remove = input("Entry Number:\n")

    entry_dicts = ENTRIES_SHEET.get_all_records()

    for dict in entry_dicts:
        uid = dict.get('User ID')
        entry_num = dict.get('Entry Number')
        if uid == user_id:
            if entry_num == int(entry_to_remove):
                entry = entry_dicts.index(dict) + 2
                ENTRIES_SHEET.delete_rows(entry)


def add_entry(user_id):
    """
    Allows user to add a new entry for their monthly spending
    """
    print("ADD NEW ENTRY:\n")
    month = input("Month:\n")
    income = int(input("Incoming(£):\n"))
    outgoing = int(input("Outgoing(£):\n"))
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

    ENTRIES_SHEET.append_row([entry_id, user_id, entry_num, month, income,
    outgoing, net])


def display_table(user_id):
    """
    Displays all of the current user's previous table entries
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

    # Code for creating a table from official tabulate documentation
    headers = ENTRIES_SHEET.row_values(1)[2:]
    print(tabulate(current_user, headers, tablefmt='psql'))
    print("Goal: \n")


def account_menu(user_id):
    """
    Displays the account menu with options for the user to add a new entry,
    remove a previous entry, edit their goals, view app information or logout
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
    
    validation = validate_menu_choices(menu_selection, 5)

    if validation:
        selection_int = int(menu_selection)
        if selection_int == 1:
            add_entry(user_id)
        elif selection_int == 2:
            remove_entry(user_id)
        elif selection_int == 3: 
            print("Edit goal:")
        elif selection_int == 4:
            display_help('account', user_id)
            account_menu(user_id)
        elif selection_int == 5:
            print("You have successfully logged out.\n")
            main_menu()
    else:
        main_menu()
    
    print()
    account_menu(user_id)
    # Add another function for menu validation and selection based on above code


def validate_username_creation():
    """
    Prompts the user to choose a username. Checks if it already exists
    and restarts if it does.
    """
    print("""Username must meet the following criteria:
    - 5 to 15 characters long
    - unique
    """)
    username = input("Username:\n")
    username_length = len(username)

    usernames = USERS_SHEET.col_values(3)[1:]

    if username_length < 5:
        print("Username too short, please try again\n")
        validate_username_creation()
    elif username_length > 15:
        print("Username too long, please try again\n")
        validate_username_creation()
    else:
        if username in usernames:
            print("That username is unavailable, please try again\n")
            validate_username_creation()
    
    return username


def validate_password_creation():
    """
    Prompts the user to choose a password. Checks if it meets all criteria
    and restarts if it doesn't.
    """
    print("""Password must meet the following criteria:
    - 5 to 15 characters long
    - at least 1 uppercase and 1 lowercase letter
    - at least 1 number
    """)
    password = input("Password:\n")

    password_length = len(password)
    length_valid = True if password_length >= 5 and password_length <= 15 else False

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
        return password
    else:
        print("Password invalid. Please try again\n")
        validate_password_creation()


def save_account_details(username, password, name):
    """
    """
    user_id = int(USERS_SHEET.col_values(1)[-1])+1
    user_row = [user_id, name, username, password]
    
    save_account = input("Please enter 1 to save details and setup account or 2 to reset details and start again:\n")
    print()
    validation = validate_menu_choices(save_account, 2)
    if validation:
        selection_int = int(save_account)
        if selection_int == 1:
            USERS_SHEET.append_row(user_row)
            print("Welcome!\n")
            account_menu(user_id)
        elif selection_int == 2:
            create_account()
    else:
        save_account_details(username, password, name)


def create_account():
    """
    Runs functions for user to input information and create account
    """
    print("ACCOUNT SETUP:\n")
    valid_username = validate_username_creation()
    print(f"Username {valid_username} is available!\n")
    valid_password = validate_password_creation()
    print("Finally, please tell us your name")
    name = input("Name:\n")
    
    print(f"""
You have entered the following details:
    Username: {valid_username}
    Password: {valid_password}
    Name: {name}
    """)

    save_account_details(valid_username, valid_password, name)
    # Add another function for menu validation and selection based on above code


def display_help(menu, id):
    """
    Called from either the main menu or account menu,
    displays information about the app and how to use it
    """
    print("""The budget and savings tracker is a handy tool where you can keep
    track of your monthly earnings and spending and calculate a budget.
    """)
    input("Press enter to return to menu\n")
    if menu == 'main':
        main_menu()
    else:
        account_menu(id)


def validate_login_details(login_attempt):
    """
    Validates the user's login request
    """
    usernames = USERS_SHEET.col_values(3)[1:]
    passwords = USERS_SHEET.col_values(4)[1:]

    list = []
    for username, password in zip(usernames, passwords):
        user = {username: password}
        list.append(user)
    
    try:
        index = list.index(login_attempt) + 1
        user_id = int(USERS_SHEET.col_values(1)[index])
        print("Welcome back!\n")
        account_menu(user_id)
    except ValueError:
        print("Username or password incorrect. Please try again\n")
        login()


def login():
    """
    Prompts the user to input their username and
    password to access their account
    """
    print("ACCOUNT LOGIN:\n")
    username = input("Username:\n")
    password = input("Password:\n")
    print()

    login_attempt = {username: password}
    validate_login_details(login_attempt)


def validate_menu_choices(response, limit):
    """
    Validates menu selection and raises error if invalide response entered
    """
    try:
        int(response)
        if int(response) > limit or int(response) < 1:
            raise ValueError()
        return True
    except ValueError:
        print(f"Invalid selection: Please choose a number between 1 and {limit}. You entered: {response}\n")
        return False


def main_menu():
    """
    Displays the main menu with options for the user to login, create account
    or view app information
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
    
    validation = validate_menu_choices(menu_selection, 3)

    if validation:
        selection_int = int(menu_selection)
        if selection_int == 1:
            login()
        elif selection_int == 2:
            create_account()
        else: 
            display_help('main', 0)
            main_menu()
    else:
        main_menu()


print("Welcome to the budget and savings tracker!\n")
main_menu()

# display_table(1)

# code to create table from official tabulate documentation
# table = [["Sun",696000,1989100000],["Earth",6371,5973.6], ["Moon",1737,73.5],["Mars",3390,641.85]]
               
# print(f"\n{tabulate(table, headers='firstrow')}")
