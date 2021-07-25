from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response, render_template

app = Flask(__name__)


def heightweight_import() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'heightWeight'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM tableHeightWeight')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

@app.route('/')
def index():
    user = {'username' : 'Spencer'}
    heightWeight = heightweight_import()
    return render_template('index.html', title='Home', user=user, heightsAndWeights = heightWeight)

@app.route('/api/heightWeight')
def index() -> str:
    js = json.dumps(heightweight_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
