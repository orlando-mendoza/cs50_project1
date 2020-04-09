# CS50 Project 1 - Web Programming with Python and JavaScript

## Project Description

This project consists of a web application using Python with Flask and SQLAlchemy that shows a preloaded list of books, which you can search by ISBN, Title or Author.

The Index Page is the initial page, showing the list of books. ISBN has a link to the book details.

The Book details page shows the reviews submited by users for that specific book. Users may submit reviews only if they are logged in, and they can't submit multiple reviews for the same book.

The details for each book include:
- ISBN number
- Title
- Author
- The Book's cover page: taken from Google Books API
- Publication Year
- Average Rating and Ratings Count from GoodReads.com API

## What is contained in each file

### import.py

Creates a connection to the DATABASE_URL and inserts all the books contained in books.csv

### application.py

The main application file. Sets the environment variables, starts the session, connect to the database and import routes.

### routes.py

Contains the routes for the app to work.

- `/` - GET method fetchs all the books / POST method fetchs only the books contained in search_text variable by search_option (ISBN, Title or Author).
- `/isbn/<string:isbn>` - Loads the book details page, with details about the book: its title, author, publication year, ISBN number, the book's cover page if found in Google Books API;  Loads a form to submit a review and any reviews users have left for the book.
- `api/<string:isbn>` - Fetch the book details and returns them in a JSON format. Returns Not Found (404) when the isbn is not found in the database.
- `/register` - Loads a flask form where the user is able to register providing at least username and password.
- `/login` - Registered users login page (Flask Form).
- `/logout` - Logged in users are able to log out of the site.

### settings.py
Loads the SECRET_KEY and API_KEY.

### goodreads.py
Contains two functions:
- `get_good_reads_reviews(isbn)`: Which expects a isbn number as parameter and calls the goodreads api. returns a JSON with the book details from GoodReads.
- `get_book_cover(isbn)`: receives a isbn number as parameter and returns a link to the book's cover thumbnail.

### forms.py
Using WTForms sets the forms for Login, Register and Review.

### requirements.txt
Contains the requirements to run the app.

### Templates folder
- layout.html - Contains the main layout html file. With a nav bar and a footer
- index.html - extends `layout.html` and contains a form to search for books, authors or titles. Shows all the books or the list of books depending on the search option.
- isbn.html - The book details page
- login.html
- register.html

#### templates/includes folder
- footer.html - Disclaimer
- nav-logout.html - Navigation bar when users are not logged in;
- nav.html - Nav bar for logged in users.

#### static/css folder
- main.css - Main Stylesheet file.


## Usage

### Set the environment variables

Create a `.env` file in your app root folder with the following:

**.env file**

1. `API_KEY` with your Good Reads API Key
2. `DATABASE_URL` for the connection to the Database
3. `SECRET_KEY` for your Flask Session

Create a `.flaskenv` with the following

**.flaskenv**

`FLASK_APP=application.py`

**Import Books**
If you've already imported the books.csv just provide the DATABASE_URL in your .env file to run the app. If you have not imported the books then you can do it typing on your terminal from the root application folder:

On Windows
``` powershell
    C:\setx DATABASE_URL "your-database-url"
    C:\python3 import.py
```

On linux or Mac
``` bash
$ export DATABASE_URL='your_database_url'
$ python3 import.py
```

The application uses virtual environment. Tu run the application enter this commands on your terminal:

On Windows
``` shell
venv/bin/activate
flask run
```

On Linux or Mac
``` bash
$ source venv/bin/activate
$ flask run
```
