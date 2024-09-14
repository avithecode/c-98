from flask import Flask, render_template, request, redirect
import os
from time import time
from wallet import Wallet
from wallet import Account

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

myWallet =  Wallet()
account = None

@app.route("/", methods= ["GET", "POST"])
def home():
    global myWallet, account

    isConnected = myWallet.checkConnection()
    balance = "No Balance"
           
    return render_template('index.html', isConnected=isConnected,  account= account, balance = balance)
   
@app.route("/createAccount", methods= ["GET", "POST"])
def createAccount(): 
    global myWallet, account
    account = Account()
    return redirect("/")

@app.route("/makeTransaction", methods = ["GET", "POST"])
def makeTransaction():
    global myWallet, account

    sender = request.form.get("senderAddress")
    receiver = request.form.get("receiverAddress")
    amount = request.form.get("amount")

    senderType = 'ganache'
    # Check if sender equals to account.address i.e our account
    if sender == account.address:
        # Set senderType to newAccountAddress
        senderType = 'newAccountAdress'

    # Send privateKey from account as a parameter
    myWallet.makeTransactions(sender, receiver, amount, senderType, account.privateKey)
    
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, port=4000)
