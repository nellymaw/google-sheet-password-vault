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

def main():
    print("Welcome to the Password Manager\n")
    account_exist()

main()
