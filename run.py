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
PW_SHEET = SHEET.worksheet('passwords')


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
            print("Your password must be between 6 and 255 characters.")
            new_pw = input("\nPlease type your password.\n")
            create_pw(new_pw)
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
            retryOrCreate = input("")
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
        if new_user in ACC_SHEET.col_values(1):
            print("-*-Username Unavailable-*-")
            new_user = None
            continue
        elif new_user not in ACC_SHEET.col_values(1) and new_user is not None:
            invalid_user = False
            if invalid_user is False:
                new_user_row = int(len(ACC_SHEET.col_values(1)))+1
                ACC_SHEET.update_cell(new_user_row, 1, f'{new_user}')
                SHEET.add_worksheet(title=f'{new_user}', rows="100", cols="3")


def create_pw(pw):
    """
    Create a password for the newly created user.
    """
    while True:
        pw_check = input("Please type your password again.")
        if pw != pw_check or len(pw) < 6 or len(pw) > 255:
            print ("\nInvalid password.")
            continue
        elif pw == pw_check:
            new_pw_row = int(len(PW_SHEET.col_values(1)))+1
            PW_SHEET.update_cell(new_pw_row, 1, f'{pw}')
            print("\nYour account has been created successfully!\n")


def pw_verify(user):
    """
    Checks user's password against database
    """
    pw_accepted = False
    while pw_accepted is False:
        pw_check = input("\nWhat's your password?\n")
        pw_counter = PW_SHEET.cell(user.row, 1).value
        if pw_check != pw_counter:
            print("\n-x-Wrong password-x-")
            continue
        elif pw_check == pw_counter:
            pw_accepted = True
            pw_passed(user)


def pw_passed(user):
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



def main():
    print("Welcome to the Password Manager\n")
    account_exist()
    existing_acc()


main()
