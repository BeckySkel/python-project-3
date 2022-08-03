# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Google Sheets and gspread set-up by Code Institute Love Sandwiches project
import gspread
from google.oauth2.service_account import Credentials

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



def validate_username_creation():
    """
    Prompts the user to choose a username. Checks if it already exists
    and restarts if it does. Returns True if username available
    """
    username = input("Username:\n")
    usernames = USERS_SHEET.col_values(3)[1:]

    if username in usernames:
        print("That username is already taken, please try again\n")
        validate_username_creation()


def create_account():
    """
    """
    validate_username = validate_username_creation()
    print("success")
    # validate_password = validate_password_creation()
    # validate_name = validate_name_creation()
    
    # if validate_username and validate_password and validate_name:
    #     print("Account created successfully! Please log in")
    #     login()
    # else:
    #     create_account()


def display_help():
    """
    Called from either the main menu or account menu,
    displays information about the app and how to use it
    """
    print("""The budget and savings tracker is a handy tool where you can keep
    track of your monthly earnings and spending and calculate a budget.
    """)
    input("Press enter to return to return to menu\n")
    main_menu()


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
        list.index(login_attempt)
        print("welcome back!")
    except ValueError:
        print("Username or password incorrect. Please try again\n")
        login()


def login():
    """
    Prompts the user to input their username and
    password to access their account
    """
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
        if int(response) > limit:
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
            display_help()
    else:
        main_menu()

# validate_login_details('login_attempt')
print("Welcome to the budget and savings tracker!\n")
main_menu()
