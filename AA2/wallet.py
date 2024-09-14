from web3 import Web3
import time
from datetime import datetime

ganacheUrl = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganacheUrl))

class Account():
    def __init__(self):
        self.account = web3.eth.account.create()
        self.address = self.account.address
        self.privateKey = self.account.key.hex()
        print("privatekey", self.privateKey)
        
    
    


class Wallet():
    def __init__(self):
        self.transactions = {}
        self.accountList = []
        self.ganach = web3.eth.accounts
        for i in self.ganach:
            self.accountList.append({"account":i, "balance": web3.eth.get_balance(i)})
            

    def checkConnection(self):
        if web3.is_connected():
           return True
        else:
            return False
        
    def getBalance(self, address):
        balance = web3.eth.get_balance(address)
        return web3.from_wei(balance, 'ether')
    
    def makeTransactions(self, senderAddress, receiverAddress, amount, senderType, privateKey = None):
        web3.eth.defaultAccount = senderAddress
        tnxHash = None
        if(senderType == 'ganache'):
            tnxHash = web3.eth.send_transaction({
                "from": senderAddress,
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether")  
                })
        else:
            transaction = {
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether"),
                "nonce": web3.eth.get_transaction_count(senderAddress), 
                "gasPrice": web3.to_wei(10, 'gwei'),
                "gas": 21000 
            }

            signedTx = web3.eth.account.sign_transaction(transaction, privateKey)
            tnxHash = web3.eth.send_raw_transaction(signedTx.rawTransaction)
         
        return tnxHash.hex()
    
    def addTransactionHash(self, tnxHash, senderAddress, receiverAddress, amount):
        self.transactions[tnxHash] = {
            "from":senderAddress,
            "to":receiverAddress,
            "tnxHash":tnxHash,
            "amount":amount,
            "time": time.time()
            }
    # Remove the address parameter from the getTransactions() method
    def getTransactions(self, address):
        userTransactions =[]
        for tnxHash in self.transactions:
            # Comment out the if condition, to append all transactions in the userTransaction list.  
            if self.transactions[tnxHash]['from'] == address or self.transactions[tnxHash]['to'] == address:
                userTransactions.append(self.transactions[tnxHash])
                if type(userTransactions[-1]['time']) == int:        
                    userTransactions[-1]['time'] = datetime.fromtimestamp(int(userTransactions[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S')
       
        userTransactions.sort(key=lambda transaction: transaction['time'], reverse=True)

        return  userTransactions
         
