from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Your name",
        validators=[DataRequired(message="Please enter your name."),
                    Length(min=2, max=80, message="Name must be 2–80 characters.")],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter your email."),
                    Email(message="Please enter a valid email address.")],
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(message="Please enter a message."),
                    Length(min=10, max=4000, message="Message must be 10–4000 characters.")],
    )
    hp_field = HiddenField()  # honeypot

    @property
    def is_honeypot_filled(self) -> bool:
        return bool(self.hp_field.data and self.hp_field.data.strip())
