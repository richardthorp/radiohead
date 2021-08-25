# Radiohead - Milestone 4
A mock website for the band Radiohead, featuring on online shop, exclusive content subscription service, api powered gig listings and media hub.

[Click here to view live website](https://radiohead-ms4.herokuapp.com/)
## Table of Contents
[Brand Objectives](#objectives)

[User Experience - UX](#UX)

[Design](#design)

[Features](#features)

[Languages and Technologies](#tech)

[Testing](#testing)

[Deployment](#deployment)

[Credits](#credits)

<a name="objectives"></a>
## Website Objectives
The primary objectives of the website are to:
* Functionality to sell music and merchandise.
* Promote upcoming concerts.
* Provide a platform for the band to announce news and release content.
* Financially capitalise on fans.

<a name="UX"></a>
## UX
### User Profiles

### User Stories
#### As a first time user, I want:
* To quickly understand the purpose of the website.
* To be able to register and sign in easily.
* To be able to sign out easily.
* To be able to navigate through the website intuitively and easily.
* To find content relating to the band Radiohead.

#### As a returning user, I want:
* To be able to log in and out easily and to be able to remain signed in.
* To be able to reset my password should I forget it.
* To be able to find details about my previous orders.
* To be able to view details about my subscription.
* To be able to easily cancel my subscription.
* To be able to easily reactivate my subscription after cancelling.
* To be able to change my subscription payment card.
* To be able to save my details to use for any future purchases.
* To be able to find new merchandise quickly in the shop.
* To be able to find new music quickly in the Media section.
* To be able to view new content quickly in the Portal area.

#### Shared user requirements:
* To be able to communicate with other fans of the band.
* To be able to buy music and merchandise from the band.
* To be able to find details about upcoming concerts.
* To be able to find and consume music.
* To be able to find recent news, updates and other content.

<a name="design"></a>
## Design
### Wireframes
[Click here to see 'Index' wireframes](readme-images/wireframes/index.png)

[Click here to see 'Add Portal Item' wireframes](readme-images/wireframes/add-portal-item.png)

[Click here to see 'Add Product' wireframes](readme-images/wireframes/add-product.png)

[Click here to see 'Media- Album Singles' wireframes](readme-images/wireframes/album-singles.png)

[Click here to see 'Basket' wireframes](readme-images/wireframes/basket.png)

[Click here to see 'Checkout' wireframes](readme-images/wireframes/checkout.png)

[Click here to see 'Live Detail' wireframes](readme-images/wireframes/live-detail.png)

[Click here to see 'Live' wireframes](readme-images/wireframes/live.png)

[Click here to see 'Media - Single Detail' wireframes](readme-images/wireframes/media-single-detail.png)

[Click here to see 'Media' wireframes](readme-images/wireframes/media.png)

[Click here to see 'Order Confirmation/Order History Detail' wireframes](readme-images/wireframes/order-confirmation.png)

[Click here to see 'Portal Item' wireframes](readme-images/wireframes/portal-item.png)

[Click here to see 'Portal (signed-in)' wireframes](readme-images/wireframes/portal-signed-in.png)

[Click here to see 'Portal (signed-out)' wireframes](readme-images/wireframes/portal-signed-out.png)

[Click here to see 'Shop - Product Detail' wireframes](readme-images/wireframes/product-detail.png)

[Click here to see 'Profile' wireframes](readme-images/wireframes/profile.png)

[Click here to see 'Shop' wireframes](readme-images/wireframes/shop.png)

[Click here to see 'Sign-in/Sign-up' wireframes](readme-images/wireframes/sign-up.png)

### Colour Scheme
The website is almost entirely monochromatic, with most components consitsing of white, grey and black. This results a very clean and simple and elegant user interface whilst also allowing features such as images to contrast sharply on the page. The static background image which can be found on every page provides a nice backdrop which makes the page more interesting visually whilst not overpowering the general aesthetic.

### Fonts
#### Logo and Navigation Links
The font found throughout the website header is EuroseWide Heavy. This font is used by Radiohead on much of their official branding, including the band logo on the album 'OK Computer'. As the font is bold and highly legible, it was an obvious choice for both the Logo and navigation links
#### Headers
The header font was chosen due to its similarity to the font found on the cover of the album 'Kid A'. Whilst the actual Kid A font (BD Plakatbau) was used in the 'Welcome to the home of Radiohead' animation on the home page, it lacked several punctuation charactors, making it unsuitable to use throughout the website. 
The font 'Righteous' from Google fonts was used as a replacement for all headers due to it's similarity to 'BD Plakatbau'.

** Insert images of BD Plakatbau and Righteous.

#### Main content
The font found throughout the main body of the website is 'Oswald' from Google Fonts. The font is highly legible and compliments the 'Righteous' found found in the headers.

### Database Schema
Below is a diagram detailing the database schema, with the connecting lines showing the tables relationships to one another.

** Insert DB diagram image

<a name="features"></a>

## Features
### Shared Features
#### Header
* The header element, which features the websites navigation links and logo is at the top of every page on the website.
    * The header is responsive, with the navigation links moving into a dropdown menu on screens 1200px and smaller.
    * The header features a seperate dropdown for functionality relating to user profiles and signing in and out.
    * The shopping cart icon displays the current number of individual items in the users bag
        * Clicking on the shopping cart icon diplays items currently in the users shopping bag as well as the price totals, including how much more the user needs to spend to be eligable for free postage. 
* Only one dropdown menu can be viewed at once. If the user click on a dropdown menu icon whilst a different dropdown is being displayed, a Javascript function is called to hide the original dropdown. This ensures the screen doesn't get overloaded with dropdown menus.
* Every page can display messages in the form of a 'toast', which appear just below the website header. These messages are available to the user to view for 4 seconds before fading away. The toast features different colour highlights for different message categories (green for success, blue for general information, red for errors).

#### Footer
* Every page features a simple footer which contains links to the band's social media and Spotify channels.

#### Site-wide Features
* The website is responsive down to a screen size of 320px
* Where possible, the URL scheme features 'slugified' URLs which provide more meaningful and understandable URL's

#### Authentication and Security Features
* The website's authentication features are implemented using django-allauth. This 3rd party package provides the website's sign-in and sign-out functionality, as well as providing basic templates to the authentication pages which have then been customised to match the rest of the wesites design and branding.
* Any restricted pages or views (either due to being for website staff or to paying users) redirect users that try to access them without the correct credentials.
* All secret keys related to the website are kept in enviromental variables and have been kept out of source control.
* All payments are handled by the Stripe API.
* Access to the websites subscription content can only be accessed after a webhook from the Stripe API has been received confirming a successful payment and active subscription.

#### Staff User Features
* If the logged in user has staff privileges, additional links are rendered on certain pages.
    * In the profiles dropdown menu found in the header, an additional link to the 'Admin Hub' is rendered.
        * Within the 'Admin Hub', users can quickly navigate to any areas of the website that deal with adding content (such as shop products, media content and portal blog posts), as well as some brief additional information. These links can also be found at the top of each app's main page.
    * Staff users can edit or delete individual shop products, media items and portal blog posts by navigating to the item and clicking the 'edit' or 'delete' buttons that are rendered at the top of the content.
    * Staff users can delete comments made by other users in the Media and Portal apps.
    * Staff users can not access the main website admin features provided by Django, such as editing the database.

### Individual App features
#### Home App Features
* A simple landing page (index.html) featuring a Javascript powered welcome text animation and a brief description of the websites 'Portal' subscription service.
* An 'Admin Hub', as described in the 'Staff User Features' section above.

#### Profiles App Features
* The Profile app allows users to add and update delivery information, add a profile image, view the details of their Portal subscription if one exists, and browse a list of previous orders.
* If a user has an active Portal subscription, the option to cancel the subscription or to change the payment method are presented on the profile page.
* By clicking on an order in the 'Order History' section of the profile page, the user is directed to an 'Order Details' page containing details about the order.

#### Live App Features
* The Live app provides users with a paginated list of upcoming concerts. 
* Concert listings are provided by the Songkick API. As Radiohead don't actually have any upcoming gigs, the results currently on the website are in fact for The Beach Boys. Slightly different vibe but probably still a great concert.
* The table that contains the concert listings is responsive, with the table headers moving to the left hand side on screen sizes of 768px and less.
* Clicking on the 'More Info' button of a concert listing takes the user to the 'Event Info' page. This page contains more information about the concert as well as a map showing the location of the venue on an interactive map. The map is powered by the Google Maps API.
* Cicking on the 'Find Tickets' button on the 'Event Info' page links to the Songkick website and a page which contains links to ticket vendors for the concert.

#### Media App Features
* The Media app provides users with access to all music videos that belong to singles released by the band.
* The singles are grouped by the album from which they came.
* Whilst browsing an albums singles, a link to view to album in the shop is always on screen.
* When on a 'Single Detail' page, a Javascript function ensures that the Youtube iframe is always a good size for the users viewport.
* Each 'Single Detail' page features a link to view the related album in the shop, and to listen to the album on Spotify.
* Logged in users can leave comments underneath the video. Comments are sent and rendered asynchronously to allow the video to play uninterupted.

#### Portal App
* The Portal app contains the content that is made available to users only by paying a subscription fee.
* If a non subscribed user clicks on a 'Portal' link in the navbar or anywhere else thoughout the website, a page that explains the benefits of subscribing is presented, as well as links to either register/sign-in or subscribe.
* If a subscribed user or staff member clicks on a 'Portal' link, they are automatically redirected to the actual portal content.
* Portal content comes in three different formats, each with slightly different templates:
    * Text post - The post is just text and does not feature any additional media (ie. videos or images).
    * Video post - The post features text content as well as a video. The page features a Javascript function which ensures that the Youtube iframe is always a good size for the users viewport.
    * Images post - The post contains text content as well as up to 8 images which are viewed in a Bootstrap carousel.
* All posts include a comment feature at the bottom of the page. Comments are sent and rendered asynchronously to allow the video to play uninterupted.
* When on the main portal page, users can filter the types of post they want to see using the buttons at the top of the page.

#### Shop App
* The Shop app provides a paginated list of items for sale.
* Items in the shop can be filtered by 'Music', 'Clothing' or 'Other'.
* Different templates are used to present different products in the shop.
* The album template allows users to select a product of a certain format(CD or Vinyl) as well as displaying the albums tracklisting.
* The product template allows users to choose as size if sizes for that product are available(Small, Medium and Large).
* Both templates allow users to select a quantity of the product to add to their bag.

#### Bag App
* The bag app allows users to view the current contents of their bag, as well as update any quantities or remove items entirely
* Whilst viewing the bag, the individual costs are presented to the user (order total, delivery total and grand total) These costs are automatically updated if the user updates the quantity or removes an item in the bag.
* Whilst viewing the bag, if the user hasn't reached the threshold for free delivery (£25), a small notification is displayed above the grand total to tell them how much more they need to spend to qualify for free delivery.

#### Checkout App
* By navigating to the checkout page, a payment intent for the value of the users current bag is generated though the Stripe API.
* The checkout page contains 2 forms:
    * An order form which collects customer details.
    * A payment forms generated via the Stripe API, which collects the users payment information.
* After a succeessful payment, the user is directed to the 'Order Confirmed' page, which features a summary of the order.

#### 404 Page
* If a user tries to navigate to an non existant URL, a custom '404 Page Not Found' page is rendered with a link back to the home page.

#### 500 Page
* Should there be a server error, the user is presented with a custom '500 Server Error' page containing a link back to the home page.

#### Potential Future Features
* Social media sign in could be implemented via All-Auth's SocialApp functionality.
* I would like to be able to allow users to click 'attending' on the 'Event Detail' page in the Live app as well as 'add comment' functionality.

<a name="tech"></a>

## Languages and Technologies
### Languages
* HTML5 - to structure and add content to the front-end.
* CSS3 - to add styles and responsivity to the front-end.
* JavaScript - to provide any interactive elements on the front end including the comment functionality, as well as making calls to the Stripe, Songkick and Google Maps APIs.
* Python - used to code the back-end of the website.

### Technologies
#### Main Libraries, Frameworks and Packages 
* [Django](https://www.djangoproject.com/) - provides the web app's framework.

* [Stripe](https://stripe.com/gb) - allows the web app to communicate with the Stripe API

* [Bootstrap](https://getbootstrap.com/) - for some of the front-end styling, responsive design and interactive features, such as menu drop-downs and modals.

* [jQuery](https://jquery.com/) - simplifies the apps asyncronous functions syntax, as well as shortening and simplifying JavaScript for DOM manipulation and traversal.

* [Django-Crispy-Forms](https://django-crispy-forms.readthedocs.io/) - provides additional styles to forms.

* [Django-Countries](https://pypi.org/project/django-countries/) - ensures the 'Country' field in forms provide valid ISO 3166-1 values.

* [Gunicorn](https://gunicorn.org/) - to act as the web server once deployed to Heroku.

* [Coverage](https://coverage.readthedocs.io/en/coverage-5.5/) - to provide information the scope of the apps testing modules.

* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - allows the app to communicate and integete with Amazon's S3 services.

* [dj-database-url](https://pypi.org/project/dj-database-url/) - parses the database URL from the enviromental variables on Heroku.

* [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - an adaptor for Python and PostgreSQL databases. 

#### IDE, Version control and Deployment
* [Gitpod](https://www.gitpod.io/) - The IDE used to write the code for the website.
   
* [Git](https://git-scm.com) - Used for version control during the website build via the command terminal in Gitpod
   
* [GitHub](https://pages.github.com/) - Used to store the code after being 'committed' and 'pushed' using Git.

* [Heroku](https://www.heroku.com/) - Used to deploy the website.

#### Database
* [SQLite](https://www.sqlite.org/index.html) - The database used during development.

* [Heroku Postgres](https://www.heroku.com/postgres) - The database used in production.

#### Design and Fonts
* [Balsamiq](https://balsamiq.com/) - Software used to create wireframes of website.

* [Google Fonts](https://fonts.google.com/) - Used to provide the 'Oswald' and 'Righteous' fonts used throughout the website.

* [Font Awesome](https://fontawesome.com/) - Used to provide icons in the website.

* [Font Squirrel](https://www.fontsquirrel.com/) - Used to convert ttf font files to woff and woff2 formats.

* [RealFaviconGenerator](https://realfavicongenerator.net/) - Used to refine the favicon and provide the HTML to link to the file.

* [dbdiagram](https://dbdiagram.io/) - Used to make image of database schema.

#### Testing, Optimisation and Validation
* [W3C Markup Validation Service](https://validator.w3.org/) - Validation of the HTML code.

* [W3C CSS Validation Service (Jigsaw)](https://jigsaw.w3.org/css-validator/) - Validation of the CSS code

* [JSHint](https://jshint.com/) - Validation of the JavaScript code.

* [Autoprefixer](https://autoprefixer.github.io/) - Used to ensure cross browser validity for CSS.

* [PEP 8](https://www.python.org/dev/peps/pep-0008/) - Used as a style guide for Python code.

* [TinyPNG](https://tinypng.com/) - Used to compress images.

* [Am I Responsive?](http://ami.responsivedesign.is/) - Used to test for responsive design and to create the mock-ups found at the top of this README.

* [Chrome DevTools](https://developer.chrome.com/docs/devtools/) - Used to test responsivity of website and test contrast between backgrounds and fonts. Also used to check for any JavaScript errors or warnings printing the console.

<a name="testing"></a>

## Testing
### Testing against Website Objectives
* Functionality to sell music and merchandise.
    * This objective is met via the Shop app.
* Promote upcoming concerts.
    * This objective is met via the Live app.
* Provide a platform for the band to announce news and release content.
    * This objective is met via the Portal app.
* Financially capitalise on fans.
    * This objective is met via both the Portal and Shop apps. Additionaly, as users need an email address to sign in to the website, these email addresses can be used for marketing campaigns or upcoming promotions etc.

### Testing against User Stories
#### As a first time user, I want:
* To quickly understand the purpose of the website.
    * The landing page feaures the animated text 'Welcome to the home of Radiohead' ensuring the user understands this is a website about Radiohead.
    * The home page features a brief summary of what users can find in the Portal app.
    * The website is designed using standard UX principles, such as providing links to the other pages in the header.
        * All navigation links have names that are quite clear as to what content they links to.
* To be able to register and sign in easily.
    * All pages feature the profile icon which triggers a dropdown with links to the registration and sign in pages.
    * A profile icon that either links directly to or provides links to account features is a common feature throughout web design and will be recognised by users as such.
* To be able to sign out easily.
    * Again, as the profile dropdown is present on every page, the user can quickly and easily sign out.
* To be able to navigate through the website intuitively and easily.
    * Navigation links are easily accessible on all pages of the website. As the website features common UX principles, navigating through the pages is intuitive.
    * All relevant pages feature 'back to' links so the user doesn't have to rely on the main navigation links to navigate the site.
* To find content relating to the band Radiohead.
    * As this website features only content relating the band Radiohead, this user story is met!

#### As a returning user, I want:
* To be able to log in and out easily and to be able to remain signed in.
    * As with the **first time user** user story, this requirement is met via the profile icon in the navigation bar.
    * On the sign in page, the option to 'remember me' is presented enabling the user to return to the website and be automatically logged in.
* To be able to reset my password should I forget it.
    * The sign in page offers a link that states 'forgot password?' which links to a page that allows users to input their email address and be sent a reset password link. 
* To be able to find details about my previous orders.
    * The profile page features a, 'Orders' section containing a list of previous orders.
        * By clicking on a previous order, users can view th details of that order, including items orderered, costs and delivery information.
* To be able to view details about my subscription.
    * The profile page features a 'Subscriptions' section.
        * The subsciptions section shows users when their subsciption payment is due, as well as which card will be charged.
        * If the user cancels their subscription, text is rendered tell the user when the subscription will end.
* To be able to easily cancel my subscription.
    * The profile page offers an obvious button to 'Cancel Subscription', which stops the user being charged when their susbcription renewal date is reached. Users can still access the Portal content until this date however.
* To be able to easily reactivate my subscription after cancelling.
    * If the user wishes to reactivate their subsciption before the current billing period has ended, a button to 'Reactivate Subscription' is presented.
* To be able to change my subscription payment card.
    * The profile page offers an obvious link to 'Change Payment Card'
* To be able to save my details to use for any future purchases.
    * Any page that includes a form to collect users data features a checkbox which enables the user to save their information for next time.
    * The profile page features a form for users to add or update their default details.
* To be able to find new merchandise quickly in the shop.
    * Items in the shop are by default listed with newest items at the top of the page.
* To be able to find new music quickly in the Media section.
    * Albums on the media page are by default listed with the newest albums at the top of the page.
* To be able to view new content quickly in the Portal area.
    * Posts on the Portal page are by default listed with the newest posts at the top of the page.

#### Shared user requirements:
* To be able to communicate with other fans of the band.
    * Users can comment on pages in both the Media and Portal apps.
* To be able to buy music and merchandise from the band.
    * Users can make purchases though the shop app.
* To be able to find details about upcoming concerts.
    * Users can view upcoming concerts though the Live app.
* To be able to find and consume music.
    * Users can find and consume music though the Media app.
* To be able to find recent news, updates and other content.
    * Users can get updates though the Portal app.

### Technical Testing
#### Validation
##### HTML
The HTML code has been validated with the [W3C Markup Validator](https://validator.w3.org/). This was done by copying the HTML code from Chrome Dev Tools once rendered in the browser, for all pages whilst both logged in and logged out of the website, and pasting the code into the validator. This was necessary to test the code in its final state after being processed by the django templates. The HTML code contains no validity issues.

##### CSS and Javascript
The CSS code has been validated with the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) and the JavaScript with the [JS Hint](https://jshint.com/) code analysis tool, with any issues highlighted by the validators fixed. The code contains no validity issues.

##### Python
All Python code was written to be PEP 8 compliant. **ADD ANY FINAL WARNINGS HERE**

#### Responsive testing
The website has been developed and tested to ensure a high level of responsiveness. This has been achieved using Google Chrome Dev Tools, testing on different physical devices as listed below and by viewing the site on [Am I Responsive?](http://ami.responsivedesign.is/).
##### Responsive testing procedure
Check that text, images and all other elements load with correct styles and spacing on all pages. On mobile and tablet, rotate the screen to landscape orientation and repeat the checks. Whilst testing on a laptop, using each browsers developer tools, resize the page and ensure all elements respond to the screen size accordingly.

The tests detailed in this section were all completed using the following web browsers and hardware:
|                            | Chrome             | Edge             | Firefox            | Safari |
| -------------             |:------------------:| -----------------:|-------------------:|--------:|
| Microsoft Surface 3 (15") | :heavy_check_mark: |:heavy_check_mark: | :heavy_check_mark: |         |
| Samsung Galaxy A6         | :heavy_check_mark: |:heavy_check_mark: | :heavy_check_mark: |         |
| Huawei P Smart 2019       | :heavy_check_mark: | :heavy_check_mark:| :heavy_check_mark: |         |
| Macbook Pro 2016 (13")    | :heavy_check_mark: |                   | :heavy_check_mark: | :heavy_check_mark: |
| iPad 7th generation 2019  | :heavy_check_mark: |                   | :heavy_check_mark: |:heavy_check_mark: |

#### Automated Testing
The website has been thoroughly tested using the in-build django testing functionality. These tests can ensure the following:
    * Views return correct templates, status codes, and any additional data expected to be returned, as well as ensuring that they interact with the database correctly. Tests were also written to ensure certain user credentials are required to access restricted areas of the website.
    * Forms return the correct string method values, any required fields are rendered as such and the ensuring the order of the fields when rendered on the front-end are correct.
    * Models accept the correct data types and that any functions attached to the model's class behave accordingly.

The package 'Coverage' was used to assess how much of the code is being tested by the automated tests. The coverage report states that **??INSERT FINAL % HERE???** has been covered by the tests.

Any calls to the Stripe API were not included in the unit testing. These areas of the code have been tested manually as detailed in the **Manual Testing** section below.


<a name="deployment"></a>

## Deployment
### Version Control with Github
Github has been used to host the website's remote repository. To create and connect to the repository I completed the following steps:

#### Create a Github repository and Gitpod workspace
1. Log in to the **GitHub** website and click on 'New' from the 'Repositories' section in the top left of the screen.

2. Once on the 'Create a new repository' page, I selected the Code Institute template from the 'Repository template' dropdown menu, gave the repository a name and description and clicked 'Create Repository.

3. Once the repository was created, I click on the 'Gitpod' button towards the top right of the screen. This opened a new Gitpod workspace and automatically connected the workspace to the repository. 

#### Forking the Repository
If you wish to work on this project within your own repository, it can be forked using the following process:

1. Log in to your **GitHub account** on the **GitHub** website.

2. Using the search bar in the top left of the screen, search for **'richardthorp/radiohead'**.

3. Click on the search result and then click on the **'Fork'** button to the right of the screen, above the list of files and folders.

4. The repository is now 'forked' and saved in your own repository.

#### Cloning the Repository
If you wish to clone the repository to work on locally, follow these steps:

1. Log in to **GitHub** and navigate to the repository (follow step 2 from 'Forking the Repository').

2. Click on the green **'Code'** button to the top right of the list of files and folders.

3.  Copy the URL displayed underneath the **underlined 'HTTPS'**.

4. In your local IDE, launch **Git Bash** and create or navigate to the folder in which you wish to make the clone.

5. On the CLI type **'git clone'** followed by the URL copied from step 3 and press enter. You will now have a local clone of the repository.

### Deploying to Heroku

##### Gunicorn
Gunicorn is used as the server when the app is deployed to Heroku. To install Gunicorn run `pip3 install Gunicorn` and then add the package to the apps `requirements.txt` file using `pip3 freeze > requirements.txt`

##### Procfile
Heroku needs a 'Procfile' to know how to run the app. In this instance, a Profile was created in the root directory of the project with the code `web: gunicorn radiohead.wsgi:application` saved to it.

#### Create a Heroku app
Heroku provide a Postgres database to integrate with the app. To set up the database, I followed these steps:

1. Sign in/sign up to [Heroku](https://www.heroku.com/).

2. Once signed in, click on the 'Create New App' button.

!['Create new app' button](readme-images/deployment-images/create-new-app.jpg)

3. Name the app, select the local region and click 'Create App'.

4. In the top menu, select the 'Deploy' tab, and then click 'Connect to GitHub' in the 'Deployment method' section.

!['Deploy' tab and 'Connect to GitHub' button](readme-images/deployment-images/connect-to-github.jpg)

5. Connect your GitHub account to your Heroku account by clicking on the 'Connect to GitHub' button (if already connected, move to step 6).

6. Search for the GitHub repository which contains the app you wish to deploy, and then click 'connect'.

![Repository search bar and 'Connect' button](readme-images/deployment-images/search-for-repo.jpg)

7. Once connected, you can choose to automatically deploy any updates made in the GitHub repository or to do so manually by selecting the branch you wish to deploy and clicking on the appropriate button.

![Choose branch dropdowns and automatic and manual deploy buttons](readme-images/deployment-images/auto-deploy.jpg)

8. Following this, click on the 'Settings' tab and then click 'Reveal Config Vars'

!['Settings' tab and 'Reveal Config Vars' button](readme-images/deployment-images/settings-tab.jpg)

9. Within the 'Reveal Config Vars' section, add the variables which would be found in your local enviroment variables. These variables are saved here as they contain sensitive data such as the passwords and secret keys.

![Config vars form](readme-images/deployment-images/config-vars.jpg)

10. Add the new app url and `localhost` to the project's `settings.py` file in the 'ALLOWED_HOSTS' section:
    * `ALLOWED_HOSTS = ['app-name.herokuapp.com', 'localhost']`

#### Set up Heroku Postgres
Heroku provide a Postgres database to be used in the project. To set up the database I followed thse steps:

1. On Heroku, within the app dashboard, click on the resources tab at the top of the page.

2. In the 'Add-ons' search bar, type in 'Heroku Postrgres' and click on the resulting option.

3. Ensure 'Hobby Dev' is selected as the plan name and click on 'Submit Order Form'. This will automatically attach the database to the app and add the database URL to the app's 'Config Vars' in the settings page. 

5. Install the packages required to integrate the app and database using pip:
    * `pip3 install dj_database_url`
    * `pip3 install psycopg2_binary`

6. Add the packages to a `requirements.txt` file in the root directory to ensure Heroku knows which dependencies are required to run the app:
    * `pip3 freeze > requirements.txt`

7. To ensure that Django's default SQLite database was used in development and the Heroku Postres database used in production, the following `if/else` statement was added to the projects `settings.py` file having imported `dj_database_url` at the top the file:

```
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

#### Push the code to Github and Deploy to Heroku
With the previous steps complete, in the project terminal run `python3 manage.py makemigrations` and then `python3 manage.py migrate` to ensure any outstanding migrations have been completed on the local database and migration files are up to date and ready to use in the deployed app.

1. Commit all changes and push to Github:
    * `git add .`
    * `git commit -m "Commit files to deploy to Heroku"`
    * `git push`
2. In the Heroku app dashobard on heroku.com, navigate to the 'Settings' tab and within the 'Config Vars' section, add a new variable set to:
    `DISABLE_COLLECTSTATIC: 1`
This is to temporarily stop Heroku collecting the app's static files as these will later be hosted using Amazon's S3 service.
3. In the 'Deploy' tab of the Heroku dashboard, click on 'Deploy Branch' with 'master' selected (this is only neccessary if automatic deploys are not enabled).
4. Once the appication has been built, click on the 'more' button at the top right of the page and click on 'Run Console'. With the console running, type the command `python3 manage.py migrate` to apply migrations to the Heroku Postrgres database.
5. Following the migrate command, create a new superuser for the deploted app using `python3 manage.py createsuperuser`.
6. The app is now deployed to Heroku.

### Host and serve static files using Amazon's S3
#### Create an S3 bucket and set up bucket permissions
1. Navigate to `aws.amazon.com` and click on 'Create a new user', fill in the 'Create a new user' form and submit the form.
2. On the following page, select the 'Personal - for your own projects' option and fill out the rest of the form and submit.
3. Next, add payment details for the account and continue with the sign up process.
4. Once signed up and signed in, search for 'S3' in the search bar at the top of the page and click on the 'S3' option.
5. On the next page, click 'Create Bucket' and then name the bucket and select the appropriate region. Under 'Block Public Access settings for this bucket', untick the 'Block all public access' option and click 'Create bucket' at the bottom of the page.
6. In the following 'buckets' page, click on the newly created bucket and in the 'properties' tab, navigate to the bottom of the page and click on 'Edit' under 'Static website hosting', setting the option to enable. Add some values to the 'Index Document' and 'Error Document' and saving the changes.
7. Click on the 'Permissions' tab and scroll down to 'Cross-origin resource sharing (CORS)', click edit. Paste the following into the textfield and click 'Save changes'

```
[
    {
        "AllowedHeaders": [
            "Authorization"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```
8. Still in the 'Permissions' tab, navigate to the 'Bucket policy' section and click on 'Edit'. Copy the 'Bucket ARN' from this page before clicking on the 'Policy generator' button.
9. In the policy generator, make the following changes:
    * Step 1: Select Policy Type
        * 'Select Type of Policy' : 'S3 Bucket Policy'
    * Step 2: Add Statement(s)
        * 'Principal': '*'
        * 'Actions': 'GetObject'
        * 'Amazon Resource Name (ARN)': Paste the ARN copied in step 8.
    * Click on 'Add Statement' and then 'Generate Policy'.
        * Copy the policy and paste it into the 'Edit Bucket Policy' back on the main S3 bucket page.
        * Before saving, add '/*' to the 'Resource' tab to allow access to all resources.
10. Within the 'Permissions' tab of the bucket, find the 'Access control list (ACL)' section and click on 'Edit'.
    * Next to 'Everyone (public access)', click on the 'list' checkbox before saving the changes.

#### Create a user to access the bucket
1. Navigate to the AWS Services menu and search for 'AIM', selecting the resulting IAM option.
2. Click on 'User Groups' in the menu on the left side of the page and then click 'Create group'.
3. Name the new group, giving it a name which clearly relates to the S3 bucket created in the last section and then click 'Create group'.
4. Click on 'Policies' in the menu on the left side of the page and then click 'Create policy'.
5. Click on the 'JSON' tab and then click 'Import managed policy'. Search for 'S3' in the searchbar and then click on the 'AmazonS3FullAccess' policy. Click 'Import' at the bottom of the page.
6. Find and copy the bucket ARN in the 'properties' section of the S3 buckets page.
7. Back in the 'JSON' tab on the 'Create policy' page, add the following the resource section:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource":  [
                "arn:aws:s3:::<your bucket name>",
                "arn:aws:s3:::<your bucket name>/*"
            ]
        }
    ]
}
```
This allows access to both the bucket, and any files and folders within the bucket.

8. Click on the 'Tags' button at the bottom of the page and then the 'Next: Review' button before giving the policy a suitable name and description and clicking 'Create policy'.
9. Return to the 'User groups' by clicking the link in the menu of the left side of the page. Click on the 'Permissions' tab and then 'Add permissions'. In the 'Add permissions' dropdown, click 'Attach Policies' and select the policy created in the previous step before clicking 'Add permisions' at the bottom of the page.
10. On the 'Users' page found through the left side menu, click 'Add Users'. Give the user a name which clearly relates to the bucket and click on 'Programmatic access' under the 'Access type' section before clicking 'Next: Permissions' at the bottom of the page.
11. Select the group created in step 3, click 'Next' and click 'Next' again on the 'Add tags (optional)' page, before clicking 'Create User'.
12. Click 'Download .csv' and ensure the downloaded file is saved as this file contains the access credentials required to use the S3 bucket. 

#### Configure Django to use S3 
<a name="credits"></a>

## Credits

### Code

### Content

### Acknowledgements
