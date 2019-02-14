from flask import Flask, render_template
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getListings')
def returnListings():
    dictToReturn = dict()
    listToReturn = ['Test 1','Active','Test Item']
    dictToReturn['test1'] = listToReturn
    dictToReturn['test2'] = ['Test 2','Sold','Test Item 2']
    dictToReturn['test3'] = ['Test 3','Sold','Test Item 3']

    return json.dumps(dictToReturn)

if __name__ == '__main__':
    app.run(debug = True)
