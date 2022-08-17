"""
Module used to store functions which interact with a Google Sheets database
"""

from tabulate import tabulate
from constants import USERS_SHEET, ENTRIES_SHEET, HEADERS, MONTHS
import utils


def get_user_entries(user_id: int) -> list:
    """
    Retrieves the user's entries from the entries worksheet

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in

    Outputs: list, returns a list of lists of the user's entries
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


def entries_by_date(user_id: int) -> list:
    """
    Accesses and sorts all the user's entries by month, then year

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in

    Outputs: list, returns a list of lists of the user's entries,
    sorted by date
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
    # Code to remove duplicates from
    # https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    remove_dupicates = list(dict.fromkeys(entered_years))

    sorted_by_year = []
    for y in remove_dupicates:
        for entry in sorted_by_month:
            year = int(entry[1].split()[1])
            if y == year:
                sorted_by_year.append(entry)

    return sorted_by_year


def get_entry_row(user_id: int, entry_num: int) -> int:
    """
    Produces the row number of the inputted entry number to retrieve
    from database

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in
        entr_num: int, user input used to select the desired entry

    Outputs: int, returns the row index of the inputted entry number
    """
    all_entries = ENTRIES_SHEET.get_all_values()[1:]

    for entry in all_entries:
        uid = int(entry[1])
        num = int(entry[2])
        if uid == user_id:
            if entry_num == int(num):
                row_num = all_entries.index(entry) + 2
                return row_num


def get_user_row(user_id):
    """
    Produces the row number of the user's data to retrieve
    from database

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in

    Outputs: int, returns the row index of the user id
    """
    all_users = USERS_SHEET.get_all_values()[1:]

    for entry in all_users:
        uid = int(entry[0])
        if uid == user_id:
            return all_users.index(entry) + 2


def save_budget_info(user_id: int, goal_amount: float, goal_date: str):
    """
    Updates user row in users worksheet with new budget data

    Parameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in
        goal_amount: float, amount inputted by the user
        goal_date: str, month inoutted by the user

    Outputs: Updates user savings info in database
    """
    row_num = get_user_row(user_id)
    USERS_SHEET.update(f'E{row_num}:F{row_num}', [[goal_amount, goal_date]])


def display_table(user_id: int):
    """
    Displays all of the current user's previous entries in an easy-to-read
    table

    Parameters:
        user_id: the unique identifier of the user's account, used to access
        and display the data of the user who is currently logged in

    Outputs: prints table of current user's spending data to the console
    """
    # Code for creating a table from official tabulate documentation
    print(tabulate(entries_by_date(user_id), HEADERS, tablefmt='psql'))

    total_savings = calculate_total_savings(user_id)
    print(f"Total Savings(£): {total_savings}")

    row_num = get_user_row(user_id)
    user_row = USERS_SHEET.row_values(row_num)

    try:
        # row_num = get_user_row(user_id)
        # user_row = USERS_SHEET.row_values(row_num)
        goal_amount, goal_date = user_row[4], user_row[5]
        print(f"Overall Savings Goal(£): {goal_amount} by {goal_date}")
        savings_goal = calculate_budget(user_id, goal_amount, goal_date)
        print(f"Monthly Savings Goal(£): {savings_goal}\n")
    except IndexError:
        print()


def append_row(row: int, sheet: str):
    """
    Appends row to worksheet

    Parameters:
        row: list, the information to add to the worksheet
        sheet: str, the name of the worksheet to append to

    Outcomes: adds inputted row data to the specified sheet
    """
    if sheet == 'users':
        USERS_SHEET.append_row(row)
    else:
        ENTRIES_SHEET.append_row(row)


def next_user_id() -> int:
    """
    Produces the next available user id

    Parameters: none

    Outputs: int, returns next available number in sequence
    """
    return int(USERS_SHEET.col_values(1)[-1])+1


def next_entry_id() -> int:
    """
    Produces the next available entry id

    Parameters: none

    Outputs: int, returns next available number in sequence
    """
    try:
        entry_id = int(ENTRIES_SHEET.col_values(1)[-1])+1
    except IndexError:
        entry_id = 1

    return entry_id


def get_usernames() -> list:
    """
    Produces list of all saved usernames

    Parameters: none

    Outputs: list, returns list of usernames
    """
    return USERS_SHEET.col_values(3)[1:]


def get_passwords() -> list:
    """
    Produces list of all saved passwords

    Parameters: none

    Outputs: list, returns list of passwords
    """
    return USERS_SHEET.col_values(4)[1:]


def uid_by_index(index: int) -> int:
    """
    Produces the user id at the row index provided

    Parameters:
        index: int, the row index to retrieve the user id

    Outputs: int, user id
    """
    return int(USERS_SHEET.col_values(1)[index])


def calculate_total_savings(user_id: int) -> float:
    """
    Calculates the sum of all the user's savings data

    Parameters:
        user_id: the unique identifier of the user's account, used to access
        and display the data of the user who is currently logged in

    Outputs: float, returns sum of user's savings data
    """
    user_entries = get_user_entries(user_id)

    all_savings = sum([float(entry[-1]) for entry in user_entries])

    return all_savings


def calculate_budget(user_id: int, goal_amount: float, goal_date: str):
    """
    Calculates how much the user would need to save each month to reach
    their goal

    Prameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in
        goal_amount: float, amount inputted by the user
        goal_date: str, month inoutted by the user

    Outputs: float, amount needed to save each month
    """
    all_savings = calculate_total_savings(user_id)

    savings_difference = float(goal_amount) - all_savings
    total_months_difference = calc_months_difference(user_id, goal_date)

    return utils.currency(savings_difference/total_months_difference)


def calc_months_difference(user_id, goal_date):
    """
    Calculates the months difference between the user's most recent
    entry and their inputted goal date

    Prameters:
        user_id: int, the unique identifier of the user's account,
        used to access and display the data of the user who is currently
        logged in
        goal_date: str, month inoutted by the user

    Outputs: int, months between latest entry and goal date
    """
    all_month_entries = [entry[1] for entry in entries_by_date(user_id)]

    month_index = MONTHS.index(goal_date.split()[0])
    latest_month = MONTHS.index(all_month_entries[-1].split()[0])
    months_difference = month_index - latest_month

    goal_year = int(goal_date.split()[1])
    latest_year = int(all_month_entries[-1].split()[1])
    years_difference = goal_year - latest_year

    return (years_difference*12) + months_difference


# row_num = get_user_row(4)
# print(row_num)
# user_row = USERS_SHEET.row_values(row_num)
# print(user_row)