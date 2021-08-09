from flask import Flask, request, jsonify, render_template
import mysql.connector
from getpass import getpass
from mysql.connector import connect

connection = connect(host='localhost', user='root', password='Raptor//Kona9', database='leads')
cursor = connection.cursor()
connection2 = connect(host='localhost', user='root', password='Raptor//Kona9', database='fox_data_consulting')
cursor2 = connection2.cursor()

def processUserInput(name, customer, domain):
    name = name.lower()
    if customer == 'yes':
        customer = 1
    if customer == 'no':
        customer = 0
    domain = domain.lower()
    return name, customer, domain

def writeQuery(name, landingPage, customer, domain, model, source, adspend, hardcosts):
    q = 'INSERT INTO survey (name, landingPage, customer, domain, model, source, adspend, hardcosts) VALUES ({}, {}, {}, {}, {});'
    pass

def storeEmail(email):
    pass

app = Flask(__name__)
name, customer, domain = processUserInput(name, customer, domain)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def store():
    pass

if __name__ == "__main__":
    app.run(debug=True, threaded=True)