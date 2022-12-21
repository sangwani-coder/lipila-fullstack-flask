# SKOOLPAY
Online Fee collection system for Zambian Schools.
### Description 
This web application supports payments of various fees to lerning institutions. The student/parent makes payments to the school using either MTN or airtel mobile money. The web app can be used by:
- Universities
- Colleges
- Primary Schools
- Secondary Schools
- Tuition centers

### benefits
- fast and secure payments
- no need to be tracking paper receipts
- cheaper
- saves time, no more bank queues
- complete payments in 5 seconds

## Admin Features
The application supports the following features for admin user:
- Login into the application
- Registering a new school
- Adding a new student
- Checking history of all payments

## Student Features
The application supports the following features for student/parent users:
- Check all payments history
- Make a payment

## Technologies
- Python3
- Flask
- HTML / CSS
- Database: Sqlite3 in development and Postgresql in production
- pytest

## Project Layout
|file / directory | description |
|-------------------------|----------------|
|[skoolpay/](/.skoolpay)|package containing project files|
|[skoolpay/momo](/.skoolpay/momo)|package with modules for quering third party mobile money API's|
|[skoolpay/momo/airtel_momo.py](/.skoolpay/momo/airtel_momo.py)|module that queries the Airtel momo API.|
|[skoolpay/momo/mtn_momo.py](/.skoolpay/momo/mtn_momo.py)|module that queries the MTN momo API.|
|[skoolpay/momo/momo](/.skoolpay/momo/momo)|module with Momo base class definition|
|[skoolpay/static](/.skoolpay/static)|directory with css static files|
|[skoolpay/templates](/.skoolpay/templates)|directory with html template files|
|[skoolpay/views](/.skoolpay/views)|package with application views|
|[skoolpay/views/admin](/.skoolpay/views/admin)|module with views that handle admin functions eg. adding new users|
|[skoolpay/views/auth](/.skoolpay/views/auth)|module with views that handle authentication|
|[skoolpay/views/skoolpay](/.skoolpay/views/skoolpay)|module with views to handle student payments|
|[skoolpay/__init__.py](/.skoolpay/__init__.py)| project factory, the entry point to the project|
|[skoolpay/db.py](/.skoolpay/db.py)| contains functions to initialize the database and creating database connections|
|[skoolpay/schema.sql](/.skoolpay/schema.sql)| file defining the database tables|
|[skoolpay/tests](/.skoolpay/tests)| package containing unittests|

## Running The Application Locally
Clone this repo and cd into `SKOOLPAY` the top-level directory.

### Initializing the Database
You initialize the database by calling the init-db method that has been registered with the app, it can be called using the flask command.

Run the init-db command:

**$ flask --app skoolpay init-db**
Initialized the database.

There will now be a skoolpay.sqlite file in the instance folder in your project.

## Starting the web server
Now you can run your application using the flask command. From the terminal, tell Flask where to find your application, then run it in debug mode. Remember, you should still be in the top-level directory, not the skoolpay package.

Debug mode shows an interactive debugger whenever a page raises an exception, and restarts the server whenever you make changes to the code.

**$ flask --app skoolpay --debug run**

### contributors
Sangwani Peter Zyambo zyambo@icloud.com
