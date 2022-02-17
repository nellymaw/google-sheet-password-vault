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


def does_account_exist():
    """
    Enquires the user if he has an account
    """
    answer_low = ""
    while True:
        answer = input("Do you have an account? Y/N\n")
        answer_low = answer.lower()
        if answer_low == "no" or answer_low == "n":
            create_account()
        elif answer_low == "yes" or answer_low == "y":
            return answer_low
        else:
            print("\nInvalid response.")
            continue


def verify_account():
    """
    Check the existence of the account on the user list.
    """
    while True:
        user_check = input("\nWhat's your username?\n")
        if user_check.upper() in ACC_SHEET.col_values(1):
            user_found = ACC_SHEET.find(f"{user_check.upper()}")
        else:
            print("\nUser not found. RETRY or CREATE a new one?")
            retry_create = input("\n")
            if retry_create.lower() == "retry":
                continue
            elif retry_create.lower() == "create":
                create_account()
                continue
            else:
                print("Invalid response")
                continue
        verify_password(user_found)


def create_account():
    """
    Create a username for the user's account
    """
    invalid_user = True
    new_user = None
    while invalid_user is True:
        new_user = input("\nWhat username would you like to use?\n").upper()
        if new_user in str(ACC_SHEET.col_values(1)).upper() or " " in new_user or len(new_user) < 1:
            print("-*-Username Unavailable-*-")
            continue
        elif new_user.upper() not in str(ACC_SHEET.col_values(1)).upper() and new_user is not None:
            invalid_user = False
            if invalid_user is False:
                new_user_row = int(len(ACC_SHEET.col_values(1)))+1
                ACC_SHEET.update_cell(new_user_row, 1, f'{new_user}')
                SHEET.add_worksheet(title=f'{new_user}', rows="100", cols="3")
        print("\nYour password must be between 6 and 255 characters.")
        create_master_password(new_user)


def create_master_password(user):
    """
    Create a password for the newly created account
    """
    while True:
        new_password = input("Please type your password.\n")
        password_check = input("\nPlease type your password again.\n")
        if new_password != password_check or len(new_password) < 6 or len(new_password) > 255:
            print ("\nInvalid password.")
            continue
        elif password_check == new_password:
            new_pw_row = ACC_SHEET.find(f"{user}").row
            ACC_SHEET.update_cell(new_pw_row, 2, f'{new_password}')
            print("\nYour account has been created successfully!\n")
        break


def verify_password(user):
    """
    Verifies the entered password against the database
    """
    password_accepted = False
    while password_accepted is False:
        password_check = input("\nWhat's your password?\n")
        password_counter = ACC_SHEET.cell(user.row, 2).value
        if password_check != password_counter:
            print("\n-x-Wrong password-x-")
            continue
        elif password_check == password_counter:
            password_accepted = True
            account_options(user)


def account_options(user):
    """
    Display account options
    """
    while True:
        print("\nWhat would you like to do?")
        print("1.Create a new password.")
        print("2.Check an existing password.")
        print("3.Modify an existing password.")
        print("4.Modify your master password.")
        choice = input("5.Exit\n\n")
        if choice == "1":
            create_new_password(user)
        elif choice == "2":
            check_existing_password(user)
        elif choice == "3":
            change_single_password(user)
        elif choice == "4":
            change_master_password(user)
        elif choice == "5":
            print("\nYou've been logged off.")
            quit()
        else:
            print("Invalid choice.\n")
            continue


def create_new_password(user):
    """
    Creates a new item in the user's vault
    """
    while True:
        user_worksheet = ACC_SHEET.cell(user.row, user.col).value
        local_ws = SHEET.worksheet(user_worksheet)
        new_obj = input("\nWebsite/app name:\n")
        if new_obj not in local_ws.col_values(1):
            new_un = input("\nUsername:\n")
            new_pass = input("\nPassword:\n")
            local_ws.update_cell((len(local_ws.col_values(1))+1), 1, new_obj.upper())
            local_ws.update_cell((len(local_ws.col_values(2))+1), 2, new_un)
            local_ws.update_cell((len(local_ws.col_values(3))+1), 3, new_pass)
            print(f"Successfully created {new_obj}")
        else:
            print("Already have a password for that.\n")
        break


def check_existing_password(user):
    """
    Print a list of passwords saved in the user's vault,
    asks for input, then display the selected password
    """
    while True:
        user_worksheet = ACC_SHEET.cell(user.row, 1).value
        local_ws = SHEET.worksheet(user_worksheet)
        print("\nWhich password would you like to retrieve?")
        print (f"{str(local_ws.col_values(1)).upper()}")
        password_choice = input("\nPlease type the exact name\n")
        if password_choice.upper() in str(local_ws.col_values(1)).upper():
            local_pws = local_ws.find(f"{password_choice}").row
            print(f"\nUsername: {local_ws.cell(local_pws,2).value}")
            print(f"Password: {local_ws.cell(local_pws,3).value}")
            break
        else:
            print("Invalid response\n")
            continue


def change_single_password(user):
    """
    Locate and update a password inside the user's vault
    """
    while True:
        user_worksheet = ACC_SHEET.cell(user.row, user.col).value
        local_ws = SHEET.worksheet(user_worksheet)
        print("\nWould you like to CHECK whick apps/websites")
        print("you have a password for or do you already know")
        answer = input("Which password you want to CHANGE?\n")
        if answer.lower() == "check":
            print(str(local_ws.col_values(1)).upper())
        elif answer.lower() == "change":
            change_pw = input("Please type your new password\n")
            if change_pw in local_ws.col_values(1):
                pw_location = local_ws.find(f"{change_pw}")
                new_pw = input("What's the new password?\n")
                local_ws.update_cell(pw_location.row, 3, new_pw)
                print("Password changed successfully.")
            else:
                print("Invalid entry")
                continue
        else:
            print("invalid entry")
            continue
        break


def change_master_password(user):
    '''
    Change the master password for the user's account
    '''
    while True:
        new_master = input('\nEnter new master password.\n')
        check_new_master = input ('\nPlease repeat your new master password.\n')
        if len(new_master) >= 6 and len(new_master) <= 255 and new_master == check_new_master:
            ACC_SHEET.update_cell(user.row, 2, f'{new_master}')
            print("Master password modified successfully!")
            break
        else:
            print("Invalid master password")
            continue


def main():
    print("Welcome to the Password Manager\n")
    does_account_exist()
    verify_account()


if __name__ == '__main__':
    main()
