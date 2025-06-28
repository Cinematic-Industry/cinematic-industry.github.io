from flask import Flask, render_template, request, session
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os, random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_key")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['name'] = name
    session['email'] = email
    session['message'] = message

    msg = Message('Your OTP Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Hello {name},\n\nYour OTP is: {otp}\n\nThank you!"
    mail.send(msg)

    return render_template('otp.html')

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']
    if user_otp == session.get('otp'):
        return f"✅ Verified!<br><br><b>Name:</b> {session.get('name')}<br><b>Email:</b> {session.get('email')}<br><b>Message:</b> {session.get('message')}"
    else:
        return "❌ Invalid OTP. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
