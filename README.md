# Flask Stock Analysis

	export FLASK_APP=flaskr/
	flask run
	
Follows https://flask.palletsprojects.com/en/1.1.x/tutorial/

## Works locally using a SQLite database, but trying to switch to PostgreSQL to host on Heroku.
Runs on Heroku, but there is a issue with the database. Heroku does not support SQLite. Probably need PostgreSQL.

## Designing Webscraper based on PageObject Design Pattern
https://selenium-python.readthedocs.io/page-objects.html


# Refactory Branch
This branch is created to match the code from the Selenium PageObjects design pattern. I did not understand how the PageObject design pattern worked before.
This is an experiment on getting it to work.


# SEC Website Sending Post Request
application/x-www-form-urlencoded means parameters encoded in URL. 
application/x-www-form-urlencoded