#Samantha Lambert -  samantha.carol.lambert@gmail.com - Coding Challenge - 8/2/2018

import os, csv, locale
from flask import Flask, flash, request, redirect, url_for, render_template
from models import db, DataSet, DataInfo
from werkzeug.utils import secure_filename

app = Flask(__name__)

locale.setlocale( locale.LC_ALL, '' )
UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = set(['tsv'])
SECRET_KEY = 'development key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'challenge.db')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)

db.init_app(app)

#initilizes database -> freshly creates all tables (flask initdb)
@app.cli.command('initdb')
def initdb_command():
	db.drop_all()
	db.create_all()
	db.session.commit()
	print('Initialized the database.')

#checks for file types in the previously listed ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#adds the data to the DB from the uploaded file - also calculates and saves the total revenue 
def addData(filename):
	total = 0
	f = open('./data/' + filename, "r")
	if f.mode == 'r':
		reader = csv.DictReader(f, dialect='excel-tab')
		for row in reader:
			revenuePerItem = float(row['Item_price']) * float(row['Item_count'])
			total = total + revenuePerItem
			db.session.add(DataInfo(filename, row['Item'], row['Item_description'], row['Item_price'], row['Item_count'], row['Vendor'], row['Vendor_address']))
		db.session.add(DataSet(filename, total))
		db.session.commit()

#helper to get all the rows from the Data Set table - sorted in descending order based on total revenue
def getAllFileSets():
	fileList = DataSet.query.order_by(DataSet.totalRevenue.desc())
	return fileList

#helper to get all data for each set
def getEachDataSet(filename):
	rv = DataInfo.query.filter_by(dataSetName=filename)
	return rv if rv else None

#helper to get revenue for each set - formates it to readable currency 
def getRevenueforSet(filename):
	rv = DataSet.query.filter_by(filename=filename).first()
	return "{0:,.2f}".format(rv.totalRevenue) if rv else None

#helper to get the total count of rows in the uploaded file
def getCountforSet(filename):
	rv = DataInfo.query.filter_by(dataSetName=filename).count()
	return rv

#helper to check if the filename already exists in the DB
def inFilenameList(filename):
	rv = DataSet.query.filter_by(filename=filename).first()
	return rv if rv else None

@app.route("/")
def default():
	return redirect(url_for("upload"))

@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
    	#if view data button is pressed -> go to corresponding table
    	if 'viewData' in request.form:
    		return redirect(url_for('tables', filename=request.form['fileName']))
        #checks to make sure file is valid within given contstraints
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
        	flash('File type not supported')
        	return redirect(request.url)
        if inFilenameList(secure_filename(file.filename)):
        	flash('File has already been uploaded')
        	return redirect(request.url)
        #if file is good you can use it yay
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File successfully uploaded")
            addData(filename)
            return redirect(url_for("upload"))
    return render_template('home.html', fileList=getAllFileSets())


@app.route('/table/<filename>', methods=['GET', 'POST'])
def tables(filename):
	#if go to home page button is pressed -> go back to main page
	if request.method == 'POST':
		return redirect(url_for("upload"))
	return render_template("viewData.html", dataList=getEachDataSet(filename), dataCount=getCountforSet(filename), totalRev=getRevenueforSet(filename), filename=filename)



