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
# Create your views here.

labels={}
# cost = []
labels1=[]
costs1 = []
def index(request):
    #db operations
    expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
    try:
        budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
        expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
        fig,ax=plt.subplots()
        ax.bar(['Expenses','Budget'], [abs(expense_total['expenses']),budget_total['budget']],color=['red','green'])
        # ax.set_title('Your total expenses vs total budget')
        plt.savefig('budget_app/static/budget_app/expense.png')

        labels1=[]
        costs1 = []
        for expense_item in expense_items:
            
            if((expense_item.cost)<0):
                if(expense_item.expense_name in labels.keys()):
                    labels[expense_item.expense_name]+=abs(expense_item.cost)
                
                else:
                    labels[expense_item.expense_name]=abs(expense_item.cost)
                print(labels)
                # costs1.append(abs(expense_item.cost))
                # labels1.append(expense_item.expense_name)
        labels1=labels.keys()
        costs1=labels.values()
        print("printing from index")

        print(labels1)
        print(costs1)

        # fig1, ax1 = plt.subplots()
        # ax1.pie(costs1,labels=labels1,autopct='%1.1f%%',startangle=90)
        # ax1.axis('equal')
        # ax1.set_title('Your Monthly expenses')
        # plt.savefig('budget_app/static/budget_app/costs.png')
        fig1, ax1 = plt.subplots(figsize=(6,4), subplot_kw=dict(aspect="equal"))
        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)
        wedges, texts, autotexts = ax1.pie(costs1, autopct='%1.1f%%',textprops=dict(color="w"))

        ax1.legend(wedges,labels1,title="Expenditures",loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=10, weight="bold")
        # ax1.set_title("Your Monthly Expenses")
        plt.savefig('budget_app/static/budget_app/costs.png')



    except TypeError:
        print('No data.')
    if(type(expense_total['expenses'])==None):
        expense_total['expenses']=0
    if(type(budget_total['budget'])==None):
        budget_total['budget']=0
    context = {'expense_items':expense_items,'budget':budget_total['budget'],'expenses':abs(expense_total['expenses'])}
    return render(request,'budget_app/index.html',context=context)

def add_item(request):
    name = request.POST['expense_name']
    expense_cost = request.POST['cost']
    expense_date = request.POST['expense_date']
    #db operations
    if(int(expense_cost)<0):
        labels1.append(name)
        costs1.append(expense_cost)

    print("printing from add item")
    print(labels1)
    print(costs1)
    ExpenseInfo.objects.create(expense_name=name,cost=expense_cost,date_added=expense_date,user_expense=request.user)
    budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
    expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
    fig,ax=plt.subplots()
    if(type(expense_total['expenses']==None)):
        expense_total['expenses']=0
    ax.bar(['Expenses','Budget'], [abs(expense_total['expenses']),budget_total['budget']],color=['red','green'])
    # ax.set_title('Your total expenses vs. total budget')
    plt.savefig('budget_app/static/budget_app/expense.png')

    # fig1, ax1 = plt.subplots()
    # ax1.pie(costs1,labels=labels1,autopct='%.1f%%',startangle=90)
    # ax1.axis('equal')
    # plt.savefig('budget_app/static/budget_app/costs.png')
    fig1, ax1 = plt.subplots(figsize=(7,4), subplot_kw=dict(aspect="equal"))
    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)
    wedges, texts, autotexts = ax1.pie(costs1, autopct='%1.1f%%',textprops=dict(color="w"))

    ax1.legend(wedges,labels1,title="Expenditures",loc="center left", bbox_to_anchor=(1, 0.5, 0.5, 1))
    plt.setp(autotexts, size=10, weight="bold")
    # ax1.set_title("Your Monthly Expenses")
    plt.savefig('budget_app/static/budget_app/costs.png')

    return HttpResponseRedirect('app')

def clear_item(request):
    ExpenseInfo.objects.all().delete()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


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
