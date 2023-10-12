from flask import Flask, send_file

import pandas as pd

app = Flask(__name__)

TYPES = [
    'bullet',
    'blitz',
    'rapid',
    'classical',
    'correspondence',
    'antichess',
    'atomic',
    'chess960',
    'crazyhouse',
    'horde',
    'kingOfTheHill',
    'racingKings',
    'threeCheck'
]

@app.route('/')
@app.route('/home')
def welcome_page():
    return send_file('index.html')

@app.route('/lichess')
def lichess():
    return send_file('html/lichess.html')

@app.route('/lichess/<type_name>')
def lichess_type(type_name):


	data = pd.read_csv('html/{type_name}.csv'),header=0)
	return render_template('lichess.html', tables=[data.to_html()], titles=[''])
        
@app.route('/lishogi')
def lishogi():
    return send_file('html/lishogi.html')

@app.route('/playstrategy')
def playstrategy():
    return send_file('html/playstrategy.html')

@app.route('/lidraughts')
def lidraughts():
    return send_file('html/lidraughts.html')

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
