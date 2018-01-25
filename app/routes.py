from app import app
from app import db
from flask import render_template
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from app.models import Request, Client, Product
from app.schema import request_schema, requests_schema, client_schema, product_schema
from dateutil import parser

@app.errorhandler(404)
def not_found(exception):
	"""
	Custom Response for 404 error
	"""
	app.logger.error(exception)
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(exception):
	"""
	Custom Response for 500 error
	"""
	app.logger.error(exception)
	db.session.rollback()
	return make_response(jsonify({'error': 'Internal Server Error'}), 500)
	
@app.route('/requests', methods=['GET'])
def get_requests():
	"""
	Method to return list of requests
	Serializing the db data using our schema before sending
	"""
	requests = Request.query.all();
	result = requests_schema.dump(requests)
	return jsonify(result.data)
	

@app.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
	"""
	Method to return specific of request detail
	Serializing the db data using our schema before sending
	
	@request_id: request id is received in URL for which the detail has to be sent
	"""
	request = Request.query.get(request_id);
	result = request_schema.dump(request)
	return jsonify(result.data)
	

@app.route('/addrequest', methods=['POST'])
def create_request():
	"""
	Method to create a new request object and save in database
	
	Data received in request object:
	@title: request title
	@desc: request description 
	@target_date: target date to complete that request
	@priority: request priority
	@client_id: client associated to this request
	@product_id: product associated to this request
	
	Everything will be roll-backed it there is any issue at any level
	"""
	if not request.get_json() or not 'title' in request.get_json():
		abort(400)
	try:
		client_id = request.json['client_id']
		product_id = request.json['product_id']
		feature_title = request.json['title'].strip()
		feature_desc = request.json['desc'].strip()
		target_date = request.json['target_date']
		priority = request.json['priority']
		
		"""
		Reorder the priority of other features for the same client
		"""
		older_priorities = Request.query.filter(Client.client_id == 1).filter(Request.priority >= 1)
		for row in older_priorities:
			row.priority = row.priority + 1 
		
		""" Return 404 if Client or Product data not found in database"""
		client = Client.query.get(client_id)
		if client is None:
			app.logger.error("Client Data not found for client id ", client_id)
			return make_response(jsonify({'error': 'Client Not found'}), 404)
		
		product = Product.query.get(product_id)
		if product is None:
			app.logger.error("Product Data not found for product id ", product_id)
			return make_response(jsonify({'error': 'Product Not found'}), 404)
			
		""" 
		Save request data into database 
		"""
		request_data = Request(title=feature_title, 
							desc=feature_desc, 
							target_date = parser.parse(target_date).date(), 
							priority=priority, 
							client=client, 
							product=product)
		
		db.session.add(request_data)
		db.session.commit()
		result = request_schema.dump(request_data)
		return jsonify(result.data)
	except Exception as e:
		app.logger.error(repr(e))
		db.session.rollback()
		return make_response(jsonify({'error': 'Error while saving request data into database'}), 400)
		
@app.route('/clients', methods=['GET'])
def get_client():
	"""
	Method to return list of clients from db
	Serializing the db data using our schema before sending
	"""
	clients = Client.query.all();
	result = client_schema.dump(clients)
	return jsonify(result.data)
	
@app.route('/products', methods=['GET'])
def get_products():
	"""
	Method to return list of products from db
	Serializing the db data using our schema before sending
	"""
	products = Product.query.all();
	result = product_schema.dump(products)
	return jsonify(result.data)

@app.route('/', methods=['GET'])
def index():
	user = {'username': 'miguel'}
	return render_template('feature-list.html', title='Home', user=user)