## Samantha Lambert - samantha.carol.lambert@gmail.com - Coding Challenge - 8/2/2018

Used - Python 2.7.10

## Files Included:
	* requirements.txt
	* main.py
	* models.py
	* data -> empty folder for uploads
	* static -> style.css
	* templates -> home.html, layout.html, viewData.html

## Ran by using Command line prompts:

	python -m virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt
	export FLASK_APP=main.py
	flask initdb
	flask run


## Basic User Walkthrough:

* Home page initally displays a button for selecting and uploading a file. 
	* Files with the same name are not accepted as well as files that do not have the extension ".tsv" 
	* Messages should be displayed to notify the user of these errors

* After a file has been uploaded, the filename and the calculated total revenue will be displyed to the user on the hompage 
	* If you click on the "View Data" button beneath each filename section you will be taken to a page that displays all of the data items in a table
	* On the "View Data" page you can see the total revenue and the row count at the top of the page. 
	* This page also has a button to take you back to the home page

* On the homepage you can continue to upload files and view the data sets they contain, they will appear in order of highest total revenue to lowest total revenue








