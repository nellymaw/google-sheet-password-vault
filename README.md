# Password Vault
 
## Overview
The main focus of this project is to develop a password vault for storage of previously generated passwords, ideally using the [Password Generator](https://nellymaw.github.io/password-generator/) created for the portfolio project 2. 

This program can create a new master account, with a unique username and personalized password, change the master password in case of need, it can also create and modify new items inside itself (i.e. Facebook account, Slack account), it also able to display the passwords stored within it.

## How to use
Once the program starts users will be asked if they have an account. 

![HaveAcc](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/haveAcoount.png)

If the user doesn't, they will be set to create one, if on the other hand, they do, it will request their username and password, and compare it to the database.

![HaveAcc](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/whatUsername.png)

![CreateSuccess](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/createSucces.png)

In case the provided data is incorrect the user will be prompted with a choice of retrying their credentials or creating a new account.

![CreateOrRetry](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/createOrRetry.png)

If their credentials match the ones on the database, they will be displayed 5 options: Create a new password (this will allow the user to create an item inside the vault), check existing passwords(check all items inside the vault, asks for input on which should be retrieved and displays that one), change one of the existing passwords stored inside the vault, change the master password(changes password needed to log into vault's account) or exit the program.

![WhatToDo](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/whatToDo.png)

1. Create a new password.

![CreateItem](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/createItem.png)

2. Check an existing password.

![CheckItem](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/checkItem.png)

3. Modify an existing password.

![pwChange](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/pwChange.png)

4. Modify Master Password.

![pwMaster](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/pwMaster.png)

5. Exit.

Quit the program


## Design
### Flowchart

![Flowchart](https://github.com/nellymaw/google-sheet-password-vault/blob/main/readmeContent/Flowchart.svg)

## Features
**************************

## Data Model

The user used throughout the second half of the program's run contains 3 values <CELL RowN#ColN# "Value"> this data type is automatically generated via Gspread.

Through the program's code, the value is used to locate rows and columns and also values on occasion to pinpoint where the next logical step for the program is.


## Testing
I have manually tested the project by doing the following:
- Passed the code through a PEP8 linter and confirmed that there are no errors.
- Given invalid inputs, passwords too long or too short, and inputs that shouldn't be used.
- Tested in my local terminal.

I Had it tested through Heroku by a third-party.

## Bugs
### Solved Bugs
- When a new user is created but there was already a user with the same username.
- If a search returned empty there would be an AttributeError, that has been resolved.
- User use empty username

### Known Bugs
- No known bugs remaining.

## Validator Testing
- PEP8 Linter - no errors were returned from PEP8online.com

## Deployment

### GitHub Pages

The project was deployed to GitHub Pages using the following steps...

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/nellymaw/google-sheet-password-vault)
2. At the top of the Repository (not the top of the page), locate the "Settings" button on the menu.
3. Scroll down the Settings page until you locate the "GitHub Pages" Section.
4. Under "Source", click the dropdown called "None" and select "Master Branch".
5. The page will automatically refresh.
6. Scroll back down through the page to locate the now published site [link](https://github.com/nellymaw/google-sheet-password-vault) in the "GitHub Pages" section.

### Forking the GitHub Repository

By forking the GitHub Repository we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository by using the following steps...

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/nellymaw/google-sheet-password-vault)
2. At the top of the Repository (not top of page) just above the "Settings" button on the menu, locate the "Fork" button.
3. You should now have a copy of the original repository in your GitHub account.

### Making a Local Clone

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/nellymaw/google-sheet-password-vault)
2. Under the repository name, click "Clone or download".
3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

7. Press Enter. Your local clone will be created.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `CI-Clone`...
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```
### Gitpod

1. Install the gitpod browser extension. [Gitpod Browser Extension](https://www.gitpod.io/docs/browser-extension/)
2. Go to the project repository. [Google sheet password vault](https://github.com/nellymaw/google-sheet-password-vault)
3. click the gitpod button beside the about section.  ![Gitpod Deploy](https://github.com/nellymaw/password-generator/blob/main/readmeContent/gitpodDeploy.png)

## Credits
[GSpread user guide](https://docs.gspread.org/en/latest/user-guide.html)
[GSpread documentation](https://docs.gspread.org/en/latest/api.html)
[Stackoverflow](https://stackoverflow.com/questions/13949540/gspread-or-such-help-me-get-cell-coordinates-not-value)
[Stackoverflow](https://stackoverflow.com/questions/45134764/getting-all-column-values-from-google-sheet-using-gspread-and-python)
[Stackoverflow](https://stackoverflow.com/questions/40781295/how-to-find-the-first-empty-row-of-a-google-spread-sheet-using-python-gspread)