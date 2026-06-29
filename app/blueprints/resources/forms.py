from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ResourceForm(FlaskForm):
    name = StringField('Име', validators=[DataRequired()])
    description = TextAreaField('Описание')
    category = SelectField('Категория', choices=[
        ('vehicle', 'Превозно средство'),
        ('equipment', 'Оборудване'),
        ('water', 'Вода'),
        ('fuel', 'Гориво'),
        ('other', 'Друго')
    ])
    quantity = IntegerField('Количество', validators=[NumberRange(min=0)], default=0)
    unit = StringField('Мерна единица', default='бр.')
    status = SelectField('Статус', choices=[
        ('available', 'Наличен'),
        ('in_use', 'В употреба'),
        ('low', 'Ограничен'),
        ('depleted', 'Изчерпан')
    ])
    location = StringField('Местоположение')
    submit = SubmitField('Запази')

class ResourceRequestForm(FlaskForm):
    resource_id = SelectField('Ресурс', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    incident_id = SelectField('Произшествие', coerce=int)
    team_id = SelectField('Екип', coerce=int)
    submit = SubmitField('Заяви')