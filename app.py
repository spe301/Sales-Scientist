from flask import Flask, request, jsonify, render_template
import mysql.connector
from getpass import getpass
from mysql.connector import connect

connection = connect(host='localhost', user='root', password='Raptor//Kona9', database='leads')
cursor = connection.cursor()
connection2 = connect(host='localhost', user='root', password='Raptor//Kona9', database='fox_data_consulting')
cursor2 = connection2.cursor()

app = Flask(__name__)
#name, customer, domain = processUserInput(name, customer, domain)

@app.route('/')
def home():
    return render_template('index.html')

#try using another function with the same name
@app.route('/store', methods=['POST'])
def store():
    name = request.form['name'].lower()
    cursor.execute('''INSERT INTO test (col1) VALUES ('{}');'''.format(name))
    connection.commit()
    return name



'''@app.route('/predict', methods=['POST'])
def predict():
    name = get_name()
    landingPage = get_landingPage()
    cursor.execute('INSERT INTO test (col1, col2) VALUES ('{}', '{}');'.format(name, landingPage))
    connection.commit()
    return render_template('index.html')'''

if __name__ == "__main__":
    app.run(debug=True, threaded=True)