import os
import unittest
from microblog import app, db
from app.models import Client, Product, Request
from datetime import datetime
import json

basedir = os.path.abspath(os.path.dirname(__file__)) 
TEST_DB = 'test.db'
 
class BasicTests(unittest.TestCase):
	"""
	Unit test class to test our APIs
	It will create a dummy database which will get deleted once all the tests are executed
	"""
    # executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()
		
		dummy_client = Client(name='Client 1')
		db.session.add(dummy_client)
		
		dummy_product = Product(product='Product 1')
		db.session.add(dummy_product)
		
		dummy_request = Request(title='test title', 
							desc='test desc', 
							target_date = datetime.now().date(), 
							priority=2, 
							client=dummy_client, 
							product=dummy_product)
		db.session.add(dummy_request)
		
		db.session.commit()
 
    # executed after each test
	def tearDown(self):
		db.drop_all()

	def test_main_page(self):
		"""
		Test if our APIs are running correctly
		We will send a request to our main page and will check the response status code
		"""
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)
 
	def test_request_exist(self):
		"""
		Test if the request (which we create in setUp()) exists or not
		"""
		self.assertTrue(
			db.session.query(Request).filter(Request.title=='test title').first()
			is not None)
	
	def test_create_request(self):
		"""
		Test create_request method by making a POST request to '/addrequest' URL
		and checking the result returned in response
		"""
		request_data = dict(
					client_id=1, 
					product_id=1, 
					title='test request', 
					desc='test desc', 
					target_date= '10-02-2018', 
					priority=1
				)
		result = self.app.post('/addrequest', data=json.dumps(request_data), content_type='application/json')
		request_result = json.loads(result.get_data())
		self.assertEqual(request_result['title'], 'test request')
	
	def test_get_requests(self):
		"""
		Test to check get_requests() by making a GET request to '/requests' URL
		and then checking it with the data created in setUp() above
		"""
		result = self.app.get('/requests')
		request_list = json.loads(result.get_data())
		
		#test with the data which was created in setUp()
		self.assertEqual(request_list[0]['title'], 'test title')
		
if __name__ == "__main__":
	unittest.main()