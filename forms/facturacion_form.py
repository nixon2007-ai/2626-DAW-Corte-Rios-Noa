from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class FacturacionForm(FlaskForm):
    numero = StringField(
        "Número de factura",
        validators=[DataRequired(message="El número es obligatorio.")]
    )
    cliente_id = SelectField(
        "Cliente",
        coerce=int,
        validators=[DataRequired(message="Seleccione un cliente.")]
    )
    mesa = StringField(
        "Mesa",
        validators=[DataRequired(message="La mesa es obligatoria.")]
    )
    fecha = StringField(
        "Fecha y hora",
        validators=[DataRequired(message="La fecha es obligatoria.")]
    )
    metodo_pago = SelectField(
        "Método de pago",
        choices=[("Efectivo", "Efectivo"), ("Tarjeta", "Tarjeta"), ("Transferencia", "Transferencia")],
        validators=[DataRequired()]
    )
    estado = SelectField(
        "Estado",
        choices=[("Pendiente", "Pendiente"), ("Pagada", "Pagada")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Generar factura")