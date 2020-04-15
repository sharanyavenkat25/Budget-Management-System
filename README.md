# Budget-Management-System

This project is implemented as a part of the _WT-II Lab course UE17CS355_

## About BudgetIt

BudgetIt is a website that allows the user to manage their budget smartly using the integrated analytics which helps them make better decisions in the future in regards to their financial condition. It allows users to enter their budget, and keep track of all their expenses, with dates of purchase, in a secure account using CSRF tokens.
The easy-to-use and attractive interface allows users to review their credits and debits, view how much of their allocated money for the month is left currently, and brings it to the attention of the user if they go beyond their means, and are overspending. 

Most importantly, we use REST API routing and predictive fetch patterns to make the user experience as seamless as possible, making each user’s personalized dashboard quickly accessible. The personalized dashboard, displays graphically the spends of the user, for easy assimilation (as it is proven that large amounts of data can be better understood in a pictorial form, as it will imprint better in the memory, hence enabling users to make smarter decisions), as well as predicts future spend using forecasting models, so users can prepare for the next week/month, depending on the use case. 

## Technologies

Tech-stack
* Django ( Backend Framework )
* REST API
* Ajax Patterns ( Predictive fetch )
* Jquery
* Jinja2
* JavaScript
* HTML
* CSS
* Statsmodels for intelligent functionality
* Matplotlib for graphical Representation


## Prerequisites


Installing Django

```
pip install django
```

Use this command to run the application

```
python3 manage.py runserver
```
Once the server is running proceed to open localhost on any browser (http://127.0.0.1:8000/)


