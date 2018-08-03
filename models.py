from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DataSet(db.Model):
	dataID = db.Column(db.Integer)
	filename = db.Column(db.String(100), nullable=False, primary_key=True)
	totalRevenue = db.Column(db.Float, nullable=False)

	def __init__(self, filename, totalRevenue):
		self.filename = filename
		self.totalRevenue = totalRevenue


class DataInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dataSetName = db.Column(db.Integer, db.ForeignKey(DataSet.filename),nullable=False)
	item = db.Column(db.String(100))
	item_description = db.Column(db.String(150))
	item_price = db.Column(db.Float, nullable=False)
	item_count = db.Column(db.Integer, nullable=False)
	vendor = db.Column(db.String(80))
	vendor_address = db.Column(db.String(80))

	dataRel = db.relationship('DataSet', backref=db.backref('DataInfo', cascade="all,delete"), lazy='joined')

	def __init__(self, dataSetName, item, item_description, item_price, item_count, vendor, vendor_address):
		self.dataSetName = dataSetName
		self.item = item
		self.item_description = item_description
		self.item_price = item_price
		self.item_count = item_count
		self.vender = vendor
		self.vendor_address = vendor_address