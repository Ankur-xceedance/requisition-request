from app import db
from datetime import datetime
from app import ma
from sqlalchemy.orm import relationship
from marshmallow import fields

class Client(db.Model):
	"""
	Represents client table in DB
	"""
	client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), unique=True)

	def __repr__(self):
		return self.name
		
class Product(db.Model):
	"""
	Represents client table in DB
	"""
	product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	product = db.Column(db.String(100), unique=True)


class Request(db.Model):
	"""
	Represents request table in DB
	"""
	request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(100))
	desc = db.Column(db.String(1000))
	target_date = db.Column(db.Date, index=True)
	priority = db.Column(db.Integer)
	client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
	product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
	client = relationship("Client", foreign_keys="Request.client_id")
	product = relationship("Product", foreign_keys="Request.product_id")
		
	def __repr__(self):
		return 'Request ()>'.format(self.title)
	