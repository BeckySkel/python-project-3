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
        print("That username is unavailable, please try again\n")
        validate_username_creation()
    
    return username


def validate_password_creation():
    """
    Prompts the user to choose a password. Checks if it is at least 5
    characters long and contains at least 1 uppercase character
    """
    print("""Password must meet the following criteria:
    - 5 to 15 characters long
    - contain at least 1 uppercase and 1 lowercase letter
    - contain at least 1 number and no special characters
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
        print('Password valid!\n') 
    else:
        print('Password invalid. Please try again\n')
        validate_password_creation()


def create_account():
    """
    """
    valid_username = validate_username_creation()
    print(f"Username {valid_username} is available!\n")
    valid_password = validate_password_creation()
    # print(f"Password valid!\n")
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
