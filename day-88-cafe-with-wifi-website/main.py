import os
from dotenv import load_dotenv
import logging
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

# Ensure the instance directory exists
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))

# Check if the database file exists before creating it
if not os.path.exists('instance/cafes.db'):
    with app.app_context():
        db.create_all()

class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = SelectField("Has Sockets", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    has_toilet = SelectField("Has Toilet", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    has_wifi = SelectField("Has Wifi", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    can_take_calls = SelectField("Can Take Calls", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    seats = StringField("Seats")
    coffee_price = StringField("Coffee Price")
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        try:
            new_cafe = Cafe(
                name=form.cafe.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                has_sockets=form.has_sockets.data == "True",
                has_toilet=form.has_toilet.data == "True",
                has_wifi=form.has_wifi.data == "True",
                can_take_calls=form.can_take_calls.data == "True",
                seats=form.seats.data,
                coffee_price=form.coffee_price.data
            )
            db.session.add(new_cafe)
            db.session.commit()
            logger.info(f"Added new cafe: {new_cafe.name}")
            return redirect(url_for('cafes'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding cafe: {e}")
            return f"An error occurred while adding the cafe: {e}", 500
    return render_template('add.html', form=form, method='PUT')

@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    try:
        cafe_to_delete = Cafe.query.get(cafe_id)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            logger.info(f"Deleted cafe: {cafe_to_delete.name}")
            return redirect(url_for('cafes'))
        else:
            logger.warning(f"Cafe with id {cafe_id} not found")
            return f"Cafe with id {cafe_id} not found", 404
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting cafe: {e}")
        return f"An error occurred while deleting the cafe: {e}", 500

@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    return render_template('cafes.html', cafes=all_cafes)

if __name__ == '__main__':
    app.run(debug=True)
