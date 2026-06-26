from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional

class IncidentForm(FlaskForm):
    title = StringField('Заглавие', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    type = SelectField('Тип', choices=[('fire', 'Пожар'), ('rescue', 'Спасителна'), ('other', 'Друго')])
    address = StringField('Адрес', validators=[DataRequired()])
    latitude = FloatField('Географска ширина', validators=[Optional()])
    longitude = FloatField('Географска дължина', validators=[Optional()])
    submit = SubmitField('Запази')
