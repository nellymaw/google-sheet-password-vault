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
            
            
def main():
    print("Welcome to the Password Manager\n")
    account_exist()
    existing_acc()


main()
