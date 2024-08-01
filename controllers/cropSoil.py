import sys
from flask import request, jsonify
from flask_restful import Resource
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
import json
from math import sqrt

def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)

def get_neighbors(train, test_row, num_neighbors):
    distances = []
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = [distances[i][0] for i in range(num_neighbors)]
    return neighbors

class soilcrop(Resource):
    def post(self):
        body = request.get_json()
        print(body)
        
        N = float(body["N"])
        P = float(body["P"])
        K = float(body["K"])
        temp = float(body["temperature"])
        humidity = float(body["humidity"])
        ph = float(body["ph"])
        rainfall = float(body["rainfall"])
        test_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        data = pd.DataFrame(test_data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        
        path = Path.cwd()
        path_2 = path / "controllers" / "soil_crop.pkl"
        print(path_2)
        
        SVC_from_joblib = joblib.load(path_2)
        y_pred = SVC_from_joblib.predict(data)
        print(y_pred)
        
        path_2 = path / "Dataset" / "Crop_recommendation.csv"
        dataset = pd.read_csv(path_2).to_numpy()
        print(test_data[0])
        
        neighbors = get_neighbors(dataset, test_data[0], 120)
        pred = [neighbor[-1] for neighbor in neighbors]
        list1 = np.unique(pred).tolist()
        
        if y_pred[0] in list1:
            list1.remove(y_pred[0])
        
        res = {
            "main": [y_pred[0]],
            "alternative": list1
        }
        
        return jsonify(res)

class SoilAnalysis(Resource):
    def get(self):
        path_2 = Path.cwd() / "Dataset" / "Crop_recommendation.csv"
        df = pd.read_csv(path_2)
        
        # Ensure columns are in list format
        min_vals = df.groupby('label')[['temperature', 'humidity', 'ph', 'rainfall']].min().round(0)
        max_vals = df.groupby('label')[['temperature', 'humidity', 'ph', 'rainfall']].max().round(0)
        
        context = pd.merge(min_vals, max_vals, on="label").transpose().to_json()
        context = json.loads(context)
        
        return {'context': context}, 200
