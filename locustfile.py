import random
from locust import HttpUser, task, between


'''
Instructions to follow : 

Run locust -f locustfile.py --host=http://127.0.0.1:8000 on terminal
Navigate to http://localhost:8089/ or http://127.0.0.1:8089 on a browser

Set Number of users and Hatch rate (example: Number of users=6 Hatch Rate = 2)
ensure the host field is preset to http://127.0.0.1:8000 i.e the path where our Django web app runs
'''
class WebsiteUser(HttpUser):
	wait_time = between(5, 9)

	@task(5)
	def index(self):
		response = self.client.get('/app',auth=('Tester', 'pes12345'))

	@task(1)
	def sign_up(self):
		response = self.client.get('/sign_up')
		
	@task(5)
	def budget(self):
		response = self.client.get('/budget',auth=('Tester', 'pes12345'))
		

	def on_start(self):
		""" on_start is called when a User starts before any task is scheduled """
		self.login()

	def login(self):
		response = self.client.get('/')
		csrftoken = response.cookies['csrftoken']
		self.client.post('/',
						 {'username': 'Tester', 'password': 'pes12345'}, 
						 headers={'X-CSRFToken': csrftoken})

		