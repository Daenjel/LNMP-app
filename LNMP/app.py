import requests
import json
import os
from flask_restful import reqparse
from flask import Flask,request, render_template
from requests.auth import HTTPBasicAuth

def parse_arg_from_requests(arg, **kwargs):
    parse = reqparse.RequestParser()
    parse.add_argument(arg, **kwargs)
    args = parse.parse_args()
    return args[arg]
    
app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def index():
  if request.method == "POST":
    amount = request.form["amount"]
    PartyA = request.form["phoneNumber"]

    print(amount,PartyA)
  return render_template("index.html")

@app.route('/mpesa', methods=["POST","GET"])
def mpesa():
    amount = parse_arg_from_requests('amount')
    PartyA = parse_arg_from_requests('phoneNumber')
    print(amount,PartyA)
    
    consumer_key = "FPjPl8OknAclG3TYOvAIanJroWGuMNfg"
    consumer_secret = "Smqt7ZQ61Xlgav8P"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret),verify=False)

    j = json.loads(r.text)
    print (j['access_token'])

    access_token = j['access_token']

    # define the variales
    # provide the following details, this part is found on your test credentials on the developer account
    BusinessShortCode = '174379'
    #Passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919' 

    AccountReference = 'DAENJEL'
    TransactionDesc = 'daenjel'
    #Timestamp = date('YmdGis')
    #Password = base64_encode(BusinessShortCode.Passkey.Timestamp)

    # callback url
    CallBackURL = 'http://26ebc457.ngrok.io/hooks/mpesa'

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" %access_token }
    request = {
      "BusinessShortCode": BusinessShortCode,
      "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTkwMzIzMTUzNDM4",
      "Timestamp": "20190323153438",
      "TransactionType": "CustomerPayBillOnline",
      "Amount": amount,
      "PartyA": PartyA,
      "PartyB": BusinessShortCode,
      "PhoneNumber": PartyA,
      "CallBackURL": CallBackURL,
      "AccountReference": AccountReference,
      "TransactionDesc": TransactionDesc
    }

    response = requests.post(api_url, json = request, headers=headers,verify=False)
    
    print (response.text)

    return response.text

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=os.environ.get("POST"))
