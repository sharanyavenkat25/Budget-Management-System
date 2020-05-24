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
import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.ar_model.AR', FutureWarning)

# Create your tests here.

class ExpenseModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		# Set up non-modified objects used by all test methods
		user = User.objects.create_user('unit_testing_user','pes12345')




	def test_views(self):

		print("\n\n\t\t\t\t\t****************************Testing Responses of views****************************\n")

		#------------------ creating user -----------------------------
		user = User.objects.get(id=1)
		c = Client()
		logged_in = c.force_login(user,backend=None)
		print("\t\t\t\t############  TEST 1 : CREATING AND LOGGING IN USER  ############")
		print("user created succesfully and logged in ")
		print("username created : ",user)
		date = datetime.date(int('2020'),int('05'),int('05'))
		

		print("\n")
		print("\n")

		#------------------ adding initial budget -----------------------------
		print("\t\t\t\t############  TEST 2 : TESING VIEW budget (adding an initial budget)  ############")
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

		#------------------ adding credit and debit -----------------------------
		print("\t\t\t\t############  TEST 3 : TESING VIEW add credit transactions  ############")
		try:
			print("\t\tTESTING CREDIT TRANSACTIONS....\n")
			response2 = c.post(reverse(views.add_item), {
			'expense_name':'salary',
			'cost':10000,
			'expense_date': date,
			'transaction': 'credit',
			})
			self.assertEqual(response2.status_code,302)
			print("STATUS CODE RETURNNED IS...",response2.status_code)
			
		except:
			print("\nSTATUS CODE RETURNED IS...",response2.status_code," instead of ",302)

		print("\n")
		print("\n")

		#------------------ adding credit and debit -----------------------------
		print("\t\t\t\t############  TEST 4 : TESING VIEW add debit transactions  ############")
		try:
			
			print("\t\tTESTING DEBIT TRANSACTIONS....\n")
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
		
		print("\t\t\t\t############  TEST 5 : TESING VIEW append credit transactions under the same name  ############")
		try:
			print("\t\tAdding 30000 rp more to the existing salary....\n")
			response7 = c.post(reverse(views.add_item), {
			'expense_name':'salary',
			'cost':30000,
			'expense_date': date,
			'transaction': 'credit',
			})
			self.assertEqual(response7.status_code,302)
			print("STATUS CODE RETURNNED IS...",response7.status_code)
			response8 = c.post(reverse(views.budget))
			
		except:
			print("\nSTATUS CODE RETURNED IS...",response2.status_code," instead of ",302)


		print("\n")
		print("\n")
		print("\t\t\t\t############  TEST 6 : Tesing for ML functionaility  ############")
	
		try:
			
			print("\t\t Making a set of 12 debits to showcase ML functionaility\n")
			date=[datetime.date(int('2020'),int('05'),int('01')),
				datetime.date(int('2020'),int('05'),int('02')),
				datetime.date(int('2020'),int('05'),int('03')),
				datetime.date(int('2020'),int('05'),int('04')),
				datetime.date(int('2020'),int('05'),int('05')),
				datetime.date(int('2020'),int('05'),int('06')),
				datetime.date(int('2020'),int('05'),int('07')),
				datetime.date(int('2020'),int('05'),int('08')),
				datetime.date(int('2020'),int('05'),int('09')),
				datetime.date(int('2020'),int('05'),int('10')),
				datetime.date(int('2020'),int('05'),int('11')),
				datetime.date(int('2020'),int('05'),int('12'))]
			for i in range(0,12):
				resp='r'+str(i)
				resp= c.post(reverse(views.add_item), {
				'expense_name':'misc_'+str(i),
				'cost':1000+(i*100),
				'expense_date': date[i],
				'transaction': 'debit',
				})

			response10 = c.post(reverse(views.budget))
			self.assertEqual(response10.status_code,200)
			print("STATUS CODE RETURNNED IS...",response10.status_code)
		except:
			print("\nSTATUS CODE RETURNED IS...",response10.status_code," instead of ",200)


		print("\n")
		print("\n")


		print("\t\t\t\t############  TEST 7 : TESING VIEW make a debit more than credit  ############")
		try:
			print("\t\tDebiting more than credit exists\n")
			response9 = c.post(reverse(views.add_item), {
			'expense_name':'misc_expenses',
			'cost':500000,
			'expense_date': date,
			'transaction': 'debit',
			})
			self.assertEqual(response9.status_code,302)
			print("STATUS CODE RETURNNED IS...",response9.status_code)
			# c.post(reverse(views.budget))
			c.post(reverse(views.index))
				
		 
			
		except:
			print("\nSTATUS CODE RETURNED IS...",response2.status_code," instead of ",302)

		

		print("\t\t\t\t############  TEST 8 : TESING VIEW invalid entry  ############")
		try:
			print("\t\t Testing for Invalid Entry... \n")
			r_9 = c.post(reverse(views.add_item), {
			'expense_name':'invalid_credit',
			'cost':'inavlid cost',
			'expense_date': date,
			'transaction': 'credit',
			})
			self.assertEqual(r_9.status_code,302)
			print("STATUS CODE RETURNNED IS...",r_9.status_code)
			

		 
			
		except:
			print(" Inavlid entry type in field rasied ")


		print("\n")
		print("\n")

		#------------------ checking logout  -----------------------------
		print("\t\t\t\t############  TEST 9 : TESING VIEW logout (logging out a user and redirecting to login page)  ############")
		try:
			print("View redirects to homepage/login page")
			r_1 = c.post(reverse('logout'))
			self.assertEqual(r_1.status_code,302)
			print("\nSTATUS CODE RETURNNED IS...",r_1.status_code)
		except:
			print("\nSTATUS CODE RETURNED IS...",r_1.status_code," instead of ",302)


		print("\n")
		print("\n")
		
		#------------------ testing dashboard  -----------------------------
		print("\t\t\t\t############  TEST 10 : TESING VIEW dashboard (checking if it renders the dashboard.html)  ############")
	
		try:
			
			response6 = c.post(reverse(views.view))
			self.assertEqual(response6.status_code,200)
			print("View renders dashboard.html page with the images")
			print("\nSTATUS CODE RETURNNED IS...",response6.status_code)
		except:
			print("\nSTATUS CODE RETURNED IS...",response6.status_code," instead of ",200)




		



		






		