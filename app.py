import os
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,validators
import requests
import csv
from flask import Flask, render_template, request,Response
app = Flask(__name__)
rates=[]
rateList=[]
currencyCodes=[]
class Form(FlaskForm):
  currency=SelectField('currency',choices=currencyCodes)
  amount=StringField('amount', [validators.data_required(), validators.length(max=10)])

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/currency', methods=["GET", "POST"])
def choosecurrency():
  form=Form()
  form.currency.choices=currencyCodes
  if request.method=='POST':
    return '<h1>Currency : {},Calculation: {} PLN</h1>'.format(form.currency,calculate(form.currency.data,form.amount.data))
  return render_template('currency.html',form=form)

def calculate(code,amount):
  result = 0.0
  for item in rateList:
    if item["code"]==code:
      result=float(item["bid"])*float(amount)
      break
  return result    

def load_items_from_csv():
    rates.clear()
    filepath = "currency.csv"
    with open(filepath,"r") as csv_file:
    
        reader = csv.DictReader(csv_file)
        for item in reader:
            
            rates.append(dict(item))


def export_items_to_csv():
    filename = "currency.csv"
    with open(filename,"w") as csv_file:
        fields = ['currency', 'code', 'bid', 'ask'] 
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rateList)

    print("Succesfully added file")
    return 1


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates.append(data)

rate=rates[0]
for item in rate:     
  for rate in item["rates"]:
    print(rate["code"])
    currencyCodes.append(rate["code"])
    rateList.append(rate)

export_items_to_csv()  

if __name__ == '__main__':
    app.run(debug=True)

