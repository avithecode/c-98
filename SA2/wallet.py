from web3 import Web3

ganacheUrl = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganacheUrl))

class Account():
    def __init__(self):
        self.account = web3.eth.account.create()
        self.address = self.account.address
        self.privateKey = self.account.key.hex()

class Wallet():
    def checkConnection(self):
        if web3.is_connected():
           return True
        else:
            return False
            
    def makeTransactions(self, senderAddress, receiverAddress, amount, senderType, privateKey = None):
        web3.eth.defaultAccount = senderAddress
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
            
    # Define getBalance method that takes address as parameter
    def getBalance(self, address):
        # Pass address to web3.eth.get_balance() and store the result in balance variable
        balance = web3.eth.get_balance(address)
        # return balance after converting it to ether using web3.form_wei(amount, converted to) method 
        return web3.from_wei(balance, "ether")