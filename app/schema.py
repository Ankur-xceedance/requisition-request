from app.models import Client, Product, Request
from app import ma
from marshmallow import fields

class ClientSchema(ma.ModelSchema):
	"""
	Schema to serialize client data before sending the response
	"""
	class Meta:
		model = Client

class ProductSchema(ma.ModelSchema):
	"""
	Schema to serialize product data before sending the response
	"""
	class Meta:
		model = Product

class RequestSchema(ma.ModelSchema):
	"""
	Schema to serialize request data before sending the response
	"""
	client_name = fields.Method("get_client_name")
	product_area = fields.Method("get_client_name")
	
	def get_client_name(self, obj):
		"""
		This method will return client name from the object
		"""
		return obj.client.name
	
	def get_product_area(self, obj):
		"""
		This method will return product area from the object
		"""
		return obj.product.product
		
	class Meta:
		model = Request

""" Following are the schema objects"""
client_schema = ClientSchema(many=True)
product_schema = ProductSchema(many=True)
request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)