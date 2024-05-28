from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data for authentication
users = {
    'ayush_pundhir': generate_password_hash('password123')
}

class BankAccount:
    def __init__(self, account_number, account_holder):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        return self.balance

# Create a global account for simplicity
account = BankAccount("123456789", "Ayush Pundhir")

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', account=account)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['amount'])
        if account.deposit(amount):
            return redirect(url_for('index'))
        else:
            flash('Invalid deposit amount')
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['amount'])
        if account.withdraw(amount):
            return redirect(url_for('index'))
        else:
            flash('Invalid withdrawal amount or insufficient funds')
    return render_template('withdraw.html')

@app.route('/balance')
def balance():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('balance.html', balance=account.check_balance())

if __name__ == '__main__':
    app.run(debug=True)
