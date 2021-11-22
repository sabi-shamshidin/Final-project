from datetime import datetime, timedelta
from functools import wraps
from flask import Flask
from flask.helpers import make_response
from flask import request
from flask import render_template
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from transformers import *
from requests import Session
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyforappconfig'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:0000@localhost/python"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), unique=True, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id


class currency_infoo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    sum = db.Column(db.String(), nullable=False)

    def __init__(self, *args, **kwargs):
        super(currency_infoo, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Currency id: {}\nTitle: {}\nDescription: {}>'.format(self.id, self.title, self.description)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Hello, Could not verify the token'}), 403
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def login_form():
    return render_template('login.html')


@app.route('/', methods=['POST'])
def login():
    username = request.form['u']
    password = request.form['p']
    users = Users.query.filter_by(login=username).first()

    if users.password == password and users.login == username:
        token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                            app.config['SECRET_KEY'])
        admin = Users.query.filter_by(login=username).first()
        admin.token = token
        db.session.commit()
        return render_template('searchbar.html')
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Hello, token which is provided is correct'})


class WebScrapper:
    def search_news(self, query):
        summarizer = pipeline("summarization")
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        files = {'name': query}
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '14de27c1-787d-419a-888e-b4677b7e7a45',
        }
        session = Session()
        session.headers.update(headers)

        response = session.get(url, files=files)
        coin = response.json()
        inside = coin['data']
        data = inside[0]

        for i in range(len(data)):
            data = inside[i]
            id = data['id']
            name = data['name']
            if name.lower() == query.lower():
                break

        url = 'https://api.coinmarketcap.com/content/v3/news?coins=' + str(id) + '&page=1&size=5'
        response = session.get(url)
        news = response.json()
        inside = news['data']
        be = inside[1]
        tut = be['meta']

        for i in range(len(be)):
            be = inside[i]
            tut = be['meta']
            title = tut['title']
            subtitle = tut['subtitle']
            summa = summarizer(subtitle, max_length=100, min_length=15, do_sample=False)
            newVar = summa[0]
            c_i = currency_infoo(id=i + 1, title=title, description=subtitle, sum=newVar['summary_text'])
            db.session.add(c_i)
            db.session.commit()

        coins = currency_infoo.query.all()
        return coins


@app.route('/search', methods=['GET', 'POST'])
def search():
    q = request.form['q']
    newWebScrapper = WebScrapper()
    if q:
        newWebScrapper.search_news(q)
        coins = currency_infoo.query.all()
        return render_template("output.html", coins=coins)
    else:
        return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
