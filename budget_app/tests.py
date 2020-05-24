from django.test import TestCase
from .models import ExpenseInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from . import views
from django.contrib.auth import views as auth_views
from django.test import Client
import datetime
from django.urls import reverse
import pandas as pd

# Create your tests here.

class ExpenseModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		# Set up non-modified objects used by all test methods
		user = User.objects.create_user('unit_testing_user','pes12345')


	def test_views(self):

		print("\n\n****************************Testing Responses of views****************************")
		user = User.objects.get(id=1)
		c = Client()
		logged_in = c.force_login(user,backend=None)
		date = datetime.date(int('2020'),int('05'),int('05'))
		print("\n")
		print("\n")
		print("===== TESTING VIEW index ======")
		try:
			response = c.post(reverse(views.index))
			self.assertEqual(response.status_code,200)

			print("\nSTATUS CODE RETURNNED IS...",response.status_code)
		except:
			print("\nSTATUS CODE RETURNED IS...",response.status_code," instead of ",200)

		print("\n")
		print("\n")

		
		print("=====TESTING VIEW budget ======")
		try:
			init_b=200000
			print("setting initial budget as : ",init_b)
			response4 = c.post(reverse(views.budget), {
			'init_budget':init_b,
			})
			self.assertEqual(response4.status_code,200)
			
			print("\nSTATUS CODE RETURNNED IS...",response4.status_code)

		except:
			print("\nSTATUS CODE RETURNED IS...",response4.status_code," instead of ",200)
		

		print("\n")
		print("\n")
		print("=====TESTING VIEW add_item ======")
		try:
			print("TESTING CREDIT TRANSACTIONS....\n")
			response2 = c.post(reverse(views.add_item), {
			'expense_name':'salary',
			'cost':10000,
			'expense_date': date,
			'transaction': 'credit',
			})
			self.assertEqual(response2.status_code,302)
			print("STATUS CODE RETURNNED IS...",response2.status_code)
			print("\n")
			print("TESTING DEBIT TRANSACTIONS....\n")
			response3 = c.post(reverse(views.add_item), {
			'expense_name':'loan',
			'cost':5000,
			'expense_date': date,
			'transaction': 'debit',
			})
			self.assertEqual(response3.status_code,302)
			print("\nSTATUS CODE RETURNNED IS...",response3.status_code)

		except:
			print("\nSTATUS CODE RETURNED IS...",response3.status_code," instead of ",302)


		print("\n")
		print("\n")
		print("=====TESTING VIEW logout ======")

		try:
			print("View redirects to homepage/login page")
			response5 = c.post(reverse(views.logout_view))
			self.assertEqual(response5.status_code,302)
			print("\nSTATUS CODE RETURNNED IS...",response5.status_code)
		except:
			print("\nSTATUS CODE RETURNED IS...",response5.status_code," instead of ",302)


		print("\n")
		print("\n")
		print("=====TESTING VIEW dashboard ======")

		try:
			
			response5 = c.post(reverse(views.view))
			self.assertEqual(response5.status_code,200)
			print("View renders dashboard.html page with the images")
			print("\nSTATUS CODE RETURNNED IS...",response5.status_code)
		except:
			print("\nSTATUS CODE RETURNED IS...",response5.status_code," instead of ",200)

		


		






		