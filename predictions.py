import joblib
import mysql
from flask import session, jsonify, request

from app import mysql_config

# Load the saved model
model = joblib.load('model/random_forest_model.pkl')
def AddTransaction():
    if 'id' not in session:
        return jsonify({'error': 'User not logged in'}), 403  # User must be logged in to proceed

    data = request.form.to_dict()
    transaction_types = {0: "Cash In", 1: "Cash Out", 2: "Debit", 3: "Payment", 4: "Transfer"}
    transaction_type = transaction_types.get(int(data.get('type', 0)), "Unknown")  # Get transaction type with default

    # Ensure all six features are provided correctly:
    input_data = [[
        float(data.get('type', 0)),  # Assuming 'type' needs to be included as a feature
        float(data.get('amount', 0)),
        float(data.get('oldbalanceOrg', 0)),
        float(data.get('newbalanceOrig', 0)),
        float(data.get('oldbalanceDest', 0)),
        float(data.get('newbalanceDest', 0))
    ]]

    prediction = model.predict(input_data)[0]
    prediction = int(prediction)  # Convert numpy int to standard Python int

    # Save the prediction and input data to the database
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("""
           INSERT INTO predictions (userId, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFraud)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
       """, (session['id'], transaction_type, data['amount'], data['oldbalanceOrg'], data['newbalanceOrig'],
             data['oldbalanceDest'], data['newbalanceDest'], prediction))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'prediction': prediction})