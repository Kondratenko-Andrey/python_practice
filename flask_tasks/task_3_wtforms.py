from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    # Необходимо установить специальный сторонний пакет под
    # названием email_validator можно с помощью команды:
    # (venv) $ pip install email_validator
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), NumberRange(min=1_000_000_000, max=9_999_999_999)])
    name = StringField(validators=[InputRequired])
    address = StringField(validators=[InputRequired])
    index = IntegerField()
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
