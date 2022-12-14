# Website Testing

###  Python Linter
- All python files run through [pep8online](http://pep8online.com/)
- Any issues found have been rectified and all pages now pass with no errors to show. Any warnings receive explained below.

#### run.py
![Feedback from run through the pep8online linter for run.py](/assets/images/run-result.png)

#### utils.py
![Feedback from run through the pep8online linter for utils.py](/assets/images/utils-result.png)

#### constants.py
![Feedback from run through the pep8online linter for constants.py](/assets/images/constants-result.png)

#### google_sheets.py
![Feedback from run through the pep8online linter for google_sheets.py](/assets/images/gsheet-result.png)

#### validations.py
![Feedback from run through the pep8online linter for validations.py](/assets/images/validations-result.png)

---
## Manual testing

### Valid inputs
- All inputs for all functions tested with valid input on *17/8/22* and found to be working as intended

### Invalid inputs
- Main Menu inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - 0
    - 4
    - cat
    - (empty)
- Login inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - incorrect username, correct password
    - correct password, incorrect username
    - incorrect both
    - numbers
    - (empty)
- Create Account inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - a (username too short)
    - abcdefghijklmnopqrs (username too long)
    - username (username taken)
    - Aa1 (password too short)
    - Abcdefghijklmnopqrs1 (password too long)
    - password1 (doesn't contain uppercase)
    - PASSWORD1 (doesn't contain lowercase)
    - Password (doesn't contain number)
- Account Menu inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - 0
    - 7
    - cat
    - (empty)
- Month Entry inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - 0
    - 2022
    - jan
    - jan2022
    - jan 22
    - (empty)
- Amount Entry inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - -300
    - cat
    - (empty)
- Entry Number inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - 0
    - 25
    - cat
    - (empty)
- Logout inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - 0
    - 3
    - cat
    - (empty)
- Confirm Action inputs tested with the following **incorrect** inputs on *17/8/22* and found to be working as intended:
    - 0
    - 3
    - cat
    - (empty)


---
## Different browsers
- Tested and found to be working as intended on the following browsers :
    - Chrome
    - Firefox
    - Microsoft Edge
- Unable to test on Safari as unble to download on my Windows PC

---
## Bugs
### Resolved Bugs
- Initially when taking a username input, the first input was taking dispite failing validation. This was corrected by moving the input request to a seperate function.
- It was originally very difficult to find out which row number to use for removing entries but after a lot of trial and error, I realised it as the index + 2 due to only taking the entries and not the headings. 
- coloured text shows too dark in CI terminal, made bold coloured text bold to combat this and improve readability

### Unresolved Bugs
- To my knowledge, there are no unresolved bugs.
