import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
# from flaskr.db import get_db
# import json

location = (490, 430)
text_color = (0, 0, 0)
font = ImageFont.truetype("Tera-Regular.ttf", 30)

bp = Blueprint('', __name__, url_prefix='')


@bp.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        form = request.form
        df = pd.read_excel("Polle1.xlsx")
        x = df.loc[df['የባንክ አካውንት ቁጥር'] == int(form['account'])]

        if not x['ምርጫ ክልል ሰራተኛ ስም'].values.any():
            return render_template('/certificate.html', data="")
        session['account'] = int(form['account'])
        data = {'region': x["ክልል"].values[0], 'zone': x['ዞን'].values[0],
                'full_name': x['ምርጫ ክልል ሰራተኛ ስም'].values[0], 'position': x['ሃላፊነት '].values[0], 'cert': 'officer.jpeg'}
        return render_template("/index.html", data=data)

    return render_template("/index.html")


@bp.route('/confirm',  methods=['GET', 'POST'])
def confirm():
    date = session.get("account")
    df = pd.read_excel("Polle1.xlsx")
    x = df.loc[df['የባንክ አካውንት ቁጥር'] == date]
    # print(x['ሃላፊነት '].values[0])
    if (x['ሃላፊነት '].values[0] == "ምርጫ ክልል ሰራተኛ "):
        im = Image.open("officer.jpeg")
        d = ImageDraw.Draw(im)
        d.text(location,  x['ምርጫ ክልል ሰራተኛ ስም'].values[0],
               fill=text_color, font=font)
        im.save("app/static/certificate_" + str(date) + ".pdf")
        return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")
    elif (x['ሃላፊነት '] == "ምክትል ዞን አስተባባሪ"):
        im = Image.open("dzc.jpeg")
        d = ImageDraw.Draw(im)
        d.text(location, date, fill=text_color, font=font)
        return render_template("/certificate.html", data="certificate_"+str(date)+".pdf")

    # elif (x[''] == ''):
    #     im = Image.open("dzt.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     pass
    # elif (x[''] == ''):
    #     im = Image.open("ict.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     pass
    # elif (x[''] == ''):
    #     im = Image.open("mts.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     pass
    # elif (x[''] == ''):
    #     im = Image.open("pw.jpeg")
    #     d = ImageDraw.Draw(im)
    #     d.text(location, date, fill=text_color, font=font)
    #     pass
    else:
        pass
    return render_template('/certificate.html', date=date)


@bp.route('/cancle',  methods=['GET', 'POST'])
def cancle():
    return render_template('/cancle.html')
