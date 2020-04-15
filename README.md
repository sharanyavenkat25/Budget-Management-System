# Budget-Management-System

This project is implemented as a part of the _WT-II Lab course UE17CS355_

## About Budget-It

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

## Techniques Implemented

* ### Pedictive Fetch

This Ajax technique guesses what the user is going to do next and retrieves the appropriate data. It is always helpful to know what the user is going to do next, to optimize the user experience, and hence this technique has proved to be rather important in web applications. In our website, we assume that on checking their credits and debits, and entering new expenses, a user would be likely to visit their dashboard for a quick view on how they are spending, how much on a certain category etc., and hence use this as part of predictive fetch.

* ### REST APIs

Each functionality is defined by an API. Using the required frameworks, we ensure that on click of any button which is supposed to perform a function, it is routed to it’s respective API. All requests are sent through forms using POST method, while all graphical representations are accessed by default GET methods

## Intelligent Functionality Implemented

* ### Forecasting Models for Prediction

We used two forecasting models for predicting next spend based on the last 
10+ credits made by the user ; the Auto Regression model, which uses data from the same input variable at previous time steps, hence referred to as an autoregression (regression of self) and the Holt-Winter’s model, which tries to take into account trend and seasonality while predicting a future value. These 2 models provide a range of expected spend for the user, and we show this graphically as well, again for easier understanding. 

* ### Graphical Representation

Our application presents the user with 3 graphs: one showing them the difference between their budget and how much they’ve spent using a bar graph, and two pie charts, one each for the break up, or split up of entries that account for the credits and debits respectively. This enables the user to see where they’re spending/earning most of their money, as well as tell how much they’re saving currently. 


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


