from wtforms import Form
from wtforms import StringField, IntegerField, RadioField, SelectMultipleField, widgets
from wtforms import validators

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PizzaForm(Form):
    nombre = StringField("Nombre completo", [
        validators.DataRequired(message='El campo es requerido')
    ])
    direccion = StringField("Dirección", [
        validators.DataRequired(message='El campo es requerido')
    ])
    telefono = StringField("Teléfono", [
        validators.DataRequired(message='El campo es requerido')
    ])
    
    tamano = RadioField("Tamaño", choices=[
        ("chica", "Chica $40"),
        ("mediana", "Mediana $80"), 
        ("grande", "Grande $120")
    ], validators=[validators.DataRequired(message='Selecciona un tamaño')])
    
    ingredientes = MultiCheckboxField("Ingredientes", choices=[
        ("jamon", "Jamón $10"),
        ("piña", "Piña $10"),
        ("champiñones", "Champiñones $10")
    ])
    
    num_pizzas = IntegerField("Número de pizzas", [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1, message='Debe ser al menos 1')
    ])