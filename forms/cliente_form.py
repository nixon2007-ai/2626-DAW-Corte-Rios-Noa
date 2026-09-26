from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class ClienteForm(FlaskForm):
    nombre = StringField(
        "Nombre completo",
        validators=[DataRequired(message="El nombre es obligatorio."),
                    Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres.")]
    )
    cedula = StringField(
        "Cédula",
        validators=[DataRequired(message="La cédula es obligatoria."),
                    Length(min=10, max=10, message="Debe tener 10 dígitos.")]
    )
    correo = StringField(
        "Correo electrónico",
        validators=[DataRequired(message="El correo es obligatorio."),
                    Email(message="Ingrese un correo válido.")]
    )
    telefono = StringField(
        "Teléfono",
        validators=[DataRequired(message="El teléfono es obligatorio."),
                    Length(min=10, max=10, message="Debe tener 10 dígitos.")]
    )
    tipo = SelectField(
        "Tipo de cliente",
        choices=[("Nuevo", "Nuevo"), ("Frecuente", "Frecuente")],
        validators=[DataRequired()]
    )
    mesa_preferida = SelectField(
        "Mesa preferida",
        choices=[("Barra", "Barra"), ("Salon Interior", "Salon Interior"), ("Terraza", "Terraza")],
        validators=[DataRequired()]
    )
    reservas = IntegerField(
        "Número de reservas previas",
        validators=[DataRequired(), NumberRange(min=0, message="No puede ser negativo.")]
    )
    submit = SubmitField("Guardar cliente")