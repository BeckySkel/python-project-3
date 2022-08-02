# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Google Sheets and gspread set-up provided by Code Institute Love Sandwiches project
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


users = SHEET.worksheet('users')

data = users.get_all_values()

# print(data)

def main_menu():
    """
    Runs the main functions
    """
    print(
        """To continue, please select an option from the below menu and input below

        1- Login
        2- Create Account
        3- Help
        """)
    menu_select = input("Input 1, 2 or 3:\n")
    
    if menu_select == 1:
        login()
    elif menu_select == 2:
        create_account()
    else: 
        display_help()


print("Welcome to the budget and savings tracker!\n")
main_menu()