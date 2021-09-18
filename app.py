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
    f = request.form['csvfile']
    #with open(f) as file:
    data = []
    csvfile = pd.DataFrame(csv.reader(f))
    return render_template('index.html', data=csvfile.shape)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)