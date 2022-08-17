# BUDGE: The budget and savings tracker

![The BUDGE terminal displayed on different devices](/assets/images/responsive-test.png)

- BUDGE is a handy tool where you can keep track of your monthly spending and saving. Whether you're saving for a house or a holiday, BUDGE provides a friendly push in the right direction by analysing your spending data and providing insights on how much you should be saving each month. 
        
- Start by entering your monthly incoming and outgoing and BUDGE will calculate your savings. After you've entered a few months data, why not set a saving goal and see how much you'll need to save each month in order to reach it?

## Links

[Link to the live project (right click to open in new tab)](https://budge-savings-tracker.herokuapp.com/)

[Link to the project repository (right click to open in new tab)](https://github.com/BeckySkel/python-project-3)

---
## Table of Contents
- [Strategy](https://github.com/BeckySkel/python-project-3/blob/main/README.md#strategy)
    - [Target Audience](https://github.com/BeckySkel/python-project-3/blob/main/README.md#target-audience)
    - [User Stories](https://github.com/BeckySkel/python-project-3/blob/main/README.md#user-stories)
- [Scope](https://github.com/BeckySkel/python-project-3/blob/main/README.md#scope)
    - [Research](https://github.com/BeckySkel/python-project-3/blob/main/README.md#research)
    - [Future Features](https://github.com/BeckySkel/python-project-3/blob/main/README.md#future-features)
    - [Testing](https://github.com/BeckySkel/python-project-3/blob/main/README.md#testing)
- [Structure](https://github.com/BeckySkel/python-project-3/blob/main/README.md#structure)
    - [Flowchart](https://github.com/BeckySkel/python-project-3/blob/main/README.md#flowchart)
    - [Information Architecture](https://github.com/BeckySkel/python-project-3/blob/main/README.md#information-architecture)
    - [Data model](https://github.com/BeckySkel/python-project-3/blob/main/README.md#data-model)
- [Skeleton](https://github.com/BeckySkel/python-project-3/blob/main/README.md#skeleton)
    - [Current Features](https://github.com/BeckySkel/python-project-3/blob/main/README.md#current-features)
    - [Technologies Used](https://github.com/BeckySkel/python-project-3/blob/main/README.md#technologies-used)
- [Surface](https://github.com/BeckySkel/python-project-3/blob/main/README.md#surface)
    - [Design](https://github.com/BeckySkel/python-project-3/blob/main/README.md#design)
    - [Deployment](https://github.com/BeckySkel/python-project-3/blob/main/README.md#deployment)
- [Credits](https://github.com/BeckySkel/python-project-3/blob/main/README.md#credits)
    - [Content](https://github.com/BeckySkel/python-project-3/blob/main/README.md#content)
    - [Media](https://github.com/BeckySkel/python-project-3/blob/main/README.md#media)
    - [Acknowledgemnets](https://github.com/BeckySkel/python-project-3/blob/main/README.md#acknowledgements)

---
## Strategy

### Target Audience
- Directed at those who wish to save some money or keep track of their monthly spending, this application will most likely attract those who are saving for a specific event/item or for those who are new to keeping track of their own finances, most likely teenagers and young adults, and need some guidance on how to set a budget.

### User Stories

#### Savers
*Individuals who are saving for a specific event or purchase, an end date and/or set amount is in mind*
- As a saver, I would like to be able to set a goal to work towards.
- As a saver, I would like guidance on how to reach my savings goal in the required timeframe.
- As a saver, I would like feedback on my progress towards my goal so that I may adjust my spending accordingly.

#### Budgeters
*Individuals who do not necessarily have a specific event ot purchase in mind but would like to set a budget for themselves to follow*
- As a budgeter, I would like to easily enter my monthly income and spending and calculate the difference.
- As a budgeter, I would like to be able to view my average income, outgoings and savings.
- As a budgeter, I would like to view my total savings.

---
## Scope

### Research
- Before planning, I considered my target audience and which features would be most beneficial too them. I also considered which features would translate well to a Python-only, command-line application.

### Future Features

#### Password encryption
- Typically, passwords would be encrypted whilst being processed. But due to the learning curve and time constraints, it was not something I could include at this stage but would hope to implement in the future. No sensitive personal information is stored for the site due to this.

#### Extend budgeting options
- I'd like to introduce more ways that the user could interact with their budget and provide further resources for planning their monthly spending. Introducing a feature where the user could categorise their income or expenses would provide further insight on where they could cut down.

#### Graphs
- Introducing graphs plotted with each monthly entry would be a great way for the user to visualise their spending habits and spot any trends.

### Testing
- Throughout the project, I relied on [Gitpod](https://www.gitpod.io/)'s built-in command-line interface to interact with the app and highlight any bugs or exceptions that needed addressing. I also used the built-in Python linter to check for problems whilst building.
- Please follow [this link](assets/documents/TESTING.md) for full list of final tests carried out on this app.

---
## Structure

### Flowchart
- [Lucid](https://lucid.app/) was used to create a flowchart to map out the functions and processes of the application.
![Image of a flow chart showing the flow of the application](/assets/images/flowchart.png)

### Information architecture
- BUDGE is a web application built with Python where users can interact with a database to store monthly saving data and calculate a budget based on their inputs.
- The user interacts with the mock-terminal present in the deployed site (provided by [Code Institute's Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template)) to call actions and manipulate data.
- A "Run Program "button is present so that the user can start/reset the app.
- All data is stored within a Google Sheets workbook containing 2 worksheets: users & entries.

### Data model
- The app is linked to a Google Sheets database and uses a variety of functions to interact with and manipulate the data.
- The database is split into 2 worksheets: users & entries.
- In the 'users' worksheet exists a table with each user's user id (their unique identifier, used to acceess the correct data), their name, username, password (both used to provide a level of security before accessing the data), their chosen goal month and goal amount for their savings budget (both used to calculate how much they should be saving each month in order to reach their goals).
- The 'entries' sheet holds a table with the entry id (unique identifier of the entry, used by the app to locate the correct entry when editing), the user's id (their unique identifier), the entry number (used by the user to interact with the entry), the month, incoming and outgoing data (all used to store and display the user's saving data) and the net savings calculated from the incoming and outgoing amounts.
- The majority of the functions use the user_id to locate the correct user's data to be manipulated but some also use indexing.

---
## Skeleton

### Current Features

#### Start-up
![Screenshot of the start-up screen, including the logo, welcome message and main menu](/assets/images/welcome.png)
##### Logo
- The logo is large and bold. Printed in capitals to improve readability.
- Created with [https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20]()
- The logo is displayed upon initial launch and whenever the terminal is cleared (after login and logout). 
##### Welcome message
- Reads "Welcome to Budge: The budget and savings tracker!"
- Provides a greeting to the user as well as a quick introduction to the function of the app.
##### Main menu
- Displays a list of follow-up actions (login, create account and help), numbered 1 to 3. User input's number ascociated with the desired action. Re-called if input is invalid or if following action is exited.
- Menu also displayed after logout.

#### Start-up actions
##### Help
- Provides information about the app to the user.
- Called from the main menu and account menu, exited with empty input.
![Screenshot of help display](/assets/images/help-display.png)

##### Login
- User inputs their username and password to login and combination validated against database (not encrypted, see [Future Features](https://github.com/BeckySkel/python-project-3/blob/main/README.md#future-features)).
- Re-called with failed attempts, exited with 'exit' input.

    ![Screenshot of account login](/assets/images/login.png)

##### Create account
- User chooses and inputs a username and password and also inputs their name. Inputs then confirmed before adding to database and logging in.
- Each input re-called with failed validation, exited with 'exit' input.
![Screenshot of account setup](/assets/images/create-account.png)

#### Account
##### Entries display
- Displays a table of the user's previous entries as well as a few insights into their budgeting (total savings, overall savings goal, monthly savings goal).
- Called from account menu.
![Screenshot of entries table](/assets/images/table-display.png)

##### Account menu
- Displays a list of follow-up actions (add entry, remove entry, edit entry, edit budget, help, logout), numbered 1 to 6. User input's number ascociated with the desired action. Re-called if input is invalid or if following action is exited.
- Called after successful login or account creation and loops after each account action.
- Logout to exit to main menu.

    ![Screenshot of the account menu](/assets/images/account-menu.png)

##### Add, remove, edit entry
- User inputs entry number, month, income and/or outgoings as needed. Each input is validated.
- Inpupts are displayed and requests confirmation from user before actioning.
- Re-called after failed validation, exited with 'exit' or cancelling at confirmation.
![Screenshot of adding an entry](/assets/images/add-entry.png)
![Screenshot of removing an entry](/assets/images/remove-entry.png)
![Screenshot of editing an entry](/assets/images/edit-entry.png)

##### Budget Calculator
- Allows user to input their savings goal and a date to acheive it and provides insights and a budget that the user can save and refer back to. Monthly savings is updated with new entries so that user can adjust their spending accordingly.
- Inpupts are displayed and requests confirmation from user before saving.
- Re-called after failed validation, exited with 'exit' or cancelling at confirmation.
![Screenshot of the calculation process](/assets/images/edit-budget.png)

#### Logout
- Allows the user to logout of their account. Clears terminal and returns to main menu.
- Requests confirmation before logging out. Cancelled and returns to accouont menu if confirmation denied.
![Screenshot of logout display](/assets/images/logout.png)

### Technologies used

#### Languages
- [HTML](https://en.wikipedia.org/wiki/HTML)(Provided by Code Institute Template)
- [CSS](https://en.wikipedia.org/wiki/CSS)(Provided by Code Institute Template)
- [Git](https://en.wikipedia.org/wiki/Git) for version control
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)(Provided by Code Institute Template)
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

#### Imported modules
- [os](https://docs.python.org/3/library/os.html) to clear terminal
- [gspread](https://docs.gspread.org/en/latest/) to interact with Google Sheets
- [termcolor](https://pypi.org/project/termcolor/)
- [tabulate](https://pypi.org/project/tabulate/)

#### APIs
- [Google Drive API](https://developers.google.com/drive/api) to interact with Google files
- [Google Sheets API](https://developers.google.com/sheets/api) to interact with Google Sheets

#### Other resources
- [Gitpod](https://www.gitpod.io/) to alter and manage website files
- [Github](https://github.com/) to create and store website files
- [Heroku](https://dashboard.heroku.com/apps) to deploy web application
- [Code Institute](https://codeinstitute.net/) fullstack developer course to learn how to create and provide project template
- [W3Schools](https://www.w3schools.com/) for help with common coding queries and issues
- [GeeksforGeeks](https://www.geeksforgeeks.org/) for help with common coding queries and issues
- [Am I Responsive?](https://ui.dev/amiresponsive) for device simulations

---
## Surface

### Design

#### Colour scheme
- Text colours from [termcolor](https://pypi.org/project/termcolor/)
- Red was used for negative feedback (e.g. invalid input), green for positive feedback (e.g. input valid), yellow for alerts, magenta for menus and input info and cyan for headings.
- The consistent use of colours helps the user to determine the nature of the message before reading.
- Printed in bold to to improve readability.

#### Imagery
- There are no images used in this site.

#### Typography
- Standard font was provided by [Code Institute's Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template)).
- Logo created at [https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20]().

#### Icons
- There are no icons used in this site.

### Deployment
- This site was developed using [Gitpod](https://www.gitpod.io/), stored on [Github](https://github.com/) and deployed with [Heroku](https://dashboard.heroku.com/apps).

- Testing on Gitpod:
    1. In the terminal, type "python3 run.py" and press enter to begin the application
    2. Follow prompts on screen
    3. Once finished, use Ctrl + C to close the application

- Deploying on Heroku:
    1. From the homescreen, click "New" and select "Create new app"
    2. Choose app name, select region and click "Create"
    3. Go to "Settings" and add PORT : 8000 to the Config Vars (CREDS : {contents of creds.json file} also added but excluded from Github for security reasons)
    4. Add heroku/python and heroku/nodejs buildpacks (in that order)
    5. Go to "Deploy" and connect Github repository
    6. Select "Enable Automatic Deploys" and click "Deploy Branch"

---
## Credits

### Content
- Code to remove duplicates from date entries by [https://www.w3schools.com/python/python_howto_remove_duplicates.asp]()
- Splitting and joining string to remove extra whitespace in user response inspired by [https://www.geeksforgeeks.org/python-program-split-join-string/#:~:text=the%20split()%20method%20in,joined%20by%20the%20str%20separator.]()
- Code for creating a table from official [tabulate](https://pypi.org/project/tabulate/) documentation
- Code to clear terminal from [https://stackoverflow.com/questions/2084508/clear-terminal-in-python]()

### Media
- Logo created with [https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20]()
- Mock terminal provided by [Code Institute's Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template)).
- Text colours from [termcolor](https://pypi.org/project/termcolor/)

### Acknowledgements
- [Code Institute](https://codeinstitute.net/) for providing excellent learning content and support
- Reuben Ferrante as my mentor and providing vital feedback throughout the project's development
- [W3Schools](https://www.w3schools.com/) for quick and easy guidance
- The users of [Stack Overflow](https://stackoverflow.com/) for asking and answering some of the harder Python questions
- Other CI students for sharing their work and providing inspiration and guidance

---

Becky Skelcher 2022