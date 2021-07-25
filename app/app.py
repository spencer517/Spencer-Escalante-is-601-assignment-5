from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'heightWeight'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username' : 'Spencer'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightWeight')
    heightWeight = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, heightsAndWeights = heightWeight)

@app.route('/api/v1/heightWeight')
def heightsAndWeights(patient_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightWeight WHERE id=%s', patient_id)
    result = cursor.fetchall()
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/view/<int:patient_id>', methods=['GET'])
def rec_view(patient_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightWeight WHERE id=%s', patient_id)
    result = cursor.fetchall()
    return render_template('view.html', title='Home', patient=result[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
