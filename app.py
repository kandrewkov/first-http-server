from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Player_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_number = db.Column(db.String(4))
    chanel_id = db.Column(db.String(2))
    group_number = db.Column(db.String(2))
    time_hour = db.Column(db.String(2))
    time_minute = db.Column(db.String(2))
    time_sec = db.Column(db.String(2))
    time_part_sec = db.Column(db.String(3))

    def __repr__(self):
        return '<Player_info %r>' % self.id

    def separation(self, a):
        self.player_number = a.split(' ')[0]
        self.chanel_id = a.split(' ')[1]
        time = a.split(' ')[2]
        self.group_number = a.split(' ')[3]
        self.time_hour = time.split(':')[0]
        self.time_minute = time.split(':')[1]
        self.time_sec = time.split(':')[2]
        self.time_part_sec = self.time_sec.split('.')[1][0]
        self.time_sec = self.time_sec.split('.')[0]


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/add', methods=['POST', 'GET'])
def add():

    if request.method == "POST":
        data = request.form['data']

        player_info = Player_info()
        player_info.separation(data)
        f = open("all.txt", "w")
        f.write(data)


        try:
            db.session.add(player_info)
            db.session.commit()
            return redirect("/results")
        except:
            return redirect("/results")

    else:
        return render_template("add.html")


@app.route('/results', methods=['POST', 'GET'])
def results():
    info = Player_info.query.order_by(Player_info.group_number).all()
    info1 = list(filter(lambda x: x.group_number == '00', info))
    return render_template("results.html", results=info1)


if __name__ == "__main__":
    app.run(debug=True)
