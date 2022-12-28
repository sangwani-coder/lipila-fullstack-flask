# lipila
Lipila is an Online Fees Collection System suitable for educational institutes of all sizes. Lipila is a powerful combination of Fee Management Software + Online Payment Gateway by which you can collect fees from your students online & manage everything like a Pro!

### Description 
Lipila is software focused to provide solutions to schools, colleges, universities, coaching institutes, academies, etc.

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
- reportlab: creating pdf invoinces

## Project Layout
|file / directory | description |
|-------------------------|----------------|
|[lipila/](./lipila)|package containing project files|
|[lipila/momo](./lipila/momo)|package with modules for quering third party mobile money API's|
|[lipila/momo/airtel_momo.py](./lipila/momo/airtel_momo.py)|module that queries the Airtel momo API.|
|[lipila/momo/mtn_momo.py](./lipila/momo/mtn_momo.py)|module that queries the MTN momo API.|
|[lipila/momo/momo](./lipila/momo/momo)|module with Momo base class definition|
|[lipila/static](./lipila/static)|directory with css static files|
|[lipila/templates](./lipila/templates)|directory with html template files|
|[lipila/views](./lipila/views)|package with application views|
|[lipila/views/admin](./lipila/views/admin)|module with views that handle admin functions eg. adding new users|
|[lipila/views/auth](./lipila/views/auth)|module with views that handle authentication|
|[lipila/views/lipila](./lipila/views/lipila)|module with views to handle student payments|
|[lipila/__init__.py](./lipila/__init__.py)| project factory, the entry point to the project|
|[lipila/db.py](./lipila/db.py)| contains functions to initialize the database and creating database connections|
|[lipila/schema.sql](./lipila/schema.sql)| file defining the database tables|
|[lipila/tests](./lipila/tests)| package containing unittests|

## Running The Application Locally
Clone this repo and cd into `lipila` the top-level directory.

### Initializing the Database
You initialize the database by calling the init-db method that has been registered with the app, it can be called using the flask command.

Run the init-db command:

**$ flask --app lipila init-db**
Initialized the database.

There will now be a lipila.sqlite file in the instance folder in your project.

## Starting the web server
Now you can run your application using the flask command. From the terminal, tell Flask where to find your application, then run it in debug mode. Remember, you should still be in the top-level directory, not the lipila package.

Debug mode shows an interactive debugger whenever a page raises an exception, and restarts the server whenever you make changes to the code.

**$ flask --app lipila --debug run**

## MTN API
In order to use the MTN momo API you must signup for the service at [momodeveloper](https://momodeveloper.mtn.com)
After creating an account you should subscribe to the collections product.
Checkout my tutorial on how to use the mtn momo api on [medium]()

### contributors
Sangwani Peter Zyambo zyambo@icloud.com
