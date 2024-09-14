from web3 import Web3

ganacheUrl = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganacheUrl))

class Account():
    def __init__(self):
        self.account = web3.eth.account.create()
        self.address = self.account.address
        # Create self.private key and store self.account.key.hex() in it
        self.privateKey = self.account.key.hex()

class Wallet():
    def checkConnection(self):
        if web3.is_connected():
           return True
        else:
            return False
            
    # Accept privateKey parameter with default value None
    def makeTransactions(self, senderAddress, receiverAddress, amount, senderType, privateKey = None):
        
        web3.eth.defaultAccount = senderAddress

        if(senderType == 'ganache'):
            tnxHash = web3.eth.send_transaction({
                "from": senderAddress,
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether")  
                })
        #Else    
        else:
            # Create a dict with "to", "value", "nonce", gasPrice, gas as keys
            # Calculate nonce as web3.eth.get_transaction_count(senderAddress)
            # Set gasPrice to web3.to_wei(10, 'gwei')
            # Set gas to 21000
            transaction = {
                "to":receiverAddress,
                "value":web3.to_wei(amount, "ether"),
                "nonce":web3.eth.get_transaction_count(senderAddress),
                "gasPrice":web3.to_wei(10, 'gwei'),
                "gas":21000
            }
            

            # Use web3.eth.account.sign_transaction() method and pass it transaction and privateKey
            # Store return value in signedTx
            signedTx = web3.eth.account.sign_transaction(transaction, privateKey)
            # Call web3.eth.send_raw_transaction()and pass it signedTx.rawTransaction and store return value in tnxHash
            tnxHash = web3.eth.send_raw_transaction(signedTx.rawTransaction)

            # Print tnxHash
            print(tnxHash)