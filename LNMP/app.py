import requests
import json
import os
from flask import Flask, render_template
from flask import request
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
  if request.method == "POST":
    amount = request.form["amount"]
    PartyA = request.form["phoneNumber"]

    print(amount,PartyA)
  return render_template("index.html")

@app.route("/mpesa", methods=["POST","GET"])
def mpesa():
  if request.method == "POST":
    amount = request.form["amount"]
    PartyA = request.form["phoneNumber"]

    #amount = '1'
    #PartyA = '254718453698'
    
    consumer_key = "CONSUMER KEY"
    consumer_secret = "CONSUMER SECRET"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret),verify=False)

    j = json.loads(r.text)
    print (j['access_token'])

    access_token = j['access_token']

    # define the variales
    # provide the following details, this part is found on your test credentials on the developer account
    BusinessShortCode = 'BUSINESSCODE'
    Passkey = 'PASSKEY' 

    AccountReference = 'ACCT'
    TransactionDesc = 'DESC'
    #Timestamp = date('YmdGis')
    #Password = base64_encode(BusinessShortCode.Passkey.Timestamp)

    # callback url
    CallBackURL = 'CALLBACK URL'

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" %access_token }
    request = {
      "BusinessShortCode": BusinessShortCode,
      "Password": "PASSKEY",
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

    return render_template("index.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=os.environ.get("POST"))
