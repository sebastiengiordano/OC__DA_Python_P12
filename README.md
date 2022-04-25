<p align="center">
    <a href="https://user.oc-static.com/upload/2020/09/22/16007804386673_P10.png"><img src="https://user.oc-static.com/upload/2020/09/22/16007804386673_P10.png" alt="Logo"></a>
    <h1 align="center">Epic Events</h1>
    <h2 align="center">RESTful API for consulting and event management company.</h2>
    </br>
    <p align="left">
        This application allows users to do CRUD operations on the followings endpoints:
		<ul>
			<li>users, </li>
			<li>clients,</li>
			<li>contracts,</li>
			<li>events.</li>
		</ul>
		<br>
		A secure database is implemented with Django ORM and PostgreSQL.
		<br>
    </p>
</p>

<br>
<br>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [How run this program](#how-run-this-program)
  * [Prerequisite](#prerequisite)
  * [Installation](#installation)
  * [Run the program](#run-the-program)
  * [Additional informations](#additional-informations)

<br>
<br>

<!-- HOW RUN THIS PROGRAM -->
## How run this program

<br>

### Prerequisite
<br>
This API works with Python 3.9.
In order ot create your datbase, you'll also need to install PostgreSQL 14.2.
<br>

### Installation

1. Created a folder for this project. Then, open a terminal and go to this folder:
	```sh
	cd "folder project path"
	```

2. Clone the repository:
	```sh
	git clone https://github.com/sebastiengiordano/OC__DA_Python_P12
	```

3. Go to folder OC__DA_Python_P12:
	```sh
	cd OC__DA_Python_P12
	```

4. Create a virtual environment:
	```sh
	python -m venv env  # Windows
	python3 -m venv venv  # MacOs & Linux
	```

5. Activate the virtual environment:
	```sh
	.\env\Scripts\activate  # Windows
	./venv/bin/activate  # MacOs & Linux
	```

6. From the "requirements.txt" file, install dependencies:
	```sh
	python -m pip install -r requirements.txt
	```

7. Create and configure database :
	- Create the database

With PostgreSQL (14.2) installed on your machine, create a databe using [SQL shell (psql)](https://docs.postgresql.fr/14/app-psql.html) or [PGadmin tool](https://www.pgadmin.org/docs/pgadmin4/development/modifying_tables.html). Please refers to PostgreSQL documentation for more information, cf. previous link.

	- Setut the project:
In order to configure this project, a script has been made. To launch the script run the following commande:

	```sh
        setup.py
	```
	The script will asked for database name, username, password, host and port. It will also generate a 50 character random string to be usable as secret key.

	- Make database migrations with:
	```sh
	python manage.py makemigrations
	python manage.py migrate
	```

<br>
<br>

### Run the program
1. Open a terminal and go to the folder OC__DA_Python_P12 (if its not already the case):
	```sh
	cd "folder project path" & cd OC__DA_Python_P12
	```
2. Activate the virtual environment (if its not already the case):
	```sh
	.\env\Scripts\activate
	```
3. Run the server:
	```sh
	python manage.py runserver
	```
4. Use the following end-points:
	```sh
	https://documenter.getpostman.com/view/18383749/UVXbuzji
	```
or import the following export (you could find in the root of this API):
	```sh
	Issue Tracking System.postman_collection.json
	```

<br>
<br>

### Additional informations

For more details on this API, please refer to its [documentation](https://documenter.getpostman.com/view/18383749/UyrBkGae) (Postman), and the CRM entity-relationship diagram below.

<br>
<br>

### Entity relation diagram
<br>
![Entity relation diagram](/doc/Epic-Events_CurstomerRelationshipManagement.pngEpic-Events_CurstomerRelationshipManagement.png)
<br>
