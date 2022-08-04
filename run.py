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
    and restarts if it does.
    """
    username = input("Username:\n")
    usernames = USERS_SHEET.col_values(3)[1:]

    if username in usernames:
        print("That username is already taken, please try again\n")
        validate_username_creation()
    
    return username


def validate_password_creation():
    """
    Prompts the user to choose a password. Checks if it is at least 5
    characters long and contains at least 1 uppercase character
    """
    print("""Password must meet the following criteria:
    - at least 5 characters long
    - contain at least 1 upppercase and 1 lowercase letter
    """)
    password = input("Password:\n")

    password_length = len(password)
    length_valid = True if password_length >= 5 else False
    print(f"Password is {password_length} characters long, therefore length_valid is {length_valid}")
    print()

    uppercase_count = 0
    for char in password:
        if char.isupper():
            uppercase_count =+ 1
            break

    lowercase_count = 0
    for char in password:
        if char.islower():
            lowercase_count =+ 1
            break

    cases_valid = True if uppercase_count >= 1 and lowercase_count >= 1 else False
    print(f"cases_valid is {cases_valid}")


def create_account():
    """
    """
    valid_username = validate_username_creation()
    print(f"Username {valid_username} is available!\n")
    valid_password = validate_password_creation()
    print(f"Password valid!\n")
    print("Finally, please tell us your name")
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
