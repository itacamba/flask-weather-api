import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# city Model
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city')
        if city_name:
            new_city = City(name=city_name)
            db.session.add(new_city)
            db.session.commit()
    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=05bf1db93d294f543bed979244a2f527'
    data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()
        print(r)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        data.append(weather)
        print(weather)

    print(data)

    return render_template('weather.html', data=data)

@app.route('/delete/<name>', methods=['POST'])
def delete_city(name):
    city = City.query.filter_by(name=name).one()
    db.session.delete(city)
    db.session.commit()

    # redirect and url_for work together, url_for takes in as an argument a method
    return redirect(url_for('index'))