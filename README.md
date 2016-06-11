#Butter and Toast

Butter is an eCash to NuBits on/off ramping service that integrates with services such 
as OKPay and PerfectMoney to provide a way to purchase and sell NuBits away for 
traditional exchanges.

Toast is a burn service. It provides an API to prove destruction of NuBits. The 
intention is that other service providers can integrate with this to use a a 
paywall/gateway for content and/or services

##Development  
 
1) create a virtual environment in the project root  
`virtualenv ve`  
2) activate the virtualenv  
`. ve/bin/activate`  
3) install the requirements  
`pip install -r requirements.txt`  
4) run the database migrations  
`python manage.py migrate`  
5) run the test server  
`python manage.py runserver`  
  
Steps 4,5 and 6 will be needed after most changes to the repo. 
When happy with changes, submit a pul request
