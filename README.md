# Lipila
Lipila is an Online Fees Collection System suitable for businesses to collect fees online. Lipila is a powerful combination of Fee Management Software + Online Payment Gateway.

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
|[lipila/schema-pro.sql](./lipila/schema-pro.sql)| file defining the database tables|
|[lipila/tests](./lipila/tests)| package containing unittests|

## Running The Application Locally
Download the code by cloning this respository

        git clone git@github.com:sangwani-coder/lipila.git

# Set environment variables

Navigate into the project directory and make a copy of the example environment variables file.

        cd lipila
        cp env.example .env

## MTN api key
In order to use the MTN momo API you must signup for the service at [momodeveloper](https://momodeveloper.mtn.com)
After creating an account you should subscribe to the collections product.

## Env Vars
* SUB_KEY= _copy your secret api key from mtn and paste it here_
* LIP_ENV=db

* PGUSER=lipila_dev
* PGPASSWORD=password
* PGDATABASE=lipiladb
* PGHOST=localhost

* MAIL_USERNAME=_your gmail account_
* MAIL_PASSWORD=_your password associated with your email account_

## Initializing the Database
* create a postgres database named lipiladb

You initialize the database by calling the init-db method that has been registered with the app, it can be called using the flask command.

The databasse tables will be created once you start the application.

Run the app
Run the following commands in the project directory to install the dependencies and run the app.
When running the commands, you may need to type python3/pip3 instead of python/pip depending on your setup.

        python -m venv venv

        . venv/bin/activate
        
        pip install -r requirements.txt

Make sure you are in the root directory containing thr run_server.py file, and run:

        python run_server.py

### contributors
Sangwani Peter Zyambo zyambopeter1@gmail.com
