from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/medical_management"
mongo = PyMongo(app)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    result = mongo.db.patients.insert_one(data)
    return jsonify({'status': 'Patient created', 'id': str(result.inserted_id)})

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = mongo.db.patients.find()
    patient_list = []
    for patient in patients:
        patient['_id'] = str(patient['_id'])
        patient_list.append(patient)
    return jsonify(patient_list)

@app.route('/delete_patient/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    result = mongo.db.patients.delete_one({'_id': ObjectId(patient_id)})
    if result.deleted_count > 0:
        return jsonify({'status': 'Patient deleted'})
    else:
        return jsonify({'status': 'Patient not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
