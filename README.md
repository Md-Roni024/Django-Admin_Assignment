## Table of Contents
1. [Overview ](#Overview )
1. [Features](#features)
2. [Tools & Technologies](#technologies)
3. [Project Structure](#project-structure) 
5. [Run & Setup](#Running-the-project)
6. [Schema Design](#Design-Database-Schema)
7. [Contributing](#Contributing)
8. [Contact](#Contact)
10. [License](#license)


## Overview

This assignment is based on previous Scrapy assignment, where I grab hotels information like: title,price,rating,longitude,latitude ,room type & image from trip.com website. Beside the grabing image url we also download image in physical storage. In this django admin dashboard assignmnet we build a Command Line Interface(CLI) application that move all hotel inforamtion from 'Scrapy_databasse' to 'dajngo_database' then we implements CRUD(Create,Read,Update & Delete) operations on this hotels data. 




## Features

- Scrape hotels data from Trip.com url
- Store hotel image locally
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
│
├── hotel_scrapper/
│   ├── scrapy.cfg
│   ├── hotel_scrapper/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   ├── spiders/
│   │   │   └── __init__.py
│   │   │   └── hotel_spider.py
│
├── manage.py
├── .gitignore
├── start_cli.py
└── requirements.txt

```

## Running-the-project

1. Clone the repository:
   ```bash
   git clone https://github.com/Md-Roni024/Django-Assignment

   ```

2. Go to the project directory and Create Virtual Environment & activate
    ```bash
    cd django_assignment
    python3 -m venv venv
    source venv/bin/activate
    ```


3. Install all the dependencies :
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file then add variables credentials as like:
    ```bash
    DB_USER=postgres
    HOST=localhost
    PASSWORD=p@stgress
    PORT=5433
    SCRAPY_DATABASE=scrapy_database
    SCRAPY_DATABASE=django_database
    ```
5. Go to scrapy folder & Run Spider
    ```bash
    cd hotel_scrapper
    scrapy crawl hotel_spider

    ```
7. Now Migrate the django datbase table

    ```bash
    cd ..
    python manage.py makemigrations
    python manage.py migrate

    ```
8. Run CLI Application to migrate data to django project database
    ```bash
      python start_cli.py

    ```
9. Run dajango admin

   ```bash
   python manage.py runserver
   ```
   Go to this url: http://127.0.0.1:8000/admin/

10. Create super admin by terminal

   ```bash
    python manage.py createsuperuser
    Username: 'Put Your Username'
    Username: 'Put your password, minimum 8 alphanumeric character'
   ```
   Then login tho the dashboard


## Demo Data that are scrap by spider:

  ```json
    {
      "title": "Cititel Mid Valley",
      "rating": "4.3",
      "location": "Lingkaran Syed Putra, Mid Valley City, 59200 Kuala Lumpur, Wilayah Persekutuan",
      "latitude": 3.117932,
      "longitude": 101.678354,
      "room_type": "Superior Twin Room",
      "price": 57,
      "image_url": "https://ak-d.tripcdn.com/images/hotel/136000/135821/67BA76B8-5DBA-4025-A417-701341BC8C3A_R_250_250_R5_D.jpg",
      "image_path": "propert_images/67BA76B8-5DBA-4025-A417-701341BC8C3A_R_250_250_R5_D.jpg"
    }
  ```

  

### Design-Database-Schema
- Database for Scrapy
    - Database name: scrapy_database
    - Create Table as 
        ```SQL
        CREATE TABLE hotels_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            rating FLOAT,
            location VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            room_type VARCHAR(255),
            price FLOAT,
            image_url TEXT,
            image_path TEXT
        );
        ```
- Database for Django Assignment

- Name: django_database

- Table-1: myapp_property
  ```sql
    CREATE TABLE myapp_property (
        property_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        create_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
  ```
  - Table-2: myapp_location
  ```sql
    CREATE TABLE myapp_location (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        latitude DECIMAL(9, 6) NOT NULL,
        longitude DECIMAL(9, 6) NOT NULL,
        create_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
  ```
  - Table-3: myapp_amenity
  ```sql
    CREATE TABLE myapp_amenity (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        create_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
  ```
  - Table: myapp_property_locations
  ```sql
    CREATE TABLE property_locations (
        property_id INTEGER NOT NULL,
        location_id INTEGER NOT NULL,
        PRIMARY KEY (property_id, location_id),
        FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE,
        FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE CASCADE
    );
  ```

    - Table: myapp_property_amenities
  ```sql
    CREATE TABLE myapp_property_amenities (
        property_id INTEGER NOT NULL,
        amenity_id INTEGER NOT NULL,
        PRIMARY KEY (property_id, amenity_id),
        FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE,
        FOREIGN KEY (amenity_id) REFERENCES amenity(id) ON DELETE CASCADE
    );
  ```

    - Table: myapp_image
  ```sql
    CREATE TABLE myapp_image (
        id BIGSERIAL PRIMARY KEY,
        property_id INTEGER,
        image VARCHAR(255),
        create_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE SET NULL
    );
  ```

## Contributing
- Contributing is an open invitation for collaboration on the project. You're encouraged to participate by opening issues for bugs or feature requests and submitting pull requests with your improvements or fixes. Your contributions help enhance and grow the project, making it better for everyone.

## Contact

- For any questions or feedback, please reach out to me at roni.cse024@gmail.com. I welcome all inquiries and look forward to hearing from you. Your input is valuable and appreciated!

## Licences
- Distributed under the MIT License. See LICENSE.txt for more information.
