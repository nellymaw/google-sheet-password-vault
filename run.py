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
SHEET = GSPREAD_CLIENT.open('pwManager')
ACC_SHEET = SHEET.worksheet('usernames')


def account_exist():
    """
    Asks if the user has an account
    """
    answerLow = ""
    while True:
        answer = input("Do you have an account? Y/N\n")
        answerLow = answer.lower()
        if answerLow == "no" or answerLow == "n":
            create_acc()
        elif answerLow == "yes" or answerLow == "y":
            return answerLow
        else:
            print("\nInvalid response.")
            continue


def existing_acc():
    """
    Check the existence of the account on the user list.
    """
    while True:
        user_check = input("\nWhat's your username?\n")
        if user_check in ACC_SHEET.col_values(1):
            user_found = ACC_SHEET.find(f"{user_check}")
        else:
            print("User not found. RETRY or CREATE a new one?")
            retryOrCreate = input("\n")
            if retryOrCreate.lower() == "retry":
                continue
            elif retryOrCreate.lower() == "create":
                create_acc()
                continue
            else:
                print("Invalid response")
                continue
        pw_verify(user_found)


def create_acc():
    """
    Create a new user on the first empty row on the users spreadsheet
    """
    invalid_user = True
    while invalid_user is True:
        new_user = input("\nWhat username would you like to use?\n")
        if new_user in ACC_SHEET.col_values(1) or " " in new_user:
            print("-*-Username Unavailable-*-")
            new_user = None
            continue
        elif new_user not in ACC_SHEET.col_values(1) and new_user is not None:
            invalid_user = False
            if invalid_user is False:
                new_user_row = int(len(ACC_SHEET.col_values(1)))+1
                ACC_SHEET.update_cell(new_user_row, 1, f'{new_user}')
                SHEET.add_worksheet(title=f'{new_user}', rows="100", cols="3")
        print("Your password must be between 6 and 255 characters.")
        new_pw = input("\nPlease type your password.\n")
        create_pw(new_pw,new_user)

def create_pw(pw,user):
    """
    Create a password for the newly created user.
    """
    while True:
        pw_check = input("Please type your password again.\n")
        if pw != pw_check or len(pw) < 6 or len(pw) > 255:
            print ("\nInvalid password.")
            continue
        elif pw == pw_check:
            new_pw_row = ACC_SHEET.find(f"{user}").row
            ACC_SHEET.update_cell(new_pw_row, 2, f'{pw}')
            print("\nYour account has been created successfully!\n")
        break


def pw_verify(user):
    """
    Checks user's password against database
    """
    pw_accepted = False
    while pw_accepted is False:
        pw_check = input("\nWhat's your password?\n")
        pw_counter = ACC_SHEET.cell(user.row, 2).value
        if pw_check != pw_counter:
            print("\n-x-Wrong password-x-")
            continue
        elif pw_check == pw_counter:
            pw_accepted = True
            pw_passed(user)


def pw_passed(user):
    """
    Presents options for the user to interact with his account.
    """
    while True:
        print("\nWhat would you like to do?")
        print("1.Create a new password.")
        print("2.Check an existing password.")
        print("3.Modify an existing password.")
        print("4.Modify your master password.")
        choice = input("5.Exit\n")
        if choice == "1":
            inner_new(user)
        elif choice == "2":
            inner_check(user)
        elif choice == "3":
            single_change(user)
        elif choice == "4":
            master_change(user)
        elif choice == "5":
            print("\nGoodbye")
            quit()
        else:
            print("Invalid choice.\n")
            continue


def inner_new(user):
    """
    Creates a new item in the vault
    """
    while True:
        user_page = ACC_SHEET.cell(user.row, user.col).value
        local_ws = SHEET.worksheet(user_page)
        new_obj = input("Website/app name:\n")
        if new_obj not in local_ws.col_values(1):
            new_un = input("Username:\n")
            new_pass = input("Password:\n")
            local_ws.update_cell((len(local_ws.col_values(1))+1), 1, new_obj)
            local_ws.update_cell((len(local_ws.col_values(2))+1), 2, new_un)
            local_ws.update_cell((len(local_ws.col_values(3))+1), 3, new_pass)
        else:
            print("Already have a password for that.\n")
        break


def single_change(user):
    """
    Locate and change a password inside the user's worksheet
    """
    while True:
        user_page = ACC_SHEET.cell(user.row, user.col).value
        local_ws = SHEET.worksheet(user_page)
        print("\nWould you like to CHECK whick apps/websites")
        print("you have a password for or do you already know")
        answer = input("Which password you want to CHANGE?\n")
        if answer.lower() == "check":
            print(local_ws.col_values(1))
        elif answer.lower() == "change":
            change_pw = input("What password would you like to change it to?\n")
            if change_pw in local_ws.col_values(1):
                pw_location = local_ws.find(f"{change_pw}")
                new_pw = input("What's the new password?\n")
                local_ws.update_cell(pw_location.row, 3, new_pw)
            else:
                print("Invalid entry")
                continue
        else:
            print("invalid entry")
            continue
        break
    pass


def inner_check(user):
    """
    Print a list of passwords saved in the database,
    asks for input, and display the password selected
    """
    while True:
        user_page = ACC_SHEET.cell(user.row, 1).value
        local_ws = SHEET.worksheet(user_page)
        print("Which password would you like to retrieve?")
        print (f"{local_ws.col_values(1)}")
        pw_choice = input("\nPlease type the exact name\n")
        if pw_choice in local_ws.col_values(1):
            local_pws = local_ws.find(f"{pw_choice}").row
            print(f"\nUsername: {local_ws.cell(local_pws,2).value}")
            print(f"Password: {local_ws.cell(local_pws,3).value}")
            break
        else:
            print("Invalid response\n")
            continue
    pass


def master_change(user):
    while True:
        new_master = input('\nEnter new master password\n')
        if len(new_master) >= 6 and len(new_master) <= 255:
            PW_SHEET.update_cell(user.row, 1, f'{new_master}')
            print("Password modified successfully!")
            break
        else:
            print("Invalid master password")
            continue


def main():
    print("Welcome to the Password Manager\n")
    account_exist()
    existing_acc()


main()
