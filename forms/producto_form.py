from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductoForm(FlaskForm):
    """Formulario para registrar/editar un producto del menú del gastrobar."""

    nombre = StringField(
        "Nombre del producto",
        validators=[DataRequired(message="El nombre es obligatorio."),
                    Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres.")]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("Plato Fuerte", "Plato Fuerte"),
            ("Cóctel", "Cóctel"),
            ("Entrada", "Entrada"),
            ("Postre", "Postre"),
            ("Bebida", "Bebida"),
        ],
        validators=[DataRequired(message="Seleccione una categoría.")]
    )

    precio = FloatField(
        "Precio ($)",
        validators=[DataRequired(message="El precio es obligatorio."),
                    NumberRange(min=0.01, max=200, message="El precio debe estar entre 0.01 y 200.")]
    )

    estado = SelectField(
        "Estado",
        choices=[("Disponible", "Disponible"), ("Agotado", "Agotado")],
        validators=[DataRequired(message="Seleccione el estado.")]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria."),
                    Length(min=10, max=300, message="Debe tener entre 10 y 300 caracteres.")]
    )

    produccion_diaria = IntegerField(
        "Producción diaria (unidades)",
        validators=[DataRequired(message="Indique cuántos se hacen al día."),
                    NumberRange(min=0, message="No puede ser negativo.")]
    )

    imagen = FileField(
        "Imagen del producto",
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], "Solo imágenes JPG, PNG o WEBP.")]
    )

    submit = SubmitField("Guardar producto")