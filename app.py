from flask import Flask, render_template, redirect, url_for, request, flash
from tinydb import TinyDB, Query, where
from flask_cors import CORS
from web3 import Web3, HTTPProvider, contract
import json
import time

# Contract setupp
contract_address = "0x3374df6907edB97AFcC9e2D614F0c4B4c9E20308"
infura_url = "https://ropsten.infura.io/v3/806041cdff964ee0b2cbd2ef55cb3122"
wallet_address = "0xE75D9DE667F7FFaCD7a300E02dc4e6654598cA77"
wallet_private_key = "2CE8FABF78D208C16CC4C9A6A379AD83BD8AFAEB52B82CA918B4670D71B9EF42"

with open("abi.json") as f:
    info_json = json.load(f)
abi = info_json

w3 = Web3(HTTPProvider(infura_url))
w3.eth.enable_unaudited_features()
contract = w3.eth.contract(address = contract_address, abi = abi)
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\nG\xec]/'
CORS(app)

loginList = list()
dictToReturn = dict()

loginMap = dict()


db = TinyDB('database/db.json')
ip_user = db.table('ip_user')
user_table = db.table('user_table')
listing_table = db.table('listing_table')
user = None


# user_table.insert({
#   'ip': 'ip here',
#   'user_id': '1',
#   'user_name': 'admin',
#   'password': 'admin',
#   'funds': 100,
# })
#
# listing_table.insert({
#     'user_id': '1',
#     'listing_id': '1',
#     'title': 'FlexTape',
#     'price': 10,
#     'description': 'FLEX TAPE!!!',
#     'status': 'SOLD',
#     'date_listed': '2/15/19',
#     'date_sold': '2/16/19'
# })

def proccess_transaction_blockchain(txn_dict):
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.getTransactionReceipt(result)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        print(tx_receipt)

    if tx_receipt is None:
        print("Transaction failed!")
        return False
    return True

def add_listing_blockchain(listing_id, user_id, title, description, price, status, date_listed, date_sold):
    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.addListing(int(listing_id), int(user_id), title, description, int(price), status, date_listed, date_sold).buildTransaction({
        'chainId': 3,
        'gas': 1400000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })
    proccess_transaction_blockchain(txn_dict)


def settle_payment_blockchain(listing_id, buyer_id, seller_id):
    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.settlePayment(int(listing_id), int(buyer_id), int(seller_id)).buildTransaction({
        'chainId': 3,
        'gas': 1400000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })
    proccess_transaction_blockchain(txn_dict)

def add_new_user_blockchain(user_id, username, password):
    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.addUser(int(user_id), username, password, 1000).buildTransaction({
        'chainId': 3,
        'gas': 140000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })
    proccess_transaction_blockchain(txn_dict)

def add_new_user(username, password):
    count = 0
    for user in user_table:
        count = count + 1
    user_id = count + 1
    user_table.insert({
        'ip': request.remote_addr,
        'user_id': user_id,
        'username': username,
        'password': password,
        'funds': 0,
        'address' : ""
    })
    return

def add_new_listing(title, description, price):
    count = 0
    for item in listing_table:
        count = count + 1
    listing_id = count + 1
    User = Query()
    print()
    add_listing_blockchain(((user_table.search(User.username == currentUser))[0])['user_id'],listing_id, title, description,price, "For sale", "date1", "NULL")
    listing_table.insert({
        'user_id': ((user_table.search(User.username == currentUser))[0])['user_id'],
        'listing_id': listing_id,
        'title': title,
        'description': description,
        'price': price,
        'status': 'For sale',
        'date_listed': 'date1',
        'date_sold': 'NULL'

    })
    return listing_id

def valid_user(username,password):
    User = Query()
    if(len(user_table.search(User.username == username)) > 0):
        if(((user_table.search(User.username == username))[0])['password'] == password):
            return True
    return False

@app.route('/')
def index():
    if request.remote_addr in loginList:
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/test')
def testMeta():
    return render_template('test.html')

@app.route('/funds', methods=['GET','POST'])
def add_funds():
    User = Query()
    if request.remote_addr in loginList:
        if request.method == 'POST':
            user_table.update({'funds': int(request.form['funds'])}, where('username') == currentUser)
            return render_template("index.html")
        return render_template('funds.html')
    else:
        return redirect("http://localhost:5000/login", code=302)

@app.route('/address', methods=['GET','POST'])
def update_address():
    User = Query()
    if request.remote_addr in loginList:
        if request.method == 'POST':
            user_table.update({'address': request.form['address']}, where('username') == currentUser)
            return render_template("index.html")
        return render_template('funds.html')
    else:
        return redirect("http://localhost:5000/login", code=302)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        add_new_user(request.form['username'], request.form['password'])
        return redirect("http://localhost:5000/login", code=302)
    return render_template('create_account.html')


@app.route('/getListings')
def returnListings():
    global dictToReturn
    return json.dumps(listing_table.all())

@app.route('/f')
def returnMyListings():
    userId = user_table.search(where('username') == loginMap[request.remote_addr])[0]['user_id']
    balance = w3.fromWei(w3.eth.getBalance(user_table.search(where('username') == loginMap[request.remote_addr])[0]['address']), 'ether')
    user_table.update({'funds': float(balance)}, where('username') == currentUser)
    return (json.dumps([listing_table.search(where('user_id') == userId),user_table.search(where('username') == loginMap[request.remote_addr])[0]]))

@app.route('/buy', methods=['GET','POST'])
def buyItem():
    itemID = request.args.get('itemID')
    Listing = Query()
    item = listing_table.search(Listing.listing_id == int(itemID))[0]
    price = int(item['price'])
    balanceFromBlockchain = w3.fromWei(w3.eth.getBalance(user_table.search(where('username') == loginMap[request.remote_addr])[0]['address']), 'ether')
    user_table.update({'funds': float(balanceFromBlockchain)}, where('username') == currentUser)
    balance = user_table.search(where('username') == loginMap[request.remote_addr])[0]['funds']
    address = user_table.search(where('username') == loginMap[request.remote_addr])[0]['address']
    if(address == ''):
        pass
    else:
        if item['status'] == 'Sold':
            flash('Already sold')
        else:
            if balance - price > 0:
                user_table.update({'funds': balance-price}, where('username') == currentUser)
                listing_table.update({'status': 'Sold'}, where('listing_id') == int(itemID))
                flash('Successfully purchased')
            else:
                flash('Not enough fund')
    return redirect("http://localhost:5000/", code=302)

@app.route('/getItem', methods=['GET','POST'])
def getItem():
    if not request.remote_addr in loginList:
        return redirect("http://localhost:5000/login", code=302)
    Listing = Query()
    itemID = request.args.get('item')
    item = listing_table.search(Listing.listing_id == int(itemID))[0]
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
<html>
<head>
    <title>Lab 1</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons">
    <link rel="stylesheet" href="https://unpkg.com/bootstrap-material-design@4.1.1/dist/css/bootstrap-material-design.min.css" integrity="sha384-wXznGJNEXNG1NFsbm0ugrLFMQPWswR3lds2VeinahP8N0zJw9VWSopbjv2x7WCvX" crossorigin="anonymous">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>

  
    <nav class="navbar navbar-dark bg-dark">
            <a class="navbar-brand" href="http://localhost:5000">CSE4/510 Lab1</a>
            <ul class="nav nav-pills">
                    <li class="nav-item">
                      <a class="nav-link" href="http://localhost:5000/submit">Create a listing</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="http://localhost:5000/my">My Page</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="http://localhost:5000/address">Update my address</a>
                    </li>
                  </ul>
                  </nav>
        <br>


        <div class="container"> 
        <span class="badge badge-primary" id="b1">Balance: """ + str(user_table.search(where('username') == loginMap[request.remote_addr])[0]['funds']) +""" ETH</span>
                <div class="row" id="p1">
                <h1>Checkout</h1>  """  + """
                    <div class="col-sm-6">
                     <div class="card">
                        <div class="card-body">
                        <h4 class="card-title">
                        Title: """ + item['title'] + """
                        </h4>
                        <h6 > Price: """ + item['price'] +  """ETH
                        
                        </h6>
                        <br>
                        <p class="card-text"> """ + item['description'] + """</p>
                        <a href="http://localhost:5000/buy?itemID=""" + str(itemID)+ """" class="btn btn-primary">Buy</a>
                    </div>
                </div>
                </div>

                </div>
          </div>
          </body>
</html>
        """
        return json.dumps(listing_table.search(Listing.listing_id == int(itemID)))
    return render_template('checkout.html')

@app.route('/getUser', methods=['GET', 'POST'])
def getUserFunds():
    User = Query()
    if(request.method == 'GET'):
        return user_table.search(User.username == currentUser)[0]['funds']
        

@app.route('/submit', methods=['GET','POST'])
def submitNow():
    if request.remote_addr in loginList:
        if request.method == 'POST':
            itemId = add_new_listing(request.form['title'], request.form['description'], request.form['price'])
            global dictToReturn
            dictToReturn[itemId] = [request.form['title'],'Active',request.form['description'],request.form['price']]
            return redirect("http://localhost:5000/", code=302) 
        return render_template('submit.html')
    else:
        return redirect("http://localhost:5000/login", code=302)

@app.route('/my')
def returnMyPage():
    if request.remote_addr in loginList:
        return render_template('my.html')
    else:
        return redirect("http://localhost:5000/login", code=302)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_user(request.form['username'], request.form['password']):
            global loginList
            global loginMap
            loginMap[request.remote_addr] = request.form['username']
            loginList.append(request.remote_addr)
            global currentUser
            currentUser = request.form['username']
        else:
            error = 'Invalid Credentials. Please try again.'
        return redirect("http://localhost:5000/", code=302)
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')