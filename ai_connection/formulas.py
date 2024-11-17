# formulas.py

"""
Loan amount -> price of house - down payment
Interest rate (APR) -> get it from an api call if possible
Loan term length ->
Morgage insurance -> 'If you make a down payment of less than 20%, you’ll have to pay private mortgage insurance (PMI) on a conventional loan until you reach 20% equity. FHA loans have mandatory insurance premiums that may last for the life of the loan, depending on your down payment amount.'
Property taxes -> typically built into mortgage payment. 'reasonably accurate estimate of your property taxes will provide a better picture of the cost. Regardless of whether you have an escrow account, you’ll need to account for property taxes when determining the total cost of homeownership.'
Homeowners insurance
HOA fees
"""
# rates api
#https://www.zillowgroup.com/developers/api/mortgage/get-current-rates/

# Calculating morgage payments.
"""
calculate your mortgage payment based on the loan principal and interest before taxes, along with homeowners insurance and HOA fees
M = monthly payment
P = principal amount
I = interest rate (base interest rate and not the APR)
(Additionally, your mortgage interest rate is an annual interest rate that represents the interest that’s supposed to be paid monthly over the course of the year, so you’ll need to divide this by 12 to get the monthly interest rate)
N = number of payments (This is the total number of payments in your loan repayment term. For instance, if it’s a 30-year mortgage with monthly payments and you always pay the minimum amount, you’ll make 360 payments.)
"""
# M = (P*(I*(1+I)**N)) / (((1+I)**N)-1)





"""
3 Types Of Mortgage Calculators

A few types of mortgage calculators can prove helpful depending on your situation:

1. Purchase calculator: A purchase calculator allows you to figure out how much cash you need for a down payment, or you can figure out how much you can afford based on your down payment and monthly income. You’ll need information such as the sales price and your down payment, credit score, income, debts and ZIP code.

2. Refinance calculator: A refinance calculator can help you determine whether a new mortgage loan makes sense for your situation. You’ll need to know your home’s estimated value, your mortgage balance and how long you plan to stay in your home, in addition to your income, debts and credit score.

3. Amortization calculator: A mortgage amortization calculator can show you how much interest and how many months of payments you can save by putting extra money toward your principal payment. You’ll need to input your loan amount, loan term length, interest rate and the state you live in.
"""


from datetime import date
import requests
import json
from dotenv import load_dotenv

load_dotenv()

mortgage_rate_url = 'https://api.api-ninjas.com/v1/mortgagerate'
response = requests.get(
    mortgage_rate_url,
    headers={'X-Api-Key': 'MORTAGAGE_RATE'}
    )
if response.status_code == requests.codes.ok:
    json.loads(response.text)[0]['data']
    frm30 = json.loads(response.text)[0]['data']['frm_30']
    frm15 = json.loads(response.text)[0]['data']['frm_15']
    print(frm30, frm15)
else:
    print("Error:", response.status_code, response.text)
