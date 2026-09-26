from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(message="Ingrese su usuario.")])
    password = PasswordField("Contraseña", validators=[DataRequired(message="Ingrese su contraseña.")])
    captcha = IntegerField(
        "Verificación",
        validators=[DataRequired(message="Resuelva la operación para continuar.")]
    )
    submit = SubmitField("Iniciar Sesión")