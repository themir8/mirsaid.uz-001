from flask import Flask, render_template, redirect, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging
import time
import telebot


API_TOKEN = '1274554591:AAHDdFclafV1eYi-cLKgOGGvX006g3Ezrj4'

bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SDBUYCFSUIBFVCIYSBECIEVSCDSV'
app.config['SERVER_NAME']='mirsaid.uz'
app.url_map.default_subdomain = "www"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Article {self.id}>'
        

#----------------------------------------------------------------------------
@app.route('/', methods=["POST", "GET"])
@app.route('/home/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form['username']
        tel = request.form['tel']
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        msg = MIMEMultipart()
        message = f"Username: {username}\nTel: {tel}\nIp address: {ip}"
        password = "mlrs@ld08"
        msg['From'] = "oliver.jones.bafer@gmail.com"
        msg['To'] = "mirzohidovm8@gmail.com"
        msg['Subject'] = "Diqqat! Yangi zakazchi!"

        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

        user = Contact(username=username, tel=tel, ip=ip)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
       
        except Exception as e:
            return "error error error \n"+e
    return render_template("index.html")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/web")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://mirsaid.uz/' + API_TOKEN)
    return "!", 200

@app.route('/', subdomain ='creator')
def practice(): 
    return "Coding Practice Page"


if __name__=='__main__':
    app.run(host="0.0.0.0")
