from flask import Flask, render_template, redirect, url_for, request
from tinydb import TinyDB, Query
from flask_cors import CORS
import json
import uuid


app = Flask(__name__)
CORS(app)

loginList = list()
dictToReturn = dict()


db = TinyDB('database/db.json')
user_table = db.table('user_table')
listing_table = db.table('listing_table')
user = None
#
# user_table.insert({
#   'user_id': '1',
#   'user_name': 'admin',
#   'password': 'admin',
#   'funds': 100,
#   'listings': [
#     'test1',
#     'test2',
#     'test3'
#   ]
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    return render_template('create_account.html')

@app.route('/getListings')
def returnListings():
    global dictToReturn
    return json.dumps(dictToReturn)

@app.route('/submit', methods=['GET','POST'])
def submitNow():
    if request.method == 'POST':
        print(request.form['title'])
        print(request.form['description'])
        print(request.form['price'])
        global dictToReturn
        dictToReturn[str(uuid.uuid4())] = [request.form['title'],'Active',request.form['description']]
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
    return render_template('submit.html')

@app.route('/my')
def returnMyPage():
    if request.remote_addr in loginList:
        return redirect("http://localhost:5000/", code=302)
    else:
        return redirect("http://localhost:5000/login", code=302)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            global loginList
            loginList.append(request.remote_addr)
        return redirect("http://localhost:5000/", code=302)
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug = True)
