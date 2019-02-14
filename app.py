from flask import Flask, render_template
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getListings')
def returnListings():
    dictToReturn = dict()
    listToReturn = ['Test1','Active','Test Item']
    dictToReturn['test1'] = listToReturn
    return json.dumps(dictToReturn)

if __name__ == '__main__':
    app.run(debug = True)
