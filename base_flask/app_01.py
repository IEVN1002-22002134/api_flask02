from flask import Flask, render_template, request, make_response, jsonify
import json
import pizza

app = Flask(__name__)

@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    pizzas_carrito = []
    ventas_totales = []
    mensaje_confirmacion = ""
    mostrar_ventas = False
    total_dia = 0

    formulario_pizza = pizza.PizzaForm(request.form)
    cookie_pizzas = request.cookies.get("pizzas_temporales")
    if cookie_pizzas:
        pizzas_carrito = json.loads(cookie_pizzas)
    cookie_ventas = request.cookies.get("cookie_ventas")
    if cookie_ventas:
        ventas_totales = json.loads(cookie_ventas)
    if request.method == 'POST':

        if 'btnAgregar' in request.form and formulario_pizza.validate():
            tamaño_seleccionado = formulario_pizza.tamano.data
            ingredientes_seleccionados = formulario_pizza.ingredientes.data
            cantidad_pizzas = formulario_pizza.num_pizzas.data

            precios_tamaño = {"chica": 40, "mediana": 80, "grande": 120}
            precios_ingredientes = {"jamon": 10, "piña": 10, "champiñones": 10}
            
            precio_base = precios_tamaño[tamaño_seleccionado]
            
            costo_ingredientes = 0
            if ingredientes_seleccionados:
                for ingrediente in ingredientes_seleccionados:
                    costo_ingredientes += precios_ingredientes.get(ingrediente, 0)
            
            subtotal_pizza = (precio_base + costo_ingredientes) * cantidad_pizzas

            ingredientes_texto = ", ".join(ingredientes_seleccionados) if ingredientes_seleccionados else "Sin ingredientes extra"

            nueva_pizza = {
                "tamano": tamaño_seleccionado,
                "ingredientes": ingredientes_texto,
                "num_pizzas": cantidad_pizzas,
                "subtotal": subtotal_pizza
            }
            pizzas_carrito.append(nueva_pizza)

            response = make_response(render_template("pizzeria.html", 
                form=formulario_pizza, 
                pizzas_carrito=pizzas_carrito,
                mensaje_confirmacion="Pizza Agregada!!! :3"))
            response.set_cookie("pizzas_temporales", json.dumps(pizzas_carrito))
            return response

        elif 'btnQuitar' in request.form:
            if pizzas_carrito:
                pizzas_carrito.pop()
                mensaje_confirmacion = "Se eliminola ultima pizza "
            else:
                mensaje_confirmacion = "No hay pizzas r"

            response = make_response(render_template("pizzeria.html", 
                form=formulario_pizza, 
                pizzas_carrito=pizzas_carrito,
                mensaje_confirmacion=mensaje_confirmacion))
            response.set_cookie("pizzas_temporales", json.dumps(pizzas_carrito))
            return response

        elif 'btnTerminar' in request.form:
            if formulario_pizza.validate():
                nombre_cliente = formulario_pizza.nombre.data
                direccion_cliente = formulario_pizza.direccion.data
                telefono_cliente = formulario_pizza.telefono.data

                if pizzas_carrito:
                    total_pedido = sum(pizza["subtotal"] for pizza in pizzas_carrito)
                    nueva_venta = {
                        "nombre": nombre_cliente,
                        "direccion": direccion_cliente,
                        "telefono": telefono_cliente,
                        "total": total_pedido
                    }
                    ventas_totales.append(nueva_venta)
                    mensaje_confirmacion = f"Pedido de : {nombre_cliente} se registro. El Total a pagar es: ${total_pedido}"
                    mostrar_ventas = True

                    response = make_response(render_template("pizzeria.html", 
                        form=formulario_pizza, 
                        pizzas_carrito=[],
                        ventas_totales=ventas_totales,
                        mensaje_confirmacion=mensaje_confirmacion,
                        mostrar_ventas=mostrar_ventas,
                        total_dia=total_dia))
                    response.set_cookie("cookie_ventas", json.dumps(ventas_totales))
                    response.set_cookie("pizzas_temporales", json.dumps([]))
                    return response
                else:
                    mensaje_confirmacion = "Agrega al menos una pizza porfis "
            else:
                mensaje_confirmacion = "Completa todos datos :3"

        elif 'btnVentas' in request.form:
            mostrar_ventas = True

    if ventas_totales:
        total_dia = sum(venta["total"] for venta in ventas_totales)

    response = make_response(render_template("pizzeria.html", 
        form=formulario_pizza,
        pizzas_carrito=pizzas_carrito,
        ventas_totales=ventas_totales,
        mensaje_confirmacion=mensaje_confirmacion,
        mostrar_ventas=mostrar_ventas,
        total_dia=total_dia))
    
    response.set_cookie("pizzas_temporales", json.dumps(pizzas_carrito))
    if ventas_totales:
        response.set_cookie("cookie_ventas", json.dumps(ventas_totales))
    
    return response

@app.route("/ventas_totales")
def ventas_totales():
    ventas_str = request.cookies.get('cookie_ventas')
    if not ventas_str:
        return "No hay ventas registradas"
    
    ventas = json.loads(ventas_str)
    return jsonify(ventas)

if __name__ == '__main__':
    app.run(debug=True)
    