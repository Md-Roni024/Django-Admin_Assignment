## Table of Contents
1. [Overview ](#Overview )
1. [Features](#features)
2. [Tools & Technologies](#technologies)
3. [Project Structure](#project-structure) 
5. [Run & Setup](#Running-the-project)
6. [Schema Design](#Design-Database)
7. [Contributing](#Contributing)
8. [Contact](#Contact)
10. [License](#license)


## Overview

This assignment is based on previous Scrapy assignment, where I grab hotels information like: title,price,rating,longitude,latitude ,room type & image from trip.com website. Beside the grabing image url we also download image in physical storage. In this django admin dashboard assignmnet we build a Command Line Interface(CLI) application that move all hotel inforamtion from 'Scrapy_databasse' to 'dajngo_database' then we implements CRUD(Create,Read,Update & Delete) operations on this hotels data. 




## Features

- Store Scrap data in Postgresql database.
- Move hotels data from 'scrapy_database' to 'django_database' by CLI application.
- Maintain proper data table realtionship with different property like:(One to Many , Many to Many)
- Apply CRUD operations

## Technologies
- Django
- Scrapy
- Python
- SQLAlchemy
- PostgreSQL
- Command Line Interface

 

## Project Structure

Here I add my scrapy spider in django project, so that I can grab hote data in django project.

```
django_assignment/
│
├── django_assignment/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── myapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── templates
│   │   └── __hello.html
│   ├── migrations/
│   │   └── __init__.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
├── manage.py
├── .gitignore
├── start_cli.py
└── requirements.txt

```


### Design-Database
- Create databasse for Django Project
  ```
  CREATE DATABASE scrapy_database;
  ```


## Running-the-project

1. Clone the repository:
   ```bash
   git clone https://github.com/Md-Roni024/Django-Admin_Assignment

   ```

2. Go to the project directory and Create Virtual Environment & activate
    ```bash
    cd Django-Admin_Assignment
    python3 -m venv venv
    #For Linux or MacOS
    source venv/bin/activate

    #For Windows
    venv\Scripts\activate
    ```


3. Install all the dependencies :
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file then add variables credentials as like:
    ```bash
      HOST=localhost
      PORT=5433
      DB_USER=postgres
      PASSWORD=p@stgress
      SCRAPY_DATABASE=hotel_db
      DJANGO_DATABASE=django_database
    ```


5. Now Migrate the django datbase table

    ```bash
    cd django_assignment

    python manage.py makemigrations
    python manage.py migrate
    ```
8. Run CLI Application to migrate data to django project database
    ```bash
      python start_cli.py
    ```

9. Create super admin by terminal

   ```bash
    python manage.py createsuperuser
    Username: 'Put Your Username'
    Username: 'Put your password, minimum 8 alphanumeric character'
   ```
10. Run dajango admin
    ```bash
    python manage.py runserver
    ```

   Go to this url: http://127.0.0.1:8000/admin/

  

## Contributing
- Contributing is an open invitation for collaboration on the project. You're encouraged to participate by opening issues for bugs or feature requests and submitting pull requests with your improvements or fixes. Your contributions help enhance and grow the project, making it better for everyone.

## Contact

- For any questions or feedback, please reach out to me at roni.cse024@gmail.com. I welcome all inquiries and look forward to hearing from you. Your input is valuable and appreciated!

## Licences
- Distributed under the MIT License. See LICENSE.txt for more information.
