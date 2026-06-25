# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
 # Imports Flask and related modules for web application development
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'your secret key'

 # This code initializes the Flask application and sets a secret key for session management

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'H@r1teja'
app.config['MYSQL_DB'] = 'moneymate'

mysql = MySQL(app)

# This code defines the login route to handle user login functionality

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM students WHERE username = % s \
                        AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['student_id'] = account['student_id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', account=account)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

# Render the login page with the message

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('student_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'school' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'country' in request.form and 'postalcode' in request.form:
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        school = request.form['school']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM students WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO students VALUES \
                        (NULL, % s, % s, % s,% s, % s, % s, % s, % s, % s, % s, % s)',
                           (username, password, firstname, lastname, email,
                            school, address, city,
                            state, country, postalcode, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/income', methods=['GET', 'POST'])
def income():
    msg = ''
    if request.method == 'POST' and 'transaction_detail' in request.form and 'transaction_amount' in request.form and 'transaction_date' in request.form:
        student_id = session['student_id']
        transaction_category = "Income"
        transaction_type = request.form['transaction_type']
        transaction_detail = request.form['transaction_detail']
        transaction_amount = request.form['transaction_amount']
        transaction_date = request.form['transaction_date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'[0-9]+', transaction_amount):
            msg = 'transaction amount must be an amount !'
        elif not re.match(r'[0-9]+', transaction_date):
            msg = 'transaction date must be a date !'
        else:
            cursor.execute('INSERT INTO transactions VALUES \
            (NULL,%s,%s,%s, % s, % s,% s)',
                           (student_id, transaction_category, transaction_type, transaction_detail, transaction_amount, transaction_date, ))
            mysql.connection.commit()
            msg = 'You have successfully submitted Income !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('income.html', msg=msg)

#This is a function that is connected to the expenses.html file, it is written in the .py folder
# Complex and simple variables were used
#MySQL Code was used too; to connect with the table "Insert into transactions"

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    msg = ''
    if request.method == 'POST' and 'transaction_detail' in request.form and 'transaction_amount' in request.form and 'transaction_date' in request.form:
        student_id = session['student_id']
        transaction_category = "Expenses"
        transaction_type = request.form['transaction_type']
        transaction_detail = request.form['transaction_detail']
        transaction_amount = request.form['transaction_amount']
        transaction_date = request.form['transaction_date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'[0-9]+', transaction_amount):
            msg = 'transaction amount must be an amount !'
        elif not re.match(r'[0-9]+', transaction_date):
            msg = 'transaction date must be a date !'
        else:
            cursor.execute('INSERT INTO transactions VALUES \
            (NULL,%s,%s,%s, % s, % s,% s)',
                           (student_id, transaction_category, transaction_type, transaction_detail, transaction_amount, transaction_date, ))
            mysql.connection.commit()
            msg = 'You have successfully submitted expenses !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('expenses.html', msg=msg)


@app.route("/home")
def home():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE student_id = % s',
                       (session['student_id'], ))
        account = cursor.fetchone()
        return render_template("home.html", account=account)
    return redirect(url_for('login'))

# This code is a transactions "function" that is coded in the main .py file
# which is later used in the transaction.html file
@app.route("/transactions")
def transactions():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM transactions WHERE student_id = % s',
                       (session['student_id'], ))
        rows = cursor.fetchall()
        return render_template("transactions.html", rows=rows)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'school' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            school = request.form['school']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM students WHERE username = % s',
                (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE students SET username =% s,\
                                password =% s, email =% s, school =% s, \
                                address =% s, city =% s, state =% s, \
                                country =% s, postalcode =% s WHERE student_id =% s', (
                    username, password, email, school,
                    address, city, state, country, postalcode,
                    (session['student_id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


@app.route("/summary")
def summary():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select sum(total_income) as total_income, sum(total_expenses) as total_expenses, sum(total_income)-sum(total_expenses) as account_balance from (select sum(transaction_amount) as total_income, 0 as total_expenses from transactions where transaction_category=\'Income\' and student_id = % s union select 0 as total_income, sum(transaction_amount) total_expenses from transactions where transaction_category=\'Expenses\'  and student_id = % s )a ',
                       (session['student_id'], session['student_id'], ))
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM transactions WHERE student_id = % s',	(session['student_id'], ))
        transactions = cursor.fetchall()
        # Calculate total income and expense
        total_income = sum(t["transaction_amount"] for t in transactions if t["transaction_category"] == "Income")
        total_expense = sum(t["transaction_amount"] for t in transactions if t["transaction_category"] == "Expenses")
        balance = total_income - total_expense
        # Calculate spending percentage by type
        expense_by_type = {}
        for t in transactions:
            if t["transaction_category"] == "Expenses":
                expense_by_type[t["transaction_type"]] = expense_by_type.get(t["transaction_type"], 0) + t["transaction_amount"]

        total_spending = sum(expense_by_type.values())
        type_percentages = {type: (amount / total_spending) * 100 for type, amount in expense_by_type.items()}
        return render_template("summary.html", account=account,balance=balance,
        total_income=total_income,
        total_expense=total_expense,
        category_percentages=type_percentages,
        expense_by_category=expense_by_type)
    return redirect(url_for('login'))

@app.route("/edit_transaction/<int:transaction_id>", methods=["POST"])
def edit_transaction(transaction_id):
    if 'loggedin' in session:
        transaction_category = request.form['transaction_category']
        transaction_type = request.form['transaction_type']
        transaction_detail = request.form['transaction_detail']
        transaction_amount = request.form['transaction_amount']
        transaction_date = request.form['transaction_date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            UPDATE transactions
            SET transaction_category = %s, transaction_type = %s, transaction_detail = %s, transaction_amount = %s, transaction_date = %s
            WHERE transaction_id = %s AND student_id = %s
        """, (transaction_category, transaction_type, transaction_detail, transaction_amount, transaction_date, transaction_id, session['student_id']))
        
        mysql.connection.commit()
        return redirect(url_for('transactions'))
    return redirect(url_for('login'))

@app.route("/delete_transaction/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            DELETE FROM transactions
            WHERE transaction_id = %s AND student_id = %s
        """, (transaction_id, session['student_id']))
        
        mysql.connection.commit()
        return redirect(url_for('transactions'))
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
