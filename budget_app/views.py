from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import ExpenseInfo
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Q
import datetime

#ml part
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.ar_model import AR
from random import random
import os
# Create your views here.

labels={}
cred_labels={}
dates=[]
#for debit (expenses)
labels1=[]
costs1 = []

#for credit (additions)
labels2=[]
costs2= []


def index(request):

	init_name = request.POST.get('init_name','Budget')
	init_budget = request.POST.get('init_budget',0)
	init_expense_date = request.POST.get('init_expense_date','2020-04-01')
	
	# #db operations
	ExpenseInfo.objects.create(expense_name=init_name,cost=init_budget,date_added=init_expense_date,user_expense=request.user)
	expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
	budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
	expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
	
	if(budget_total['budget'] is None):
		budget_total['budget']=0
	if(expense_total['expenses'] is None):
		expense_total['expenses']=0

	context = {'expense_items':expense_items,'budget':budget_total['budget'],'diff': budget_total['budget']+expense_total['expenses'],'expenses':abs(expense_total['expenses'])}
	return render(request,'budget_app/index.html',context=context)
	# return HttpResponseRedirect('budget')

def add_item(request):
	name = request.POST['expense_name']
	expense_cost = request.POST['cost']
	expense_date = request.POST['expense_date']
	transaction = request.POST['transaction']

	#db operations
	if(transaction=='debit'):
		expense_cost=int(expense_cost) * (-1)
	else:
		expense_cost=int(expense_cost)* (1)
	print("TRANSACTION TYPE : ",transaction)
	print(transaction=='debit')
	print(type(expense_cost),expense_cost)

	if(int(expense_cost)<0):
		labels1.append(name)
		costs1.append(expense_cost)
	else:
		labels2.append(name)
		costs2.append(expense_cost)

	print("printing from add item")
	print("debit")
	print(labels1)
	print(costs1)
	print("credit")
	print(labels2)
	print(costs2)

	ExpenseInfo.objects.create(expense_name=name,cost=expense_cost,date_added=expense_date,user_expense=request.user)
	budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
	expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))	
	
	fig,ax=plt.subplots(figsize=(6,4))
	if(expense_total['expenses'] is None):
		expense_total['expenses']=0
	if(budget_total['budget'] is None):
		budget_total['budget']=0
	ax.bar(['Expenses','Budget'], [abs(expense_total['expenses']),abs(budget_total['budget'])],color=['red','green'])
	# ax.set_title('Your total expenses vs. total budget')
	plt.savefig('budget_app/static/budget_app/expense.png')

	# fig1, ax1 = plt.subplots()
	# ax1.pie(costs1,labels=labels1,autopct='%.1f%%',startangle=90)
	# ax1.axis('equal')
	# plt.savefig('budget_app/static/budget_app/costs.png')
	fig1, ax1 = plt.subplots(figsize=(6,4), subplot_kw=dict(aspect="equal"))
	def func(pct, allvals):
		absolute = int(pct/100.*np.sum(allvals))
		return "{:.1f}%\n({:d} g)".format(pct, absolute)
	wedges, texts, autotexts = ax1.pie(costs1, autopct='%1.1f%%',textprops=dict(color="w"))

	ax1.legend(wedges,labels1,title="Expenditures",loc="center left", bbox_to_anchor=(1, 0.5, 0.5, 1))
	plt.setp(autotexts, size=10, weight="bold")
	# ax1.set_title("Your Monthly Expenses")
	plt.savefig('budget_app/static/budget_app/costs.png')

	fig2, ax2 = plt.subplots(figsize=(6,4), subplot_kw=dict(aspect="equal"))
	wedges_, texts_, autotexts_ = ax2.pie(costs2, autopct='%1.1f%%',textprops=dict(color="w"))
	ax2.legend(wedges_,labels2,title="Credits",loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
	plt.setp(autotexts_, size=10, weight="bold")
	plt.savefig('budget_app/static/budget_app/credits.png')

	
	return HttpResponseRedirect('budget')
def budget(request):
	if(os.path.exists("budget_app/static/budget_app/expense.png")):
		os.remove("budget_app/static/budget_app/expense.png")
	if(os.path.exists("budget_app/static/budget_app/credits.png")):
		os.remove("budget_app/static/budget_app/credits.png")
	if(os.path.exists("budget_app/static/budget_app/costs.png")):
		os.remove("budget_app/static/budget_app/costs.png")
	if(os.path.exists("budget_app/static/budget_app/predict.png")):
		os.remove("budget_app/static/budget_app/predict.png")
	print("\t \t -----Removing all static files...------")
	init_name = request.POST.get('init_name','Budget')
	init_budget = request.POST.get('init_budget',0)
	init_expense_date = request.POST.get('init_expense_date','2020-04-01')
	
	# #db operations
	ExpenseInfo.objects.create(expense_name=init_name,cost=init_budget,date_added=init_expense_date,user_expense=request.user)
	expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
	budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
	expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
	if(expense_total['expenses'] is None):
		expense_total['expenses']=0
	if(budget_total['budget'] is None):
		budget_total['budget']= 0
	
		
	fig,ax=plt.subplots()
	ax.bar(['Expenses','Budget'], [abs(expense_total['expenses']),abs(budget_total['budget'])],color=['red','green'])
	plt.savefig('budget_app/static/budget_app/expense.png')

	labels1=[]
	costs1 = []
	labels2=[]
	costs2=[]
	debit_dates=[]
	labels={}
	cred_labels={}
	for expense_item in expense_items:
		
		if((expense_item.cost)<0):
			debit_dates.append(expense_item.date_added)	
			if(expense_item.expense_name in labels.keys()):
				labels[expense_item.expense_name]+=abs(expense_item.cost)
				
			else:
				labels[expense_item.expense_name]=abs(expense_item.cost)
			# print(labels)
		else:
			if(expense_item.expense_name in cred_labels.keys()):
				cred_labels[expense_item.expense_name]+=abs(expense_item.cost)
			else:
				cred_labels[expense_item.expense_name]=abs(expense_item.cost)
			# print(cred_labels)
	
	labels1=labels.keys()
	costs1=labels.values()

	labels2=cred_labels.keys()
	costs2=cred_labels.values()
	# print(list(debit_dates))
	print("printing from index for debit")

	print(labels1)
	print(list(costs1))
	print("printing from index for credit")

	print(labels2)
	print(costs2)

		
	fig1, ax1 = plt.subplots(figsize=(6,4), subplot_kw=dict(aspect="equal"))
	def func(pct, allvals):
		absolute = int(pct/100.*np.sum(allvals))
		return "{:.1f}%\n({:d} g)".format(pct, absolute)


	wedges, texts, autotexts = ax1.pie(costs1, autopct='%1.1f%%',textprops=dict(color="w"))

	ax1.legend(wedges,labels1,title="Expenditures",loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
	plt.setp(autotexts, size=10, weight="bold")
	plt.savefig('budget_app/static/budget_app/costs.png')

	fig2, ax2 = plt.subplots(figsize=(6,4), subplot_kw=dict(aspect="equal"))
	wedges_, texts_, autotexts_ = ax2.pie(costs2, autopct='%1.1f%%',textprops=dict(color="w"))

	ax2.legend(wedges_,labels2,title="Credits",loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
	plt.setp(autotexts_, size=10, weight="bold")
	plt.savefig('budget_app/static/budget_app/credits.png')
	
	lower=0
	upper=0


	def unique(sequence):
	    seen = set()
	    return [x for x in sequence if not (x in seen or seen.add(x))]


	fig3, ax3 = plt.subplots(figsize=(6,4))
	fig3.autofmt_xdate()
	copy=[]
	copy=list(costs1)
	# print("before ...",debit_dates)
	debit_dates=unique(debit_dates)
	# print("after ... ",debit_dates)
	if(len(debit_dates)==len(copy)):
		ax3.plot(debit_dates, copy)
		plt.savefig('budget_app/static/budget_app/predict.png')

	if(len(debit_dates)>=10):
			fig3, ax3 = plt.subplots(figsize=(6,4))
			model = AR(list(costs1))
			model_fit = model.fit()
			# make prediction
			yhat = model_fit.predict(len(costs1), len(costs1))
			print("PREDICTED EXPENSE...")
			print(yhat)  #new expense
			# copy=[]
			# copy=list(costs1)
			print(costs1)
			print(copy)
			print(debit_dates)
			#copy.append(yhat)
			#debit_dates.append(debit_dates[0]+datetime.timedelta(days=1))
			if(len(debit_dates)==len(copy)):
				fig3.autofmt_xdate()
				ax3.plot(debit_dates, copy)

				  #line graph for AR
				plt.savefig('budget_app/static/budget_app/predict.png')

			#fig4, ax4 = plt.subplots()
			model2 =  ExponentialSmoothing(list(costs1))
			model_fit2 = model2.fit()
			# make prediction
			yhat2 = model_fit2.predict(len(costs1), len(costs1))
			print("Range of expenses:")
			print(yhat[0], "-", yhat2[0])  #new expense
			#copy2=[]
			#copy2=list(costs1)
			#copy2.append(yhat2)
			#ax4.plot(debit_dates, copy, "b")
			#ax4.plot(debit_dates, copy2, "r")  #line graph for AR
			#ax4.set_title("helllllllo")
			#plt.savefig('budget_app/static/budget_app/predict2.png')
			lower=round(yhat[0],2)
			upper=round(yhat2[0],2)


	context = {'expense_items':expense_items,'budget':budget_total['budget'],'diff': budget_total['budget']+expense_total['expenses'],'expenses':abs(expense_total['expenses']), 'lower':lower,'upper':upper}
	#render(request, "budget_app/dashboard.html", context=context)
	return render(request,'budget_app/budget.html',context=context)

def clear_item(request):
	return HttpResponseRedirect('/')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def view(request):
	form = UserCreationForm
	return render(request,'budget_app/dashboard.html',{'form':form})

def sign_up(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user=form.save()
			login(request,user)
			return HttpResponseRedirect('app')
		else:
			for msg in form.error_messages:
				print(form.error_messages[msg])
	else:
		form = UserCreationForm
		return render(request,'budget_app/sign_up.html',{'form':form})
