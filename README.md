# SKOOLPAY
School Fee Collection System
## Requirements:
- Python3
- Flask

## Usage Linux:
**Set ENV Variables**
- $ cd SKOOLPAY
- $ export FLASK_ENV=development
- $ export FLASK_APP=app
- $ flask run

## Usage Windows:
- cd SKOOLPAY
- $ python app.py

## Language
- Python3
## Framework
- Flask
## Database
Sqlite in developmeent and MySQL in production

## Features
- Collect Fees
- Add/Remove students
- Update details/Admin
- Adds payments to DB automatically
- Print reports

## Run The Application
Now you can run your application using the flask command. From the terminal, tell Flask where to find your application, then run it in debug mode. Remember, you should still be in the top-level directory, not the SKOOLPAY package.

Debug mode shows an interactive debugger whenever a page raises an exception, and restarts the server whenever you make changes to the code. You can leave it running and just reload the browser page as you follow the tutorial.

$ flask --app SKOOLPAY --debug run

## Initialize the Database File
You initialize the database by calling the init-db method that has been registered with the app, it can be called using the flask command, similar to the run command from the previous page.

Run the init-db command:

$ flask --app flaskr init-db

Initialized the database.

There will now be a skoolpay.sqlite file in the instance folder in your project.

Auth: Zyambo <zyambo@icloud.com>
