from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField

class DashboardFilterForm(FlaskForm):
    date_range = SelectField('Период', choices=[('today', 'Днес'), ('week', 'Седмица'), ('month', 'Месец')])
    submit = SubmitField('Приложи')