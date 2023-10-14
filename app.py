from flask import Flask, send_file

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
def chess_bot_type(type_name):
    if type_name in TYPES:
        return send_file(f'lichess/{type_name}.html')
    else:
        return "Loại không hợp lệ", 404

#@app.route('/lishogi')
#def lishogi():
#    return send_file('html/lishogi.html')
#
#@app.route('/lishogi/<type_name>')
#def shogi_bot_type(type_name):
#    if type_name in TYPES:
#        return send_file(f'lishogi/{type_name}.html')
#    else:
#        return "Loại không hợp lệ", 404
#
#@app.route('/playstrategy')
#def playstrategy():
#   return send_file('html/playstrategy.html')
#
#@app.route('/playstrategy/<type_name>')
#def strategy_bot_type(type_name):
#    if type_name in TYPES:
#        return send_file(f'playstrategy/{type_name}.html')
#    else:
#        return "Loại không hợp lệ", 404
#
#@app.route('/lidraughts')
#def lidraughts():
#    return send_file('html/lidraughts.html')
#
#@app.route('/lidraughts/<type_name>')
#def draughts_bot_type(type_name):
#    if type_name in TYPES:
#        return send_file(f'lidraughts/{type_name}.html')
#    else:
#        return "Loại không hợp lệ", 404

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
