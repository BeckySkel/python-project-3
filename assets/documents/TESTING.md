# Website Testing

###  Python Linter
- Some warnings displayed due to splitting of Python code betweeen multiple files. When code combined and ran together, these warnings disappear.
- Any issues found have been rectified and all pages now pass with no errors to show. Any warnings receive explained below.

#### run.py
![Feedback from run through the pep8online linter for run.py](/assets/images/display-jshint-result.png)

---
## Lighthouse
- All pages were ran through Lighthouse on Chrome Devtools for both desktop and mobile device display. Ran in incognito mode. Any issues were dealt with and all now have a high passing mark.

#### index.html
- Desktop

![Screenshot of Lighthouse score for standard display of index.html on desktop](/assets/images/index-desktop.png)

- Mobile

![Screenshot of Lighthouse score for standard display of index.html on mobile](/assets/images/index-mobile.png)

---
## Manual testing

### Inputs
- All navigation buttons tested manually **8/7/22** and found to be working as intended
- All game buttons tested manually **8/7/22** and found to be working as intended
- All game levels tested manually on **8/7/22** and found to be working as intended
- All upgrade unlocks tested manually on **8/7/22** and found to be working as intended
- All uprgade toggles tested manually on **8/7/22** and found to be working as intended

### 404.html
- - All navigation buttons tested manually **10/7/22** and found to be working as intended

---
## Different browsers
- Tested and found to be working as intended on the following browsers :
    - Chrome
    - Firefox
    - Microsoft Edge
- Unable to test on Safari as unble to download on my Windows PC
- Certain features are not supported on Internet Explorer and therefore some feature are not displaying properly. However, Internet Explorer was retired by Microsoft in August 2021 and is no longer supported.

---
## Different devices with Chrome Devtools
- Tested on the following devices via Chrome Devtools and found to be working as intended:
    - iPhone SE
    - iPhone XR
    - iPhone 12 Pro
    - Pixel 5
    - Samsung Galaxy S8+
    - Samsung Galaxy S20 Ultra
    - iPad Air
    - iPad Mini
    - Surface Pro 7
    - Surface Duo 
    - Samsung Galaxy A51/71
    - Nest Hub
    - Nest Hub Max

---
## Media Queries
- Media queries were introduced at the below break points:
    - 1024px
    - 770px
    - 600px
    - 340px

---
## Bugs
### Resolved Bugs
- Issue where screen would inch to left slightly when displayed message at bottom of screen, solved with help from by adding `overflow: hidden;` to budy during function and removing once element removed.
- Issue with dividing width of score bar and multiplying by points to increment progress bar not calling a level-up solved by reducing precision of condition.
- Issue with level 5 progress bar extending past the container solved by applying `overflow: hidden;` to container.
- Originally tried to call multiple messages to display but this caused a bug as it meant multiples of the same ID. Fixed by removing old message once finished with.
- Error was displayed in console when displaying the rules message type. This did not affect the message being displayed. Solved by altering function to display message by removing code to populate butttons if rules message called.
- Bug where upgraded backgrouns colour was not taking up whole screen when applied solved by adding JavaScript to add in-line style to overide any other styles.
- Issue with trying to display the chosen weapon icon by using code to map the index in an array solved with code from [Borislav Hadzhiev](https://bobbyhadz.com/blog/javascript-array-find-index-of-object-by-property)
- Issue where player is able to display multiple level-up messages by raidly clicking game buttons, thus causing mutliple elements of the same ID and causing the the game to break. Solved by calling the disableBackground function immediately after level-up is established, before the message is displayed.

### Unresolved Bugs
- Scrolling on mobile device very briefly displays white background at the bottom of the page - have tried a few combinations of background properties but none have fixed this. It is only brief and does not affext user experience.
