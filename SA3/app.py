from flask import Flask, render_template, request, redirect, session
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
    # Create transactions variable and set it to None
    transactions = None
    if(account):
        balance = myWallet.getBalance(account.address)
        # Call getTransactions() method and pass it account.address and store the result in transactions variable
        transactions = myWallet.getTransactions(account.address)

    # Pass transaction as transaction attribute
    return render_template('index.html', isConnected=isConnected,  account= account, balance = balance, transactions = transactions)


@app.route("/makeTransaction", methods = ["GET", "POST"])
def makeTransaction():
    global myWallet, account

    sender = request.form.get("senderAddress")
    receiver = request.form.get("receiverAddress")
    amount = request.form.get("amount")

    senderType = 'ganache'
    if(sender == account.address):
        senderType = 'newAccountAddress'

    tnxHash= myWallet.makeTransactions(sender, receiver, amount, senderType, account.privateKey)
    myWallet.addTransactionHash(tnxHash, sender, receiver, amount)
    return redirect("/")


@app.route("/createAccount", methods= ["GET", "POST"])
def createAccount(): 
    global myWallet, account
    account = Account()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, port=4000)