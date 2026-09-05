from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp


class FacturacionForm(FlaskForm):
    """Formulario para registrar/editar una factura por mesa.

    El IVA y el total se calculan automáticamente a partir del subtotal
    ingresado, por lo que no se piden como campos del formulario.
    """

    numero = StringField(
        "N° de factura",
        validators=[DataRequired(message="El número de factura es obligatorio."),
                    Regexp(r"^\d{3}-\d{3}-\d{9}$",
                           message="Formato esperado: 001-001-000000123.")]
    )

    cliente = StringField(
        "Cliente",
        validators=[DataRequired(message="El nombre del cliente es obligatorio."),
                    Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres.")]
    )

    mesa = IntegerField(
        "N° de mesa",
        validators=[DataRequired(message="El número de mesa es obligatorio."),
                    NumberRange(min=1, max=50, message="Ingrese una mesa entre 1 y 50.")]
    )

    productos = TextAreaField(
        "Productos consumidos (separados por coma)",
        validators=[DataRequired(message="Debe indicar al menos un producto."),
                    Length(min=3, max=300, message="Debe tener entre 3 y 300 caracteres.")]
    )

    subtotal = FloatField(
        "Subtotal ($)",
        validators=[DataRequired(message="El subtotal es obligatorio."),
                    NumberRange(min=0.01, max=1000, message="El subtotal debe estar entre 0.01 y 1000.")]
    )

    metodo_pago = SelectField(
        "Método de pago",
        choices=[("Efectivo", "Efectivo"), ("Tarjeta", "Tarjeta"), ("Transferencia", "Transferencia")],
        validators=[DataRequired(message="Seleccione el método de pago.")]
    )

    estado = SelectField(
        "Estado",
        choices=[("Pagada", "Pagada"), ("Pendiente", "Pendiente")],
        validators=[DataRequired(message="Seleccione el estado.")]
    )

    fecha = StringField(
        "Fecha (dd/mm/aaaa)",
        validators=[DataRequired(message="La fecha es obligatoria."),
                    Regexp(r"^\d{2}/\d{2}/\d{4}$", message="Formato esperado: dd/mm/aaaa.")]
    )

    submit = SubmitField("Guardar factura")
