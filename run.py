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








def login():
    """
    Prompts the user to input their credentials to access their account
    """
    username = input("Username:\n")
    password = input("Password:\n")

    login_attempt = {username: password}
    print(login_attempt)
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
        """To continue, please select an option from the below menu

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


print("Welcome to the budget and savings tracker!\n")
main_menu()
