from tabulate import tabulate
from constants import USERS_SHEET, ENTRIES_SHEET, HEADERS, MONTHS
import utils


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


def entries_by_date(user_id):
    """"""
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


def get_user_row(user_id):
    """
    """
    all_users = USERS_SHEET.get_all_values()[1:]

    for entry in all_users:
        uid = int(entry[0])
        if uid == user_id:
            return all_users.index(entry) + 2


def save_budget_info(user_id, goal_amount, goal_date):
    """"""
    row_num = get_user_row(user_id)
    USERS_SHEET.update(f'E{row_num}:F{row_num}', [[goal_amount, goal_date]])


def display_table(user_id):
    """
    Displays all of the current user's previous table entries

    Parameters: user_id: the unique identifier of the user's account,
    used to access and display the data of the user who is currently logged in

    Outputs: prints table of current user's spending data to the console
    """
    # Code for creating a table from official tabulate documentation
    print(tabulate(entries_by_date(user_id), HEADERS, tablefmt='psql'))

    total_savings = calculate_total_savings(user_id)
    print(f"Total Savings(£): {total_savings}")

    user_row = USERS_SHEET.row_values(get_user_row(user_id))
    try:
        goal_amount, goal_date = user_row[4], user_row[5]
        print(f"Overall Savings Goal(£): {goal_amount} by {goal_date}")
        savings_goal = calculate_budget(user_id, goal_amount, goal_date)
        print(f"Monthly Savings Goal(£): {savings_goal}\n")
    except IndexError:
        print()


def append_row(row, sheet):
    """"""
    if sheet == 'users':
        USERS_SHEET.append_row(row)
    else:
        ENTRIES_SHEET.append_row(row)


def next_user_id():
    """"""
    return int(USERS_SHEET.col_values(1)[-1])+1


def next_entry_id():
    """"""
    try:
        entry_id = int(ENTRIES_SHEET.col_values(1)[-1])+1
    except IndexError:
        entry_id = 1

    return entry_id


def get_usernames():
    """"""
    return USERS_SHEET.col_values(3)[1:]


def get_passwords():
    """"""
    return USERS_SHEET.col_values(4)[1:]


def uid_by_index(index):
    """"""
    return int(USERS_SHEET.col_values(1)[index])


def calculate_total_savings(user_id):
    """"""
    user_entries = get_user_entries(user_id)

    all_savings = sum([float(entry[-1]) for entry in user_entries])

    return all_savings


def calculate_budget(user_id, goal_amount, goal_date):
    """
    """
    all_savings = calculate_total_savings(user_id)

    savings_difference = float(goal_amount) - all_savings
    total_months_difference = calc_months_difference(user_id, goal_date)

    # return round(savings_difference/total_months_difference, 2)
    return utils.currency(savings_difference/total_months_difference)


def calc_months_difference(user_id, goal_date):
    """"""
    all_month_entries = [entry[1] for entry in entries_by_date(user_id)]

    month_index = MONTHS.index(goal_date.split()[0])
    latest_month = MONTHS.index(all_month_entries[-1].split()[0])
    months_difference = month_index - latest_month

    goal_year = int(goal_date.split()[1])
    latest_year = int(all_month_entries[-1].split()[1])
    years_difference = goal_year - latest_year

    return (years_difference*12) + months_difference
