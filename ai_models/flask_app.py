from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from functools import wraps
import logging
import sys

# Placeholder imports for Scapy, which will be used if installed
try:
    from scapy.all import sniff
except ImportError:
    sniff = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Should be replaced with a real secret key

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Form class for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

# User authentication dictionary for demo purposes
# In a real application, use a proper database
users = {'admin': 'password'}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == users.get(form.username.data) and form.password.data == 'password':
            session['logged_in'] = True
            flash('You were successfully logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were successfully logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # This will be the dashboard displaying real-time data
    # For now, it's just a placeholder
    return render_template('dashboard.html')

# Real-time data capture function using Scapy
def real_time_capture(interface='eth0', count=0, timeout=None):
    if sniff is None:
        logging.error('Scapy is not installed. Real-time capture is not available.')
        sys.exit(1)
    logging.info(f'Starting real-time packet capture on interface {interface}.')
    # In an actual application, this function would capture packets and process them.
    # For now, it's just a placeholder using sniff from Scapy.
    sniff(iface=interface, count=count, timeout=timeout, prn=lambda x: x.show())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
