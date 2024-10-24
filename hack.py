from flask import Flask, request, render_template, redirect, url_for, session
from collections import defaultdict
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key in production

# User data for authentication (username:password)
USER_DATA = {'admin': 'password123'}  # Replace with a more secure method in production

# Tracking failed attempts
failed_attempts = defaultdict(list)
TIME_WINDOW = 300  # 5 minutes
THRESHOLD = 5  # Number of failed attempts to trigger an action


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    ip_address = request.remote_addr  # Get the client's IP address

    # Check if the username and password are correct
    if username in USER_DATA and USER_DATA[username] == password:
        session['username'] = username
        return redirect(url_for('welcome'))
    else:
        # Log failed attempt
        log_failed_attempt(ip_address, username)
        return "Login Failed! Please try again."


@app.route('/welcome')
def welcome():
    return f"Welcome, {session['username']}!"


def log_failed_attempt(ip_address, username):
    current_time = time.time()
    failed_attempts[ip_address].append((username, current_time))

    # Remove attempts older than the time window
    failed_attempts[ip_address] = [
        (user, t) for user, t in failed_attempts[ip_address]
        if current_time - t <= TIME_WINDOW
    ]

    # Check if threshold is exceeded
    if len(failed_attempts[ip_address]) > THRESHOLD:
        print(f"Brute force attack detected from IP: {ip_address}")
        # Here you could implement an action like blocking the IP or notifying an admin


if __name__ == "__main__":
    app.run(debug=True)
