from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

	def on_start(self):

		self.client.post("login", {
			'username': 'locust_test', 'password': 'load12345'
		})

	@task
	def get_budget(self):
		self.client.get('budget')

	@task
	def get_app(self):
		self.client.get('index')

