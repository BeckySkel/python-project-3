import os


def display_logo():
    """"""
    # Logo created at https://patorjk.com/software/taag/
    print("""
 ______  _     _ _____    ______ _______
(____  \| |   | (____ \  / _____|_______)
 ____)  ) |   | |_   \ \| /  ___ _____ 
|  __  (| |   | | |   | | | (___)  ___)
| |__)  ) |___| | |__/ /| \____/| |_____
|______/ \______|_____/  \_____/|_______)

""")


# def confirm_action(action):
#     """"""
#     print()
#     print(f"Please enter 1 to confirm {action} or 2 to cancel.")
#     menu_selection = input("Input 1 or 2:\n")
#     print()
#     if validations.validate_menu_choice(menu_selection, 2):
#         return True if int(menu_selection) == 1 else False
#     else:
#         confirm_action(action)


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


def calc_average(num_list):
    """"""
    average = sum(num_list)/len(num_list)
    return round(float(average), 2)


def clear_terminal():
    """"""
    # code to clear terminal from
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')
    display_logo()


def currency(amount):
    """"""
    amount_as_currency = round(float(amount), 2)
    return amount_as_currency
