from datetime import datetime

import joblib
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
import re
import predictions
app = Flask(__name__)

# Load the saved model
model = joblib.load('model/QuadraticDiscriminantAnalysisl.pkl')

app.secret_key = "your_secret_key"  # Change this to a random string

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'atm_laundering'
}
@app.route('/')
def index():
    if 'fullName' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # This should be hashed and checked securely

        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user['password'] == password:  # Replace with hashed password comparison
            session['id'] = user['id']
            session['fullName'] = user['fullName']
            session['email'] = user['email']
            session['dob'] = str(user['dob'])
            session['gender'] = user['gender']
            session['location'] = user['location']
            session['userRole'] = user['userRole']
            session['joinDate'] = user['joinDate'].strftime('%Y-%m-%d %H:%M:%S')

            if user['userRole'] == 'User':
                return redirect(url_for('index'))
            else:
                return redirect(url_for('adminDashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullName = request.form['fullName']
        email = request.form['email']
        password = request.form['password']  # This should be hashed before storing
        dob = request.form['dob']
        gender = request.form['gender']
        location = request.form['location']

        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            age = (datetime.now() - dob_date).days / 365.25
            if age < 18:
                return render_template('signup.html', error='You must be at least 18 years old to register.')
        except ValueError:
            return render_template('signup.html', error='Invalid date format. Please use YYYY-MM-DD.')

        # Check if the name is valid
        if not is_valid_name(fullName):
            return render_template('signup.html', error='Invalid name. Please enter a valid name.')

        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template('signup.html', error='Email already exists')

        cursor.execute("""
            INSERT INTO users (fullName, email, password, dob, gender, location, userRole)
            VALUES (%s, %s, %s, %s, %s, %s, 'User')
        """, (fullName, email, password, dob, gender, location))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/dashboard')
def adminDashboard():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Query to count total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Query to count total admins
    cursor.execute("SELECT COUNT(*) FROM users WHERE userRole='Admin'")
    total_admins = cursor.fetchone()[0]

    # Query to count total regular users
    cursor.execute("SELECT COUNT(*) FROM users WHERE userRole='User'")
    total_regular_users = cursor.fetchone()[0]

    # Query to count total predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    # Query to count total non-fraudulent predictions
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE isFraud=0")
    total_non_fraud = cursor.fetchone()[0]

    # Query to count total fraudulent predictions
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE isFraud=1")
    total_fraud = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template('adminDashboard.html', content='home', total_users=total_users,
                           total_admins=total_admins, total_regular_users=total_regular_users,
                           total_predictions=total_predictions, total_non_fraud=total_non_fraud,
                           total_fraud=total_fraud)

def is_valid_name(name):
    # Add your validation logic here, for example:
    # Name should contain only alphabets and spaces
    return bool(re.match("^[a-zA-Z ]+$", name))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def home():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Query to count total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Query to count total admins
    cursor.execute("SELECT COUNT(*) FROM users WHERE userRole='Admin'")
    total_admins = cursor.fetchone()[0]

    # Query to count total regular users
    cursor.execute("SELECT COUNT(*) FROM users WHERE userRole='User'")
    total_regular_users = cursor.fetchone()[0]

    # Query to count total predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    # Query to count total non-fraudulent predictions
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE isFraud=0")
    total_non_fraud = cursor.fetchone()[0]

    # Query to count total fraudulent predictions
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE isFraud=1")
    total_fraud = cursor.fetchone()[0]


    cursor.close()
    conn.close()


    return render_template('adminDashboard.html', content='home', total_users=total_users,
                           total_admins=total_admins, total_regular_users=total_regular_users,
                           total_predictions=total_predictions, total_non_fraud=total_non_fraud,
                           total_fraud=total_fraud)


@app.route('/users')
def users():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('adminDashboard.html', users=users, content='users')

@app.route('/users/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        fullName = request.form['fullName']
        email = request.form['email']
        password = request.form['password']
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hashing the password
        dob = request.form['dob']
        gender = request.form['gender']
        location = request.form['location']
        userRole = request.form['userRole']

        try:
            conn = mysql.connector.connect(**mysql_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (fullName, email, password, dob, gender, location, userRole)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (fullName, email, password, dob, gender, location, userRole))
            conn.commit()
        except mysql.connector.Error as err:
            flash('Failed to add user: {}'.format(err), 'error')
            return redirect(url_for('users'))  # Redirecting back to users page with error
        finally:
            cursor.close()
            conn.close()

        flash('User successfully added', 'success')
        return redirect(url_for('users'))

@app.route('/users/update/<int:id>', methods=['POST'])
def update_user(id):
    fullName = request.form['fullName']
    email = request.form['email']
    password = request.form['password']  # Make sure to hash passwords in production!
    dob = request.form['dob']
    gender = request.form['gender']
    location = request.form['location']
    userRole = request.form['userRole']  # Ensuring the name matches the HTML form field

    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Corrected SQL query
    cursor.execute("""
        UPDATE users SET fullName=%s, email=%s, password=%s, dob=%s, gender=%s, location=%s, userRole=%s WHERE id=%s
    """, (fullName, email, password, dob, gender, location, userRole, id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('User successfully updated')
    return redirect(url_for('users'))


@app.route('/users/delete/<int:id>', methods=['GET'])
def delete_user(id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('User successfully deleted')
    return redirect(url_for('users'))

@app.route('/transactions')
def predictions():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM predictions")
    transaction = cursor.fetchall()

    # Reverse mapping from string to numeric values
    transaction_types_reverse = {
        "Cash In": 0,
        "Cash Out": 1,
        "Debit": 2,
        "Payment": 3,
        "Transfer": 4
    }

    cursor.close()
    conn.close()
    return render_template('adminDashboard.html', transaction=transaction, content='transactions',
                           transaction_types_reverse=transaction_types_reverse)

@app.route('/transactions/update/<int:id>', methods=['POST'])
def update_transactions(id):
    data = request.form.to_dict()

    transaction_types = {0: "Cash In", 1: "Cash Out", 2: "Debit", 3: "Payment", 4: "Transfer"}

    type_numeric = float(data.get('type', 0))
    transaction_type = transaction_types.get(int(type_numeric), "Unknown")

    input_data = [
        type_numeric,
        float(data.get('amount', 0)),
        float(data.get('oldbalanceOrg', 0)),
        float(data.get('newbalanceOrig', 0)),
        float(data.get('oldbalanceDest', 0)),
        float(data.get('newbalanceDest', 0))
    ]

    try:
        prediction = model.predict([input_data])[0]
        prediction = int(prediction)

        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE predictions 
            SET type=%s, amount=%s, oldbalanceOrg=%s, newbalanceOrig=%s, oldbalanceDest=%s, newbalanceDest=%s, isFraud=%s 
            WHERE id=%s
        """, (transaction_type, data['amount'], data['oldbalanceOrg'], data['newbalanceOrig'],
              data['oldbalanceDest'], data['newbalanceDest'], prediction, id))
        conn.commit()

        return jsonify({'prediction': prediction})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/transactions/add', methods=['POST'])
def add_transaction():
    if 'id' not in session:
        return jsonify({'error': 'User not logged in'}), 403

    data = request.form.to_dict()
    transaction_types = {0: "Cash In", 1: "Cash Out", 2: "Debit", 3: "Payment", 4: "Transfer"}
    transaction_type = transaction_types.get(int(data.get('type', 0)), "Unknown")

    input_data = [
        float(data.get('type', 0)),
        float(data.get('amount', 0)),
        float(data.get('oldbalanceOrg', 0)),
        float(data.get('newbalanceOrig', 0)),
        float(data.get('oldbalanceDest', 0)),
        float(data.get('newbalanceDest', 0))
    ]

    prediction = model.predict([input_data])[0]
    prediction = int(prediction)

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

@app.route('/transactions/delete/<int:id>', methods=['GET'])
def delete_transaction(id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'delteUser': "delete"})



@app.route('/reports')
def reports():
    is_fraud = request.args.get('isFraud', default=None, type=int)

    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)

    if is_fraud is not None:
        query = """
        SELECT users.fullName as 'Customer Name', TIMESTAMPDIFF(YEAR, users.dob, CURDATE()) AS Age, users.gender, users.location, predictions.*
        FROM users
        JOIN predictions ON predictions.userId = users.id
        WHERE predictions.isFraud = %s
        """
        cursor.execute(query, (is_fraud,))
    else:
        query = """
        SELECT users.fullName as 'Customer Name', TIMESTAMPDIFF(YEAR, users.dob, CURDATE()) AS Age, users.gender, users.location, predictions.*
        FROM users
        JOIN predictions ON predictions.userId = users.id
        """
        cursor.execute(query)

    report_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('adminDashboard.html', report_data=report_data, content="reports")



@app.route('/predict', methods=['POST'])
def predict():
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
    """, (session['id'], transaction_type, data['amount'], data['oldbalanceOrg'], data['newbalanceOrig'], data['oldbalanceDest'], data['newbalanceDest'], prediction))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True, port=2024)
