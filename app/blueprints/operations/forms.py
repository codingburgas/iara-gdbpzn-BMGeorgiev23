from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Заглавие на задача', validators=[DataRequired()])
    description = TextAreaField('Описание')
    priority = SelectField('Приоритет', choices=[
        ('critical', 'Критичен'),
        ('high', 'Висок'),
        ('medium', 'Среден'),
        ('low', 'Нисък')
    ])
    assigned_to = SelectField('Назначен на', choices=[], coerce=int)
    submit = SubmitField('Създай задача')