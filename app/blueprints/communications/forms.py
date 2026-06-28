from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class MessageForm(FlaskForm):
    content = TextAreaField('Съобщение', validators=[DataRequired()])
    incident_id = SelectField('Произшествие', coerce=int)
    submit = SubmitField('Изпрати')

class TemplateForm(FlaskForm):
    name = StringField('Име на шаблон', validators=[DataRequired()])
    content = TextAreaField('Съдържание', validators=[DataRequired()])
    submit = SubmitField('Запази шаблон')

class NotificationForm(FlaskForm):
    title = StringField('Заглавие', validators=[DataRequired()])
    message = TextAreaField('Съобщение', validators=[DataRequired()])
    type = SelectField('Тип', choices=[
        ('info', 'Информация'),
        ('warning', 'Предупреждение'),
        ('success', 'Успех'),
        ('danger', 'Спешно')
    ])
    user_id = SelectField('Потребител', coerce=int)
    submit = SubmitField('Изпрати')