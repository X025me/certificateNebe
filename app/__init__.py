from enum import unique
import os
import datetime

from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from flask_migrate import Migrate
import flask 




location = (490, 430)

location_date = (300, 725)
data_encoder_date=(300, 670)
pole_woker_data=[300, 690]
text_color = (0, 0, 0)
font = ImageFont.truetype("Tera-Regular.ttf", 30)
font_english = ImageFont.truetype("SourceSansPro-Regular.otf", 30)


connection_url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="9Sn#9H{#",
    host="0.0.0.0",
    port=1433,
    database="POLE",
    
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        # "authentication": "ActiveDirectoryIntegrated",
    },
)

# create and configure the app

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',

)

app.config['SQLALCHEMY_DATABASE_URI'] = connection_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['MYSQL_CHARSET'] = 'utf16'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Workers(db.Model):
    bank_account = db.Column(db.String(200), primary_key=True)
    region = db.Column(db.Unicode((200), collation='utf16'), unique=False, nullable=False)
    full_name = db.Column(
        db.Unicode((200), collation='utf16'), unique=False, nullable=False)
    full_name_update = db.Column(
        db.Unicode((200), collation='utf16'), unique=False, nullable=True)
    zone = db.Column(db.Unicode((200), collation='utf16'), unique=False, nullable=True)
    constituency = db.Column(
        db.Unicode((200), collation='utf16'), unique=False, nullable=True)
    position = db.Column(db.Unicode((200), collation='utf16'), unique=False, nullable=True)
    position_update = db.Column(db.Unicode((200), collation='utf16'), unique=False, nullable=True)
    approved = db.Column(db.String(20), unique=False, nullable=True)
    edited = db.Column(db.Boolean, nullable=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(200), nullable=True)
    request_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    account_number = db.Column(db.String(200), nullable=True)



@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        form = request.form
        data = Workers.query.get(form['account'])
        if not data:
            return render_template('/certificate.html', data="")
        if data.edited == True:
            return render_template('/cancle.html')
        session['account'] = form['account']
        datas = {'region': data.region, 'zone': data.zone, 'constituency': data.constituency,
                'full_name': data.full_name, 'position': data.position, 'cert': 'officer.jpeg'}
        # print('data is', data)
        # df = pd.read_excel("pole.xlsx")
        # x = df.loc[df['የባንክ አካውንት ቁጥር'] == int(form['account'])]
        # if not x['ምርጫ ክልል ሰራተኛ ስም'].values.any():
        #     return render_template('/certificate.html', data="")
        # session['account'] = int(form['account'])
        # data = {'region': x["ክልል"].values[0], 'zone': x['ዞን'].values[0],
        #         'full_name': x['ምርጫ ክልል ሰራተኛ ስም'].values[0], 'position': x['ሃላፊነት '].values[0], 'cert': 'officer.jpeg'}
        return render_template("/index.html", data=datas)

    return render_template("/index.html")

@app.route('/import', methods=['GET', 'POST'])
def imports():
    data = pd.read_excel ('pole.xlsx') 
    data = data.rename(columns={'ተ/ቁ': 'index', 'ክልል':'region', 'ዞን': 'zone', 'ምርጫ ክልል': 'constituency', 'ምርጫ ክልል ሰራተኛ ስም': 'full_name', 'የባንክ አካውንት ቁጥር': 'account', 'ሃላፊነት ': 'position' })
    for item in data.itertuples():
        accounts = str(item.account)
        accounts = accounts.replace('.0', '')            
        h = Workers(bank_account=accounts, region=item.region, full_name=item.full_name, zone=item.zone, constituency=item.constituency, position=item.position)            
        db.session.add(h)
        db.session.commit()

    
    

    return ('Done')

@app.route('/confirm',  methods=['GET', 'POST'])
def confirm():
    from datetime import date
    dater = date.today()
    today = dater.strftime("%d/%m/%Y")
    # print(session['account'])
    dates = session["account"]
    datas = Workers.query.get(dates)
    ip_address = flask.request.remote_addr


    log = Log(ip=str(ip_address),account_number=dates)
    db.session.add(log)
    db.session.commit()
    if (datas.position == 'ምርጫ ክልል ሰራተኛ '):
        im = Image.open("officer.jpeg")
        d = ImageDraw.Draw(im)
        print(datas.full_name)
        d.text(location,  datas.full_name,
               fill=text_color, font=font)

        d.text(location_date, today, fill=text_color, font=font)
        im.save("app/static/certificate_" + str(dates) + ".pdf")
        return render_template("/certificate.html", data="certificate_"+str(dates)+".pdf")
    elif (datas.position == 'የውሂብ መቀየሪያ'):
        im = Image.open("de.jpeg")
        d = ImageDraw.Draw(im)
        print(datas.full_name)
        d.text(location,  datas.full_name,
               fill=text_color, font=font)

        d.text(data_encoder_date, today, fill=text_color, font=font)
        im.save("app/static/certificate_" + str(dates) + ".pdf")
        return render_template("/certificate.html", data="certificate_"+str(dates)+".pdf")

    elif (datas.position == 'የዞኑ ምክትል አስተባባሪ'):
        im = Image.open("dzc.jpeg")
        d = ImageDraw.Draw(im)
        print(datas.full_name)
        d.text(location,  datas.full_name,
               fill=text_color, font=font)

        d.text(location_date,today, fill=text_color, font=font)
        im.save("app/static/certificate_" + str(dates) + ".pdf")
        return render_template("/certificate.html", data="certificate_"+str(dates)+".pdf")
    
    elif (datas.position == 'የአይሲቲ ቡድን መሪ'):
        im = Image.open("ict.jpeg")
        d = ImageDraw.Draw(im)
        d.text(location,  datas.full_name,
               fill=text_color, font=font)

        d.text(location_date, today, fill=text_color, font=font)
        im.save("app/static/certificate_" + str(dates) + ".pdf")
        return render_template("/certificate.html", data="certificate_"+str(dates)+".pdf")

    elif (datas.position == 'የምርጫ ሰራተኛ'):
        im = Image.open("pw.jpeg")
        d = ImageDraw.Draw(im)
        d.text(location,  datas.full_name,
               fill=text_color, font=font)

        d.text(pole_woker_data, today, fill=text_color, font=font)
        im.save("app/static/certificate_" + str(dates) + ".pdf")
        return render_template("/certificate.html", data="certificate_"+str(dates)+".pdf")


    # df = pd.read_excel("pole.xlsx") 
    # x = df.loc[df['የባንክ አካውንት ቁጥር'] == date]
    # print(x['ሃላፊነት '].values[0])
    # if (x['ሃላፊነት '].values[0] == "ምርጫ ክልል ሰራተኛ "):
    #     im = Image.open("officer.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location,  x['ምርጫ ክልል ሰራተኛ ስም'].values[0],
    #            fill=text_color, font=font)

    #     d.text(location_date, '18-04-2022', fill=text_color, font=font)
    #     im.save("app/static/certificate_" + str(date) + ".pdf")
    #     return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")
    # elif (x['ሃላፊነት '] == "ምክትል ዞን አስተባባሪ "):
    #     im = Image.open("dzc.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")

    # elif (x['ሃላፊነት '] == 'dzt '):
    #     im = Image.open("dzt.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")

    # elif (x['ሃላፊነት '] == 'ict'):
    #     im = Image.open("ict.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")

    # elif (x['ሃላፊነት '] == 'mts'):
    #     im = Image.open("mts.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")

    # elif (x['ሃላፊነት '].values[0] == 'pw'):
    #     im = Image.open("pw.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location,  x['ምርጫ ክልል ሰራተኛ ስም'].values[0], fill=text_color, font=font)
    #     d.text(location_date, '18-04-2022', fill=text_color, font=font)
    #     im.save("app/static/certificate_" + str(date) + ".pdf")
    #     return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")

    else:
        pass
    return render_template('/certificate.html', date=date)

@app.route('/update',  methods=['GET', 'POST'])
def update():
    account = session['account']
    print(account)
    if request.method == 'POST':
        worker = Workers.query.get(account)
        print(worker)
        form = request.form
        worker.full_name_update = form['name']
        worker.position_update = form['position']
        worker.edited = True
        db.session.commit()
        return render_template('/cancle.html')
    return render_template('/update.html')



@app.route('/cancle',  methods=['GET', 'POST'])
def cancle():
    return render_template('/cancle.html')


if __name__ == '__main__':
    app.run()
