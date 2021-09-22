import numpy as np
from flask import Flask, request, jsonify, render_template, Response
from scoring import WrapScoring
import pandas as pd 
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    #dp = r'C:\Users\aacjp\Sales-Scientist\datasets\check6.csv'
    #lp = r'C:\Users\aacjp\Sales-Scientist\datasets\prospects.csv'
    path = request.form['Text']
    data = pd.read_csv(path)
    base = path.split('.')[0]
    dp = base + '_leads'
    lp = base + '_actions'
    data = WrapScoring(data, dp, lp)
    return render_template('index2.html', data=data.to_html())

if __name__ == "__main__":
    app.run(debug=True, threaded=True)